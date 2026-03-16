import bpy
import mathutils
import bmesh

import math


class OP_Export_Single_Animation(bpy.types.Operator):
    bl_idname = "hymodler.export_single_animation"
    bl_label = "AddNewAnimation"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class OP_Add_New_Animation(bpy.types.Operator):
    bl_idname = "hymodler.add_new_animation"
    bl_label = "AddNewAnimation"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def execute(self, context):
        bpy.context.scene.hymodler_animations.add()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class OP_Remove_Animation(bpy.types.Operator):
    bl_idname = "hymodler.remove_animation"
    bl_label = "RemoveAnimation"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    hymodler_id: bpy.props.IntProperty(
        name="ID", description="", default=0, subtype="NONE"
    )

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def execute(self, context):
        bpy.context.scene.hymodler_animations.remove(self.hymodler_id)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


def register():
    bpy.utils.register_class(OP_Remove_Animation)
    bpy.utils.register_class(OP_Add_New_Animation)
    bpy.utils.register_class(OP_Export_Single_Animation)


def unregister():
    bpy.utils.unregister_class(OP_Remove_Animation)
    bpy.utils.unregister_class(OP_Add_New_Animation)
    bpy.utils.unregister_class(OP_Export_Single_Animation)
