"""
Build BADBOY_PUPPET_v1.blend from the canonical face mark.

Run headless:
  /Applications/Blender.app/Contents/MacOS/Blender --background --python build_puppet.py

Source of truth: ../INSIDEFACE NOBG.png (traced exactly, never redrawn).
../FACE.jpg used only to derive the outer head silhouette (also traced,
not hand-drawn, since the two source images share the same coordinate frame).
"""
import bpy, bmesh, math, os

RIG_DIR = os.path.dirname(os.path.abspath(__file__))
INSIDE_FLAT = os.path.join(RIG_DIR, ".build_inside_flat.png")
FACE_SMALL = os.path.join(RIG_DIR, ".build_face_small.png")
BLEND_OUT = os.path.join(RIG_DIR, "BADBOY_PUPPET_v1.blend")
TESTS_DIR = os.path.join(RIG_DIR, "tests")

CREAM = (1.0, 1.0, 0.8392, 1.0)          # #FFFFD6
INK = (0.02, 0.02, 0.02, 1.0)
SUIT_NAVY = (0.055, 0.075, 0.13, 1.0)
SUIT_STRIPE = (0.62, 0.65, 0.72, 1.0)
TIE_MAROON = (0.35, 0.05, 0.08, 1.0)

FPS = 24
LOOP_FRAMES = FPS * 2  # 2 second loop


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def trace_image(path, threshold=0.5):
    """Trace a flattened raster into closed polygon point loops (local X/Z)."""
    bpy.ops.object.load_reference_image(filepath=path)
    empty = bpy.context.active_object
    bpy.context.view_layer.objects.active = empty
    empty.select_set(True)
    bpy.ops.gpencil.trace_image(target='NEW', thickness=10, resolution=5, scale=1.0,
                                 sample=0, threshold=threshold, turnpolicy='MINORITY', mode='SINGLE')
    gp = [o for o in bpy.data.objects if o.type == 'GPENCIL'][-1]
    gp.rotation_euler = (0, 0, 0)
    strokes = []
    for layer in gp.data.layers:
        for frame in layer.frames:
            for stroke in frame.strokes:
                strokes.append([(p.co.x, p.co.z) for p in stroke.points])
    bpy.data.objects.remove(gp, do_unlink=True)
    bpy.data.objects.remove(empty, do_unlink=True)
    return strokes


def stroke_diag(pts):
    xs = [p[0] for p in pts]
    zs = [p[1] for p in pts]
    return ((max(xs) - min(xs)) ** 2 + (max(zs) - min(zs)) ** 2) ** 0.5


def stroke_bbox_center(pts):
    xs = [p[0] for p in pts]
    zs = [p[1] for p in pts]
    return ((min(xs) + max(xs)) / 2.0, (min(zs) + max(zs)) / 2.0)


def polygon_to_mesh(name, points_xz, y=0.0, collection=None):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    verts = [bm.verts.new((x, y, z)) for x, z in points_xz]
    try:
        bm.faces.new(verts)
    except ValueError as e:
        print("face create warning for", name, e)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    (collection or bpy.context.scene.collection).objects.link(obj)
    return obj


def emission_material(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    emit = nt.nodes.new("ShaderNodeEmission")
    emit.inputs[0].default_value = color
    nt.links.new(emit.outputs[0], out.inputs[0])
    return mat


def pinstripe_material(name, base_color, stripe_color, frequency=26.0, stripe_width=0.06):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    emit = nt.nodes.new("ShaderNodeEmission")
    coord = nt.nodes.new("ShaderNodeTexCoord")
    wave = nt.nodes.new("ShaderNodeTexWave")
    wave.wave_type = 'BANDS'
    wave.bands_direction = 'X'
    wave.inputs['Scale'].default_value = frequency
    wave.inputs['Distortion'].default_value = 0.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = 'CONSTANT'
    # CONSTANT ramp colors the segment [pos_i, pos_(i+1)) with element i's color, so a
    # thin pulse needs base -> stripe -> base back-to-back (not just two stops).
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = base_color
    ramp.color_ramp.elements[1].position = 1.0 - stripe_width
    ramp.color_ramp.elements[1].color = stripe_color
    back_to_base = ramp.color_ramp.elements.new(0.995)
    back_to_base.color = base_color
    nt.links.new(coord.outputs['Object'], wave.inputs['Vector'])
    nt.links.new(wave.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], emit.inputs['Color'])
    nt.links.new(emit.outputs[0], out.inputs[0])
    return mat


