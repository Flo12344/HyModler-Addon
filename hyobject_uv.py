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


def unrotate_uv():
    pass


def rotate_uv():
    pass


def update_uv_EDIT():
    pass


def update_uv_OBJECT():
    pass
