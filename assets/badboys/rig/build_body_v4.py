import bpy, bmesh, math, json

bpy.ops.wm.read_factory_settings(use_empty=True)

# --- reload the real head outline from the puppet blend, so we're working
# against the actual validated geometry, not a guess.
HEAD_PTS = [[-0.2462, 1.4627], [-0.51, 1.3867], [-0.772, 1.2417], [-1.0132, 1.0406], [-1.2147, 0.7964], [-1.3031, 0.6479], [-1.3715, 0.496], [-1.4198, 0.3405], [-1.4482, 0.1816], [-1.4525, 0.1029], [-1.4521, 0.0016], [-1.4478, -0.0974], [-1.44, -0.1694], [-1.3491, -0.4341], [-1.1865, -0.6396], [-0.9541, -0.7845], [-0.6539, -0.8669], [-0.5739, -0.875], [-0.474, -0.8796], [-0.3722, -0.8802], [-0.2861, -0.8764], [-0.1661, -0.8619], [-0.044, -0.8397], [0.0701, -0.8119], [0.1664, -0.7806], [0.2914, -0.726], [0.4644, -0.6428], [0.6454, -0.5509], [0.794, -0.4701], [0.8751, -0.4215], [0.959, -0.3679], [1.0398, -0.3131], [1.1117, -0.261], [1.1862, -0.1987], [1.2677, -0.1216], [1.3418, -0.0438], [1.3945, 0.0204], [1.4627, 0.1357], [1.5085, 0.255], [1.5314, 0.3763], [1.5307, 0.4977], [1.5042, 0.6367], [1.4552, 0.7651], [1.3835, 0.8827], [1.2892, 0.9898], [1.117, 1.1247], [0.901, 1.2341], [0.6261, 1.3242], [0.2773, 1.4012], [0.2194, 1.412], [0.1566, 1.424], [0.0965, 1.4357], [0.0467, 1.4456], [-0.0377, 1.4603], [-0.1127, 1.4679], [-0.1812, 1.4686], [-0.2462, 1.4627]]
HEAD_INNER_PTS = [[-0.0175, 1.3718], [0.0145, 1.3652], [0.0651, 1.3554], [0.1272, 1.3437], [0.1939, 1.3314], [0.3201, 1.3078], [0.4169, 1.2884], [0.4992, 1.2699], [0.5817, 1.2494], [0.8952, 1.1439], [1.1381, 1.0077], [1.3119, 0.8396], [1.4182, 0.6387], [1.4496, 0.3648], [1.3512, 0.1049], [1.1186, -0.1477], [0.7473, -0.4], [0.5863, -0.4873], [0.3994, -0.5812], [0.2252, -0.663], [0.1022, -0.7139], [-0.0938, -0.7659], [-0.3026, -0.7938], [-0.5108, -0.7966], [-0.705, -0.7732], [-0.957, -0.6911], [-1.1515, -0.5584], [-1.2865, -0.3771], [-1.3601, -0.149], [-1.376, 0.0356], [-1.3618, 0.2196], [-1.3175, 0.4023], [-1.2433, 0.583], [-1.1147, 0.7951], [-0.953, 0.9845], [-0.7628, 1.1464], [-0.5488, 1.2762], [-0.4046, 1.3377], [-0.2686, 1.3741], [-0.1399, 1.3854], [-0.0175, 1.3718]]

head_cx = 0.5 * (min(p[0] for p in HEAD_PTS) + max(p[0] for p in HEAD_PTS))
head_bottom = min(p[1] for p in HEAD_PTS)
head_width = max(p[0] for p in HEAD_PTS) - min(p[0] for p in HEAD_PTS)
print("head_cx", head_cx, "head_bottom", head_bottom, "head_width", head_width)

