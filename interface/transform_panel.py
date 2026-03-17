import bpy
from .. import helper


class HYMODLER_transform_panel(bpy.types.Panel):
    bl_label = "Transform"
    bl_idname = "HYMODLER_TRANSFORM_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ""
    bl_category = "HyModler"
    bl_order = 1
    bl_options = {"HEADER_LAYOUT_EXPAND"}
    bl_ui_units_x = 0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        if helper.is_selected_valid():
            obj = bpy.context.active_object
            main_col = layout.column(heading="", align=True)
            main_col.alert = False
            main_col.enabled = True
            main_col.active = True
            main_col.use_property_split = True
            main_col.use_property_decorate = False
            main_col.scale_x = 1.0
            main_col.scale_y = 1.0
            main_col.alignment = "Expand".upper()
            main_col.operator_context = "INVOKE_DEFAULT"
            sub_col = main_col.column(heading="", align=True)
            sub_col.alert = False
            sub_col.enabled = True
            sub_col.active = True
            sub_col.use_property_split = True
            sub_col.use_property_decorate = True
            sub_col.scale_x = 1.0
            sub_col.scale_y = 1.0
            sub_col.alignment = "Expand".upper()
            sub_col.operator_context = "INVOKE_DEFAULT"
            sub_col.label(text="Position", icon_value=0)
            sub_col.prop(
                bpy.data.objects[obj.name],
                "location",
                text="X",
                icon_value=0,
                emboss=True,
                index=0,
            )
            sub_col.prop(
                bpy.data.objects[obj.name],
                "location",
                text="Y",
                icon_value=0,
                emboss=True,
                index=1,
            )
            sub_col.prop(
                bpy.data.objects[obj.name],
                "location",
                text="Z",
                icon_value=0,
                emboss=True,
                index=2,
            )
            sub_col.label(text="Rotation", icon_value=0)
            if obj.rotation_mode == "QUATERNION":
                sub_col.prop(obj, "rotation_quaternion", text="W", index=0)
                sub_col.prop(obj, "rotation_quaternion", text="X", index=1)
                sub_col.prop(obj, "rotation_quaternion", text="Y", index=2)
                sub_col.prop(obj, "rotation_quaternion", text="Z", index=3)

            elif obj.rotation_mode == "AXIS_ANGLE":
                sub_col.prop(obj, "rotation_axis_angle", text="Angle", index=0)
                sub_col.prop(obj, "rotation_axis_angle", text="X", index=1)
                sub_col.prop(obj, "rotation_axis_angle", text="Y", index=2)
                sub_col.prop(obj, "rotation_axis_angle", text="Z", index=3)

            else:
                sub_col.prop(obj, "rotation_euler", text="X", index=0)
                sub_col.prop(obj, "rotation_euler", text="Y", index=1)
                sub_col.prop(obj, "rotation_euler", text="Z", index=2)

            sub_col.label(text="Stretch", icon_value=0)
            sub_col.prop(
                bpy.data.objects[obj.name],
                "scale",
                text="X",
                icon_value=0,
                emboss=True,
                index=0,
            )
            sub_col.prop(
                bpy.data.objects[obj.name],
                "scale",
                text="Y",
                icon_value=0,
                emboss=True,
                index=1,
            )
            sub_col.prop(
                bpy.data.objects[obj.name],
                "scale",
                text="Z",
                icon_value=0,
                emboss=True,
                index=2,
            )
            sub_col.label(text="Size", icon_value=0)
            sub_col.prop(
                obj,
                "hymodler_size",
                text="X",
                icon_value=0,
                emboss=True,
                index=0,
            )
            sub_col.prop(
                obj,
                "hymodler_size",
                text="Y",
                icon_value=0,
                emboss=True,
                index=1,
            )
            if obj["type"] != "quad":
                sub_col.prop(
                    obj,
                    "hymodler_size",
                    text="Z",
                    icon_value=0,
                    emboss=True,
                    index=2,
                )
            main_col.separator(factor=1.0)
            main_col.prop(
                obj,
                "hymodler_shadingmode",
                text="Shading Mode",
                icon_value=0,
                emboss=True,
            )
            main_col.prop(
                obj,
                "hymodler_doublesided",
                text="Double Sided",
                icon_value=0,
                emboss=True,
            )


def register():
    bpy.utils.register_class(HYMODLER_transform_panel)


def unregister():
    bpy.utils.unregister_class(HYMODLER_transform_panel)
