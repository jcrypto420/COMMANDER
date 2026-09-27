"""
Stage 4 v2: animation-craft pass, responding to Josh's Gate 2 kill on v1.

What changed vs animate_scene.py (kept for history):
  - Ambient idle bounce REMOVED entirely. Holds are now bit-for-bit frozen --
    the joke is stillness, so stillness has to be real, not a 1%-amplitude
    sine wave running the whole clip ("characters just bouncing up and down").
  - Every real gesture (blink, cup raise/lower, smirk-widen) now has
    anticipation + overshoot + settle instead of a flat ease-in/ease-out ramp.
    That hold-vs-move contrast is the actual craft that was missing.
  - Camera, monitor, audio, caption are UNCHANGED this pass (Jost asked to
    see animation craft alone first).

Run headless:
  /Applications/Blender.app/Contents/MacOS/Blender --background \
    --python animate_scene_v2.py
"""
import bpy, os, math

EP_DIR = os.path.dirname(os.path.abspath(__file__))
SCENE_BLEND = os.path.join(EP_DIR, "t2ep1_scene.blend")
TESTS_DIR = os.path.join(EP_DIR, "tests")

FPS = 24


def f(t):
    return round(1 + t * FPS)


bpy.ops.wm.open_mainfile(filepath=SCENE_BLEND)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 432

arm_a = bpy.data.objects["Puppet_Rig_A"]
arm_b = bpy.data.objects["Puppet_Rig_B"]


def key_curve(action, data_path, index, frame_values, easing='EASE_IN_OUT'):
    fc = action.fcurves.find(data_path, index=index)
    if fc is None:
        fc = action.fcurves.new(data_path, index=index)
    fc.keyframe_points.clear()
    for frm, val in frame_values:
        fc.keyframe_points.insert(frm, val, options={'FAST'})
    for kp in fc.keyframe_points:
        kp.interpolation = 'BEZIER'
        kp.easing = easing
    fc.update()
    return fc


# ---------------------------------------------------------------------------
# No ambient bounce this pass -- holds are frozen. (Both armatures get a
# fresh empty action so nothing lingers from the old idle-loop curves.)
# ---------------------------------------------------------------------------
for arm in (arm_a, arm_b):
    if arm.animation_data is None:
        arm.animation_data_create()
    arm.animation_data.action = bpy.data.actions.new(f"{arm.name}_Action_v2")

# ---------------------------------------------------------------------------
# Banker B: single blink at 5.5s -- fast close, brief hold-closed, overshoot
# on reopen (lid flutters slightly wider than rest), then settle.
# ---------------------------------------------------------------------------
blink_center = f(5.5)  # 133
action_b = arm_b.animation_data.action
blink_pts = [
    (blink_center - 3, 1.0),     # 130 open (rest)
    (blink_center - 1, 0.05),    # 132 closed (fast 2f close)
    (blink_center, 0.05),        # 133 hold-closed 1f
    (blink_center + 3, 1.08),    # 136 open, overshoot past rest
    (blink_center + 5, 1.0),     # 138 settle
]
for bone_name in ("EyelidL", "EyelidR"):
    key_curve(action_b, f'pose.bones["{bone_name}"].scale', 1, blink_pts, easing='EASE_OUT')

# ---------------------------------------------------------------------------
# Banker A: coffee cup -- now driven by TWO bones (upper arm + the new elbow
# joint), a real bicep-curl instead of the whole rigid arm swinging across
# the face like a clock hand (that's what Josh flagged as "retarded" -- the
# rig had no elbow before). Angles verified empirically against the mouth's
# actual position via depsgraph-evaluated mesh centers, then eyeballed in a
# render: arm=-80/forearm=-160 lands the cup right at chin/mouth height with
# a natural-looking bend. Anticipation + overshoot + settle on both bones.
# Sip SFX (muxed separately) still lands at frame 193 / 8.0s.
# ---------------------------------------------------------------------------
arm_a.pose.bones["ArmR"].rotation_mode = 'XYZ'
arm_a.pose.bones["ForearmR"].rotation_mode = 'XYZ'
arm_a.pose.bones["Head"].rotation_mode = 'XYZ'
action_a = arm_a.animation_data.action

ARM_TARGET = -80.0
FOREARM_TARGET = -160.0

arm_pts = [
    (178, 0.0),                                  # rest
    (181, math.radians(6.0)),                    # anticipation: small opposite wind-up
    (191, math.radians(ARM_TARGET - 8.0)),       # raise, overshoot past target
    (193, math.radians(ARM_TARGET)),             # settle into sip pose (SFX lands here)
    (211, math.radians(ARM_TARGET)),             # hold
    (221, math.radians(5.0)),                    # lower, overshoot past rest
    (223, 0.0),                                  # settle to rest
]
key_curve(action_a, 'pose.bones["ArmR"].rotation_euler', 2, arm_pts, easing='EASE_IN_OUT')

