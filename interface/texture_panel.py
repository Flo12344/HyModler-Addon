import bpy


class HYMODLER_texture_panel(bpy.types.Panel):
    bl_label = "Texture"
    bl_idname = "HYMODLER_TEXTURE_PANEL"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_context = ""
    bl_category = "HyModler UV"
    bl_order = 0
    bl_ui_units_x = 0

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        op = layout.operator(
            "hymodler.generate_template_texture",
            text="new Template texture",
            icon_value=0,
            emboss=True,
            depress=False,
        )


def register():
    bpy.utils.register_class(HYMODLER_texture_panel)


def unregister():
    bpy.utils.unregister_class(HYMODLER_texture_panel)
