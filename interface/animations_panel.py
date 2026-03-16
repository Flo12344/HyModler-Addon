import bpy
from .. import helper


class HYMODLER_animations_panel(bpy.types.Panel):
    bl_label = "Animations"
    bl_idname = "HYMODLER_ANIMATIONS_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ""
    bl_category = "HyModler"
    bl_order = 8
    bl_ui_units_x = 0

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        for i in range(len(bpy.context.scene.hymodler_animations)):
            box = layout.box()
            box.alert = False
            box.enabled = True
            box.active = True
            box.use_property_split = False
            box.use_property_decorate = False
            box.alignment = "Expand".upper()
            box.scale_x = 1.0
            box.scale_y = 1.0
            row = box.row(heading="", align=False)
            row.enabled = True
            row.active = True
            row.use_property_split = False
            row.use_property_decorate = False
            row.scale_x = 1.0
            row.scale_y = 1.0
            row.alignment = "Expand".upper()
            row.operator_context = "INVOKE_DEFAULT"
            col = row.column(heading="", align=True)
            col.alert = False
            col.enabled = True
            col.active = True
            col.use_property_split = True
            col.use_property_decorate = False
            col.scale_x = 1.0
            col.scale_y = 1.0
            col.alignment = "Expand".upper()
            col.operator_context = "INVOKE_DEFAULT"
            col.prop(
                bpy.context.scene.hymodler_animations[i],
                "name",
                text="Name",
                icon_value=0,
                emboss=True,
            )
            col.prop(
                bpy.context.scene.hymodler_animations[i],
                "action",
                text="Action",
                icon_value=0,
                emboss=True,
            )
            col.prop(
                bpy.context.scene.hymodler_animations[i],
                "start",
                text="Start",
                icon_value=0,
                emboss=True,
            )
            col.prop(
                bpy.context.scene.hymodler_animations[i],
                "end",
                text="End",
                icon_value=0,
                emboss=True,
            )

            col = row.column(heading="", align=True)
            op = col.operator(
                "hymodler.remove_animation",
                text="",
                icon_value=101,
                emboss=True,
                depress=False,
            )
            col.operator(
                "hymodler.export_single_animation",
                text="",
                icon="FILE_TICK",
            )
            op.hymodler_id = i
        op = layout.operator(
            "hymodler.add_new_animation",
            text="",
            icon_value=50,
            emboss=True,
            depress=False,
        )
        if len(bpy.context.scene.hymodler_animations) > 1:
            op = layout.operator(
                "hymodler.export_all_animations",
                text="Export All",
                icon="FILE_TICK",
                emboss=True,
                depress=False,
            )


def register():
    bpy.utils.register_class(HYMODLER_animations_panel)


def unregister():
    bpy.utils.unregister_class(HYMODLER_animations_panel)
