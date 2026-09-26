"""
Stage 4 (part 4): mux VO + SFX onto the silent render via Blender's VSE
(bundled FFmpeg, no system ffmpeg needed) and render the final master.

NOTE: office-hum bed and the optional terminal beep from the storyboard's
audio mix map are NOT included -- no such assets exist yet and generating
new SFX costs ElevenLabs credits, which needs Josh's go-ahead first (see
CLAUDE.md "Ask before: spending API credits"). VO (both lines) + coffee sip
are the load-bearing beats and are included in full.

Run headless:
  /Applications/Blender.app/Contents/MacOS/Blender --background \
    --python mux_audio.py
"""
import bpy, os, math

EP_DIR = os.path.dirname(os.path.abspath(__file__))
SILENT_MP4 = os.path.join(EP_DIR, "t2ep1_silent.mp4")
VO_DIR = os.path.join(EP_DIR, "vo")
SFX_DIR = os.path.join(EP_DIR, "sfx")
MASTER_MP4 = os.path.join(EP_DIR, "t2ep1_master.mp4")

FPS = 24


def f(t):
    return round(1 + t * FPS)


def db_to_linear(db):
    return 10 ** (db / 20)


bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.fps = FPS
scene.frame_start = 1
scene.frame_end = 432

scene.sequence_editor_create()
seq = scene.sequence_editor

seq.sequences.new_movie(name="Master_Video", filepath=SILENT_MP4, channel=1, frame_start=1)

vo1 = seq.sequences.new_sound(
    name="VO_Line1", filepath=os.path.join(VO_DIR, "line1-your-funds-are-moving.mp3"),
    channel=2, frame_start=f(2.5),
)
vo1.volume = db_to_linear(-3)

vo2 = seq.sequences.new_sound(
    name="VO_Line2", filepath=os.path.join(VO_DIR, "line2-always-been-moving.mp3"),
    channel=2, frame_start=f(9.6),
)
vo2.volume = db_to_linear(-3)

sip = seq.sequences.new_sound(
    name="SFX_CoffeeSip", filepath=os.path.join(SFX_DIR, "coffee-sip.mp3"),
    channel=3, frame_start=f(8.0),
)
sip.volume = db_to_linear(-12)

scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.ffmpeg.constant_rate_factor = "HIGH"
scene.render.ffmpeg.ffmpeg_preset = "BEST"
scene.render.ffmpeg.audio_codec = "AAC"
scene.render.ffmpeg.audio_bitrate = 192
scene.render.filepath = MASTER_MP4

bpy.ops.render.render(animation=True)
print("MASTER RENDER DONE", MASTER_MP4)
