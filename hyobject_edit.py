import bpy
import bmesh
import mathutils
import math
from . import hyobject_uv


def set_texture_size(size, context):
    for i in range(len(bpy.context.scene.objects)):
        if "hymesh" in bpy.context.scene.objects[i]:
            update_hyobject_uv(bpy.context.scene.objects[i], context)


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


def update_hyobject_uv(mesh, context):
    obj_type = mesh["type"]
    if obj_type == "none":
        return
    texture_size = bpy.context.scene.hymodler_texturesize
    mesh_size = mesh.hymodler_size
    bm = bmesh.new()
    bm.from_mesh(mesh.data)
    uv_lay = bm.loops.layers.uv.verify()
    PIXEL_WIDTH = 1.0 / texture_size[0]
    PIXEL_HEIGHT = 1.0 / texture_size[1]

    def normal_to_hytale_wh(normal, mesh_size):
        mn = 0.5
        if normal.x > mn or normal.x < -mn:
            return mesh_size[1], mesh_size[2]
        elif normal.z > mn or normal.z < -mn:
            return mesh_size[0], mesh_size[1]
        elif normal.y > mn or normal.y < -mn:
            return mesh_size[0], mesh_size[2]

    def rotate(v, r):
        x, y = v
        r %= 4
        if r == 0:
            return x, y
        if r == 1:
            return -y, x
        if r == 2:
            return -x, -y
        if r == 3:
            return y, -x

    def rotation_offset(v, r):
        x, y = v
        r %= 4
        if r == 0:
            return 0, 0
        if r == 1:
            return y, 0
        if r == 2:
            return x, y
        if r == 3:
            return 0, x

    for face in bm.faces:
        width, height = normal_to_hytale_wh(face.normal, mesh_size)
        cr = mesh["fd"]["r"][face.index]
        w = width
        h = height
        ox, oy = rotation_offset((w, h), cr)
        x = face.loops[0][uv_lay].uv.x
        y = face.loops[0][uv_lay].uv.y
        local_uvs = [
            (0, 0),
            (w, 0),
            (w, h),
            (0, h),
        ]
        for loop, uv in zip(face.loops, local_uvs):
            rx, ry = rotate(uv, cr)
            loop[uv_lay].uv = mathutils.Vector(
                (x + PIXEL_WIDTH * rx, y + PIXEL_HEIGHT * ry)
            )
    bm.to_mesh(mesh.data)
    bm.free()