def circle_points(cx, cz, r, n=16):
    return [(cx + r * math.cos(2 * math.pi * i / n), cz + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def rounded_body_points(cx, top_z, bottom_z, top_w, bottom_w, corner_r, n_per_corner=6):
    """A tapered rounded torso silhouette (wide shoulders -> narrower waist)."""
    top_l = (cx - top_w / 2 + corner_r, top_z - corner_r)
    top_r = (cx + top_w / 2 - corner_r, top_z - corner_r)
    bot_l = (cx - bottom_w / 2 + corner_r, bottom_z + corner_r)
    bot_r = (cx + bottom_w / 2 - corner_r, bottom_z + corner_r)
    pts = []
    # top edge L->R
    pts.append((cx - top_w / 2 + corner_r * 0.3, top_z))
    pts.append((cx + top_w / 2 - corner_r * 0.3, top_z))
    # top-right corner arc (90 -> 0 deg)
    for i in range(n_per_corner + 1):
        a = math.pi / 2 * (1 - i / n_per_corner)
        pts.append((top_r[0] + corner_r * math.cos(a), top_r[1] + corner_r * math.sin(a)))
    # right side down to bottom-right corner
    for i in range(n_per_corner + 1):
        a = -math.pi / 2 * (i / n_per_corner)
        pts.append((bot_r[0] + corner_r * math.cos(a), bot_r[1] + corner_r * math.sin(a)))
    # bottom edge R->L
    pts.append((cx + bottom_w / 2 - corner_r * 0.3, bottom_z))
    pts.append((cx - bottom_w / 2 + corner_r * 0.3, bottom_z))
    # bottom-left corner arc
    for i in range(n_per_corner + 1):
        a = math.pi + math.pi / 2 * (1 - i / n_per_corner)
        pts.append((bot_l[0] + corner_r * math.cos(a), bot_l[1] + corner_r * math.sin(a)))
    # left side up to top-left corner
    for i in range(n_per_corner + 1):
        a = math.pi / 2 + math.pi / 2 * (i / n_per_corner)
        pts.append((top_l[0] + corner_r * math.cos(a), top_l[1] + corner_r * math.sin(a)))
    return pts


def outline_pair(name, points_xz, fill_mat, outline_scale=1.06, collection=None):
    """Build a bold-outline flat shape: black shape behind, scaled-up copy of fill in front."""
    cx = sum(p[0] for p in points_xz) / len(points_xz)
    cz = sum(p[1] for p in points_xz) / len(points_xz)
    outer_pts = [(cx + (x - cx) * outline_scale, cz + (z - cz) * outline_scale) for x, z in points_xz]
    outer = polygon_to_mesh(name + "_Outline", outer_pts, y=0.02, collection=collection)
    outer.data.materials.append(ink_mat)
    inner = polygon_to_mesh(name + "_Fill", points_xz, y=0.0, collection=collection)
    inner.data.materials.append(fill_mat)
    return outer, inner


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

reset_scene()

scene = bpy.context.scene
scene.render.fps = FPS
scene.frame_start = 1
scene.frame_end = LOOP_FRAMES

col_rig = bpy.data.collections.new("Rig")
scene.collection.children.link(col_rig)
col_plain = bpy.data.collections.new("Costume_Plain")
scene.collection.children.link(col_plain)
col_banker = bpy.data.collections.new("Costume_PinstripeBanker")
scene.collection.children.link(col_banker)

ink_mat = emission_material("Ink_Black", INK)
cream_mat = emission_material("Skin_Cream", CREAM)
suit_mat = pinstripe_material("Suit_Pinstripe", SUIT_NAVY, SUIT_STRIPE, frequency=8.0, stripe_width=0.12)
tie_mat = emission_material("Tie_Maroon", TIE_MAROON)
button_mat = emission_material("Button_Black", (0.01, 0.01, 0.01, 1.0))

# --- trace canonical mark + head reference -------------------------------
face_strokes = trace_image(FACE_SMALL)
inside_strokes = trace_image(INSIDE_FLAT)

face_sorted = sorted(face_strokes, key=stroke_diag, reverse=True)
outer_pts, inner_pts = face_sorted[0], face_sorted[1]
feature_strokes = [s for s in inside_strokes if stroke_diag(s) > 0.1]
feature_strokes.sort(key=lambda s: -stroke_bbox_center(s)[1])  # rough top-to-bottom

def polygon_area(pts):
    """Shoelace formula."""
    a = 0.0
    n = len(pts)
    for i in range(n):
        x1, z1 = pts[i]
        x2, z2 = pts[(i + 1) % n]
        a += x1 * z2 - x2 * z1
    return abs(a) / 2.0


def classify_features(strokes):
    # mouth is by far the widest stroke; eyes are round (high fill-ratio vs bbox),
    # brows are wedges (lower fill-ratio) regardless of their individual aspect ratio.
    info = []
    for s in strokes:
        xs = [p[0] for p in s]; zs = [p[1] for p in s]
        w = max(xs) - min(xs); h = max(zs) - min(zs)
        cx, cz = stroke_bbox_center(s)
        area = polygon_area(s)
        fill_ratio = area / (w * h) if w * h > 0 else 0
        info.append(dict(pts=s, w=w, h=h, cx=cx, cz=cz, fill_ratio=fill_ratio))
    mouth = max(info, key=lambda d: d['w'])
    rest = [d for d in info if d is not mouth]
    rest.sort(key=lambda d: -d['fill_ratio'])
    eyes = rest[:2]
    brows = rest[2:]
    eyeL = min(eyes, key=lambda d: d['cx'])
    eyeR = max(eyes, key=lambda d: d['cx'])
    browL = min(brows, key=lambda d: d['cx'])
    browR = max(brows, key=lambda d: d['cx'])
    return dict(mouth=mouth, eyeL=eyeL, eyeR=eyeR, browL=browL, browR=browR)

feat = classify_features(feature_strokes)

# head bounding box (for placing body/camera)
head_xs = [p[0] for p in outer_pts]
head_zs = [p[1] for p in outer_pts]
head_min_x, head_max_x = min(head_xs), max(head_xs)
head_min_z, head_max_z = min(head_zs), max(head_zs)
head_bottom_z = head_min_z
head_width = head_max_x - head_min_x
head_cx = (head_min_x + head_max_x) / 2.0

print("Feature classification centers:",
      {k: (round(v['cx'], 2), round(v['cz'], 2)) for k, v in feat.items()})
print("Head bbox:", head_min_x, head_max_x, head_min_z, head_max_z)

# ---------------------------------------------------------------------------
# Rig collections
# ---------------------------------------------------------------------------

col_face = bpy.data.collections.new("Face")
col_rig.children.link(col_face)

# --- head: bold outline + cream fill (traced ring, not redrawn) ----------
head_outer = polygon_to_mesh("Head_Outline", outer_pts, y=0.03, collection=col_face)
head_outer.data.materials.append(ink_mat)
head_inner = polygon_to_mesh("Head_Fill", inner_pts, y=0.02, collection=col_face)
head_inner.data.materials.append(cream_mat)

# --- canonical features: solid ink shapes traced from INSIDEFACE NOBG.png
feature_objs = {}
for key in ("eyeL", "eyeR", "browL", "browR", "mouth"):
    obj = polygon_to_mesh(f"Face_{key}", feat[key]["pts"], y=0.0, collection=col_face)
    obj.data.materials.append(ink_mat)
    feature_objs[key] = obj

# mouth gets a shape key for "smirk widen" (stretch the hook further, thin the stroke)
mouth_obj = feature_objs["mouth"]
mouth_obj.shape_key_add(name="Basis")
widen_key = mouth_obj.shape_key_add(name="Smirk_Widen")
mouth_cx, mouth_cz = feat["mouth"]["cx"], feat["mouth"]["cz"]
for v in widen_key.data:
    # push points outward from center horizontally, and lift the right hook tip a bit more
    dx = v.co.x - mouth_cx
    stretch = 1.18 if dx > 0 else 1.08
    v.co.x = mouth_cx + dx * stretch
    if dx > 0:
        v.co.z += 0.03 * (dx / max(abs(p[0] - mouth_cx) for p in feat["mouth"]["pts"]))

print("STAGE 2 DONE (head + features + smirk shape key)")

# ---------------------------------------------------------------------------
# Body + costumes
# ---------------------------------------------------------------------------

BODY_TOP_Z = head_bottom_z + head_width * 0.10
BODY_BOTTOM_Z = BODY_TOP_Z - head_width * 0.95
BODY_TOP_W = head_width * 0.82
BODY_BOTTOM_W = head_width * 0.64
BODY_CORNER_R = head_width * 0.16
body_pts = rounded_body_points(head_cx, BODY_TOP_Z, BODY_BOTTOM_Z, BODY_TOP_W, BODY_BOTTOM_W, BODY_CORNER_R)

# plain costume: naked cream body
body_outer_plain, body_fill_plain = outline_pair("Body_Plain", body_pts, cream_mat, collection=col_plain)

# banker costume: same silhouette, navy pinstripe jacket + lapels + buttons + tie
body_outer_suit, body_fill_suit = outline_pair("Body_Suit", body_pts, suit_mat, collection=col_banker)

# lapels: two triangles forming a V opening below the collar, revealing a cream shirt sliver
collar_z = BODY_TOP_Z - head_width * 0.05
v_bottom_z = BODY_TOP_Z - head_width * 0.42
shirt_pts = [
    (head_cx, v_bottom_z),
    (head_cx - head_width * 0.14, collar_z),
    (head_cx + head_width * 0.14, collar_z),
]
shirt = polygon_to_mesh("Suit_Shirt", shirt_pts, y=-0.01, collection=col_banker)
shirt.data.materials.append(cream_mat)

lapel_l_pts = [
    (head_cx - head_width * 0.02, v_bottom_z),
    (head_cx - head_width * 0.16, collar_z),
    (head_cx - head_width * 0.32, collar_z + head_width * 0.03),
    (head_cx - head_width * 0.20, v_bottom_z - head_width * 0.06),
]
lapel_r_pts = [(head_cx + (head_cx - x), z) for x, z in lapel_l_pts]  # mirror across head_cx
lapel_l = polygon_to_mesh("Suit_Lapel_L", lapel_l_pts, y=-0.015, collection=col_banker)
lapel_l.data.materials.append(ink_mat)
lapel_r = polygon_to_mesh("Suit_Lapel_R", lapel_r_pts, y=-0.015, collection=col_banker)
lapel_r.data.materials.append(ink_mat)

# tiny tie
tie_top_z = v_bottom_z + head_width * 0.02
tie_pts = [
    (head_cx, tie_top_z),
    (head_cx - head_width * 0.045, tie_top_z - head_width * 0.05),
    (head_cx, tie_top_z - head_width * 0.22),
    (head_cx + head_width * 0.045, tie_top_z - head_width * 0.05),
]
tie = polygon_to_mesh("Suit_Tie", tie_pts, y=-0.02, collection=col_banker)
tie.data.materials.append(tie_mat)

# double-breasted buttons: 2 columns x 3 rows
button_r = head_width * 0.018
btn_col_offset = head_width * 0.13
btn_top_z = v_bottom_z - head_width * 0.10
for row in range(3):
    bz = btn_top_z - row * head_width * 0.12
    for side in (-1, 1):
        bx = head_cx + side * btn_col_offset
        b = polygon_to_mesh(f"Suit_Button_{row}_{side}", circle_points(bx, bz, button_r, 10),
                             y=-0.025, collection=col_banker)
        b.data.materials.append(button_mat)

print("STAGE 3 DONE (body + plain/banker costumes)")

# --- TEMP CHECKPOINT: quick render to sanity-check stage 3 -----------------
if os.environ.get("PUPPET_CHECKPOINT") == "3":
    col_banker.hide_render = False
    col_plain.hide_render = True
    bpy.ops.object.camera_add(location=(head_cx, -8, (head_max_z + BODY_BOTTOM_Z) / 2),
                               rotation=(math.radians(90), 0, 0))
    cam = bpy.context.active_object
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = (head_max_z - BODY_BOTTOM_Z) * 1.15
    scene.camera = cam
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 600
    scene.render.resolution_y = 900
    scene.view_settings.view_transform = 'Standard'
    scene.world = bpy.data.worlds.new("World")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = CREAM
    scene.render.filepath = os.path.join(RIG_DIR, ".build_checkpoint3.png")
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(RIG_DIR, ".build_debug.blend"))
    print("CHECKPOINT 3 RENDER DONE")
    import sys
    sys.exit(0)

# ---------------------------------------------------------------------------
# Armature + rig
# ---------------------------------------------------------------------------

BONE_LEN = head_width * 0.05
ROOT_Z = (BODY_TOP_Z + BODY_BOTTOM_Z) / 2.0
HEAD_PIVOT_Z = head_bottom_z

bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
armature = bpy.context.active_object
armature.name = "Puppet_Rig"
col_rig.objects.link(armature)
for c in list(armature.users_collection):
    if c != col_rig:
        c.objects.unlink(armature)

eb = armature.data.edit_bones
eb.remove(eb[0])  # drop the default bone


def make_bone(name, x, z, parent=None):
    b = eb.new(name)
    b.head = (x, 0, z)
    b.tail = (x, 0, z + BONE_LEN)
    b.roll = 0.0
    if parent:
        b.parent = eb[parent]
    return b

make_bone("Root", head_cx, ROOT_Z)
make_bone("Head", head_cx, HEAD_PIVOT_Z, parent="Root")
make_bone("BrowL", feat["browL"]["cx"], feat["browL"]["cz"], parent="Head")
make_bone("BrowR", feat["browR"]["cx"], feat["browR"]["cz"], parent="Head")
make_bone("EyelidL", feat["eyeL"]["cx"], feat["eyeL"]["cz"], parent="Head")
make_bone("EyelidR", feat["eyeR"]["cx"], feat["eyeR"]["cz"], parent="Head")
make_bone("Mouth", feat["mouth"]["cx"], feat["mouth"]["cz"], parent="Head")

bpy.ops.object.mode_set(mode='OBJECT')


def bone_parent(mesh_objs, bone_name):
    for o in bpy.data.objects:
        o.select_set(False)
    for o in mesh_objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)
    armature.data.bones.active = armature.data.bones[bone_name]
    bpy.ops.object.parent_set(type='BONE', keep_transform=True)


