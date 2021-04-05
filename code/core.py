import logging
import os
import sys

import bpy


def idle_from_default_animation(import_scale: str, fbx_file_path: str, export_directory_path: str,
                                export_suffix: str, start_frame: str, end_frame: str, last_key_frames_ahead: str,
                                better_fbx_install_path: str):

    start_frame = int(start_frame)
    end_frame = int(end_frame)
    import_scale = int(import_scale)
    last_key_frames_ahead = int(last_key_frames_ahead)

    imported_fbx_file_name = os.path.basename(fbx_file_path)
    imported_fbx_file_name = imported_fbx_file_name.strip(".fbx")

    bpy.ops.object.mode_set(mode='OBJECT')
    try:
        bpy.ops.better_import.fbx(filepath=imported_fbx_file_name, my_scale=import_scale,
                                  use_auto_bone_orientation=False,
                                  use_optimize_for_blender=True)
    except AttributeError:
        bpy.ops.preferences.addon_install(filepath=better_fbx_install_path)
        bpy.ops.preferences.addon_enable(module="better_import_fbx")
        bpy.ops.better_import.fbx(filepath=fbx_file_path, my_scale=import_scale,
                                  use_auto_bone_orientation=False,
                                  use_optimize_for_blender=True)

    bpy.ops.object.mode_set(mode='OBJECT')
    imported_objects = [o for o in bpy.context.selected_objects if o.type == 'ARMATURE']

    if len(imported_objects) > 1:
        logging.error("imported more than one armature!")
        exit(1)

    armature = imported_objects[0]
    fcurves = armature.animation_data.action.fcurves

    for fc in fcurves:
        for i in reversed(range(0, len(fc.keyframe_points))):
            kfp = fc.keyframe_points[i]
            frame_number = int(kfp.co[0])
            if frame_number < start_frame or frame_number > end_frame:
                fc.keyframe_points.remove(kfp, fast=True)

    for fc in fcurves:
        fc.keyframe_points.insert(end_frame + last_key_frames_ahead, fc.keyframe_points[0].co.y)

    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame + last_key_frames_ahead

    # frame_range = armature.animation_data.action.frame_range
    # last_frame = frame_range[1] * 5
    # bpy.context.scene.frame_end = last_frame

    export_name = imported_fbx_file_name + export_suffix
    # bpy.context.scene.render.fps = 60
    # bpy.context.scene.render.frame_map_new = 500
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.data.objects["Armature"].select_set(True)

    full_export_path = os.path.join(export_directory_path, export_name + ".fbx")
    bpy.ops.export_scene.fbx(filepath=full_export_path, use_selection=True, apply_scale_options="FBX_SCALE_UNITS",
                             object_types={'ARMATURE', 'MESH'}, apply_unit_scale=True, use_mesh_modifiers=True,
                             add_leaf_bones=False, use_armature_deform_only=False,
                             bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False,
                             bake_anim_use_all_actions=False, bake_anim_force_startend_keying=True)


if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"

    if len(argv) != 8:
        logging.critical("wrong parameters count")
        bpy.ops.wm.quit_blender()
        exit(1)

    idle_from_default_animation(*argv)
