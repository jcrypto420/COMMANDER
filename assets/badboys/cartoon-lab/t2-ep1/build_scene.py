"""
Stage 4 (part 1): build the T+2 shot scene from BADBOY_PUPPET_v1.blend.

Duplicates the puppet twice (BANKER A left w/ coffee cup, scaled 1.03 depth
cheat; BANKER B right), builds the wall-monitor prop + coffee cup prop, sets
camera/world for the two-puppet composition, and saves a new .blend. This
script does NOT animate beats (see animate_scene.py) or render final video.

Run headless:
  /Applications/Blender.app/Contents/MacOS/Blender --background \
    --python build_scene.py
"""
import bpy, bmesh, os, math

EP_DIR = os.path.dirname(os.path.abspath(__file__))
RIG_DIR = os.path.join(EP_DIR, "..", "..", "rig")
SRC_BLEND = os.path.join(RIG_DIR, "BADBOY_PUPPET_v1.blend")
OUT_BLEND = os.path.join(EP_DIR, "t2ep1_scene.blend")
TESTS_DIR = os.path.join(EP_DIR, "tests")
os.makedirs(TESTS_DIR, exist_ok=True)

INK = (0.02, 0.02, 0.02, 1.0)
SLATE = (0.10, 0.12, 0.145, 1.0)
TERMINAL_GREEN = (0.62, 0.93, 0.72, 1.0)
CREAM = (1.0, 1.0, 0.8392, 1.0)

OFFSET_X = 1.7          # banker center offset from x=0
SCALE_A = 1.03          # depth cheat
SCALE_B = 1.0

MONITOR_WIDTH = 6.0
MONITOR_HEIGHT = 3.2
MONITOR_BORDER = 0.12
MONITOR_BOTTOM_Z = 1.98   # just above head top (~1.48) with a gap

CAM_ORTHO_SCALE = 12.0


def get_or_make_material(name, color, emission=True):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    if emission:
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = color
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    mat.diffuse_color = color
    return mat


def polygon_mesh(name, points_xz, y, material, collection):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    verts = [bm.verts.new((x, y, z)) for x, z in points_xz]
    try:
        bm.faces.new(verts)
    except ValueError as e:
        print("face warn", name, e)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(material)
    collection.objects.link(obj)
    return obj


def rect_points(cx, cz, w, h):
    return [(cx - w / 2, cz - h / 2), (cx + w / 2, cz - h / 2),
            (cx + w / 2, cz + h / 2), (cx - w / 2, cz + h / 2)]


# ---------------------------------------------------------------------------
# Load base puppet file
# ---------------------------------------------------------------------------
bpy.ops.wm.open_mainfile(filepath=SRC_BLEND)

scene = bpy.context.scene
root_coll = scene.collection

ep_coll = bpy.data.collections.new("T2Ep1_Shot")
root_coll.children.link(ep_coll)


def duplicate_puppet(suffix, location, scale):
    orig_arm = bpy.data.objects["Puppet_Rig"]
    new_arm = orig_arm.copy()
    new_arm.name = f"Puppet_Rig_{suffix}"
    new_arm.location = location
    new_arm.scale = (scale, scale, scale)
    new_arm.animation_data_clear()
    new_arm.animation_data_create()
    action = bpy.data.actions.new(f"Action_{suffix}")
    new_arm.animation_data.action = action
    ep_coll.objects.link(new_arm)

    name_map = {}
    for coll_name in ("Base", "Costume_PinstripeBanker"):
        for obj in bpy.data.collections[coll_name].objects:
            if obj.type != "MESH":
                continue
            new_obj = obj.copy()
            new_obj.name = f"{obj.name}_{suffix}"
            new_obj.parent = new_arm
            new_obj.parent_type = "BONE"
            new_obj.parent_bone = obj.parent_bone
            new_obj.matrix_parent_inverse = obj.matrix_parent_inverse.copy()
            ep_coll.objects.link(new_obj)
            name_map[obj.name] = new_obj
    return new_arm, name_map


arm_a, objs_a = duplicate_puppet("A", (-OFFSET_X, 0.0, 0.0), SCALE_A)
arm_b, objs_b = duplicate_puppet("B", (OFFSET_X, 0.0, 0.0), SCALE_B)

# Remove original template objects (Base + costume collections) now that both
# instances have their own copies. Keep Costume_Plain / camera untouched (not
# used this shot but harmless to leave; only strip what would otherwise
# double-render).
for coll_name in ("Base", "Costume_PinstripeBanker", "Costume_Plain"):
    coll = bpy.data.collections.get(coll_name)
    if not coll:
        continue
    for obj in list(coll.objects):
        if obj.type in ("MESH",):
            bpy.data.objects.remove(obj, do_unlink=True)
orig_arm = bpy.data.objects.get("Puppet_Rig")
if orig_arm:
    bpy.data.objects.remove(orig_arm, do_unlink=True)

