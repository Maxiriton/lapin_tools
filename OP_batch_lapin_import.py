import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from .utils import get_addon_prefs

class IO_OT_BatchImportLapins(Operator, ImportHelper):
    """Import """
    bl_idname = "io.batch_import_lapins"
    bl_label = "Import all lapins"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.active_object.type == 'ARMATURE'
    
    def execute(self, context):
        return {'FINISHED'}


### Registration

classes = (
IO_OT_BatchImportLapins,
)

def register():
    for cl in classes:  
        bpy.utils.register_class(cl)

def unregister():
    for cl in reversed(classes):
        bpy.utils.unregister_class(cl)