bone_parent([head_outer, head_inner], "Head")
bone_parent([feature_objs["browL"]], "BrowL")
bone_parent([feature_objs["browR"]], "BrowR")
bone_parent([feature_objs["eyeL"]], "EyelidL")
bone_parent([feature_objs["eyeR"]], "EyelidR")
bone_parent([mouth_obj], "Mouth")

body_pieces_plain = [body_outer_plain, body_fill_plain]
body_pieces_suit = [body_outer_suit, body_fill_suit, shirt, lapel_l, lapel_r, tie] + \
    [o for o in bpy.data.objects if o.name.startswith("Suit_Button_")]
bone_parent(body_pieces_plain + body_pieces_suit, "Root")

# Pose bones default to QUATERNION rotation; switch to Euler XYZ so the rig's
# "tilt" controls (rotation_euler) actually take effect.
for pbone in armature.pose.bones:
    pbone.rotation_mode = 'XYZ'

print("STAGE 4 DONE (armature + bone parenting)")

if os.environ.get("PUPPET_CHECKPOINT") == "4":
    col_banker.hide_render = False
    col_plain.hide_render = True
    bpy.ops.object.camera_add(location=(head_cx, -8, (head_max_z + BODY_BOTTOM_Z) / 2),
                               rotation=(math.radians(90), 0, 0))
    cam = bpy.context.active_object
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = (head_max_z - BODY_BOTTOM_Z) * 1.15
    scene.camera = cam
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 600
    scene.render.resolution_y = 900
    scene.view_settings.view_transform = 'Standard'
    scene.world = bpy.data.worlds.new("World")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = CREAM

    # pose test: raise+tilt BrowR, blink EyelidL, bob Head, bounce Root
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    armature.pose.bones["BrowR"].rotation_euler.z = math.radians(45)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.update()
    print("BrowR rotation_mode:", armature.pose.bones["BrowR"].rotation_mode)
    print("BrowR rotation_euler:", armature.pose.bones["BrowR"].rotation_euler[:])
    print("BrowR pose matrix_basis:\n", armature.pose.bones["BrowR"].matrix_basis)
    print("browR mesh world matrix:\n", feature_objs["browR"].matrix_world)

    scene.render.filepath = os.path.join(RIG_DIR, ".build_checkpoint4.png")
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(RIG_DIR, ".build_debug.blend"))
    print("CHECKPOINT 4 RENDER DONE")
    import sys
    sys.exit(0)