# ---------------------------------------------------------------------------
# Coffee cup prop (Banker A only) — parented rigidly to her ArmR bone
# ---------------------------------------------------------------------------
ink_mat = bpy.data.materials["Ink"]
cream_mat = bpy.data.materials["Cream"]
slate_mat = get_or_make_material("Slate", SLATE)
green_mat = get_or_make_material("TerminalGreen", TERMINAL_GREEN, emission=True)

# Rest-pose fist location for ArmR_A (bone-local rigid attach point approx).
# ArmR bone tail (rest) sits near z=-0.595; fist sits a bit further out along
# the hanging arm. Cup drawn small, right at the fist, slightly toward camera.
cup_outline = polygon_mesh(
    "Prop_Cup_Outline_A",
    rect_points(0.09, -0.70, 0.34, 0.30),
    y=0.045, material=ink_mat, collection=ep_coll,
)
cup_fill = polygon_mesh(
    "Prop_Cup_Fill_A",
    rect_points(0.09, -0.70, 0.26, 0.22),
    y=0.035, material=cream_mat, collection=ep_coll,
)
# tiny handle loop (simple flat tab, monoline-simple rather than a true ring)
handle = polygon_mesh(
    "Prop_Cup_Handle_A",
    rect_points(0.09 + 0.22, -0.70, 0.10, 0.14),
    y=0.045, material=ink_mat, collection=ep_coll,
)

for obj in (cup_outline, cup_fill, handle):
    obj.parent = arm_a
    obj.parent_type = "BONE"
    obj.parent_bone = "ArmR"
    # rest offset already baked into vertex coords (bone-local space == the
    # armature's rest space here since ArmR has no custom parent_inverse
    # quirks); zero out matrix_parent_inverse so bone rest transform applies
    # directly.
    obj.matrix_parent_inverse = arm_a.pose.bones["ArmR"].bone.matrix_local.inverted()

# ---------------------------------------------------------------------------
# Wall monitor prop
# ---------------------------------------------------------------------------
mon_center_z = MONITOR_BOTTOM_Z + MONITOR_HEIGHT / 2

mon_outline = polygon_mesh(
    "Monitor_Outline",
    rect_points(0.0, mon_center_z, MONITOR_WIDTH + MONITOR_BORDER * 2, MONITOR_HEIGHT + MONITOR_BORDER * 2),
    y=0.12, material=ink_mat, collection=ep_coll,
)
mon_fill = polygon_mesh(
    "Monitor_Fill",
    rect_points(0.0, mon_center_z, MONITOR_WIDTH, MONITOR_HEIGHT),
    y=0.10, material=slate_mat, collection=ep_coll,
)

# Screen text: monospace, pale green, terminal style. Text curve authored in
# XY plane by default -> rotate 90 deg on X so it lies flat in our XZ screen
# plane (matches how the rest of the puppet/scene is built, camera looks +Y).
def make_text(name, body, size, loc_x, loc_z, align="CENTER"):
    curve = bpy.data.curves.new(name, type="FONT")
    curve.body = body
    curve.size = size
    curve.align_x = align
    curve.align_y = "CENTER"
    try:
        mono = bpy.data.fonts.load("/System/Library/Fonts/Menlo.ttc")
        curve.font = mono
    except Exception as e:
        print("mono font load failed, using default:", e)
    obj = bpy.data.objects.new(name, curve)
    obj.rotation_euler = (math.radians(90), 0, 0)
    obj.location = (loc_x, 0.06, loc_z)
    obj.data.materials.append(green_mat)
    ep_coll.objects.link(obj)
    return obj


status_text = make_text("Screen_StatusText", "WIRE STATUS: PENDING", 0.42,
                         0.0, mon_center_z + 0.35)
cursor = polygon_mesh(
    "Screen_Cursor",
    rect_points(2.55, mon_center_z + 0.35, 0.16, 0.32),
    y=0.055, material=green_mat, collection=ep_coll,
)

# ---------------------------------------------------------------------------
# Camera + world (reuse existing Puppet_World cream background)
# ---------------------------------------------------------------------------
cam = bpy.data.objects["Puppet_Camera"]
cam.location = (0.0, -10.0, -0.32)
cam.rotation_euler = (math.radians(90), 0, 0)
cam.data.ortho_scale = CAM_ORTHO_SCALE
ep_coll.objects.link(cam)
if cam.name in bpy.data.collections.get("Base", ep_coll).objects if bpy.data.collections.get("Base") else []:
    pass

scene.camera = cam
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 432

bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("SAVED", OUT_BLEND)

# Quick single test still at frame 1 for on-model / framing check.
scene.render.filepath = os.path.join(TESTS_DIR, "framing_check.png")
scene.render.image_settings.file_format = "PNG"
bpy.ops.render.render(write_still=True)
print("RENDERED framing_check.png")
