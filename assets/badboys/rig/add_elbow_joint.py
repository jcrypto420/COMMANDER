"""
Rig upgrade: split the single rigid ArmL/ArmR bone into an upper-arm bone
(unchanged, shoulder pivot) + a new child ForearmL/ForearmR bone (elbow
pivot), splitting the existing arm mesh shape into two pieces at the elbow
height. Without this, any gesture that lifts the hand to the head has to
swing the WHOLE arm shape across the face like a stiff clock hand -- Josh
flagged this exact thing as looking broken on the T+2 coffee-cup gesture.

Reusable across all future Cartoon Lab shorts, not a one-shot hack for this
episode -- written directly into BADBOY_PUPPET_v1.blend (backed up first as
BADBOY_PUPPET_v1_pre_elbow_backup.blend).

Run headless:
  /Applications/Blender.app/Contents/MacOS/Blender --background \
    --python add_elbow_joint.py
"""
import bpy, bmesh, os, math
from mathutils import Vector, Matrix

RIG_DIR = os.path.dirname(os.path.abspath(__file__))
BLEND_PATH = os.path.join(RIG_DIR, "BADBOY_PUPPET_v1.blend")

# Elbow height (world/local Z) to split each arm shape at. Both arms happen
# to span a similar Z range (shoulder ~-0.7 to -0.8 down to fist ~-1.8 to
# -1.9), so one split height works for both -- picked at roughly 40% down
# from the shoulder, a natural elbow position for this proportion.
ELBOW_Z = -1.15


def ordered_points(obj):
    return [(v.co.x, v.co.z) for v in obj.data.vertices]


def find_crossings(pts, z_target):
    n = len(pts)
    crossings = []
    for i in range(n):
        x0, z0 = pts[i]
        x1, z1 = pts[(i + 1) % n]
        if (z0 - z_target) * (z1 - z_target) < 0:
            t = (z_target - z0) / (z1 - z0)
            x = x0 + t * (x1 - x0)
            crossings.append({"edge": (i, (i + 1) % n), "x": x})
    return crossings


def split_arm_mesh(arm_obj, z_target, y_depth):
    """Return (upper_points, lower_points) as ordered (x,z) loops, split at
    z_target. upper = shoulder side, lower = elbow-to-fist side."""
    pts = ordered_points(arm_obj)
    crossings = find_crossings(pts, z_target)
    assert len(crossings) == 2, f"expected 2 crossings, got {len(crossings)}"
    crossings.sort(key=lambda c: c["edge"][0])
    (i0, j0), x0 = crossings[0]["edge"], crossings[0]["x"]
    (i1, j1), x1 = crossings[1]["edge"], crossings[1]["x"]

    # Walk the loop from j0 (just after first crossing) to i1 (just before
    # second crossing) -- this is the "far" arc (down around the fist end,
    # i.e. the lower/forearm piece's main body).
    n = len(pts)
    lower_mid = []
    k = j0
    while True:
        lower_mid.append(pts[k])
        if k == i1:
            break
        k = (k + 1) % n
    lower_points = [(x0, z_target)] + lower_mid + [(x1, z_target)]

    upper_mid = []
    k = j1
    while True:
        upper_mid.append(pts[k])
        if k == i0:
            break
        k = (k + 1) % n
    upper_points = [(x1, z_target)] + upper_mid + [(x0, z_target)]

    return upper_points, lower_points


def build_mesh_from_points(name, points, y, material):
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


def bone_parent_inverse(bone):
    """Match this rig's existing convention: parent-inverse anchored at the
    bone's TAIL (see build_scene.py's note -- Blender's own bone-parent
    convention, not a head-anchored one)."""
    mat = bone.matrix_local @ Matrix.Translation((0, bone.length, 0))
    return mat.inverted()


def main():
    bpy.ops.wm.open_mainfile(filepath=BLEND_PATH)
    arm_data_obj = bpy.data.objects["Puppet_Rig"]
    ink_mat = bpy.data.materials["Ink"]

    for side, coll_name in (("R", "Base"), ("L", "Base")):
        arm_name = f"Arm{side}"
        fist_name = f"Fist{side}"
        arm_obj = bpy.data.objects[arm_name]
        y_depth = arm_obj.data.vertices[0].co.y

        upper_pts, lower_pts = split_arm_mesh(arm_obj, ELBOW_Z, y_depth)

        # Replace ArmR/ArmL's mesh data in place with just the upper portion
        # (keeps the object name + existing parenting to the shoulder bone).
        old_mesh = arm_obj.data
        new_upper_mesh = bpy.data.meshes.new(f"{arm_name}_upper")
        bm = bmesh.new()
        verts = [bm.verts.new((x, y_depth, z)) for x, z in upper_pts]
        bm.faces.new(verts)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(new_upper_mesh)
        bm.free()
        new_upper_mesh.materials.append(ink_mat)
        arm_obj.data = new_upper_mesh
        bpy.data.meshes.remove(old_mesh)

        # New forearm mesh object (elbow-to-fist piece).
        forearm_obj = build_mesh_from_points(f"Forearm{side}", lower_pts, y_depth, ink_mat)
        bpy.data.collections[coll_name].objects.link(forearm_obj)

        # --- Bone hierarchy: add Forearm{side} as a child of Arm{side} ---
        bpy.context.view_layer.objects.active = arm_data_obj
        bpy.ops.object.mode_set(mode='EDIT')
        ebones = arm_data_obj.data.edit_bones
        parent_ebone = ebones[arm_name]
        elbow_x = (upper_pts[0][0] + upper_pts[-1][0]) / 2  # midpoint of the cut line
        forearm_ebone = ebones.new(f"Forearm{side}")
        forearm_ebone.head = (elbow_x, 0.0, ELBOW_Z)
        forearm_ebone.tail = (elbow_x, 0.0, ELBOW_Z + 0.15)
        forearm_ebone.parent = parent_ebone
        forearm_ebone.use_connect = False
        bpy.ops.object.mode_set(mode='OBJECT')

        forearm_bone = arm_data_obj.pose.bones[f"Forearm{side}"].bone
        p_inv = bone_parent_inverse(forearm_bone)

        # Reparent the new forearm mesh + the fist to the new bone.
        for obj in (forearm_obj, bpy.data.objects[fist_name]):
            obj.parent = arm_data_obj
            obj.parent_type = 'BONE'
            obj.parent_bone = f"Forearm{side}"
            obj.matrix_parent_inverse = p_inv

        print(f"Arm{side}/Fist{side} split complete: elbow at x={elbow_x:.3f} z={ELBOW_Z}")

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    print("SAVED", BLEND_PATH)


main()