# ---------------------------------------------------------------------------
# Camera + render settings
# ---------------------------------------------------------------------------

full_top = head_max_z
full_bottom = BODY_BOTTOM_Z
full_height = full_top - full_bottom
frame_center_z = (full_top + full_bottom) / 2.0
MARGIN = 1.15

bpy.ops.object.camera_add(location=(head_cx, -10, frame_center_z),
                           rotation=(math.radians(90), 0, 0))
camera = bpy.context.active_object
camera.name = "Puppet_Camera"
camera.data.type = 'ORTHO'
camera.data.sensor_fit = 'VERTICAL'
camera.data.ortho_scale = full_height * MARGIN
col_rig.objects.link(camera)
for c in list(camera.users_collection):
    if c != col_rig:
        c.objects.unlink(camera)
scene.camera = camera

scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.film_transparent = False
scene.view_settings.view_transform = 'Standard'

world = bpy.data.worlds.new("Puppet_World")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = CREAM
scene.world = world

print("STAGE 5 DONE (camera + render settings)")

# ---------------------------------------------------------------------------
# Idle-loop animation: blink + subtle head bob + body bounce/squash-stretch
# ---------------------------------------------------------------------------

bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE')

root_pb = armature.pose.bones["Root"]
head_pb = armature.pose.bones["Head"]
eyelidL_pb = armature.pose.bones["EyelidL"]
eyelidR_pb = armature.pose.bones["EyelidR"]