def capsule_points(cx1, cz1, r1, cx2, cz2, r2, n=14):
    """Tapered capsule (stadium) between two circles, smooth all the way round."""
    ang = math.atan2(cz2 - cz1, cx2 - cx1)
    perp = ang + math.pi / 2
    pts = []
    # side 1 (right side going from circle1 to circle2)
    pts.append((cx1 + r1 * math.cos(perp), cz1 + r1 * math.sin(perp)))
    pts.append((cx2 + r2 * math.cos(perp), cz2 + r2 * math.sin(perp)))
    # cap around circle 2
    for i in range(n + 1):
        a = perp - math.pi * (i / n)
        pts.append((cx2 + r2 * math.cos(a), cz2 + r2 * math.sin(a)))
    # side 2 back to circle1
    pts.append((cx1 + r1 * math.cos(perp + math.pi), cz1 + r1 * math.sin(perp + math.pi)))
    # cap around circle 1
    for i in range(n + 1):
        a = (perp + math.pi) - math.pi * (i / n)
        pts.append((cx1 + r1 * math.cos(a), cz1 + r1 * math.sin(a)))
    return pts

def polygon_to_mesh(name, points_xz, y=0.0):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    verts = [bm.verts.new((x, y, z)) for x, z in points_xz]
    bm.faces.new(verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

# --- narrow full body v2 -----------------------------------------------------
# Fixes vs v1 (ogre/hunchback feedback):
#   1. The face TILTS (chin sits low-left, head rides high-right). v1 centered
#      the body on the head's bounding box, so the right shoulder/arm poked way
#      up behind the raised side of the head = hunchback. v2 anchors every part
#      to the head's ACTUAL lower silhouette edge at that part's x position.
#   2. Body ink line matched to the head's traced stroke weight (was thinner).
#   3. Slimmer torso, longer legs, smaller feet = less squat/ogre.
HW = head_width

def head_bottom_edge_z(x):
    """Lowest z of the head silhouette at a given x (vertical-line crossing)."""
    crossings = []
    n = len(HEAD_PTS)
    for i in range(n):
        x1, z1 = HEAD_PTS[i]
        x2, z2 = HEAD_PTS[(i + 1) % n]
        if (x1 <= x <= x2) or (x2 <= x <= x1):
            if abs(x2 - x1) < 1e-9:
                crossings.append(min(z1, z2))
            else:
                t = (x - x1) / (x2 - x1)
                crossings.append(z1 + t * (z2 - z1))
    return min(crossings) if crossings else head_bottom

# plant the body under the chin's center of mass, not the bbox center
BODY_CX = -0.18

# --- v4: rubber-hose anatomy + mischievous-cool pose -------------------------
# Approved brainstorm: (B) arms from torso shoulders; hand-on-hip pose with
# cocked foot; shorts w/ two buttons + glove stitches; body shrunk 10% while
# hands/shoes stay FULL SIZE (oversized extremities = the cute/classic ratio).
BS = 0.9  # body scale (torso + limb lengths only, not extremities)

SHOULDER_W = HW * 0.14 * BS
HIP_W = HW * 0.23 * BS
TORSO_LEN = HW * 0.34 * BS
torso_top_z = head_bottom_edge_z(BODY_CX) + HW * 0.06   # small hidden overlap
torso_bot_z = torso_top_z - TORSO_LEN
# subtle cool-guy lean: hips shifted right of the shoulders
torso_bot_cx = BODY_CX + HW * 0.03
TORSO_VISIBLE_BOTTOM = torso_bot_z - HIP_W

def qbez(p0, p1, p2, n=24):
    """Sample a quadratic bezier."""
    out = []
    for i in range(n):
        t = i / (n - 1)
        out.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]))
    return out

