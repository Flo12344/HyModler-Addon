import bpy


class HYMODLER_uv_panel(bpy.types.Panel):
    bl_label = "HyModler UV"
    bl_idname = "HYMODLER_UV_PANEL"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_context = ""
    bl_category = "HyModler UV"
    bl_order = 0
    bl_ui_units_x = 0

    @classmethod
    def poll(cls, context):
        return "EDIT_MESH" == bpy.context.mode

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        row = layout.row(heading="", align=True)
        row.alert = False
        row.enabled = True
        row.active = True
        row.use_property_split = False
        row.use_property_decorate = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.alignment = "Expand".upper()
        row.operator_context = "INVOKE_DEFAULT"
        op = row.operator(
            "hymodler.rotate_uv_90_minus",
            text="-90",
            icon_value=0,
            emboss=True,
            depress=False,
        )
        op = row.operator(
            "hymodler.rotate_uv_90_plus",
            text="+90",
            icon_value=0,
            emboss=True,
            depress=False,
        )
        op = layout.operator(
            "hymodler.flip_uv_horizontal",
            text="Mirror X",
            icon_value=379,
            emboss=True,
            depress=False,
        )
        op = layout.operator(
            "hymodler.flip_uv_vertical",
            text="Mirror Y",
            icon_value=378,
            emboss=True,
            depress=False,
        )


def register():
    bpy.utils.register_class(HYMODLER_uv_panel)


def unregister():
    bpy.utils.unregister_class(HYMODLER_uv_panel)
