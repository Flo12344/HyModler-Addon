from . import object_panel
from . import transform_panel
from . import project_settings_panel
from . import uv_panel
from . import texture_panel
from . import animations_panel
from . import parent_panel


def register():
    object_panel.register()
    transform_panel.register()
    project_settings_panel.register()
    uv_panel.register()
    texture_panel.register()
    animations_panel.register()
    parent_panel.register()


def unregister():
    object_panel.unregister()
    transform_panel.unregister()
    project_settings_panel.unregister()
    uv_panel.unregister()
    texture_panel.unregister()
    animations_panel.unregister()
    parent_panel.unregister()