def tube_along(pts, r, cap_n=8):
    """Constant-radius noodle around a sampled curve, round caps both ends."""
    n = len(pts)
    tangents = []
    for i in range(n):
        if i == 0:
            vx, vz = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        elif i == n - 1:
            vx, vz = pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]
        else:
            vx, vz = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        m = math.hypot(vx, vz)
        tangents.append((vx / m, vz / m))
    normals = [(-t[1], t[0]) for t in tangents]
    left = [(p[0] + nm[0] * r, p[1] + nm[1] * r) for p, nm in zip(pts, normals)]
    right = [(p[0] - nm[0] * r, p[1] - nm[1] * r) for p, nm in zip(pts, normals)]
    end_ang = math.atan2(normals[-1][1], normals[-1][0])
    cap_end = [(pts[-1][0] + r * math.cos(end_ang - math.pi * i / cap_n),
                pts[-1][1] + r * math.sin(end_ang - math.pi * i / cap_n)) for i in range(1, cap_n)]
    start_ang = math.atan2(-normals[0][1], -normals[0][0])
    cap_start = [(pts[0][0] + r * math.cos(start_ang - math.pi * i / cap_n),
                  pts[0][1] + r * math.sin(start_ang - math.pi * i / cap_n)) for i in range(1, cap_n)]
    return left + cap_end + right[::-1] + cap_start

# arms attach INSIDE the pear's upper sides (start hidden behind torso)
ARM_R = HW * 0.030 * BS
HAND_R = HW * 0.075          # full size (not shrunk)
shoulder_z = torso_top_z - HW * 0.02

# viewer-left arm: relaxed hang with a slight outward bow
sh_l = (BODY_CX - SHOULDER_W * 0.7, shoulder_z)
ctrl_l = (BODY_CX - SHOULDER_W - HW * 0.10, shoulder_z - TORSO_LEN * 0.5)
end_l = (BODY_CX - SHOULDER_W - HW * 0.12, torso_bot_z - HW * 0.02)
arm_l_pts = tube_along(qbez(sh_l, ctrl_l, end_l), ARM_R)
hand_l_c = (end_l[0] - HAND_R * 0.3, end_l[1] - HAND_R * 0.8)

# viewer-right arm: HAND ON HIP (elbow winging clearly out past the pear)
sh_r = (BODY_CX + SHOULDER_W * 0.7, shoulder_z)
ctrl_r = (BODY_CX + SHOULDER_W + HW * 0.26, shoulder_z - TORSO_LEN * 0.40)
end_r = (torso_bot_cx + HIP_W * 0.70, torso_bot_z + HW * 0.09)
arm_r_pts = tube_along(qbez(sh_r, ctrl_r, end_r), ARM_R)
hand_r_c = (end_r[0] + HW * 0.015, end_r[1] - HW * 0.02)

# legs: weight on viewer-right leg (straight), left leg relaxed w/ slight splay
LEG_R = HW * 0.04 * BS
leg_top_z = TORSO_VISIBLE_BOTTOM + HW * 0.06
LEG_VISIBLE_LEN = HW * 0.26 * BS
leg_bot_z = leg_top_z - LEG_VISIBLE_LEN
hip_x = HW * 0.115 * BS
llt_x = torso_bot_cx - hip_x
llb_x = llt_x - HW * 0.035     # splayed
rlt_x = torso_bot_cx + hip_x
rlb_x = rlt_x + HW * 0.005     # near vertical (weight leg)
leg_l_pts = capsule_points(llt_x, leg_top_z, LEG_R, llb_x, leg_bot_z, LEG_R)
leg_r_pts = capsule_points(rlt_x, leg_top_z, LEG_R, rlb_x, leg_bot_z, LEG_R)

# BIG shoes (full size), pointing outward; left toe cocked UP for attitude
SHOE_R_BACK = HW * 0.06
SHOE_R_FRONT = HW * 0.075
SHOE_LEN = HW * 0.15
shoe_z = leg_bot_z - HW * 0.015
foot_l_pts = capsule_points(llb_x + LEG_R, shoe_z, SHOE_R_BACK,
                             llb_x - SHOE_LEN, shoe_z + HW * 0.03, SHOE_R_FRONT)
foot_r_pts = capsule_points(rlb_x - LEG_R, shoe_z, SHOE_R_BACK,
                             rlb_x + SHOE_LEN, shoe_z - HW * 0.01, SHOE_R_FRONT)

# shorts: bottom ~45% of the VISIBLE torso. Built by clipping the torso's own
# silhouette flat at the waist (a capsule's rounded cap would overshoot way
# above the waistline -- same overshoot bug as the v1 legs).
visible_top = head_bottom_edge_z(BODY_CX)
waist_z = TORSO_VISIBLE_BOTTOM + (visible_top - TORSO_VISIBLE_BOTTOM) * 0.45

