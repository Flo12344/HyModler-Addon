import bpy


class HYMODLER_project_settings_panel(bpy.types.Panel):
    bl_label = "ProjectSettings"
    bl_idname = "HYMODLER_PROJECT_SETTINGS_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ""
    bl_category = "HyModler"
    bl_order = 10
    bl_options = {"HEADER_LAYOUT_EXPAND"}
    bl_ui_units_x = 0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout.prop(
            bpy.context.scene,
            "hymodler_texturesize",
            text="Texture Size",
            icon_value=0,
            emboss=True,
        )
        layout.prop(
            bpy.context.scene,
            "hymodler_pos_exp_tresh",
            text="Anim pos treshold",
            icon_value=0,
            emboss=True,
        )
        layout.prop(
            bpy.context.scene,
            "hymodler_rot_exp_tresh",
            text="Anim rot treshold",
            icon_value=0,
            emboss=True,
        )


def register():
    bpy.utils.register_class(HYMODLER_project_settings_panel)


def unregister():
    bpy.utils.unregister_class(HYMODLER_project_settings_panel)
