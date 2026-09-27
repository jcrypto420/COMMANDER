"""
Build a small roster of Bad Boy Bankers for the recurring series: the
existing two (as seen in T+2 Ep.1) plus two new ones, differentiated only by
tie color (per Constitution §3 -- squeeze the cast via costume variation,
don't redesign the character). Same face, same suit cut, same elbow-jointed
rig approved for T+2.

Run headless:
  /Applications/Blender.app/Contents/MacOS/Blender --background \
    --python banker_roster.py
"""
import bpy, os, math

RIG_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_BLEND = os.path.join(RIG_DIR, "BADBOY_PUPPET_v1.blend")
OUT_BLEND = os.path.join(RIG_DIR, "banker_roster.blend")
TESTS_DIR = os.path.join(RIG_DIR, "tests")

TIE_COLORS = {
    "A_Maroon": (0.35, 0.05, 0.08, 1.0),   # existing, unchanged
    "B_Maroon": (0.35, 0.05, 0.08, 1.0),   # existing, unchanged
    "C_Navy":   (0.08, 0.11, 0.28, 1.0),
    "D_Forest": (0.06, 0.22, 0.12, 1.0),
}
OFFSET = 2.9  # wider than the T+2 two-banker shot -- 4 heads need more room


def get_or_make_tie_material(name, color):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = color
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    mat.diffuse_color = color
    return mat


bpy.ops.wm.open_mainfile(filepath=SRC_BLEND)
scene = bpy.context.scene
ep_coll = bpy.data.collections.new("Roster")
scene.collection.children.link(ep_coll)

# Costume collection is toggled off for render/viewport in the master file
# (a manual on/off layer) -- enable it so duplicated objects' source data
# reads correctly. Doesn't affect final visibility since we copy objects out
# into ep_coll below with their own hide_render explicitly set.
bpy.data.collections["Costume_PinstripeBanker"].hide_render = False
bpy.data.collections["Costume_PinstripeBanker"].hide_viewport = False


def duplicate_banker(suffix, location, tie_color_name):
    orig_arm = bpy.data.objects["Puppet_Rig"]
    new_arm = orig_arm.copy()
    new_arm.name = f"Puppet_Rig_{suffix}"
    new_arm.location = location
    new_arm.animation_data_clear()
    ep_coll.objects.link(new_arm)

    tie_mat = get_or_make_tie_material(f"Tie_{tie_color_name}", TIE_COLORS[tie_color_name])

    for coll_name in ("Base", "Costume_PinstripeBanker"):
        for obj in bpy.data.collections[coll_name].objects:
            if obj.type != "MESH":
                continue
            new_obj = obj.copy()
            new_obj.name = f"{obj.name}_{suffix}"
            new_obj.hide_render = False
            new_obj.hide_viewport = False
            new_obj.parent = new_arm
            new_obj.parent_type = "BONE"
            new_obj.parent_bone = obj.parent_bone
            new_obj.matrix_parent_inverse = obj.matrix_parent_inverse.copy()
            if obj.name == "Suit_Tie":
                new_obj.data = new_obj.data.copy()
                new_obj.data.materials.clear()
                new_obj.data.materials.append(tie_mat)
            ep_coll.objects.link(new_obj)
    return new_arm


names = list(TIE_COLORS.keys())
n = len(names)
for i, suffix in enumerate(names):
    x = (i - (n - 1) / 2) * OFFSET
    duplicate_banker(suffix, (x, 0.0, 0.0), suffix)

# Clean up originals so they don't double-render.
for coll_name in ("Base", "Costume_PinstripeBanker", "Costume_Plain"):
    coll = bpy.data.collections.get(coll_name)
    if not coll:
        continue
    for obj in list(coll.objects):
        if obj.type == "MESH":
            bpy.data.objects.remove(obj, do_unlink=True)
orig_arm = bpy.data.objects.get("Puppet_Rig")
if orig_arm:
    bpy.data.objects.remove(orig_arm, do_unlink=True)

cam = bpy.data.objects["Puppet_Camera"]
cam.location = (0.0, -10.0, -0.7)
cam.rotation_euler = (math.radians(90), 0, 0)
cam.data.ortho_scale = 12.5
scene.camera = cam
scene.render.resolution_x = 1600
scene.render.resolution_y = 1400
scene.render.engine = "BLENDER_EEVEE"

bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)

scene.render.image_settings.file_format = "PNG"
scene.render.filepath = os.path.join(TESTS_DIR, "banker_roster_group.png")
bpy.ops.render.render(write_still=True)
print("SAVED + RENDERED", OUT_BLEND)