def clip_top(pts, z_max):
    """Flatten a polygon's top at z_max, dropping duplicate flattened points."""
    out = []
    for x, z in pts:
        p = (x, min(z, z_max))
        if not out or abs(p[0] - out[-1][0]) > 1e-6 or abs(p[1] - out[-1][1]) > 1e-6:
            out.append(p)
    return out

ink = bpy.data.materials.new("Ink")
ink.use_nodes = True
nt = ink.node_tree
nt.nodes.clear()
o = nt.nodes.new("ShaderNodeOutputMaterial")
e = nt.nodes.new("ShaderNodeEmission")
e.inputs[0].default_value = (0.02, 0.02, 0.02, 1)
nt.links.new(e.outputs[0], o.inputs[0])

cream = bpy.data.materials.new("Cream")
cream.use_nodes = True
nt2 = cream.node_tree
nt2.nodes.clear()
o2 = nt2.nodes.new("ShaderNodeOutputMaterial")
e2 = nt2.nodes.new("ShaderNodeEmission")
e2.inputs[0].default_value = (1.0, 1.0, 0.8392, 1)
nt2.links.new(e2.outputs[0], o2.inputs[0])

def outline_pair(name, pts, y_back=0.05, y_front=0.04, scale=1.14):
    """Generic outline: uniform scale from centroid. Fine for round/compact shapes."""
    cx = sum(p[0] for p in pts) / len(pts)
    cz = sum(p[1] for p in pts) / len(pts)
    outer = [(cx + (x - cx) * scale, cz + (z - cz) * scale) for x, z in pts]
    o = polygon_to_mesh(name + "_outline", outer, y=y_back)
    o.data.materials.append(ink)
    f = polygon_to_mesh(name + "_fill", pts, y=y_front)
    f.data.materials.append(cream)
    return o, f

def capsule_outline_pair(name, cx1, cz1, r1, cx2, cz2, r2, margin, y_back=0.05, y_front=0.04):
    """Outline built from the SAME capsule centers with fatter radii -- no
    centroid-scale spike at a tapered tip."""
    fill_pts = capsule_points(cx1, cz1, r1, cx2, cz2, r2)
    outer_pts = capsule_points(cx1, cz1, r1 + margin, cx2, cz2, r2 + margin)
    o = polygon_to_mesh(name + "_outline", outer_pts, y=y_back)
    o.data.materials.append(ink)
    f = polygon_to_mesh(name + "_fill", fill_pts, y=y_front)
    f.data.materials.append(cream)
    return o, f

# ink weight matched to the head's traced stroke (outer ring 1.531 - inner ring
# 1.450 = ~0.08 blender units)
MARGIN = 0.08

def solid_ink(name, pts, y=0.05):
    o = polygon_to_mesh(name, pts, y=y)
    o.data.materials.append(ink)
    return o

# body pieces sit BEHIND the head (larger y = farther from camera at -Y)
capsule_outline_pair("Torso", BODY_CX, torso_top_z, SHOULDER_W, torso_bot_cx, torso_bot_z, HIP_W, MARGIN, y_back=0.09, y_front=0.08)
# limbs + shoes: solid black, same visual language as the face's features
solid_ink("ArmL", arm_l_pts, y=0.095)
solid_ink("ArmR", arm_r_pts, y=0.095)
solid_ink("LegL", leg_l_pts, y=0.095)
solid_ink("LegR", leg_r_pts, y=0.095)
solid_ink("ShoeL", foot_l_pts, y=0.06)
solid_ink("ShoeR", foot_r_pts, y=0.06)

# shorts: solid ink wrapping the pear's lower half (in front of torso, behind hands)
shorts_full = capsule_points(BODY_CX, torso_top_z, SHOULDER_W + MARGIN * 0.75,
                              torso_bot_cx, torso_bot_z, HIP_W + MARGIN * 0.75, n=28)
