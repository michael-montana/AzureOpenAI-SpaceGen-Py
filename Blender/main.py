import bpy
import random
import math

# Clear the scene (remove all objects)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Set the renderer to Cycles
bpy.context.scene.render.engine = 'CYCLES'

# Set the render resolution (1920x1080)
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100

# Set the render samples (for quality settings)
bpy.context.scene.cycles.samples = 128

# Enable adaptive sampling (for better performance)
bpy.context.scene.cycles.use_adaptive_sampling = True

# Enable denoising in the viewport and final render
bpy.context.scene.cycles.use_denoising = True
bpy.context.scene.cycles.use_preview_denoising = True





# Add camera
cam_data = bpy.data.cameras.new(name="Camera")
cam_object = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam_object)

# Position the camera
cam_object.location = (10, -35, 20)
cam_object.rotation_euler = (1.0, 0.5, 0)  # Slightly tilted downward

# Set the camera as the active camera
bpy.context.scene.camera = cam_object






# Optional: Add a second light source (e.g., point light)
light_data2 = bpy.data.lights.new(name="PointLight", type='POINT')
light_object2 = bpy.data.objects.new("PointLight", light_data2)
bpy.context.collection.objects.link(light_object2)

# Position the point light
light_object2.location = (-5, 5, 3)
light_data2.energy = 50  # Light intensity (can be adjusted)

# Optimize shadows and light bounces (specific to Cycles)
bpy.context.scene.cycles.max_bounces = 12  # Maximum number of bounces for light rays
bpy.context.scene.cycles.diffuse_bounces = 4  # Bounces for diffuse light
bpy.context.scene.cycles.glossy_bounces = 4  # Bounces for reflective light
bpy.context.scene.cycles.transmission_bounces = 12  # Bounces for transmission (for glass materials)
bpy.context.scene.cycles.volume_bounces = 2  # Bounces for volumetric materials

# Light path optimizations for a better balance between quality and performance
bpy.context.scene.cycles.sample_clamp_direct = 10  # Limit direct light samples
bpy.context.scene.cycles.sample_clamp_indirect = 5  # Limit indirect light samples

# Enable transparent shadows (important if the megastructure casts shadows)
bpy.context.scene.cycles.shadow_threshold = 0.05

# Optimize memory usage during render time (useful for complex scenes)
bpy.context.scene.cycles.use_progressive_refine = True  # Progressive refinement during render time

# Camera depth of field (optional for realistic camera effects)
cam_data.dof.use_dof = True
cam_data.dof.focus_distance = 10  # Distance to the focus point
cam_data.dof.aperture_fstop = 2.8  # Aperture size controlling the depth of field effect







# Final camera setup (for fine-tuning the view direction)
camera = bpy.context.scene.camera
camera.select_set(True)

# Focus point for the camera (depending on the position of the star and the megastructure)
# We align the camera to the center of the scene
bpy.ops.object.select_all(action='DESELECT')
camera.select_set(True)
bpy.context.view_layer.objects.active = camera
bpy.ops.view3d.camera_to_view_selected()

# Set the focal length of the camera
camera.data.lens = 50  # Focal length in mm, adjustable for wider or narrower shots

# World calculations (specific to Cycles)
# Important for calculating global illumination and realism in the scene
bpy.context.scene.cycles.use_adaptive_subdivision = True  # Adaptive subdivision for better details in textures and meshes

# Set the maximum number of light structures
bpy.context.scene.cycles.light_sampling_threshold = 0.01

# Maximum render memory (dependent on the system, e.g., for GPU rendering)
bpy.context.scene.cycles.debug_use_spatial_splits = True  # Uses spatial splitting for better memory management
bpy.context.scene.cycles.debug_bvh_type = 'STATIC_BVH'  # Static BVH for non-animated scenes (faster)

# Set the rendering device (prefer GPU if available)
bpy.context.scene.cycles.device = 'GPU'  # Sets the renderer to GPU mode if a supported GPU is available

# Further optimize adaptive sampling (to improve performance)
bpy.context.scene.cycles.sample_clamp_direct = 4.0  # Clamping of direct light samples
bpy.context.scene.cycles.sample_clamp_indirect = 2.0  # Clamping of indirect light samples













# Create the star (Tabby's Star)
bpy.ops.mesh.primitive_uv_sphere_add(radius=2, location=(0, 0, 0))
star = bpy.context.active_object
star.name = "Tabbys_Star"