forearm_pts = [
    (178, 0.0),
    (181, math.radians(8.0)),
    (191, math.radians(FOREARM_TARGET - 12.0)),
    (193, math.radians(FOREARM_TARGET)),
    (211, math.radians(FOREARM_TARGET)),
    (221, math.radians(8.0)),
    (223, 0.0),
]
key_curve(action_a, 'pose.bones["ForearmR"].rotation_euler', 2, forearm_pts, easing='EASE_IN_OUT')

head_pts = [
    (178, 0.0),
    (181, math.radians(-1.0)),
    (191, math.radians(4.5)),
    (193, math.radians(3.5)),
    (211, math.radians(3.5)),
    (221, math.radians(-0.5)),
    (223, 0.0),
]
key_curve(action_a, 'pose.bones["Head"].rotation_euler', 2, head_pts, easing='EASE_IN_OUT')

# ---------------------------------------------------------------------------
# Screen wipe -- unchanged (already snappy/mechanical, which is correct for
# a terminal refresh, not a place for organic overshoot).
# ---------------------------------------------------------------------------
wipe_start = f(11.5)
wipe_mid = wipe_start + 3
wipe_end = wipe_start + 6
for name in ("Screen_StatusText", "Screen_Cursor"):
    obj = bpy.data.objects[name]
    if obj.animation_data is None:
        obj.animation_data_create()
    if obj.animation_data.action is None:
        obj.animation_data.action = bpy.data.actions.new(f"{name}_Action")
    act = obj.animation_data.action
    fc = act.fcurves.find("scale", index=1)
    if fc is None:
        fc = act.fcurves.new("scale", index=1)
    fc.keyframe_points.clear()
    for frm, val in ((wipe_start, 1.0), (wipe_mid, 0.03), (wipe_end, 1.0)):
        fc.keyframe_points.insert(frm, val, options={'FAST'})
    for kp in fc.keyframe_points:
        kp.interpolation = 'BEZIER'
    fc.update()

# ---------------------------------------------------------------------------
# Smirk-widen -- pop past full widen, settle back, hold, ease back to neutral
# before the loop point (unchanged logic from v1, just adds the overshoot).
# ---------------------------------------------------------------------------
key_id = bpy.data.objects["Face_mouth_A"].data.shape_keys
if key_id is not None:
    if key_id.animation_data is None:
        key_id.animation_data_create()
    key_id.animation_data.action = bpy.data.actions.new("SmirkWidenAction_v2")
    act = key_id.animation_data.action
    fc = act.fcurves.new('key_blocks["Smirk_Widen"].value')
    smirk_start = f(13.5)      # 325
    smirk_overshoot = smirk_start + 20   # 345
    smirk_settle = smirk_overshoot + 6   # 351
    ease_back_start = f(17.0)  # 409
    pts = [
        (1, 0.0),
        (smirk_start, 0.0),
        (smirk_overshoot, 1.15),
        (smirk_settle, 1.0),
        (ease_back_start, 1.0),
        (432, 0.0),
    ]
    for frm, val in pts:
        fc.keyframe_points.insert(frm, val, options={'FAST'})
    for kp in fc.keyframe_points:
        kp.interpolation = 'BEZIER'
    fc.update()

# ---------------------------------------------------------------------------
# Cursor blink: unchanged mechanical 12-frame visibility cycle.
# ---------------------------------------------------------------------------
cursor = bpy.data.objects["Screen_Cursor"]
if cursor.animation_data is None:
    cursor.animation_data_create()
cursor.animation_data.action = bpy.data.actions.new("Cursor_Visibility_v2")
cursor_action = cursor.animation_data.action
hide_fc = cursor_action.fcurves.new("hide_render")
frame = 1
toggle = False
pts = []
while frame <= 432:
    pts.append((frame, 1.0 if toggle else 0.0))
    toggle = not toggle
    frame += 6
for frm, val in pts:
    hide_fc.keyframe_points.insert(frm, val, options={'FAST'})
for kp in hide_fc.keyframe_points:
    kp.interpolation = 'CONSTANT'
hide_fc.update()

bpy.ops.wm.save_as_mainfile(filepath=SCENE_BLEND)
print("SAVED v2 animation", SCENE_BLEND)

# ---------------------------------------------------------------------------
# Checkpoint stills at the new key beats.
# ---------------------------------------------------------------------------
scene.render.image_settings.file_format = "PNG"
check_frames = {
    1: "v2_f001_rest.png",
    179: "v2_f179_anticip.png",
    blink_center: "v2_f133_blink.png",
    191: "v2_f191_cup_overshoot.png",
    193: "v2_f193_cup_settled.png",
    221: "v2_f221_lower_overshoot.png",
    wipe_mid: "v2_f280_wipe.png",
    smirk_overshoot: "v2_f345_smirk_overshoot.png",
    smirk_settle: "v2_f351_smirk_settled.png",
    432: "v2_f432_loopseam.png",
}
for frm, fname in check_frames.items():
    scene.frame_set(frm)
    scene.render.filepath = os.path.join(TESTS_DIR, fname)
    bpy.ops.render.render(write_still=True)
    print("rendered", fname)
