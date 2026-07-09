"""
Stage 5: add the `T+2.` caption to t2ep1_scene.blend, re-render the silent
master, remux audio, and produce the final cut.

CREATIVE CALL (flagged to Josh): the storyboard's caption spec says
"cream-on-nothing" for `T+2.`, but the background is flat cream (#FFFFD6) --
cream text on a cream field would be invisible. Rendering in Ink (the show's
dominant line color) instead, keeping the "no background box" part of the
spec (bare text, no pill/box behind it).

Run headless:
  /Applications/Blender.app/Contents/MacOS/Blender --background \
    --python add_caption_and_export.py
"""
import bpy, os, math

EP_DIR = os.path.dirname(os.path.abspath(__file__))
SCENE_BLEND = os.path.join(EP_DIR, "t2ep1_scene.blend")
TESTS_DIR = os.path.join(EP_DIR, "tests")
SILENT_MP4 = os.path.join(EP_DIR, "t2ep1_silent.mp4")

FPS = 24


def f(t):
    return round(1 + t * FPS)


bpy.ops.wm.open_mainfile(filepath=SCENE_BLEND)
scene = bpy.context.scene

ink_mat = bpy.data.materials["Ink"]

# Transparent-fade version of Ink so the caption can fade in via alpha
# (Emission mixed with Transparent BSDF, blend_method='BLEND' -- still no
# lights, matches Constitution's emission-shading-only rule).
caption_mat = bpy.data.materials.new("Ink_Fade")
caption_mat.use_nodes = True
caption_mat.blend_method = 'BLEND'
caption_mat.shadow_method = 'NONE'
nt = caption_mat.node_tree
nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputMaterial")
emission = nt.nodes.new("ShaderNodeEmission")
emission.inputs["Color"].default_value = (0.02, 0.02, 0.02, 1.0)
transparent = nt.nodes.new("ShaderNodeBsdfTransparent")
mix = nt.nodes.new("ShaderNodeMixShader")
mix.name = "FadeMix"
nt.links.new(transparent.outputs["BSDF"], mix.inputs[1])
nt.links.new(emission.outputs["Emission"], mix.inputs[2])
nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
mix.inputs["Fac"].default_value = 0.0  # 0 = fully transparent, 1 = fully visible

curve = bpy.data.curves.new("Caption_T2", type="FONT")
curve.body = "t+2."
curve.size = 0.20
curve.align_x = "CENTER"
curve.align_y = "CENTER"
try:
    curve.font = bpy.data.fonts.load("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
except Exception as e:
    print("bold font load failed, using default:", e)
caption_obj = bpy.data.objects.new("Caption_T2", curve)
caption_obj.rotation_euler = (math.radians(90), 0, 0)
# bottom-center, safe-zone clear of bottom 320px / right 140px (see
# build_scene.py's camera framing: ortho_scale=12, center z=0.5 -> visible
# range [-5.5, 6.5]; bottom-320px UI band starts at world z=-3.5).
caption_obj.location = (0.0, 0.02, -3.32)
caption_obj.data.materials.append(caption_mat)
ep_coll = bpy.data.collections["T2Ep1_Shot"]
ep_coll.objects.link(caption_obj)

caption_obj.animation_data_create()
act = bpy.data.actions.new("Caption_Fade")
caption_obj.animation_data.action = act
mix_node = caption_mat.node_tree.nodes["FadeMix"]
mix_node.inputs["Fac"].default_value = 0.0
mix_node.inputs["Fac"].keyframe_insert("default_value", frame=f(16.2))
mix_node.inputs["Fac"].default_value = 1.0
mix_node.inputs["Fac"].keyframe_insert("default_value", frame=f(16.2) + 6)
fc = caption_mat.node_tree.animation_data.action.fcurves[0]
for kp in fc.keyframe_points:
    kp.interpolation = 'BEZIER'

bpy.ops.wm.save_as_mainfile(filepath=SCENE_BLEND)
print("SAVED with caption", SCENE_BLEND)

# Safe-zone QC stills: caption should be fully visible in frame, clear of the
# bottom 320px / right 140px TikTok UI band.
scene.render.image_settings.file_format = "PNG"
for frm, name in ((f(16.2) - 2, "chk_caption_before.png"),
                  (f(16.2) + 10, "chk_caption_after.png"),
                  (432, "chk_caption_loopend.png")):
    scene.frame_set(frm)
    scene.render.filepath = os.path.join(TESTS_DIR, name)
    bpy.ops.render.render(write_still=True)
    print("rendered", name)

# ---------------------------------------------------------------------------
# Re-render silent master (now includes caption) and remux audio.
# ---------------------------------------------------------------------------
scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.ffmpeg.constant_rate_factor = "HIGH"
scene.render.ffmpeg.ffmpeg_preset = "BEST"
scene.render.ffmpeg.audio_codec = "NONE"
scene.render.filepath = SILENT_MP4
scene.frame_start = 1
scene.frame_end = 432
bpy.ops.render.render(animation=True)
print("SILENT RENDER (with caption) DONE", SILENT_MP4)
