# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "HyModler",
    "author": "Flo_12344 (Florent Daerden)",
    "description": "",
    "blender": (4, 2, 0),
    "version": (1, 0, 0),
    "location": "",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Import/Export/Modeling",
}

from .data import register_properties
from .interface import register_interface
from .operators import register_op


def register():
    register_properties.register_properties()
    register_op.register()
    register_interface.register()


def unregister():
    register_interface.unregister()
    register_op.unregister()
    register_properties.unregister_properties()
