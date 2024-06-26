import bpy 
from bpy.types import Operator
from bpy.props import StringProperty
from mathutils import Matrix

def matrix_world(ArmatureObject,Bone):
    _bone = ArmatureObject.pose.bones[Bone]
    _obj = ArmatureObject
    return _obj.matrix_world @ _bone.matrix

# def matrix_world(armature_ob, bone_name):
#     local = armature_ob.data.bones[bone_name].matrix_local
#     basis = armature_ob.pose.bones[bone_name].matrix_basis
    
#     parent = armature_ob.pose.bones[bone_name].parent
#     if parent == None:
#         return  local * basis
#     else:
#         parent_local = armature_ob.data.bones[parent.name].matrix_local
#         return matrix_world(armature_ob, parent.name) @ (parent_local.inverted() * local) @ basis

def delete_parents_keyframes(bone):
    bone.keyframe_delete('location')
    bone.keyframe_delete('rotation_euler')
    bone.keyframe_delete('scale')
    if bone.parent != None:
        delete_parents_keyframes(bone.parent)

def reset_parent_value(bone):
    bone.matrix = Matrix()
    if bone.parent != None:
        reset_parent_value(bone.parent)


class IO_OT_BakeAnimToBone(Operator):
    """Store Anim in specific bone"""
    bl_idname = "io.bake_anim_to_bone"
    bl_label = "Bake bone animation"
    bl_options = {'REGISTER','UNDO'}

    bone_to_bake : StringProperty(
        name="Bone to store",
        default="Walk_Rabbit"
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        arma = context.active_object
        cur_action = arma.animation_data.action

        #on store la position en world 
        matrices = {}
        for frame in range(int(cur_action.frame_range[0]),int(cur_action.frame_range[1]) +1):
            context.scene.frame_set(frame)
            mat_world  = matrix_world(arma, self.bone_to_bake)
            matrices[frame] = mat_world

        #on supprime les clé d'anim sur tout les parents
        for frame in range(int(cur_action.frame_range[0]),int(cur_action.frame_range[1]) +1):
            context.scene.frame_set(frame)
            parent_bone = arma.pose.bones[self.bone_to_bake]
            delete_parents_keyframes(parent_bone)
            reset_parent_value(parent_bone)

        context.scene.frame_set(int(cur_action.frame_range[0]))



        #on reapplique la transform sur le bone en question 
        for frame in range(int(cur_action.frame_range[0]),int(cur_action.frame_range[1]) +1):
            context.scene.frame_set(frame)
            arma.pose.bones[self.bone_to_bake].matrix = matrices[frame]
            arma.pose.bones[self.bone_to_bake].keyframe_insert('location')
            arma.pose.bones[self.bone_to_bake].keyframe_insert('rotation_euler')
            arma.pose.bones[self.bone_to_bake].keyframe_insert('scale')



        print(f'prout {self.bone_to_bake}')
        return {'FINISHED'}


### Registration

classes = (
IO_OT_BakeAnimToBone,
)

def register():
    for cl in classes:  
        bpy.utils.register_class(cl)

def unregister():
    for cl in reversed(classes):
        bpy.utils.unregister_class(cl)