"""
Stage 4 (part 3): full-resolution silent render of the animated shot.

Run headless:
  /Applications/Blender.app/Contents/MacOS/Blender --background \
    --python render_silent.py
"""
import bpy, os

EP_DIR = os.path.dirname(os.path.abspath(__file__))
SCENE_BLEND = os.path.join(EP_DIR, "t2ep1_scene.blend")
SILENT_MP4 = os.path.join(EP_DIR, "t2ep1_silent.mp4")

bpy.ops.wm.open_mainfile(filepath=SCENE_BLEND)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 432

scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.ffmpeg.constant_rate_factor = "HIGH"
scene.render.ffmpeg.ffmpeg_preset = "BEST"
scene.render.ffmpeg.audio_codec = "NONE"
scene.render.filepath = SILENT_MP4

bpy.ops.render.render(animation=True)
print("SILENT RENDER DONE", SILENT_MP4)
