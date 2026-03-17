import bpy


class HYMODLER_parent_panel(bpy.types.Panel):
    bl_label = "Parent"
    bl_idname = "HYMODLER_PARENT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ""
    bl_category = "HyModler"
    bl_order = 2
    bl_ui_units_x = 0

    @classmethod
    def poll(cls, context):
        return False

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout


def register():
    bpy.utils.register_class(HYMODLER_parent_panel)


def unregister():
    bpy.utils.unregister_class(HYMODLER_parent_panel)
