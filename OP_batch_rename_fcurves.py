import bpy 
import re 
from bpy.types import Operator


class IO_OT_BatchRenameFcurves(Operator):
    """Import all lapins in scene"""
    bl_idname = "io.batch_rename_fcurves"
    bl_label = "Lapin Batch rename fcurves"
    bl_options = {'REGISTER','UNDO'}
    
    def execute(self, context):
        print('prout')

        for action in bpy.data.actions:
            print(action.name)
            for curve in action.fcurves:
                try : 
                    prefix = re.match(r'(pose.bones[\")(.+)("].+)', curve.data_path).group(1)
                    bone_name = re.match(r'(pose.bones[\")(.+)("].+)', curve.data_path).group(2)
                    postfix = re.match(r'(pose.bones[\")(.+)("].+)', curve.data_path).group(3)
                    curve.data_path = f'{prefix}{bone_name.replace(".","_")}{postfix}'
                    print(curve.data_path)
                except:
                    print(f"No match for {curve.data_path}")

        return {'FINISHED'}
    
### Registration

classes = (
IO_OT_BatchRenameFcurves,
)

def register():
    for cl in classes:  
        bpy.utils.register_class(cl)

def unregister():
    for cl in reversed(classes):
        bpy.utils.unregister_class(cl)