def keyframe(pbone, data_path, frame, value=None):
    if value is not None:
        setattr(pbone, data_path, value)
    pbone.keyframe_insert(data_path=data_path, frame=frame)


# body bounce + squash-stretch: one full cycle across the loop, max 10% scale
for f in range(1, LOOP_FRAMES + 1):
    phase = 2 * math.pi * (f - 1) / LOOP_FRAMES
    bounce = math.sin(phase) * 0.035          # world-Z bounce (bone-local Y)
    stretch = 1.0 + math.sin(phase) * 0.06    # up->stretch, down->squash
    squash = 1.0 - math.sin(phase) * 0.05

    root_pb.location.y = bounce
    root_pb.keyframe_insert(data_path="location", frame=f)
    root_pb.scale = (squash, stretch, squash)
    root_pb.keyframe_insert(data_path="scale", frame=f)

    head_bounce = math.sin(phase + 0.35) * 0.02
    head_pb.location.y = head_bounce
    head_pb.keyframe_insert(data_path="location", frame=f)

# blink: quick close-open near the start of the second half of the loop
BLINK_FRAME = LOOP_FRAMES // 2
blink_frames = {
    1: 1.0,
    BLINK_FRAME - 2: 1.0,
    BLINK_FRAME: 0.05,
    BLINK_FRAME + 2: 1.0,
    LOOP_FRAMES: 1.0,
}
for pb in (eyelidL_pb, eyelidR_pb):
    for f, val in blink_frames.items():
        pb.scale = (1.0, val, 1.0)
        pb.keyframe_insert(data_path="scale", frame=f)