shorts_pts = clip_top(shorts_full, waist_z)
solid_ink("Shorts", shorts_pts, y=0.075)

def circle_pts(cx, cz, r, n=24):
    return [(cx + r * math.cos(2 * math.pi * i / n), cz + r * math.sin(2 * math.pi * i / n)) for i in range(n)]

# two cream buttons on the shorts front
BTN_R = HW * 0.026
shorts_bottom = torso_bot_z - HIP_W
btn_z = waist_z - (waist_z - shorts_bottom) * 0.32
for side, tag in ((-1, "L"), (1, "R")):
    bx = torso_bot_cx + side * HW * 0.05
    polygon_to_mesh(f"ShortsButton_{tag}", circle_pts(bx, btn_z, BTN_R), y=0.072).data.materials.append(cream)

# gloved hands: cream circle + ink ring, in FRONT of the arm ends and shorts
solid_ink("HandL_outline", circle_pts(hand_l_c[0], hand_l_c[1], HAND_R + MARGIN), y=0.055)
polygon_to_mesh("HandL_fill", circle_pts(hand_l_c[0], hand_l_c[1], HAND_R), y=0.05).data.materials.append(cream)
solid_ink("HandR_outline", circle_pts(hand_r_c[0], hand_r_c[1], HAND_R + MARGIN), y=0.055)
polygon_to_mesh("HandR_fill", circle_pts(hand_r_c[0], hand_r_c[1], HAND_R), y=0.05).data.materials.append(cream)

# glove stitches: two short ink dashes on the back of each glove
STITCH_R = HW * 0.008
STITCH_LEN = HAND_R * 0.55
for hc, tag, direction in ((hand_l_c, "L", -1), (hand_r_c, "R", 1)):
    for i, off in enumerate((-HAND_R * 0.22, HAND_R * 0.22)):
        x0 = hc[0] + off
        z_top = hc[1] + HAND_R * 0.75
        stitch = capsule_points(x0, z_top, STITCH_R, x0 + direction * HAND_R * 0.08, z_top - STITCH_LEN, STITCH_R)
        solid_ink(f"GloveStitch_{tag}{i}", stitch, y=0.045)

# head on top, in front (smaller y = closer to camera), fully intact/untouched
head_outer = polygon_to_mesh("Head_Outline", HEAD_PTS, y=0.03)
head_outer.data.materials.append(ink)
head_inner = polygon_to_mesh("Head_Fill", HEAD_INNER_PTS, y=0.02)
head_inner.data.materials.append(cream)

import json
FEATS = json.loads(open('/private/tmp/claude-501/-Users-joshstokesberry-COMMANDER/40483013-84ce-4f68-84e4-a1c6fbe36c8d/scratchpad/featpts2.txt').read().splitlines()[1])
for fname, fpts in FEATS.items():
    fobj = polygon_to_mesh(fname, fpts, y=0.0)
    fobj.data.materials.append(ink)

# camera framing full figure
top = max(p[1] for p in HEAD_PTS)
bottom = shoe_z - SHOE_R_FRONT - MARGIN
height = top - bottom
bpy.ops.object.camera_add(location=(head_cx, -10, (top + bottom) / 2), rotation=(math.radians(90), 0, 0))
cam = bpy.context.active_object
cam.data.type = 'ORTHO'
cam.data.sensor_fit = 'VERTICAL'
cam.data.ortho_scale = height * 1.15
bpy.context.scene.camera = cam

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 900
scene.render.resolution_y = 1400
scene.view_settings.view_transform = 'Standard'
world = bpy.data.worlds.new("W")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (1.0, 1.0, 0.8392, 1.0)
scene.world = world

scene.render.filepath = "/private/tmp/claude-501/-Users-joshstokesberry-COMMANDER/40483013-84ce-4f68-84e4-a1c6fbe36c8d/scratchpad/full_body_v4.png"
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath="/private/tmp/claude-501/-Users-joshstokesberry-COMMANDER/40483013-84ce-4f68-84e4-a1c6fbe36c8d/scratchpad/full_body_v4.blend")
print("DONE")