# Add Subdivision Surface Modifier to the star (to increase resolution)
subsurf = star.modifiers.new(name="Subdivision Surface", type='SUBSURF')
subsurf.levels = 4  # Render level for subdivision

# Create material for the star
star_material = bpy.data.materials.new(name="Star_Material")
star_material.use_nodes = True
star.data.materials.append(star_material)

# Add nodes for the shader
nodes = star_material.node_tree.nodes
links = star_material.node_tree.links

# Remove all default nodes
for node in nodes:
    nodes.remove(node)

# Output node for the material
output_node = nodes.new(type='ShaderNodeOutputMaterial')

# Emission shader for glowing surface
emission_node = nodes.new(type='ShaderNodeEmission')
emission_node.inputs['Strength'].default_value = 10  # Emission strength for the glow

# Procedural noise texture for turbulent plasma surface
noise_texture = nodes.new(type='ShaderNodeTexNoise')
noise_texture.inputs['Scale'].default_value = 15.0  # Scale of the noise turbulence
noise_texture.inputs['Detail'].default_value = 5.0  # Detail level for finer structures
noise_texture.inputs['Distortion'].default_value = 1.0  # Distortion for chaotic effects

# Color ramp to control plasma colors
color_ramp = nodes.new(type='ShaderNodeValToRGB')
color_ramp.color_ramp.elements[0].position = 0.3
color_ramp.color_ramp.elements[1].position = 0.8

# Plasma colors (from orange to light yellow)
color_ramp.color_ramp.elements[0].color = (1.0, 0.3, 0.1, 1)  # Deep orange
color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 0.6, 1)  # Light yellow

# Bump mapping for texture
bump_node = nodes.new(type='ShaderNodeBump')
bump_node.inputs['Strength'].default_value = 0.1  # Strength of the bump map

# Principled BSDF for the physical surface of the star
bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf_node.inputs['Metallic'].default_value = 0  # Non-metallic
bsdf_node.inputs['Roughness'].default_value = 0.6  # Slightly rough surface
bsdf_node.inputs['Base Color'].default_value = (1.0, 0.5, 0.0, 1)  # Surface color tone

# Displacement shader for irregular shape
displacement_node = nodes.new(type='ShaderNodeDisplacement')
displacement_node.inputs['Scale'].default_value = 0.3  # Strength of the deformation
displacement_node.inputs['Midlevel'].default_value = 0.0  # Reference value for mid-level height

# Connect the nodes for the material
links.new(noise_texture.outputs['Fac'], color_ramp.inputs['Fac'])  # Connect noise texture to color ramp
links.new(color_ramp.outputs['Color'], emission_node.inputs['Color'])  # Connect color ramp to emission
links.new(noise_texture.outputs['Fac'], bump_node.inputs['Height'])  # Use noise texture as bump map
links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])  # Apply bump map to BSDF

# Combine emission and BSDF
mix_shader = nodes.new(type='ShaderNodeMixShader')
links.new(emission_node.outputs['Emission'], mix_shader.inputs[1])  # Emission to mix shader
links.new(bsdf_node.outputs['BSDF'], mix_shader.inputs[2])  # BSDF to mix shader
links.new(mix_shader.outputs['Shader'], output_node.inputs['Surface'])  # Mix shader to output

# Optional: Add glow around the star using a mix shader
glow_mix_shader = nodes.new(type='ShaderNodeMixShader')
glow_node = nodes.new(type='ShaderNodeEmission')
glow_node.inputs['Strength'].default_value = 0.8  # Adjust glow strength for extra rays
glow_node.inputs['Color'].default_value = (1.0, 0.9, 0.7, 1)  # Glow in light yellow

# Connect for glow effect
links.new(glow_node.outputs['Emission'], glow_mix_shader.inputs[2])
links.new(mix_shader.outputs['Shader'], glow_mix_shader.inputs[1])
links.new(glow_mix_shader.outputs['Shader'], output_node.inputs['Surface'])

# Use displacement map for shape alteration
links.new(noise_texture.outputs['Fac'], displacement_node.inputs['Height'])  # Use noise for displacement
links.new(displacement_node.outputs['Displacement'], output_node.inputs['Displacement'])  # Displacement to material output


















