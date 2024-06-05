import bpy
import time
import re
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty
from addon_utils import enable
from os import path

from .utils import get_addon_prefs




class IO_OT_BatchExportFBX(Operator):
    """Export every animation in a separate FBX"""
    bl_idname = "io.batch_export_fbx"
    bl_label = "Export all animation"
    bl_options = {'REGISTER','UNDO'}

    usePrefix : BoolProperty(
        name="Use Action Prefix",
        default=False
    )

    animation_prefixes : StringProperty(
        name="Action Prefixes",
        default="ac, cy",
        description="actions that start with these value will be exported"
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        better_fbx_addon_name = 'better_fbx'

        success = enable(better_fbx_addon_name)
        if not success:
            self.report({'WARNING'}, "Please enable the better fbx addon ! ")
            return {'CANCELLED'}
        else:
            print("better fbx is installed, let's export some animation")


        rel_path = get_addon_prefs().export_folder_default
        abs_path = bpy.path.abspath(rel_path)
        obj = context.active_object

        #we store the current action
        current_action = obj.animation_data.action

        for action in bpy.data.actions: 
            if self.usePrefix :
                prefixes  = self.animation_prefixes.replace(",","|").replace(" ", "")
                if not re.match(f"^({prefixes})",action.name):
                    continue

            obj.animation_data.action = action
            file_name = f"{obj.name}_{action.name}.fbx"

            file_path = path.join(abs_path, file_name)
            start = time.time()

            bpy.ops.better_export.fbx(filepath=file_path, 
                                        my_fbx_axis='Unity', 
                                        use_selection=True,
                                        use_only_deform_bones=True,
                                        use_animation=True,
                                        use_export_materials=False,
                                        my_animation_type='Active')
            
            end = time.time()
            print(f"Export for {file_name} done in {end-start}s")


        #we restore the previous current_action
        obj.animation_data.action = current_action
        return {'FINISHED'}
    
### Registration

classes = (
IO_OT_BatchExportFBX,
)

def register():
    for cl in classes:  
        bpy.utils.register_class(cl)

def unregister():
    for cl in reversed(classes):
        bpy.utils.unregister_class(cl)