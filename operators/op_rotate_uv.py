import bpy
import mathutils
import bmesh

from .. import hyobject_uv

import math


class OP_Rotate_UV_90_Plus(bpy.types.Operator):
    bl_idname = "hymodler.rotate_uv_90_plus"
    bl_label = "RotateUV90plus"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context = bpy.context
        ob = context.edit_object
        me = ob.data
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(me)
        uv_lay = bm.loops.layers.uv.verify()
        texture_size = bpy.context.scene.hymodler_texturesize
        PIXEL_WIDTH = 1.0 / texture_size[0]
        PIXEL_HEIGHT = 1.0 / texture_size[1]

        selfaces = [f for f in bm.faces if f.select]
        for f in selfaces:
            width, height = hyobject_uv.normal_to_hytale_wh(f.normal, obj.hymodler_size)
            w = width
            h = height
            cr = obj["fd"]["r"][f.index]
            bx, by = hyobject_uv.rotation_offset(
                (w, h), hyobject_uv.get_current_rotation(f.loops, uv_lay)
            )
            cr += 1
            ox, oy = hyobject_uv.rotation_offset((w, h), cr)
            x = f.loops[0][uv_lay].uv.x - PIXEL_WIDTH * bx + PIXEL_WIDTH * ox
            y = f.loops[0][uv_lay].uv.y - PIXEL_HEIGHT * by + PIXEL_HEIGHT * oy
            local_uvs = [
                (0, 0),
                (w, 0),
                (w, h),
                (0, h),
            ]
            for loop, uv in zip(f.loops, local_uvs):
                rx, ry = hyobject_uv.rotate(uv, cr)
                loop[uv_lay].uv = mathutils.Vector(
                    (x + PIXEL_WIDTH * rx, y + PIXEL_HEIGHT * ry)
                )
            obj["fd"]["r"][f.index] = cr % 4
        bmesh.update_edit_mesh(me)
        bm.free()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class OP_Rotate_UV_90_Minus(bpy.types.Operator):
    bl_idname = "hymodler.rotate_uv_90_minus"
    bl_label = "RotateUV90minus"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context = bpy.context
        ob = context.edit_object
        me = ob.data
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(me)
        uv_lay = bm.loops.layers.uv.verify()
        texture_size = bpy.context.scene.hymodler_texturesize
        PIXEL_WIDTH = 1.0 / texture_size[0]
        PIXEL_HEIGHT = 1.0 / texture_size[1]

        selfaces = [f for f in bm.faces if f.select]
        for f in selfaces:
            width, height = hyobject_uv.normal_to_hytale_wh(f.normal, obj.hymodler_size)
            w = width
            h = height
            cr = obj["fd"]["r"][f.index]
            bx, by = hyobject_uv.rotation_offset(
                (w, h), hyobject_uv.get_current_rotation(f.loops, uv_lay)
            )
            cr -= 1
            ox, oy = hyobject_uv.rotation_offset((w, h), cr)
            x = f.loops[0][uv_lay].uv.x - PIXEL_WIDTH * bx + PIXEL_WIDTH * ox
            y = f.loops[0][uv_lay].uv.y - PIXEL_HEIGHT * by + PIXEL_HEIGHT * oy
            local_uvs = [
                (0, 0),
                (w, 0),
                (w, h),
                (0, h),
            ]
            for loop, uv in zip(f.loops, local_uvs):
                rx, ry = hyobject_uv.rotate(uv, cr)
                loop[uv_lay].uv = mathutils.Vector(
                    (x + PIXEL_WIDTH * rx, y + PIXEL_HEIGHT * ry)
                )
            obj["fd"]["r"][f.index] = cr % 4
        bmesh.update_edit_mesh(me)
        bm.free()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def register():
    bpy.utils.register_class(OP_Rotate_UV_90_Plus)
    bpy.utils.register_class(OP_Rotate_UV_90_Minus)


def unregister():
    bpy.utils.unregister_class(OP_Rotate_UV_90_Plus)
    bpy.utils.unregister_class(OP_Rotate_UV_90_Minus)
