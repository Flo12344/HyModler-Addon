import bpy

from . import animation
from .. import hyobject_edit
from .. import hyobject_uv


def register_properties():
    bpy.utils.register_class(animation.GROUP_animation_data)
    bpy.types.Object.hymodler_size = bpy.props.IntVectorProperty(
        name="Size",
        description="",
        size=3,
        default=(1, 1, 1),
        subtype="NONE",
        update=hyobject_edit.set_hyobject_size,
    )
    bpy.types.Object.hymodler_uv_rotation = bpy.props.IntVectorProperty(
        name="UV Rotation",
        description="",
        size=6,
        default=(0, 0, 0, 0, 0, 0),
        subtype="NONE",
        update=hyobject_uv.update_uv,
    )
    bpy.types.Object.hymodler_uv_vertical_flip = bpy.props.BoolVectorProperty(
        name="UV Vertical Flip",
        description="",
        size=6,
        default=(False, False, False, False, False, False),
        subtype="NONE",
        update=hyobject_uv.update_uv,
    )
    bpy.types.Object.hymodler_uv_horizontal_flip = bpy.props.BoolVectorProperty(
        name="UV Horizontal Flip",
        description="",
        size=6,
        default=(False, False, False, False, False, False),
        subtype="NONE",
        update=hyobject_uv.update_uv,
    )

    bpy.types.Object.hymodler_bbname = bpy.props.StringProperty(
        name="BB Name", description="", default="", subtype="NONE", maxlen=0
    )
    bpy.types.Object.hymodler_shadingmode = bpy.props.EnumProperty(
        name="ShadingMode",
        description="",
        items=[
            ("flat", "flat", "", 0, 0),
            ("standard", "standard", "", 0, 1),
            ("fullbright", "fullbright", "", 0, 2),
            ("reflective", "reflective", "", 0, 3),
        ],
    )
    bpy.types.Object.hymodler_doublesided = bpy.props.BoolProperty(
        name="DoubleSided", description="", default=False
    )
    bpy.types.Scene.hymodler_texturesize = bpy.props.IntVectorProperty(
        name="TextureSize",
        description="",
        size=2,
        default=(32, 32),
        subtype="NONE",
        update=hyobject_edit.set_texture_size,
    )
    bpy.types.Scene.hymodler_pos_exp_tresh = bpy.props.FloatProperty(
        name="POS_EXP_TRESH",
        description="",
        default=0.0010000000474974513,
        subtype="NONE",
        unit="LENGTH",
        step=3,
        precision=6,
    )
    bpy.types.Scene.hymodler_rot_exp_tresh = bpy.props.FloatProperty(
        name="ROT_EXP_TRESH",
        description="",
        default=0.001745329238474369,
        subtype="NONE",
        unit="ROTATION",
        step=3,
        precision=6,
    )
    bpy.types.Scene.hymodler_animations = bpy.props.CollectionProperty(
        name="Animations", description="", type=animation.GROUP_animation_data
    )


def unregister_properties():
    del bpy.types.Scene.hymodler_animations
    del bpy.types.Scene.hymodler_rot_exp_tresh
    del bpy.types.Scene.hymodler_pos_exp_tresh
    del bpy.types.Scene.hymodler_texturesize
    del bpy.types.Object.hymodler_doublesided
    del bpy.types.Object.hymodler_shadingmode
    del bpy.types.Object.hymodler_size
    bpy.utils.unregister_class(animation.GROUP_animation_data)
    pass
