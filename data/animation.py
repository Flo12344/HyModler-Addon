import bpy


class GROUP_animation_data(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Name", description="", default="animation", subtype="NONE", maxlen=0
    )
    action: bpy.props.PointerProperty(
        name="Action", description="", type=bpy.types.Action
    )
    start: bpy.props.IntProperty(
        name="Start", description="", default=0, subtype="NONE"
    )
    end: bpy.props.IntProperty(name="End", description="", default=0, subtype="NONE")
