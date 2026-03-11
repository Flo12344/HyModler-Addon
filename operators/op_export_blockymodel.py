import math
import mathutils
import bpy
import bmesh
from bpy_extras.io_utils import ExportHelper
import json
from .. import helper
from .. import hyobject_uv


class HytaleSerializer:
    def __init__(self):
        self.node_id = 0

    def next_id(self):
        self.node_id += 1
        return self.node_id

    def serialize_scene(self, all_objects):
        objs, armatures = self._collect_scene_data(all_objects)
        bone_meshes = self._collect_bone_meshes(all_objects, objs)

        root_objs = [obj for obj in objs if obj.parent is None]
        root_armatures = [obj for obj in armatures if obj.parent is None]

        nodes = []
        for obj in root_objs:
            nodes.append(self.serialize_obj(obj, None))
        for obj in root_armatures:
            if obj.name in bone_meshes:
                armature_meshes = bone_meshes[obj.name]
            else:
                armature_meshes = None
            nodes.append(self.serialize_obj(obj, armature_meshes))
        return nodes

    def serialize_obj(self, obj, bone_meshes):
        node = self._create_base_node(obj)

        local_matrix = self._get_obj_local_matrix(obj)

        position = local_matrix.to_translation()
        rotation = local_matrix.to_quaternion()

        position[0] *= -1.0
        quat = mathutils.Quaternion((-rotation.x, rotation.z, rotation.y, rotation.w))

        node["position"] = helper.serialize_vq(position.xzy * 10.0, 3, 4)
        node["orientation"] = helper.serialize_vq(quat, 4, 5)

        if obj.type == "ARMATURE":
            shape = {
                "type": "none",
                "settings": {},
                "textureLayout": {},
            }

            node["shape"] = shape

            prev_pose = obj.data.pose_position
            obj.data.pose_position = "REST"
            bpy.context.view_layer.update()
            for bone in obj.data.bones:
                if bone.parent is None:
                    node["children"].append(
                        self._serialize_bone_recursive(bone, bone_meshes)
                    )

            obj.data.pose_position = prev_pose
            bpy.context.view_layer.update()
        else:
            obj_type = obj.get("type", "none")

            if obj_type == "quad":
                shape = {
                    "type": "quad",
                    "stretch": helper.serialize_vq(obj.scale.xzy, 3, 4),
                    "offset": {"x": 0, "y": 0, "z": 0},
                    "settings": {
                        "size": {
                            "x": obj.hymodler_size[0],
                            "y": obj.hymodler_size[1],
                        },
                        "normal": obj.hymodler_bbquad_orient,
                    },
                    "textureLayout": self._serialize_texture(obj),
                }
            elif obj_type == "box":
                shape = {
                    "type": "box",
                    "stretch": helper.serialize_vq(obj.scale.xzy, 3, 4),
                    "offset": {"x": 0, "y": 0, "z": 0},
                    "settings": {
                        "size": {
                            "x": obj.hymodler_size[0],
                            "y": obj.hymodler_size[2],
                            "z": obj.hymodler_size[1],
                        }
                    },
                    "textureLayout": self._serialize_texture(obj),
                }
            else:
                shape = {
                    "type": "none",
                    "stretch": {"x": 1, "y": 1, "z": 1},
                    "offset": {"x": 0, "y": 0, "z": 0},
                    "settings": {},
                }

            node["shape"] = shape
            for child in obj.children:
                if child.type != "ARMATURE":
                    node["children"].append(self.serialize_obj(child, None))

        return node

    def _collect_scene_data(self, all_objects):
        objs = []
        armatures = []

        for obj in all_objects:
            if obj.type == "ARMATURE":
                armatures.append(obj)
            else:
                objs.append(obj)
        return objs, armatures

    def _collect_bone_meshes(self, objects, collected_objects):
        bone_meshes = {}

        for obj in objects:
            if obj.type != "MESH":
                continue

            if obj.parent and obj.parent.type == "ARMATURE":
                bone_name = obj.parent_bone
                if obj.parent.name not in bone_meshes:
                    bone_meshes[obj.parent.name] = {}

                if bone_name not in bone_meshes[obj.parent.name]:
                    bone_meshes[obj.parent.name][bone_name] = []

                bone_meshes[obj.parent.name][bone_name].append(obj)
                if obj in collected_objects:
                    collected_objects.remove(obj)

        return bone_meshes

    def _serialize_bone_recursive(self, bone, bone_meshes):
        node = self._create_base_node(bone)
        shape = self._serialize_bone_shape(bone)
        node["shape"] = shape

        local_matrix = self._get_local_matrix(bone)

        position = local_matrix.to_translation()
        rotation = local_matrix.to_quaternion()

        position[0] *= -1.0
        quat = mathutils.Quaternion((-rotation.x, rotation.z, rotation.y, rotation.w))

        node["position"] = helper.serialize_vq(position.xzy * 10.0, 3, 4)
        node["orientation"] = helper.serialize_vq(quat, 4, 5)

        if bone_meshes:
            if bone.name in bone_meshes:
                for mesh_obj in bone_meshes[bone.name]:
                    node["children"].append(self.serialize_obj(mesh_obj, None))
        for child in bone.children:
            node["children"].append(self._serialize_bone_recursive(child, bone_meshes))

        return node

    def _create_base_node(self, obj):
        name = obj.name
        # if len(obj.hymodler_bbname) > 0:
        # name = obj.hymodler_bbname
        return {"id": self.next_id(), "name": name, "children": []}

    def _get_local_matrix(self, bone):
        if bone.parent:
            return bone.parent.matrix_local.inverted() @ bone.matrix_local
        return bone.matrix_local

    def _get_obj_local_matrix(self, obj):
        if obj.parent and obj.parent.type == "ARMATURE":
            arm = obj.parent
            bone = arm.data.bones[obj.parent_bone]

            bone_world = arm.matrix_world @ bone.matrix_local

            obj_world = obj.matrix_world

            return bone_world.inverted() @ obj_world

        return obj.matrix_local

    def _serialize_bone_shape(self, obj, ftype=None):
        shape = {
            "type": "none",
            "stretch": {"x": 1, "y": 1, "z": 1},  # self._serialize_stretch(obj),
            "unwrapMode": "custom",
            "visible": True,
            "shadingMode": "flat",
            "doubleSided": False,
            "offset": {"x": 0, "y": 0, "z": 0},
        }

        shape["settings"] = {"isPiece": False}
        shape["textureLayout"] = {}

        return shape

    def _serialize_texture(self, obj):
        texture = {}
        if obj.type == "ARMATURE" or obj.type == "EMPTY":
            return texture
        is_2d = obj["type"] == "quad"
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        uv_lay = bm.loops.layers.uv.active

        PIXEL_WIDTH = 1.0 / bpy.data.scenes["Scene"].hymodler_texturesize[0]
        PIXEL_HEIGHT = 1.0 / bpy.data.scenes["Scene"].hymodler_texturesize[1]
        if is_2d:
            bm.faces.ensure_lookup_table()
            face = bm.faces[0]

            mx = -1 if obj.hymodler_uv_horizontal_flip[face.index] else 0
            my = -1 if obj.hymodler_uv_vertical_flip[face.index] else 0
            x, y = obj.hymodler_size[0], obj.hymodler_size[1]
            rot = obj.hymodler_uv_rotation[face.index]
            if rot == 1:
                rot = 3
            elif rot == 3:
                rot = 1
            xoff, yoff = hyobject_uv.rotation_offset(
                (x * mx, y * my),
                rot,
            )

            angle = rot * 90
            for loop in face.loops:
                if loop.index == 3 + face.index * 4:
                    res = {}
                    uv = loop[uv_lay].uv
                    uv = mathutils.Vector(
                        (
                            (uv[0]) / PIXEL_WIDTH,
                            (1.0 - uv[1]) / PIXEL_HEIGHT,
                        )
                    )
                    res["offset"] = helper.serialize_vq(uv, 2, 0)
                    res["mirror"] = {
                        "x": obj.hymodler_uv_horizontal_flip[face.index],
                        "y": obj.hymodler_uv_vertical_flip[face.index],
                    }
                    res["angle"] = angle
                    texture[helper.face_id_to_hytale_direction(face.normal)] = res
        else:
            for face in bm.faces:
                mx = -1 if obj.hymodler_uv_horizontal_flip[face.index] else 0
                my = -1 if obj.hymodler_uv_vertical_flip[face.index] else 0
                x, y = hyobject_uv.normal_to_hytale_wh(face.normal, obj.hymodler_size)
                rot = obj.hymodler_uv_rotation[face.index]
                if rot == 1:
                    rot = 3
                elif rot == 3:
                    rot = 1
                xoff, yoff = hyobject_uv.rotation_offset(
                    (x * mx, y * my),
                    rot,
                )

                angle = rot * 90
                for loop in face.loops:
                    if loop.index == 3 + face.index * 4:
                        res = {}
                        uv = loop[uv_lay].uv
                        uv = mathutils.Vector(
                            (
                                (uv[0]) / PIXEL_WIDTH - xoff,
                                (1.0 - uv[1]) / PIXEL_HEIGHT + yoff,
                            )
                        )
                        res["offset"] = helper.serialize_vq(uv, 2, 0)
                        res["mirror"] = {
                            "x": obj.hymodler_uv_horizontal_flip[face.index],
                            "y": obj.hymodler_uv_vertical_flip[face.index],
                        }
                        res["angle"] = angle
                        texture[helper.face_id_to_hytale_direction(face.normal)] = res
            pass
        bm.free()
        return texture

    def _serialize_settings(self, obj):
        is_2d = obj["type"] == "quad"
        settings = {}
        settings["isPiece"] = False
        if obj.type != "ARMATURE":
            size = mathutils.Vector(obj.hymodler_size)
            settings["size"] = helper.serialize_vq(size.xzy, 3, 0)
            settings["isStaticBox"] = True

        if is_2d:
            settings["normal"] = "+Z"
        return settings

    def _serialize_stretch(self, obj):
        if isinstance(obj, bpy.types.Bone):
            return {"x": 0, "y": 0, "z": 0}
        else:
            return helper.serialize_vq(obj.scale.xzy, 3, 4)

    def _calculate_pivot(self, obj):
        if obj.type == "ARMATURE":
            pos = obj.location.copy()
            pos[0] *= -1.0
            return helper.serialize_vq(pos.xzy * 10.0, 3, 4)
        if obj.type == "MESH":
            if not obj.data.vertices:
                return helper.serialize_vq(mathutils.Vector((0, 0, 0)), 3, 4)

            center = sum((v.co for v in obj.data.vertices), mathutils.Vector()) / len(
                obj.data.vertices
            )

            center[0] *= -1.0
            return helper.serialize_vq(center.xzy * 10.0, 3, 4)

        return helper.serialize_vq(mathutils.Vector((0, 0, 0)), 3, 4)

    def _serialize_rotation(self, obj):
        pass


