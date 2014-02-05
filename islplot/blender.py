import bpy
from islpy import *
from islplot.support import *

def make_material(name, color_diffuse, color_specular, alpha):
    """
    Create a blender material.

    :param name: The name.
    :param color_diffuse: The diffuse color.
    :param color_specular: The specular color.
    :param alpha: The alpha channel.
    """
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color_diffuse
    mat.diffuse_shader = 'LAMBERT'
    mat.diffuse_intensity = 1.0
    mat.specular_color = color_specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    mat.use_transparency = True
    return mat

# Define a set of default colors
red = make_material('Red', (1,0.1,0.1), (1,1,1), 1)
green = make_material('Green', (0,1,0), (1,1,1), 1)
blue = make_material('Blue', (0,0.3,1), (1,1,1), 1)
white = make_material('White', (1,1,1), (0.2,0.2,0.2), 0.4)
black = make_material('Black', (0,0,0), (1,1,1), 1)

def remove_default_cube():
    """
    Remove the cube that is in the blender default scene to get an empty scene.
    """
    bpy.data.objects["Cube"].select = True
    bpy.ops.object.delete()

def set_lamp():
    """
    Set the position of the default lamp.
    """
    bpy.data.objects["Lamp"].data.type = 'HEMI'
    bpy.data.objects["Lamp"].location = (20,20,20)

def set_camera(location=(34,42,24), rotation=(1.08, 0.013, 2.43)):
    """
    Set the location of the default camera.

    :param location: The camera's location.
    :param rotation: The camera's rotation.
    """
    bpy.data.objects["Camera"].location = location
    bpy.data.objects["Camera"].rotation_euler = rotation

def set_horizon():
    """
    Set the color of the horizon.
    """
    bpy.context.scene.world.horizon_color = (1,1,1)

def set_scene():
    """
    Prepare the scene for rendering.
    """
    remove_default_cube()
    set_lamp()
    set_camera()
    set_horizon()
    bpy.context.scene.render.resolution_percentage = 60

def save(filename):
    """
    Save the current blender project.

    :param filename: The location where to save the file.
    """
    bpy.ops.wm.save_as_mainfile(filepath=filename)

def render(filename):
    """
    Render the scene to a file.

    :param filename: The location where to store the rendered file.
    """
    bpy.data.scenes['Scene'].render.filepath = filename
    bpy.ops.render.render( write_still=True )

def print_plane(height0=10, height1=10, color=white, dim=0, units=True):
    """
    Print a plane.

    :param color: The color of the plane.
    :param dim: The dimension controls the orientation and location of the plane.
    :param units: If units should be marked on the plane.
    :param height0: The width of the plane along the first direction.
    :param height1: The width of the plane along the second direction.
    """
    dim1 = None
    if dim == 0:
        rotation=(0,0,0)
        dim1 = 1
        rotation1 = (0,1.5708,0)
        dim2 = 0
        rotation2 = (1.5708,0,0)
        resize=(height1, height0, 1)
    if dim == 1:
        rotation=(0,1.5708,0)
        dim1 = 2
        rotation1 = (1.5708,0,0)
        dim2 = 1
        rotation2 = (0,0,0)
        resize=(1, height1, height0)
    if dim == 2:
        rotation=(1.5708,0,0)
        dim1 = 0
        rotation1 = (0,0,0)
        dim2 = 2
        rotation2 = (0,1.5708,0)
        resize=(height0, 1, height1)

    bpy.ops.mesh.primitive_plane_add(location=(0,0,0), rotation=rotation)
    bpy.ops.transform.resize(value=resize)
    ob = bpy.context.active_object
    ob.data.materials.append(color)

    if not units:
        return

    for i in range(-height0,height0, 1):
        if i == 0:
            continue

        location=[0,0,0]
        location[dim1] = i

        if i % 5 == 0:
            radius = 0.01 * 2
        else:
            radius = 0.01

        bpy.ops.mesh.primitive_cylinder_add(vertices=128,
            radius=radius, depth=2*height1, rotation=rotation1,
            location=location)
        ob = bpy.context.active_object
        ob.data.materials.append(black)

    for i in range(-height1,height1, 1):
        if i == 0:
            continue

        location=[0,0,0]
        location[dim2] = i

        if i % 5 == 0:
            radius = 0.01 * 2
        else:
            radius = 0.01

        bpy.ops.mesh.primitive_cylinder_add(vertices=128,
            radius=radius, depth=2*height0, rotation=rotation2,
            location=location)
        ob = bpy.context.active_object
        ob.data.materials.append(black)

