import bpy
import math


def is_selected_valid():
    return bpy.context.active_object != None and "hymesh" in bpy.context.active_object


def serialize_vq(vec, iter, dec):
    axis = ["x", "y", "z", "w"]
    res = {}
    for i in range(iter):
        if dec == 0:
            res[axis[i]] = math.trunc(vec[i])
        else:
            res[axis[i]] = round(vec[i], dec)
    return res


def face_id_to_hytale_direction(normal):
    mn = 0.5
    if normal.x > mn:
        return "left"
    elif normal.x < -mn:
        return "right"
    elif normal.z > mn:
        return "top"
    elif normal.z < -mn:
        return "bottom"
    elif normal.y > mn:
        return "front"
    elif normal.y < -mn:
        return "back"
