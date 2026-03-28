import math

import bmesh
import bpy
from . import hyobject_uv


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

    obj.name = "HyQuad"
    return obj


def create_hyarmature():
    armature_data = bpy.data.armatures.new("HyArmature")
    obj = bpy.data.objects.new("HyArmatureObject", armature_data)
    bpy.context.collection.objects.link(obj)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode="EDIT")
    bone = armature_data.edit_bones.new("Bone")
    bone.head = (0, 0, 0)
    bone.tail = (0, 0, 1)
    bpy.ops.object.mode_set(mode="OBJECT")

    obj["hymesh"] = True
    obj["type"] = "none"
    return obj


def create_attachement():
    obj = bpy.data.objects.new("HyAttachement", None)
    obj.empty_display_type = "PLAIN_AXES"
    bpy.context.collection.objects.link(obj)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    obj["hymesh"] = True
    obj["type"] = "none"
    return obj


def create_group():
    obj = bpy.data.objects.new("HyGroup", None)
    obj.empty_display_type = "PLAIN_AXES"
    bpy.context.collection.objects.link(obj)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    obj["hymesh"] = True
    obj["type"] = "none"
    return obj
