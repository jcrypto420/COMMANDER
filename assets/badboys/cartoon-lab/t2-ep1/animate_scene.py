"""
Stage 4 (part 2): keyframe every beat in STORYBOARD.md's Panels table onto
t2ep1_scene.blend (built by build_scene.py).

Run headless:
  /Applications/Blender.app/Contents/MacOS/Blender --background \
    --python animate_scene.py
"""
import bpy, os, math

EP_DIR = os.path.dirname(os.path.abspath(__file__))
SCENE_BLEND = os.path.join(EP_DIR, "t2ep1_scene.blend")
TESTS_DIR = os.path.join(EP_DIR, "tests")

FPS = 24


def f(t):
    """Storyboard seconds -> frame number (frame 1 == t=0.0)."""
    return round(1 + t * FPS)


bpy.ops.wm.open_mainfile(filepath=SCENE_BLEND)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 432  # 18.0s @ 24fps, frame 432 == frame 1 (loop seam)

arm_a = bpy.data.objects["Puppet_Rig_A"]
arm_b = bpy.data.objects["Puppet_Rig_B"]


def bulk_set(action, data_path, index, frame_values, interpolation="LINEAR"):
    fc = action.fcurves.find(data_path, index=index)
    if fc is None:
        fc = action.fcurves.new(data_path, index=index)
    fc.keyframe_points.clear()
    fc.keyframe_points.add(len(frame_values))
    flat = []
    for frm, val in frame_values:
        flat.extend((frm, val))
    fc.keyframe_points.foreach_set("co", flat)
    for kp in fc.keyframe_points:
        kp.interpolation = interpolation
    fc.update()
    return fc


# ---------------------------------------------------------------------------
# 1. Ambient idle bounce/bob for BOTH bankers, tiled across the whole 18s.
#    Reuses the shape of the approved idle-loop action (Root bounce+squash,
#    Head secondary bob), period 48 frames (2s) -- 432 / 48 = 9 whole loops,
#    so it tiles with zero seam.
# ---------------------------------------------------------------------------
def ambient_bounce(arm):
    action = arm.animation_data.action
    frames = list(range(1, 433))

    root_y = [(fr, 0.05 * math.sin(2 * math.pi * (fr - 1) / 48)) for fr in frames]
    root_sx = [(fr, 1.0 - 0.04 * math.sin(2 * math.pi * (fr - 1) / 48)) for fr in frames]
    root_sy = [(fr, 1.0 + 0.055 * math.sin(2 * math.pi * (fr - 1) / 48)) for fr in frames]
    root_sz = root_sx
    head_y = [(fr, 0.03 * math.sin(2 * math.pi * (fr - 1) / 48 + math.pi / 8)) for fr in frames]

    bulk_set(action, 'pose.bones["Root"].location', 1, root_y)
    bulk_set(action, 'pose.bones["Root"].scale', 0, root_sx)
    bulk_set(action, 'pose.bones["Root"].scale', 1, root_sy)
    bulk_set(action, 'pose.bones["Root"].scale', 2, root_sz)
    bulk_set(action, 'pose.bones["Head"].location', 1, head_y)

    # flat eyelids by default -- explicit blink beats added on top per-instance
    bulk_set(action, 'pose.bones["EyelidL"].scale', 1, [(1, 1.0), (432, 1.0)])
    bulk_set(action, 'pose.bones["EyelidR"].scale', 1, [(1, 1.0), (432, 1.0)])


ambient_bounce(arm_a)
ambient_bounce(arm_b)

# ---------------------------------------------------------------------------
# 2. Banker B: single slow blink at 5.5s (6 frames total: 3 close + 3 open).
# ---------------------------------------------------------------------------
blink_center = f(5.5)  # 133
blink_pts = [
    (blink_center - 3, 1.0),
    (blink_center, 0.06),
    (blink_center + 3, 1.0),
]
action_b = arm_b.animation_data.action
for idx_name in ('EyelidL', 'EyelidR'):
    fc = action_b.fcurves.find(f'pose.bones["{idx_name}"].scale', index=1)
    for frm, val in blink_pts:
        fc.keyframe_points.insert(frm, val, options={'FAST'})
    for kp in fc.keyframe_points:
        kp.interpolation = 'BEZIER'
    fc.update()

# ---------------------------------------------------------------------------
# 3. Banker A: coffee cup raise (12f) / hold (18f) / lower (12f) at 7.5-9.5s,
#    plus a <=4 degree head tilt during the sip. ArmR/Head local Z axis =
#    world -Y, i.e. rotation about it swings things IN the flat XZ screen
#    plane (verified against bone axes before building this rig extension).
# ---------------------------------------------------------------------------
raise_start = f(7.5)          # 181
raise_end = raise_start + 12  # 193 -- coffee sip SFX also lands here
hold_end = raise_end + 18     # 211
lower_end = hold_end + 12     # 223

RAISE_ANGLE_DEG = 90.0   # verified via depsgraph-evaluated mesh center: lands cup
                          # almost exactly at mouth height, inside the head silhouette