# hold static (no rotation) for brow/mouth rig controls -- available but unused here
for fc in armature.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = 'SINE'

bpy.ops.object.mode_set(mode='OBJECT')
scene.frame_set(1)

print("STAGE 6 DONE (idle-loop animation)")

# ---------------------------------------------------------------------------
# Render deliverables
# ---------------------------------------------------------------------------

os.makedirs(TESTS_DIR, exist_ok=True)
scene.frame_set(1)

# still_plain.png
col_plain.hide_render = False
col_banker.hide_render = True
scene.render.filepath = os.path.join(TESTS_DIR, "still_plain.png")
scene.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print("RENDERED still_plain.png")

# still_banker.png
col_plain.hide_render = True
col_banker.hide_render = False
scene.render.filepath = os.path.join(TESTS_DIR, "still_banker.png")
bpy.ops.render.render(write_still=True)
print("RENDERED still_banker.png")

# idle_loop.mp4 (banker variant, full animated loop)
scene.render.filepath = os.path.join(TESTS_DIR, "idle_loop.mp4")
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.gopsize = LOOP_FRAMES
scene.render.ffmpeg.audio_codec = 'NONE'
scene.frame_start = 1
scene.frame_end = LOOP_FRAMES
bpy.ops.render.render(animation=True)
print("RENDERED idle_loop.mp4")

# ---------------------------------------------------------------------------
# Save + cleanup
# ---------------------------------------------------------------------------

col_plain.hide_render = False
col_banker.hide_render = True
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
print("SAVED", BLEND_OUT)
print("ALL DONE")
