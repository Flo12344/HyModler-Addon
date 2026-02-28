from . import op_hyobject
from . import op_export_blockymodel
from . import op_import_blockymodel
from . import op_rotate_uv
from . import op_flip_uv
from . import op_generate_template_texture
from . import op_animations


def register():
    op_hyobject.register()
    op_export_blockymodel.register()
    op_import_blockymodel.register()
    op_rotate_uv.register()
    op_flip_uv.register()
    op_generate_template_texture.register()
    op_animations.register()


def unregister():
    op_hyobject.unregister()
    op_export_blockymodel.unregister()
    op_import_blockymodel.unregister()
    op_rotate_uv.unregister()
    op_flip_uv.unregister()
    op_generate_template_texture.unregister()
    op_animations.unregister()
