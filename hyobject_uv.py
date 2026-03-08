import bpy
import bmesh
import mathutils
import math


def normal_to_hytale_wh(normal, mesh_size):
    mn = 0.5
    if normal.x > mn or normal.x < -mn:
        return mesh_size[1], mesh_size[2]
    elif normal.z > mn or normal.z < -mn:
        return mesh_size[0], mesh_size[1]
    elif normal.y > mn or normal.y < -mn:
        return mesh_size[0], mesh_size[2]
    else:
        return 0, 0


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


def get_current_rotation(loop, lay):
    uv0 = loop[0][lay].uv
    uv1 = loop[2][lay].uv
    d = uv1 - uv0
    da = math.atan2(d.y, d.x) - math.pi / 4
    na = da % (2 * math.pi)

    return round(na / (math.pi / 2)) % 4


def unrotate_uv(w, h, loops, lay):
    texture_size = bpy.context.scene.hymodler_texturesize
    PIXEL_WIDTH = 1.0 / texture_size[0]
    PIXEL_HEIGHT = 1.0 / texture_size[1]
    x, y = rotation_offset((w, h), get_current_rotation(loops, lay))
    loops[0][lay].uv.x -= PIXEL_WIDTH * x
    loops[0][lay].uv.y -= PIXEL_HEIGHT * y
    pass


def rotate_uv(obj, w, h, face, lay):
    texture_size = bpy.context.scene.hymodler_texturesize
    PIXEL_WIDTH = 1.0 / texture_size[0]
    PIXEL_HEIGHT = 1.0 / texture_size[1]
    cr = obj.hymodler_uv_rotation[face.index]
    ox, oy = rotation_offset((w, h), cr)
    x = face.loops[0][lay].uv.x + PIXEL_WIDTH * ox
    y = face.loops[0][lay].uv.y + PIXEL_HEIGHT * oy
    local_uvs = [
        (0, 0),
        (w, 0),
        (w, h),
        (0, h),
    ]
    for loop, uv in zip(face.loops, local_uvs):
        rx, ry = rotate(uv, cr)
        loop[lay].uv = mathutils.Vector((x + PIXEL_WIDTH * rx, y + PIXEL_HEIGHT * ry))

    pass


def is_flipped(face, lay):
    area = 0.0
    uvs = [loop[lay].uv for loop in face.loops]
    for i in range(len(uvs)):
        area += uvs[i - 1].cross(uvs[i])
    return area < 0


def flip_uv(face, lay, horizontal):
    if horizontal:
        v0 = face.loops[0][lay].uv.xy
        v2 = face.loops[2][lay].uv.xy
        face.loops[0][lay].uv = face.loops[1][lay].uv.xy
        face.loops[2][lay].uv = face.loops[3][lay].uv.xy
        face.loops[1][lay].uv = v0
        face.loops[3][lay].uv = v2
    else:
        v0 = face.loops[0][lay].uv.xy
        v1 = face.loops[1][lay].uv.xy
        face.loops[1][lay].uv = face.loops[2][lay].uv.xy
        face.loops[0][lay].uv = face.loops[3][lay].uv.xy
        face.loops[2][lay].uv = v1
        face.loops[3][lay].uv = v0
    pass


def update_uv(self=None, context=None):
    obj = bpy.context.active_object
    if bpy.context.mode == "EDIT_MESH":
        ob = bpy.context.edit_object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
    elif bpy.context.mode == "OBJECT":
        bm = bmesh.new()
        bm.from_mesh(obj.data)
    else:
        return
    uv_lay = bm.loops.layers.uv.verify()
    for f in bm.faces:
        width, height = normal_to_hytale_wh(f.normal, obj.hymodler_size)
        if obj["type"] == "quad":
            width = obj.hymodler_size[0]
            height = obj.hymodler_size[1]

        w = width
        h = height
        if is_flipped(f, uv_lay):
            flip_uv(f, uv_lay, False)
        unrotate_uv(w, h, f.loops, uv_lay)

        rotate_uv(obj, w, h, f, uv_lay)
        if obj.hymodler_uv_vertical_flip[f.index]:
            flip_uv(f, uv_lay, False)
        if obj.hymodler_uv_horizontal_flip[f.index]:
            flip_uv(f, uv_lay, True)
    if bpy.context.mode == "EDIT_MESH":
        ob = bpy.context.edit_object
        me = ob.data
        bmesh.update_edit_mesh(me)
    elif bpy.context.mode == "OBJECT":
        bm.to_mesh(obj.data)
    bm.free()
    pass