class OP_Export_Blockymodel(bpy.types.Operator, ExportHelper):
    bl_idname = "hymodler.export_blockymodel"
    bl_label = "export_Blockymesh"
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
        serializer = HytaleSerializer()

        if self.hymodler_selection_only:
            objects = context.selected_objects
        else:
            objects = [
                obj
                for obj in context.scene.objects
                if obj.type in ("MESH", "EMPTY", "ARMATURE")
            ]
        nodes = serializer.serialize_scene(objects)

        j = {"format": "prop", "nodes": nodes, "lod": "auto"}

        out = json.dumps(j, indent=2)
        with open(self.filepath, mode="w") as file:
            file.seek(0)
            file.write(out)
            file.truncate()
        return {"FINISHED"}


def add_to_topbar_mt_file_export(self, context):
    layout = self.layout
    op = layout.operator(
        "hymodler.export_blockymodel",
        text="Export HyModel",
        icon_value=0,
        emboss=True,
        depress=False,
    )
    op.sna_selection_only = False


def register():
    bpy.utils.register_class(OP_Export_Blockymodel)
    bpy.types.TOPBAR_MT_file_export.append(add_to_topbar_mt_file_export)


def unregister():
    bpy.utils.unregister_class(OP_Export_Blockymodel)
    bpy.types.TOPBAR_MT_file_export.remove(add_to_topbar_mt_file_export)
