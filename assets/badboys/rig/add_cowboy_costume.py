"""
Add a Costume_Cowboy collection: the plain-face puppet + a cowboy hat prop
traced directly from the approved brand mark (../COWBAD.png), per Pilot 2
("risk management") which calls for cast: cowboy hat over the plain face.

The hat's outline points were extracted from COWBAD.png's actual ink
boundary (see .hat_outline.json, built by sampling the reference PNG's
left/right silhouette edges and mapping them into this rig's head
coordinate space via the face width + chin position as calibration anchors)
-- traced, not redrawn, per Constitution Article 1.

Run headless:
  /Applications/Blender.app/Contents/MacOS/Blender --background \
    --python add_cowboy_costume.py
"""
import bpy, bmesh, json, os

RIG_DIR = os.path.dirname(os.path.abspath(__file__))
BLEND_PATH = os.path.join(RIG_DIR, "BADBOY_PUPPET_v1.blend")
OUTLINE_JSON = os.path.join(RIG_DIR, ".hat_outline.json")
TESTS_DIR = os.path.join(RIG_DIR, "tests")

HAT_Y_OUTLINE = 0.028  # just in front of Head_Outline (0.03), behind Head_Fill (0.02)
HAT_Y_FILL = 0.018


def inset_polygon(points, factor):
    cx = sum(p[0] for p in points) / len(points)
    cz = sum(p[1] for p in points) / len(points)
    return [(cx + (x - cx) * factor, cz + (z - cz) * factor) for x, z in points]


def build_mesh(name, points, y, material):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    verts = [bm.verts.new((x, y, z)) for x, z in points]
    bm.faces.new(verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(material)
    return obj


bpy.ops.wm.open_mainfile(filepath=BLEND_PATH)

with open(OUTLINE_JSON) as f:
    outline_pts = [tuple(p) for p in json.load(f)]

ink_mat = bpy.data.materials["Ink"]
cream_mat = bpy.data.materials["Cream"]

hat_outline_obj = build_mesh("Hat_Outline", outline_pts, HAT_Y_OUTLINE, ink_mat)
fill_pts = inset_polygon(outline_pts, 0.93)
hat_fill_obj = build_mesh("Hat_Fill", fill_pts, HAT_Y_FILL, cream_mat)

costume_coll = bpy.data.collections.new("Costume_Cowboy")
bpy.context.scene.collection.children.link(costume_coll)
costume_coll.hide_render = True
costume_coll.hide_viewport = True

head_fill = bpy.data.objects["Head_Fill"]
for obj in (hat_outline_obj, hat_fill_obj):
    obj.parent = bpy.data.objects["Puppet_Rig"]
    obj.parent_type = "BONE"
    obj.parent_bone = "Head"
    obj.matrix_parent_inverse = head_fill.matrix_parent_inverse.copy()
    costume_coll.objects.link(obj)

bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
print("SAVED with cowboy hat", BLEND_PATH)

# Self-check render: plain costume + cowboy hat, banker costume hidden.
scene = bpy.context.scene
bpy.data.collections["Costume_PinstripeBanker"].hide_render = True
bpy.data.collections["Costume_Plain"].hide_render = False
costume_coll.hide_render = False
cam = bpy.data.objects["Puppet_Camera"]
cam.location = (0.0, -10.0, -0.3)
cam.data.ortho_scale = 6.5
scene.camera = cam
scene.render.resolution_x = 1400
scene.render.resolution_y = 2000
scene.render.image_settings.file_format = "PNG"
scene.frame_set(1)
scene.render.filepath = os.path.join(TESTS_DIR, "cowboy_check.png")
bpy.ops.render.render(write_still=True)
print("rendered cowboy_check.png")
