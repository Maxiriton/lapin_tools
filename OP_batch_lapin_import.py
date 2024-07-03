import bpy
import re
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from os import listdir, path, pardir
import random
from .utils import get_addon_prefs

def find_matching_object(object):
    name = object.name
    isolated_name = re.search("(rabbit_[a-zA-Z]+)(_[MRL])?", name)
    isolated_name = isolated_name.group(0)
    isolated_name = isolated_name.replace('_M','.M').replace('_L','.L').replace('_R','.R')

    if isolated_name.endswith('Shape'):
        isolated_name = isolated_name[:-5]

    return bpy.data.objects.get(isolated_name)


class IO_OT_BatchImportLapins(Operator, ImportHelper):
    """Import all lapins in scene"""
    bl_idname = "io.batch_import_lapins"
    bl_label = "Import all lapins"
    bl_options = {'REGISTER','UNDO'}
    
    def execute(self, context):
        #we list all the files in the folder 
        fdir = self.properties.filepath
        if path.isfile(fdir):
            fdir = path.abspath(path.join(fdir, pardir))

        if not bpy.data.collections.get("LapinOriginalRIg"):
            col = bpy.data.collections.new("LapinOriginalRIg")
            context.scene.collection.children.link(col)


        if not bpy.data.collections.get("LapinsCrowd"):
            col_crowd = bpy.data.collections.new("LapinsCrowd")
            context.scene.collection.children.link(col_crowd)

        col_crowd = bpy.data.collections.get("LapinsCrowd")
        #we import the default mesh_rig
        rig_file  = get_addon_prefs().lapin_rig_file
        with bpy.data.libraries.load(rig_file) as (data_from, data_to):
            data_to.objects = data_from.objects

        for obj in data_to.objects:
            if obj.type == 'MESH' and obj.name.startswith('rabbit'):
                bpy.data.collections["LapinOriginalRIg"].objects.link(obj)
                try: 
                    modifier_to_remove = obj.modifiers.get("Subdivision")
                    obj.modifiers.remove(modifier_to_remove)
                except:
                    print('No modifier subdiv to remove')
                try:
                    modifier_to_remove = obj.modifiers.get("Armature")
                    obj.modifiers.remove(modifier_to_remove)
                except:
                    print('No modifier Armature to remove')

        for file_index, file in enumerate(listdir(fdir)):
            if not path.basename(file).endswith('.usda'):
                continue
            full_path = path.join(fdir, file)
            bpy.ops.wm.usd_import(filepath=full_path, 
                import_cameras=False, 
                import_curves=False, 
                import_lights=False, 
                import_materials=True, 
                import_meshes=True, 
                import_volumes=False, 
                scale=0.01, 
                read_mesh_uvs=True, 
                read_mesh_colors=False, 
                import_subdiv=False, 
                import_visible_only=True,
                import_guide=False,
                import_proxy=True,
                import_render=True,
                set_frame_range=True,
                relative_path=True,
                create_collection=True,
                support_scene_instancing=False,
                light_intensity_scale=1.0,
                mtl_name_collision_mode='MAKE_UNIQUE',
                import_usd_preview=True,
                set_material_blend=True)
            
            active_col = context.collection
        
            context.scene.collection.children.unlink(active_col)
            col_crowd.children.link(active_col)

            skel_obj = None
            for obj in context.selected_objects:
                if obj.type == 'ARMATURE':
                    skel_obj = obj
                    break

            regex_number = re.search("Entity_(\d+).", file)
            regex_number = regex_number.group(0)

            random.seed(regex_number)
            random_value = random.random()
            for obj in context.selected_objects:
                if obj.type != 'MESH':
                    continue
                matching_obj = find_matching_object(obj)


                mesh = obj.data
                attribute = mesh.attributes.new(name="color_index", type="FLOAT", domain="POINT")
                attribute_values = [random_value for i in range(len(mesh.vertices))]
                attribute.data.foreach_set("value", attribute_values)


                for v_group in matching_obj.vertex_groups:
                    obj.vertex_groups.new(name=v_group.name)


                context.view_layer.objects.active = obj
                try:
                    bpy.ops.object.modifier_apply(modifier=data_transfer.name)
                except:
                    print(f"Impossible d'appliquer le modificateur data_trasfer pour {obj}")


                for v_group in matching_obj.vertex_groups:
                    obj.vertex_groups.new(name=v_group.name)

                data_transfer  = obj.modifiers.new(name='DATA_TRANSFER', type='DATA_TRANSFER')
                data_transfer.object = matching_obj
                data_transfer.use_vert_data = True
                data_transfer.data_types_verts = {'VGROUP_WEIGHTS'}
                data_transfer.vert_mapping = 'TOPOLOGY'

                context.view_layer.objects.active = obj
                bpy.ops.object.modifier_apply(modifier=data_transfer.name)

                #we sanitize vertex_group to match the name in armature
                for v_group in obj.vertex_groups:
                    v_group.name = v_group.name.replace('.','_')

                #we add the armature to the piece
                armature_mod = obj.modifiers.new(name="ARMATURE", type="ARMATURE")
                armature_mod.object = skel_obj
            print(f'done for {file}')
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