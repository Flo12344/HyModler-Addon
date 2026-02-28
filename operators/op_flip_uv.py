import bpy
import mathutils
import bmesh

import math


class OP_Flip_UV_Vertical(bpy.types.Operator):
    bl_idname = "hymodler.flip_uv_vertical"
    bl_label = "FlipUVVertical"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        ob = bpy.context.edit_object
        me = ob.data
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(me)

        selfaces = [f for f in bm.faces if f.select]
        for f in selfaces:
            obj.hymodler_uv_vertical_flip[f.index] = not obj.hymodler_uv_vertical_flip[
                f.index
            ]
        bm.free()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class OP_Flip_UV_Horizontal(bpy.types.Operator):
    bl_idname = "hymodler.flip_uv_horizontal"
    bl_label = "FlipUVHorizontal"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        ob = bpy.context.edit_object
        me = ob.data
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(me)
        selfaces = [f for f in bm.faces if f.select]
        for f in selfaces:
            obj.hymodler_uv_horizontal_flip[
                f.index
            ] = not obj.hymodler_uv_horizontal_flip[f.index]
        bm.free()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def register():
    bpy.utils.register_class(OP_Flip_UV_Vertical)
    bpy.utils.register_class(OP_Flip_UV_Horizontal)


def unregister():
    bpy.utils.unregister_class(OP_Flip_UV_Vertical)
    bpy.utils.unregister_class(OP_Flip_UV_Horizontal)
