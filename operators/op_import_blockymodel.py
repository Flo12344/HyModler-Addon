import math
import mathutils
import bpy
import bmesh
from bpy_extras.io_utils import ImportHelper
import json
import copy
from .. import helper
from .. import hyobjects
from .. import hyobject_edit
from .. import hyobject_uv


class HytaleDeserializer:
    def __texture_handling(self, obj, textures):
        def parse_vector(vec):
            texture_size = bpy.context.scene.hymodler_texturesize
            out = mathutils.Vector((vec["x"], vec["y"]))
            out.x /= texture_size[0]
            out.y /= texture_size[1]
            out.y = 1.0 - out.y
            return out

        bm = bmesh.new()
        bm.from_mesh(obj.data)
        uv_lay = bm.loops.layers.uv.verify()

        for f in bm.faces:
            if obj["type"] == "quad":
                uv_data = textures[next(iter(textures))]
            else:
                fname = helper.face_id_to_hytale_direction(f.normal)
                if fname not in textures:
                    continue
                uv_data = textures[fname]

            obj.hymodler_uv_rotation[f.index] = int(uv_data["angle"] / 90)
            if obj.hymodler_uv_rotation[f.index] == 3:
                obj.hymodler_uv_rotation[f.index] = 1
            elif obj.hymodler_uv_rotation[f.index] == 1:
                obj.hymodler_uv_rotation[f.index] = 3
            obj.hymodler_uv_vertical_flip[f.index] = uv_data.get("mirror", {}).get(
                "y", False
            )
            obj.hymodler_uv_horizontal_flip[f.index] = uv_data.get("mirror", {}).get(
                "x", False
            )
        bm.to_mesh(obj.data)
        bm.free()
        hyobject_uv.update_uv()
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        uv_lay = bm.loops.layers.uv.verify()
        for f in bm.faces:
            face_size_x, face_size_y = obj.hymodler_size[0], obj.hymodler_size[1]
            if obj["type"] == "quad":
                uv_data = textures[next(iter(textures))]
            else:
                hytale_face = helper.face_id_to_hytale_direction(f.normal)
                face_size_x, face_size_y = hyobject_uv.normal_to_hytale_wh(
                    f.normal, obj.hymodler_size
                )
                if hytale_face not in textures:
                    continue
                uv_data = textures[hytale_face]

            texture_size = bpy.context.scene.hymodler_texturesize
            PIXEL_WIDTH = 1.0 / texture_size[0]
            PIXEL_HEIGHT = 1.0 / texture_size[1]
            u, v = (
                uv_data["offset"]["x"] * PIXEL_WIDTH,
                1.0 - uv_data["offset"]["y"] * PIXEL_HEIGHT,
            )
            w, h = face_size_x, face_size_y
            mx = -1 if uv_data.get("mirror", {}).get("x", False) else 0
            my = -1 if uv_data.get("mirror", {}).get("y", False) else 1
            angle = obj.hymodler_uv_rotation[f.index]

            offset = mathutils.Vector((0, 0))
            if angle == 0:
                offset.x = u - w * max(mx, 0) * PIXEL_WIDTH
                offset.y = v - h * my * PIXEL_HEIGHT
            elif angle == 1:
                offset.x = u + h * my * PIXEL_WIDTH
                offset.y = v - w * mx * PIXEL_HEIGHT
            elif angle == 2:
                offset.x = u - w * max(mx, 0) * PIXEL_WIDTH
                offset.y = v + h * my * PIXEL_HEIGHT
            elif angle == 3:
                offset.x = u - h * my * PIXEL_WIDTH
                offset.y = v - w * mx * PIXEL_HEIGHT

            offset = offset - f.loops[0][uv_lay].uv

            for loop in f.loops:
                loop[uv_lay].uv += offset

        bm.to_mesh(obj.data)
        bm.free()
        pass

    def parse_node(self, node, parent_obj=None, parent_node=None):

        def parse_vector(vec):
            out = mathutils.Vector(
                (
                    -vec["x"],
                    vec["z"],
                    vec["y"],
                )
            )
            return out

        if "children" in node:
            if node["shape"]["type"] != "none":
                sub = copy.deepcopy(node)
                sub.pop("children")
                sub["position"]["x"] = sub["shape"]["offset"]["x"]
                sub["position"]["y"] = sub["shape"]["offset"]["y"]
                sub["position"]["z"] = sub["shape"]["offset"]["z"]
                sub["shape"]["offset"]["x"] = 0.0
                sub["shape"]["offset"]["y"] = 0.0
                sub["shape"]["offset"]["z"] = 0.0
                sub["orientation"]["w"] = 1.0
                sub["orientation"]["x"] = 0.0
                sub["orientation"]["y"] = 0.0
                sub["orientation"]["z"] = 0.0
                node["children"].append(sub)
                node["shape"]["type"] = "none"
                sub["shape"]["stretch"] = copy.deepcopy(node["shape"]["stretch"])
                node["shape"]["stretch"]["x"] = 1.0
                node["shape"]["stretch"]["y"] = 1.0
                node["shape"]["stretch"]["z"] = 1.0
            else:
                node["shape"]["stretch"]["x"] = 1.0
                node["shape"]["stretch"]["y"] = 1.0
                node["shape"]["stretch"]["z"] = 1.0

        origin = parse_vector(node["position"]) / 10.0
        stretch = mathutils.Vector(
            (
                node["shape"]["stretch"]["x"],
                node["shape"]["stretch"]["z"],
                node["shape"]["stretch"]["y"],
            )
        )
        offset = parse_vector(node["shape"]["offset"]) / 10.0
        rotation = mathutils.Quaternion(
            (
                node["orientation"]["w"],
                -node["orientation"]["x"],
                node["orientation"]["z"],
                node["orientation"]["y"],
            )
        )
        name = node["name"]
        match node["shape"]["type"]:
            case "none":
                if node["name"].endswith("-Attachement"):
                    obj = hyobjects.create_attachement()
                else:
                    obj = hyobjects.create_group()
                    name += "_G"

            case "quad":
                obj = hyobjects.create_hyquad()
                obj.hymodler_size[0] = node["shape"]["settings"]["size"]["x"]
                obj.hymodler_size[1] = node["shape"]["settings"]["size"]["y"]
                prot = hyobject_edit.get_initial_quad_rot(
                    node["shape"]["settings"]["normal"]
                )

                rotation = rotation @ prot
                offset.rotate(prot)

                hyobject_edit.set_origin_to_geometry_center(obj)
                hyobject_edit.add_offset_to_hyobject(obj, -offset)

                self.__texture_handling(obj, node["shape"]["textureLayout"])
            case "box":
                obj = hyobjects.create_hybox()

                #
                obj.hymodler_size[0] = node["shape"]["settings"]["size"]["x"]
                obj.hymodler_size[2] = node["shape"]["settings"]["size"]["y"]
                obj.hymodler_size[1] = node["shape"]["settings"]["size"]["z"]

                hyobject_edit.set_origin_to_geometry_center(obj)
                hyobject_edit.add_offset_to_hyobject(obj, -offset)

                self.__texture_handling(obj, node["shape"]["textureLayout"])
            case _:
                return

        obj.name = name
        obj.hymodler_bbname = node["name"]
        obj.location = origin
        obj.scale = stretch
        obj.rotation_quaternion = rotation

        if parent_obj is not None:
            if node["shape"]["type"] == "none":
                if parent_node is not None and parent_obj.name.endswith("_G"):
                    parent_offset = parse_vector(parent_node["shape"]["offset"]) / 10.0
                    obj.location = origin + parent_offset

            obj.parent = parent_obj

        if "children" in node:
            for n in node["children"]:
                self.parse_node(n, obj, node)

    def load_nodes(self, nodes):
        for node in nodes:
            self.parse_node(node)
        pass


class OP_Import_Blockymodel(bpy.types.Operator, ImportHelper):
    bl_idname = "hymodler.import_blockymodel"
    bl_label = "import_Blockymodel"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty(default="*.blockymodel", options={"HIDDEN"})
    filename_ext = ".blockymodel"
    hymodler_selection_only: bpy.props.BoolProperty(
        name="Selection Only", description="", default=False
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        deserializer = HytaleDeserializer()
        with open(self.filepath, "r") as file:
            j = json.load(file)

        if "nodes" in j:
            deserializer.load_nodes(j["nodes"])
        return {"FINISHED"}


def add_to_topbar_mt_file_import(self, context):
    layout = self.layout
    op = layout.operator(
        "hymodler.import_blockymodel",
        text="Blockymodel",
        icon_value=0,
        emboss=True,
        depress=False,
    )
    op.sna_selection_only = False


def register():
    bpy.utils.register_class(OP_Import_Blockymodel)
    bpy.types.TOPBAR_MT_file_import.append(add_to_topbar_mt_file_import)


def unregister():
    bpy.utils.unregister_class(OP_Import_Blockymodel)
    bpy.types.TOPBAR_MT_file_import.remove(add_to_topbar_mt_file_import)
