import bpy
import random

bpy.ops.mesh.primitive_grid_add(x_subdivisions=100, y_subdivisions=100, enter_editmode=False, location=(0, 0, 0))

obj = bpy.context.active_object

#[height,area],[height,area]
small_prop_sizes= [[0.02,0.4],[0.03,0.1]]
med_prop_sizes= [[0.04,0.3],[0.07,0.2]]
large_prop_sizes= [[0.3,0.2],[0.1, 0.3]]

#------------------------------------------------

def clear_materials():
    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)
        
def correct_normals():
    #CORRECT NORMALS
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.mesh.normals_make_consistent(inside=True)
    #APPLY SUBSURF MODIFIER
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 2
    bpy.context.object.modifiers["Subdivision"].render_levels = 2

    bpy.ops.object.mode_set(mode = 'OBJECT') 
    
    bpy.ops.object.modifier_apply(modifier="Subdivision")

#DISPLACE SELECTED VERTEX
def createRandom(height, area, prop_type):
    
    random_vertex = random.randrange(0, 10000)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.active_object
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj.data.vertices[random_vertex].select = True
    bpy.ops.object.mode_set(mode = 'EDIT') 
    
    bpy.ops.transform.translate(value=(0, 0, height), constraint_axis=(False, False, True), mirror=False, use_proportional_edit=True, proportional_edit_falloff=prop_type, proportional_size=area, release_confirm=True, use_accurate=False)

#SMALL UPWARDS DISPLACEMENT
def small_up_displacement(inst):
    for i in range(inst):
        random_terrain = random.randrange(0, len(small_prop_sizes))
        height_level = small_prop_sizes[random_terrain][0]
        terrain_area = small_prop_sizes[random_terrain][1]
        createRandom(height_level,terrain_area,'RANDOM')

#MEDIUM UPWARDS DISPLACEMENT
def medium_up_displacement(inst):   
    for i in range(inst):
        random_terrain = random.randrange(0, len(med_prop_sizes))
        height_level = med_prop_sizes[random_terrain][0]
        terrain_area = med_prop_sizes[random_terrain][1]
        createRandom(height_level,terrain_area,'RANDOM')
    
#LARGE UPWARDS DISPLACEMENT
def large_up_displacement(inst):
    for i in range(inst):
        random_terrain = random.randrange(0, len(large_prop_sizes))
        height_level = large_prop_sizes[random_terrain][0]
        terrain_area = large_prop_sizes[random_terrain][1]
        createRandom(height_level,terrain_area,'RANDOM')

#MEDIUM DOWN DISPLACEMENT
def medium_down_displacement(inst,mode):
    for i in range(inst):
        random_terrain = random.randrange(0, len(med_prop_sizes))
        height_level = med_prop_sizes[random_terrain][0]
        terrain_area = med_prop_sizes[random_terrain][1]
        createRandom(-height_level,terrain_area,mode)
        
#GENERATE TERRAIN (MAIN FUNCTION)
def generate(small_up, med_up, large_up, med_down_rnd, med_down_sph):
    small_up_displacement(small_up)
    medium_up_displacement(med_up)
    large_up_displacement(large_up)
    
    medium_down_displacement(med_down_rnd, "RANDOM")
    medium_down_displacement(med_down_sph, "SPHERE")
    
def add_water():
    #ADD WATER PLANE
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, 0, -0.02))
    ob = bpy.context.active_object
    
    mat = bpy.data.materials.new(name="Water_Mat")
    mat.diffuse_color = (0.106624, 0.163643, 0.8, 0)
    
    ob.data.materials.append(mat)
    
def terrain_mat():
    #APPLY TERRAIN MATERIAL
    mat = bpy.data.materials.new(name="Terrain_Mat")
    mat.diffuse_color = (0.115416, 0.353016, 0.10082, 0)

    ob.data.materials.append(mat)
    
def vertex_mat(r,g,b,mat_name,direction,value):
    #MATERIALS FOR VERTICES
    bpy.ops.object.mode_set(mode = 'OBJECT')
    ob = bpy.context.active_object
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')

    for vertex in ob.data.vertices:
        if direction == 1:
            if vertex.co.z >= value:
                vertex.select = True
        else:
            if vertex.co.z <= value:
                vertex.select = True
            
    bpy.ops.object.mode_set(mode = 'EDIT')

    mat = bpy.data.materials.new(name=mat_name)
    mat.diffuse_color = (r,g,b,0)

    ob.data.materials.append(mat)
    
    ob.active_material_index = len(ob.data.materials)-1
    bpy.ops.object.material_slot_assign()
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
#------------------------------------------------

clear_materials()
generate(5,10,10,15,3)

correct_normals()

ob = bpy.context.active_object

terrain_mat()
vertex_mat(0.8,0.635,0.329,"Sand_Mat",0,-0.01)
vertex_mat(0.202,0.3530,0.221,"High_Mat",1,0.04)
vertex_mat(0.705725,0.8,0.601591,"Snow_Mat",1,0.1)

add_water()