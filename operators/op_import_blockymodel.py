import math
import mathutils
import bpy
import bmesh
from bpy_extras.io_utils import ImportHelper
import json
import copy
from .. import hyobjects
from .. import hyobject_edit


class HytaleDeserializer:
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
                sub["orientation"]["w"] = 0.0
                sub["orientation"]["x"] = 0.0
                sub["orientation"]["y"] = 0.0
                sub["orientation"]["z"] = 1.0
                node["children"].append(sub)
                node["shape"]["type"] = "none"
                node["shape"]["stretch"]["x"] = 1.0
                node["shape"]["stretch"]["y"] = 1.0
                node["shape"]["stretch"]["z"] = 1.0
                pass
        origin = parse_vector(node["position"]) / 10.0
        stretch = parse_vector(node["shape"]["stretch"])
        stretch.x *= -1.0
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
                hyobject_edit.add_offset_to_hyobject(obj, offset)
            case "box":
                obj = hyobjects.create_hybox()

                #
                obj.hymodler_size[0] = node["shape"]["settings"]["size"]["x"]
                obj.hymodler_size[2] = node["shape"]["settings"]["size"]["y"]
                obj.hymodler_size[1] = node["shape"]["settings"]["size"]["z"]

                hyobject_edit.set_origin_to_geometry_center(obj)
                hyobject_edit.add_offset_to_hyobject(obj, offset)
            case _:
                return

        obj.name = name
        obj.hymodler_bbname = node["name"]
        obj.location = origin
        obj.rotation_quaternion = rotation
        obj.scale = stretch

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