# Function to create flat, hollow metal rings around the star
def create_hollow_ring_megastructure(num_rings=3, radius_start=3, radius_increment=1.0, thickness=0.1, frames=250):
    for ring in range(num_rings):
        outer_radius = radius_start + ring * radius_increment  # Outer radius of the ring
        inner_radius = outer_radius - thickness  # Inner radius of the ring (defines the ring thickness)

        # Create the outer cylinder (outer part of the ring)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=outer_radius,
            depth=0.8,  # Shallow depth for the ring
            location=(0, 0, 0)
        )
        outer_ring = bpy.context.active_object
        outer_ring.name = f"Hollow_Outer_Ring_{ring}"

        # Create the inner cylinder (to be subtracted)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=inner_radius,
            depth=0.81,  # Slightly larger than the outer cylinder to ensure subtraction
            location=(0, 0, 0)
        )
        inner_ring = bpy.context.active_object
        inner_ring.name = f"Hollow_Inner_Ring_{ring}"

        # Use Boolean Modifier to subtract the inner cylinder from the outer
        boolean_modifier = outer_ring.modifiers.new(type='BOOLEAN', name="HollowModifier")
        boolean_modifier.object = inner_ring
        boolean_modifier.operation = 'DIFFERENCE'

        # Apply the Boolean Modifier
        bpy.context.view_layer.objects.active = outer_ring
        bpy.ops.object.modifier_apply(modifier="HollowModifier")

        # Delete the inner cylinder as it is no longer needed
        bpy.data.objects.remove(inner_ring, do_unlink=True)

        # Random rotation of the ring around the star
        outer_ring.rotation_euler = (
            random.uniform(0, math.pi * 2),  # Random rotation around the X-axis
            random.uniform(0, math.pi * 2),  # Random rotation around the Y-axis
            random.uniform(0, math.pi * 2)   # Random rotation around the Z-axis
        )

        # Create material for the ring
        material = bpy.data.materials.new(name=f"Ring_Material_{ring}")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Remove all default nodes
        for node in nodes:
            nodes.remove(node)

        # Set up metallic shader nodes
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')

        # Color scheme for scrap or worn metal (dark and industrial)
        principled_node.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)  # Dark gray for worn metal
        principled_node.inputs['Metallic'].default_value = 1.0  # Fully metallic
        principled_node.inputs['Roughness'].default_value = 0.8  # High roughness for matte, damaged surface

        # Noise Texture for irregular patterns (updated with Musgrave-like features)
        noise_texture = nodes.new(type='ShaderNodeTexNoise')
        noise_texture.inputs['Scale'].default_value = 25.0  # Density of noise details
        noise_texture.inputs['Detail'].default_value = 15.0  # High level of detail
        noise_texture.inputs['Roughness'].default_value = 0.5  # Roughness (replaces Dimension)

        # Voronoi Texture for technological patterns
        voronoi_texture = nodes.new(type='ShaderNodeTexVoronoi')
        voronoi_texture.inputs['Scale'].default_value = 10.0  # Structure for worn surfaces

        # Bump Node for the surface
        bump_node = nodes.new(type='ShaderNodeBump')
        bump_node.inputs['Strength'].default_value = 0.3  # Slight elevation for worn metal

        # Mix the textures for complex patterns
        mix_shader = nodes.new(type='ShaderNodeMixRGB')
        mix_shader.blend_type = 'MULTIPLY'  # Combine textures by multiplication

        # Connect the textures and bump map to the Principled BSDF
        links.new(noise_texture.outputs['Fac'], mix_shader.inputs[1])
        links.new(voronoi_texture.outputs['Distance'], mix_shader.inputs[2])
        links.new(mix_shader.outputs['Color'], principled_node.inputs['Base Color'])
        links.new(noise_texture.outputs['Fac'], bump_node.inputs['Height'])  # Use noise as bump map
        links.new(bump_node.outputs['Normal'], principled_node.inputs['Normal'])  # Apply bump map to Principled BSDF

        # Link the Principled Shader to the output
        links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

        # Apply the material to the ring
        outer_ring.data.materials.append(material)

        # Animation setup for rotation around the axes
        # Choose a random axis for rotation (X, Y, or Z)
        axis = random.choice([0, 1, 2])  # 0 = X, 1 = Y, 2 = Z
        
        # Set the keyframes for rotation
        bpy.context.scene.frame_set(0)  # Set to frame 0
        outer_ring.rotation_euler[axis] = 0.0
        outer_ring.keyframe_insert(data_path="rotation_euler", index=axis)

        bpy.context.scene.frame_set(frames)  # Set to the last frame (default: 250)
        outer_ring.rotation_euler[axis] = math.pi * 2  # One full rotation (360 degrees)
        outer_ring.keyframe_insert(data_path="rotation_euler", index=axis)


