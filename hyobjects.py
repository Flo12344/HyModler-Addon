import math

import bmesh
import bpy


def create_hybox():
    size = 0.1
    verts = [
        (size, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (size, size, 0.0),
        (0.0, size, 0.0),
        (0.0, 0.0, size),
        (size, 0.0, size),
        (0.0, size, size),
        (size, size, size),
    ]
    faces = [
        (2, 3, 6, 7),  # north
        (0, 2, 7, 5),  # east
        (1, 0, 5, 4),  # south
        (3, 1, 4, 6),  # west
        (7, 6, 4, 5),  # up
        (0, 1, 3, 2),  # down
    ]
    face_uvs = [
        (0.0, 0.0),
        (0.0, 1.0),
        (1.0, 1.0),
        (1.0, 0.0),
    ]
    mesh = bpy.data.meshes.new("HyBoxMesh")
    obj = bpy.data.objects.new("HyBox", mesh)
    bpy.context.collection.objects.link(obj)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    uv_layer = mesh.uv_layers.new(name="UVMap")
    for poly in mesh.polygons:
        for i, loop_index in enumerate(poly.loop_indices):
            uv_layer.data[loop_index].uv = face_uvs[i]
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    obj["hymesh"] = True
    obj["type"] = "box"
    fd = {}
    fd["r"] = [0, 0, 0, 0, 0, 0]
    fd["mx"] = [False, False, False, False, False, False]
    fd["my"] = [False, False, False, False, False, False]
    obj["fd"] = fd
    obj.rotation_mode = "QUATERNION"
    return obj


def create_hyquad():
    size = 0.1
    verts = [
        (size, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (size, 0.0, size),
        (0.0, 0.0, size),
    ]
    faces = [
        (0, 1, 3, 2),  # down
    ]
    face_uvs = [
        (0.0, 0.0),
        (0.0, 1.0),
        (1.0, 1.0),
        (1.0, 0.0),
    ]
    mesh = bpy.data.meshes.new("HyQuadMesh")
    obj = bpy.data.objects.new("HyQuad", mesh)
    bpy.context.collection.objects.link(obj)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    uv_layer = mesh.uv_layers.new(name="UVMap")
    for poly in mesh.polygons:
        for i, loop_index in enumerate(poly.loop_indices):
            uv_layer.data[loop_index].uv = face_uvs[i]
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    obj["hymesh"] = True
    obj["type"] = "quad"
    fd = {}
    fd["r"] = [0]
    fd["mx"] = [False]
    fd["my"] = [False]
    obj["fd"] = fd

    obj.name = "HyQuad"
    obj.rotation_mode = "QUATERNION"
    return obj


def create_hyarmature():
    bpy.ops.object.armature_add()
    obj = bpy.context.active_object
    obj["hymesh"] = True
    obj["type"] = "none"
    obj.name = "HyArmature"
    obj.rotation_mode = "QUATERNION"
    return obj


def create_attachement():
    bpy.ops.object.empty_add(type="PLAIN_AXES")
    obj = bpy.context.active_object
    obj["hymesh"] = True
    obj["type"] = "none"
    obj.name = "HyAttachement"
    obj.rotation_mode = "QUATERNION"
    return obj


def create_group():
    bpy.ops.object.empty_add(type="PLAIN_AXES")
    obj = bpy.context.active_object
    obj["hymesh"] = True
    obj["type"] = "none"
    obj.name = "HyGroup"
    obj.rotation_mode = "QUATERNION"
    return obj
