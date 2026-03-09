import bpy
import bmesh
import mathutils
import math
from . import hyobject_uv


def set_texture_size(size, context):
    selected_objects = [obj.name for obj in bpy.context.selected_objects]
    active_object = (
        bpy.context.active_object.name if bpy.context.active_object else None
    )
    for obj in bpy.context.scene.objects:
        obj.select_set(False)
    for i in range(len(bpy.context.scene.objects)):
        obj = bpy.context.scene.objects[i]
        if "hymesh" in obj:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            hyobject_uv.update_uv()
            obj.select_set(False)

    for obj in selected_objects:
        if obj:
            obj.select_set(True)

    if active_object:
        bpy.context.view_layer.objects.active = active_object


def set_origin_to_geometry_center(obj):
    verts = obj.data.vertices
    center = mathutils.Vector()

    for v in verts:
        center += v.co
    center /= len(verts)

    obj.data.transform(mathutils.Matrix.Translation(-center))

    obj.matrix_world.translation += obj.matrix_world.to_3x3() @ center

    obj.data.update()


def add_offset_to_hyobject(obj, offset):
    obj.data.transform(mathutils.Matrix.Translation(-offset))

    obj.matrix_world.translation += obj.matrix_world.to_3x3() @ offset
    obj.data.update()


def set_hyobject_size(obj, context):
    size = obj.hymodler_size
    obj_type = obj["type"]

    if obj_type == "none":
        return

    bm = bmesh.new()
    bm.from_mesh(obj.data)
    vert_origin = obj.data.vertices[1].co

    xadd = vert_origin.x + size[0] * 0.1
    yadd = vert_origin.y + size[1] * 0.1
    zadd = vert_origin.z + size[2] * 0.1

    if obj_type == "box":
        for i, face in enumerate(bm.faces):
            if i == 1:
                for v in face.verts:
                    v.co.x = xadd
            elif i == 0:
                for v in face.verts:
                    v.co.y = yadd
            elif i == 4:
                for v in face.verts:
                    v.co.z = zadd
    elif obj_type == "quad":
        for i, e in enumerate(bm.edges):
            if i == 0:
                for v in e.verts:
                    v.co.x = xadd
            elif i == 3:
                for v in e.verts:
                    v.co.z = yadd
    bm.to_mesh(obj.data)
    bm.free()
    hyobject_uv.update_uv()
    # update_hyobject_uv(obj, context)


def get_initial_quad_rot(orient):
    match orient:
        case "+Z":
            return mathutils.Quaternion((1.0, 0.0, 0.0, 0.0))
        case "-Z":
            return mathutils.Quaternion((0.0, 0.0, 0.0, 1.0))
        case "+Y":
            return mathutils.Quaternion(
                (math.sqrt(2.0) / 2.0, math.sqrt(2.0) / 2.0, 0.0, 0.0)
            )
        case "-Y":
            return mathutils.Quaternion(
                (math.sqrt(2.0) / 2.0, -math.sqrt(2.0) / 2.0, 0.0, 0.0)
            )
        case "+X":
            return mathutils.Quaternion(
                (math.sqrt(2.0) / 2.0, 0.0, 0.0, math.sqrt(2.0) / 2.0)
            )
        case "-X":
            return mathutils.Quaternion(
                (math.sqrt(2.0) / 2.0, 0.0, 0.0, -math.sqrt(2.0) / 2.0)
            )

    pass
