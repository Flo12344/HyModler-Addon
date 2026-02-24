import bpy

from .. import hyobjects


class OT_create_attachement(bpy.types.Operator):
    bl_idname = "hymodler.create_attachement"
    bl_label = "CreateAttachement"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def execute(self, context):
        hyobjects.create_attachement()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class OT_create_hybox(bpy.types.Operator):
    bl_idname = "hymodler.create_hybox"
    bl_label = "CreateHybox"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def execute(self, context):
        hyobjects.create_hybox()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class OT_create_hyquad(bpy.types.Operator):
    bl_idname = "hymodler.create_hyquad"
    bl_label = "CreateHyquad"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def execute(self, context):
        hyobjects.create_hyquad()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class OT_create_hybones(bpy.types.Operator):
    bl_idname = "hymodler.create_hybones"
    bl_label = "CreateHybones"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def execute(self, context):
        hyobjects.create_hyarmature()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def register():
    bpy.utils.register_class(OT_create_attachement)
    bpy.utils.register_class(OT_create_hybox)
    bpy.utils.register_class(OT_create_hyquad)
    bpy.utils.register_class(OT_create_hybones)
    pass


def unregister():
    bpy.utils.unregister_class(OT_create_attachement)
    bpy.utils.unregister_class(OT_create_hybox)
    bpy.utils.unregister_class(OT_create_hyquad)
    bpy.utils.unregister_class(OT_create_hybones)
    pass
