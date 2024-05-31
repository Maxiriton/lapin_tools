# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Lapin Tools",
    "author": "Henri Hebeisen, Leandro ",
    "version": (0, 0, 1),
    "blender": (4, 1, 0),
    "location": "3D View > Properties Region > View",
    "description": "Various Helper tools for the Lapins team",
    "warning": "",
    "wiki_url": "",
    "category": "3D View",
    }

from .utils import get_addon_prefs

import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty
from . import OP_batch_fbx_export
from . import OP_batch_lapin_import


class LAPINS_prefs(AddonPreferences):
    bl_idname = __package__

    export_folder_default : StringProperty(
        name="Default Exports folder",
        description="Folder name for exports, should be relative to work correctly",
        default="//FBXs\\",
        subtype='DIR_PATH'
    )

    def draw(self, context):
        layout = self.layout
        row= layout.row(align=True)
        row.prop(self, "export_folder_default")
       
classes = (
    LAPINS_prefs,
)

addon_modules = (
    OP_batch_fbx_export,
    OP_batch_lapin_import,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    for mod in addon_modules:
        mod.register()
  
def unregister():
    for mod in reversed(addon_modules):
        mod.unregister()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()