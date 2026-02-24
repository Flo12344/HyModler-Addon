import bpy


class HYMODLER_object_panel(bpy.types.Panel):
    bl_label = "Objects"
    bl_idname = "HYMODLER_OBJECTS_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ""
    bl_category = "HyModler"
    bl_order = 1
    bl_ui_units_x = 0

    @classmethod
    def poll(cls, context):
        return not (False)

    # def draw_header(self, context):
    #     layout = self.layout
    #     op = layout.operator(
    #         "sn.dummy_button_operator",
    #         text="",
    #         icon_value=49,
    #         emboss=False,
    #         depress=False,
    #     )

    def draw(self, context):
        layout = self.layout
        op = layout.operator(
            "hymodler.create_hybox",
            text="Box",
            icon_value=315,
            emboss=True,
            depress=False,
        )
        op = layout.operator(
            "hymodler.create_hyquad",
            text="Quad",
            icon_value=333,
            emboss=True,
            depress=False,
        )
        op = layout.operator(
            "hymodler.create_hybones",
            text="Bone",
            icon_value=179,
            emboss=True,
            depress=False,
        )
        op = layout.operator(
            "hymodler.create_attachement",
            text="Attachement",
            icon_value=182,
            emboss=True,
            depress=False,
        )


def add_to_view3d_menu(self, context):
    layout = self.layout
    layout.menu("HYMODLER_OBJECTS_PANEL", text="HyMeshes", icon_value=0)


def register():
    bpy.utils.register_class(HYMODLER_object_panel)
    bpy.types.VIEW3D_MT_add.prepend(add_to_view3d_menu)


def unregister():
    bpy.utils.unregister_class(HYMODLER_object_panel)
    bpy.types.VIEW3D_MT_add.remove(add_to_view3d_menu)