def print_axis(height, color, dim, unit_markers=True, text=False):
    """
    Print the axis of a coordinate system.

    :param height: The length of the axis.
    :param color: The color of the axis.
    :param dim: The dimension for which the axis is printed.
    :param unit_marks: If unit markers should be plotted.
    :param text: If the name of the axis should be printed.
    """
    if dim == 2:
        rotation = (0,0,0)
    if dim == 1:
        rotation = (-1.5708,0,0)
    if dim == 0:
        rotation = (0, 1.5708, 0)
            
    bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=0.1,
                                        depth=2 * (height+1), rotation=rotation,
                                        location=(0,0,0))
    ob = bpy.context.active_object
    ob.data.materials.append(color)
    location = [0,0,0]
    location[dim] = height+1
    bpy.ops.mesh.primitive_cone_add(vertices=128, radius1=0.2, radius2=0, depth=1,
        rotation=rotation, location=location)
    ob = bpy.context.active_object
    ob.data.materials.append(color)
    top = ob

    if text:
        location=[0,0,0]
        if dim == 0:
            rotation = (1.5708,0, 2 * 1.5708)
            location[2] = 0.2
            location[1] = 0.2
            location[0] = height - 0.1
        if dim == 1:
            location[1] = height - 0.8
            location[2] = 0.2
            location[0] = 0.2
            rotation = (1.5708,0,1.5708)
        if dim == 2:
            rotation = (1.5708,0, 2 * 1.5708)
            location[2] = height - 0.9
            location[1] = 0.2
            location[0] = 1
        bpy.ops.object.text_add(enter_editmode=True, location = location,
                    rotation=rotation)
        bpy.ops.font.delete()
        bpy.ops.font.text_insert(text="i%d" % dim)
        ob = bpy.context.active_object
        ob.data.materials.append(color)

    if unit_markers:
        for i in range(-height,height, 1):
            location = [0, 0, 0]
            location[dim] = i
            if i % 5 == 0:
                depth = 2 * 0.05
            else:
                depth = 0.05
            bpy.ops.mesh.primitive_cylinder_add(vertices=128,
                radius=0.105, depth=depth, rotation=rotation,
                location=location)
            ob = bpy.context.active_object
            ob.data.materials.append(white)
    return top

def add_coordinate_system(size=[10,10,10], print_planes=True, unit_markers=True):
    """
    Plot a coordinate system.

    :param size: The size of the coordinate system along the different
                 dimensions.
    :param print_plans: Either a single boolean value that enables or disables
                        the printing of all planes or a vector of booleans that
                        enables each plane individually.
    :param unit_markers: If unit markers should be printed on the plans and
                         axis.
    """
    axis = []
    a = print_axis(size[2], black, dim=0, unit_markers=unit_markers)
    axis.append(a)
    a = print_axis(size[1], black, dim=1, unit_markers=unit_markers)
    axis.append(a)
    a = print_axis(size[0], black, dim=2, unit_markers=unit_markers)
    axis.append(a)

    if print_planes != False:
        if (print_planes == True or print_planes[0] == True):
            print_plane(size[1], size[2], dim=0)
        if (print_planes == True or print_planes[1] == True):
            print_plane(size[0], size[1], dim=1)
        if (print_planes == True or print_planes[2] == True):
            print_plane(size[2], size[0], dim=2)

    return axis