TILT_ANGLE_DEG = 3.0

arm_a.pose.bones["ArmR"].rotation_mode = 'XYZ'
arm_a.pose.bones["Head"].rotation_mode = 'XYZ'

action_a = arm_a.animation_data.action


def key_pose_rotation(action, bone_name, frame_values):
    fc = action.fcurves.find(f'pose.bones["{bone_name}"].rotation_euler', index=2)
    if fc is None:
        fc = action.fcurves.new(f'pose.bones["{bone_name}"].rotation_euler', index=2)
    for frm, val in frame_values:
        fc.keyframe_points.insert(frm, val, options={'FAST'})
    for kp in fc.keyframe_points:
        kp.interpolation = 'BEZIER'
        kp.easing = 'EASE_IN_OUT'
    fc.update()


key_pose_rotation(action_a, "ArmR", [
    (raise_start, 0.0),
    (raise_end, math.radians(RAISE_ANGLE_DEG)),
    (hold_end, math.radians(RAISE_ANGLE_DEG)),
    (lower_end, 0.0),
])
key_pose_rotation(action_a, "Head", [
    (raise_start, 0.0),
    (raise_end, math.radians(TILT_ANGLE_DEG)),
    (hold_end, math.radians(TILT_ANGLE_DEG)),
    (lower_end, 0.0),
])

# ---------------------------------------------------------------------------
# 4. Screen "refresh" wipe: 6-frame scale-Y collapse/restore at panel 6 start
#    (11.5s), text re-renders identical after.
# ---------------------------------------------------------------------------
wipe_start = f(11.5)  # 277
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
    for frm, val in ((wipe_start, 1.0), (wipe_mid, 0.03), (wipe_end, 1.0)):
        fc.keyframe_points.insert(frm, val, options={'FAST'})
    for kp in fc.keyframe_points:
        kp.interpolation = 'BEZIER'
    fc.update()

# ---------------------------------------------------------------------------
# 5. Smirk-widen shape key -- shared Key datablock (Face_mouth_A/_B share mesh
#    data via object.copy()), so ONE animation drives both smirks together,
#    matching "both smirks widen simultaneously."
#    Ramps up 13.5-14.5s, holds through 16.0s+caption, eases back to neutral
#    in the last second before the loop point so frame 432 == frame 1.
#    CREATIVE CALL (flagged to Josh): storyboard doesn't say how the smirk
#    returns to neutral for the loop -- chose a slow ease-back late in panel 8
#    rather than a hard cut, so the loop seam has no visible pop.
# ---------------------------------------------------------------------------
key_id = bpy.data.objects["Face_mouth_A"].data.shape_keys
if key_id is not None:
    if key_id.animation_data is None:
        key_id.animation_data_create()
    if key_id.animation_data.action is None:
        key_id.animation_data.action = bpy.data.actions.new("SmirkWidenAction")
    act = key_id.animation_data.action
    fc = act.fcurves.find('key_blocks["Smirk_Widen"].value')
    if fc is None:
        fc = act.fcurves.new('key_blocks["Smirk_Widen"].value')
    smirk_start = f(13.5)   # 325
    smirk_full = smirk_start + 24  # 349, i.e. 14.5s
    ease_back_start = f(17.0)  # 409
    for frm, val in (
        (1, 0.0),
        (smirk_start, 0.0),
        (smirk_full, 1.0),
        (ease_back_start, 1.0),
        (432, 0.0),
    ):
        fc.keyframe_points.insert(frm, val, options={'FAST'})
    for kp in fc.keyframe_points:
        kp.interpolation = 'BEZIER'
    fc.update()

# ---------------------------------------------------------------------------
# 6. Cursor blink: 12-frame visibility cycle (6 on / 6 off) for the whole shot.
# ---------------------------------------------------------------------------
cursor = bpy.data.objects["Screen_Cursor"]
if cursor.animation_data is None:
    cursor.animation_data_create()
if cursor.animation_data.action is None:
    cursor_action = bpy.data.actions.new("Cursor_Visibility")
    cursor.animation_data.action = cursor_action
else:
    cursor_action = cursor.animation_data.action
hide_fc = cursor_action.fcurves.find("hide_render")
if hide_fc is None:
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
print("SAVED animated", SCENE_BLEND)

# ---------------------------------------------------------------------------
# Test-render stills at key beats for self-QC before anything else happens.
# ---------------------------------------------------------------------------
scene.render.image_settings.file_format = "PNG"
check_frames = {
    1: "chk_f001_rest.png",
    blink_center: "chk_f133_blink.png",
    raise_end: "chk_f193_cupsip.png",
    wipe_mid: "chk_f280_wipe.png",
    smirk_full: "chk_f349_smirk.png",
    f(16.5): "chk_f397_caption.png",
    432: "chk_f432_loopseam.png",
}
for frm, fname in check_frames.items():
    scene.frame_set(frm)
    scene.render.filepath = os.path.join(TESTS_DIR, fname)
    bpy.ops.render.render(write_still=True)
    print("rendered", fname)
