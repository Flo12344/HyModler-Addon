import bpy
import bmesh
import json
import math
import mathutils
from .. import helper


def fix_quaternion_signs(quats):
    fixed = []
    quats[0].data = quats[0].data.normalized()
    fixed.append(quats[0])

    for q in quats[1:]:
        q.data = q.data.normalized()
        if fixed[-1].data.dot(q.data) < 0:
            q.data = -q.data
        fixed.append(q)

    return fixed


class HyFrameData:
    def __init__(self, frame, data):
        self.frame = frame
        self.data = data

    def _ser_data(self):
        if isinstance(self.data, mathutils.Vector):
            if len(self.data) == 2:
                return helper.serialize_vq(self.data, 2, 0)
            else:
                return helper.serialize_vq(self.data, len(self.data), 4)
        elif isinstance(self.data, mathutils.Quaternion):
            return helper.serialize_vq(self.data, 4, 5)

    def get_rounded(self, dec):
        out = self.data.copy()
        for i in range(len(out)):
            out[i] = round(out[i], dec)
        return out

    def as_dict(self):
        return {
            "time": self.frame,
            "delta": self._ser_data(),
            "interpolationType": "linear",
        }


class HytaleSerializer:
    data = {}
    all_dist = []

    def init_scene(self, all_objects):
        self.armatures = self._collect_scene_armatures(all_objects)

    def serialize_animation(self, anim):
        out = self._base_animation(anim)
        self.data = {}
        bpy.context.scene.frame_set(anim.start)
        bpy.context.view_layer.update()
        for arm in self.armatures:
            self._init_dict(arm)

        for i in range(anim.end - anim.start):
            for arm in self.armatures:
                for bone in arm.pose.bones:
                    if bone.parent is None:
                        self._serialize_bone_recursive(bone)

            self._next_frame()
            bpy.context.view_layer.update()

        for d in self.data:
            out["nodeAnimations"][d] = {
                "position": [],
                "orientation": [],
                "shapeStretch": [],
                "shapeVisible": [],
                "shapeUvOffset": [],
            }

            self.data[d]["position"] = self._rdp(
                self.data[d]["position"],
                bpy.context.scene.hymodler_pos_exp_tresh,
                self._vec_distance,
            )
            self.data[d]["orientation"] = fix_quaternion_signs(
                self.data[d]["orientation"]
            )
            self.data[d]["orientation"] = self._rdp(
                self.data[d]["orientation"],
                bpy.context.scene.hymodler_rot_exp_tresh,
                self._quat_distance,
            )

            for i in range(len(self.data[d]["position"])):
                out["nodeAnimations"][d]["position"].append(
                    self.data[d]["position"][i].as_dict()
                )
            for i in range(len(self.data[d]["orientation"])):
                out["nodeAnimations"][d]["orientation"].append(
                    self.data[d]["orientation"][i].as_dict()
                )

            empty = True
            for s in out["nodeAnimations"][d]:
                if len(out["nodeAnimations"][d][s]) > 0:
                    empty = False
            if empty:
                out["nodeAnimations"].pop(d)

        return out

    def _next_frame(self):
        bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)

    def _base_animation(self, info):
        out = {
            "formatVersion": 1,
            "duration": info.end - info.start,
            "holdLastKeyframe": False,
            "nodeAnimations": {},
        }
        return out

    def _quat_distance(self, point, start, end):
        f, q = point.frame, point.data
        f0, q0 = start.frame, start.data
        f1, q1 = end.frame, end.data

        if f1 == f0:
            return 0

        t = (f - f0) / (f1 - f0)
        interp = q0.slerp(q1, t)

        return interp.rotation_difference(q).angle

    def _vec_distance(self, point, start, end):
        f, v = point.frame, point.data
        f0, v0 = start.frame, start.data
        f1, v1 = end.frame, end.data

        if f1 == f0:
            return 0

        line = end.data - start.data
        if line.length == 0.0:
            return (point.data - start.data).length
        t = (f - f0) / (f1 - f0)

        projection = start.data + t * line
        return (point.data - projection).length

    def _rdp(self, points, epsilon, distance_func):
        if len(points) < 3:
            return points

        to_remove = []
        for i in range(1, len(points) - 1):
            prev = points[i - 1]
            next = points[i + 1]
            curr = points[i]
            if next.get_rounded(4) == curr.get_rounded(4) and prev.get_rounded(
                4
            ) == curr.get_rounded(4):
                to_remove.append(curr.frame)
        for i in reversed(to_remove):
            points.pop(i)

        if len(points) == 2 and points[0].get_rounded(4) == points[1].get_rounded(4):
            if isinstance(points[0].data, mathutils.Quaternion):
                if points[0].get_rounded(5) == mathutils.Quaternion((0, 0, 0, 1)):
                    return []
            elif isinstance(points[0].data, mathutils.Vector):
                if points[0].get_rounded(4).length < epsilon:
                    return []

        if epsilon == 0:
            return points
        max_dist = 0.0
        index = 0

        start = points[0]
        end = points[-1]

        for i in range(1, len(points) - 1):
            d = distance_func(points[i], start, end)
            if d > max_dist:
                index = i
                max_dist = d
        self.all_dist.append(max_dist)
        if max_dist > epsilon:
            left = self._rdp(points[: index + 1], epsilon, distance_func)
            right = self._rdp(points[index:], epsilon, distance_func)
            return left[:-1] + right
        else:
            return [start, end]

    def _init_dict(self, obj):
        for b in obj.data.bones:
            self.data[b.name] = {
                "position": [],
                "orientation": [],
                "shapeStretch": [],
                "shapeVisible": [],
                "shapeUvOffset": [],
            }

    def _collect_scene_armatures(self, all_objects):
        armatures = []

        for obj in all_objects:
            if obj.type == "ARMATURE":
                armatures.append(obj)
        return armatures

    def _serialize_bone_recursive(self, bone):
        local_matrix = self._get_bone_local_matrix(bone)
        rest = self._get_rest_bone_local_matrix(bone.bone)

        mat = rest.inverted() @ local_matrix

        position = mat.to_translation()
        rotation = mat.to_quaternion()

        position[0] *= -1.0
        quat = mathutils.Quaternion((-rotation.x, rotation.z, rotation.y, rotation.w))

        self.data[bone.name]["position"].append(
            HyFrameData(len(self.data[bone.name]["position"]), position.xzy * 10.0)
        )
        self.data[bone.name]["orientation"].append(
            HyFrameData(len(self.data[bone.name]["orientation"]), quat)
        )

        for child in bone.children:
            self._serialize_bone_recursive(child)

    def _get_bone_local_matrix(self, bone):
        if bone.parent:
            return bone.parent.matrix.inverted() @ bone.matrix
        return bone.matrix

    def _get_rest_bone_local_matrix(self, bone):
        if bone.parent:
            return bone.parent.matrix_local.inverted() @ bone.matrix_local
        return bone.matrix_local

    def _serialize_stretch(self, obj):
        if isinstance(obj, bpy.types.Bone):
            return {"x": 0, "y": 0, "z": 0}
        else:
            return helper.serialize_vq(obj.scale.xzy, 3, 4)
