import bpy
blender249 = True
blender280 = (2,80,0) <= bpy.app.version
import sys

try:
	import Blender
except:
	blender249 = False

if not blender280:
	if blender249:
		try:
			import export_fbx
		except:
			print('error: export_fbx not found.')
			Blender.Quit()
	else :
		try:
			import io_scene_fbx.export_fbx
		except:
			print('error: io_scene_fbx.export_fbx not found.')
			# This might need to be bpy.Quit()
			raise

# Accept command line arguments and load the contents of the .blend file
infile = sys.argv[5]
bpy.ops.wm.open_mainfile(filepath=infile)
outfile = sys.argv[6]


# Do the conversion
print("Starting blender to FBX conversion " + outfile)

if blender280:
	import bpy.ops
	bpy.ops.export_scene.fbx(filepath=outfile,
		check_existing=False,
		use_selection=False,
		use_active_collection=False,
		object_types= {'ARMATURE','CAMERA','LIGHT','MESH','OTHER','EMPTY'},
		use_mesh_modifiers=True,
		mesh_smooth_type='OFF',
		use_custom_props=True,
		bake_anim_use_nla_strips=False,
		bake_anim_use_all_actions=False,
		apply_scale_options='FBX_SCALE_ALL')
elif blender249:
	mtx4_x90n = Blender.Mathutils.RotationMatrix(-90, 4, 'x')
	export_fbx.write(outfile,
		EXP_OBS_SELECTED=False,
		EXP_MESH=True,
		EXP_MESH_APPLY_MOD=True,
		EXP_MESH_HQ_NORMALS=True,
		EXP_ARMATURE=True,
		EXP_LAMP=True,
		EXP_CAMERA=True,
		EXP_EMPTY=True,
		EXP_IMAGE_COPY=False,
		ANIM_ENABLE=True,
		ANIM_OPTIMIZE=False,
		ANIM_ACTION_ALL=True,
		GLOBAL_MATRIX=mtx4_x90n)
else:
	# blender 2.58 or newer
	import math
	from mathutils import Matrix
	# -90 degrees
	mtx4_x90n = Matrix.Rotation(-math.pi / 2.0, 4, 'X')
	
	class FakeOp:
		def report(self, tp, msg):
			print("%s: %s" % (tp, msg))
	
	exportObjects = ['ARMATURE', 'EMPTY', 'MESH']

	minorVersion = bpy.app.version[1];
	if minorVersion <= 58:
		# 2.58
		io_scene_fbx.export_fbx.save(FakeOp(), bpy.context, filepath=outfile,
			global_matrix=mtx4_x90n,
			use_selection=False,
			object_types=exportObjects,
			mesh_apply_modifiers=True,
			ANIM_ENABLE=True,
			ANIM_OPTIMIZE=False,
			ANIM_OPTIMIZE_PRECISSION=6,
			ANIM_ACTION_ALL=True,
			batch_mode='OFF',	
			BATCH_OWN_DIR=False)
	else:
		# 2.59 and later
		kwargs = dict(
			global_matrix=Matrix.Rotation(-math.pi / 2.0, 4, 'X'),
			use_selection=False,
			#object_types={'ARMATURE', 'EMPTY', 'MESH'},
			object_types={'EMPTY', 'CAMERA', 'LAMP', 'ARMATURE', 'MESH'},
			#mesh_smooth_type='FACE',
			mesh_smooth_type='OFF',
			use_mesh_modifiers=True,
			use_armature_deform_only=False,
			use_anim=True,
			use_anim_optimize=False,
			use_anim_action_all=True,
			use_mesh_edges=False,
			batch_mode='OFF',
			use_default_take=True,
			)
		io_scene_fbx.export_fbx.save(FakeOp(), bpy.context, filepath=outfile, **kwargs)
	# HQ normals are not supported in the current exporter

print("Finished blender to FBX conversion " + outfile)