# Create flat, hollow rings around the star
create_hollow_ring_megastructure(num_rings=8, radius_start=3.5, radius_increment=0.6, thickness=0.1, frames=250)










# Optional additional light source (e.g., for highlights on the rings)
def add_additional_light(location=(10, -10, 10), energy=1000):
    light_data = bpy.data.lights.new(name="Additional_Light", type='AREA')
    light_object = bpy.data.objects.new(name="Additional_Light", object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    
    # Positioning and settings of the light source
    light_object.location = location
    light_data.energy = energy
    light_data.size = 5.0  # Size of the light object (larger size results in softer light)
    light_data.specular_factor = 1.0  # Maximize reflective light

# Add additional light source
add_additional_light(location=(5, 10, -10), energy=1200)

# HDRI world lighting (optional)
bpy.context.scene.world.use_nodes = True
world = bpy.context.scene.world
nodes = world.node_tree.nodes

# Remove all default nodes
for node in nodes:
    nodes.remove(node)

# Set background color to black (for space effect)
bg_node = nodes.new(type='ShaderNodeBackground')
bg_node.inputs['Color'].default_value = (0, 0, 0, 1)  # RGBA for black

# Adjust background strength (how bright the background should appear)
bg_node.inputs['Strength'].default_value = 0.1  # Low brightness for a dark space

# Create output node
output_node = nodes.new(type='ShaderNodeOutputWorld')

# Connect the nodes
links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])

# Adjust the light strength of the world lighting
bg_node.inputs['Strength'].default_value = 0.5  # Slight ambient light, can be adjusted as needed











# File path to the image (update the path with the location of the image on your computer)
image_path = "D:/github/space3.png"  # <-- Update this with the correct path to your image

# Enable background shader in the world
bpy.context.scene.world.use_nodes = True
world = bpy.context.scene.world
nodes = world.node_tree.nodes
links = world.node_tree.links

# Remove all existing nodes in the world shader
for node in nodes:
    nodes.remove(node)

# Add a new Environment Texture Node
env_texture_node = nodes.new(type='ShaderNodeTexEnvironment')
env_texture_node.image = bpy.data.images.load(image_path)  # Load the image as an environment texture

# Create a background node
bg_node = nodes.new(type='ShaderNodeBackground')

# Add a Mapping Node (for scaling the image)
mapping_node = nodes.new(type='ShaderNodeMapping')
mapping_node.inputs['Scale'].default_value = (1.0, 1.0, 1.0)  # Scale the background image (X, Y, Z)

# Add a Texture Coordinate Node (for correct placement of the texture)
tex_coord_node = nodes.new(type='ShaderNodeTexCoord')

# Add a World Output Node
output_node = nodes.new(type='ShaderNodeOutputWorld')

# Link the nodes (Texture Coordinates -> Mapping -> Environment Texture -> Background -> World Output)
links.new(tex_coord_node.outputs['Generated'], mapping_node.inputs['Vector'])
links.new(mapping_node.outputs['Vector'], env_texture_node.inputs['Vector'])
links.new(env_texture_node.outputs['Color'], bg_node.inputs['Color'])
links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])

# Adjust the strength of the background (optional)
bg_node.inputs['Strength'].default_value = 0.5  # Adjust the strength as needed























# Adjust render settings for high quality
bpy.context.scene.cycles.samples = 500  # Number of samples for the final render (higher values yield better quality)
bpy.context.scene.cycles.use_adaptive_sampling = True  # Adaptive sampling for better performance
bpy.context.scene.cycles.max_bounces = 12  # Maximum number of bounces for realistic light calculation
bpy.context.scene.cycles.diffuse_bounces = 4  # Bounces for diffuse light
bpy.context.scene.cycles.glossy_bounces = 4  # Bounces for reflective light
bpy.context.scene.cycles.transmission_bounces = 12  # Bounces for light transmission (e.g., glass materials)

# Enable denoising (optional for cleaner results)
bpy.context.scene.cycles.use_denoising = True

# Adjust render resolution (e.g., 4K for high-resolution output)
bpy.context.scene.render.resolution_x = 3840
bpy.context.scene.render.resolution_y = 2160
bpy.context.scene.render.resolution_percentage = 100  # 100% of the specified resolution

# Optimize tile size (depending on your GPU/CPU)
# bpy.context.scene.render.tile_x = 256
# bpy.context.scene.render.tile_y = 256