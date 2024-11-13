import gmsh
import numpy as np

import enum 
import os
import sys
import math

def gmsh_generate_domain(d_w, d_h, c_w, c_h, l, l_cnt, s1=1.5):
    BC_L = 1
    BC_W = 2
    BC_A = 3

    names = {
        BC_L: "b 1 D 1",
        BC_W: "b 2 N None",
        BC_A: "b 3 D 0"
    }

    model = gmsh.model()
    model.add("t1")
    s2 = s1 * 10
    ccs = [
        [BC_L, BC_W],
        [BC_W, BC_W],
        # [BC_W, BC_W],
        # [BC_W, BC_W],
        [BC_W, BC_A],
        [BC_A, BC_A]
    ]

    # r_part = np.array([
    #     [c_w/2, 0- c_h],
    #     [c_w/2, 0],
    #     # [c_w/2 + w_w, 0, s1],
    #     # [c_w/2 + w_w, 0, s2],
    #     [d_w/2, 0],
    #     [d_w/2, d_h, s2]
    # ])
    s_ch = s1
    s_d = s1*10
    points_cc = []
    points_cc.append(model.geo.addPoint(c_w/2, -c_h, 0, s_ch)) # rb
    points_cc.append(model.geo.addPoint(c_w/2, 0, 0, s_ch)) # rt
    points_cc.append(model.geo.addPoint(-c_w/2, 0, 0, s_ch)) # lt
    points_cc.append(model.geo.addPoint(-c_w/2, -c_h, 0, s_ch)) # lb

    lines_cc = []
    for i in range(0, len(points_cc)):
        j = i - 1
        if i == 0:
            j = len(points_cc)-1
        lines_cc.append(model.geo.addLine(points_cc[j], points_cc[i]))
    
    
    C_c_hor = int(8)
    for i in [0, 2]:
        model.geo.mesh.setTransfiniteCurve(lines_cc[i] , C_c_hor)# b. t
    for i in [1, 3]:
        model.geo.mesh.setTransfiniteCurve(lines_cc[i] , int(s1*c_h / 1e-3))# l, r
    loop_cc = model.geo.addCurveLoop(lines_cc)
    surface_cc = model.geo.addPlaneSurface([loop_cc])
    model.geo.mesh.setTransfiniteSurface(surface_cc, "Left")

    lines_ed = []
    points_ed = []
    points_ed.append(model.geo.addPoint(d_w/2, 0, 0, s_d)) # rb
    points_ed.append(model.geo.addPoint(d_w/2, d_h, 0, s_d)) # rt
    points_ed.append(model.geo.addPoint(-d_w/2, d_h, 0, s_d)) # lt
    points_ed.append(model.geo.addPoint(-d_w/2, 0, 0, s_d)) # lb
    points_ed_new_lines = [points_cc[1]] + points_ed + [points_cc[2]]
    for i in range(1, len(points_ed_new_lines)):
        lines_ed.append(model.geo.addLine(points_ed_new_lines[i-1], points_ed_new_lines[i]))

    

    # for i in [1, 3]:
    C_low = 4

    model.geo.mesh.setTransfiniteCurve(lines_ed[1] , int(10), "Progression", 1.2 )# l, r
    model.geo.mesh.setTransfiniteCurve(lines_ed[3] , int(10), "Progression", -1.2 )# l, r
    model.geo.mesh.setTransfiniteCurve(lines_ed[0] , int(C_low), "Progression", 1.1 )# l, r
    model.geo.mesh.setTransfiniteCurve(lines_ed[4] , int(C_low), "Progression", -1.1 )# l, r
    model.geo.mesh.setTransfiniteCurve(lines_ed[2] , int(C_low*2 + C_c_hor -2))# l, r


    lines_ed.append(-lines_cc[2])


    

    loop_ed = model.geo.addCurveLoop(lines_ed)
    surface_ed = model.geo.addPlaneSurface([loop_ed])

    model.geo.mesh.setTransfiniteSurface(surface_ed, "Left", points_ed)

    model.geo.mesh.setRecombine(2, surface_cc)
    model.geo.mesh.setRecombine(2, surface_ed)


    ov = model.geo.extrude([(2, surface_cc), (2, surface_ed)], 0, 0, l, [l_cnt], [], recombine=True)

    # ov = model.geo.revolve([(2, surface_cc), (2, surface_ed)], 0.1, 0, 0, 0, 1, 0, math.pi/2, [l_cnt], recombine=True)
    print(ov)
    v1 = ov[1][1]
    v2 = ov[7][1]
    print(v1, v2)
    start = [surface_cc]


    end = [ov[0][1]]

    air = list(map(lambda x: x[1], ov[6:-1]))


    model.addPhysicalGroup(2, start, name="start") # boundary
    model.addPhysicalGroup(2, end, name="end") # boundary
    model.addPhysicalGroup(2, air, name="air") # boundary
    model.addPhysicalGroup(2, [ov[2][1]], name="liquid") # boundary
    model.addPhysicalGroup(2, [ov[3][1],  ov[5][1]], name="wall") # boundary

    # for k, lis in border_conditions.items():
    #     # c = border_conditions[k]
    model.addPhysicalGroup(3, [v1,v2], name="internal") # internal

    # l_part = r_part.copy()[::-1]; l_part[:, 0] *= -1

    # points = np.vstack([r_part, l_part])
    # ccss = ccs + [c[::-1] for c in ccs[::-1]]
    # # print(ccss)

    # # add points
    # for pi, p in enumerate(points):
    #     model.geo.addPoint(p[0], p[1], 0, p[2], pi+1)
    # # l_tags = range()
    # lines = []
    # tag = 1
    # for pi in range(1, len(points)):
    #     model.geo.addLine(pi, pi+1, tag)
    #     lines.append((tag, (pi, pi+1)))
    #     tag += 1
    # model.geo.addLine(len(points), 1, tag)
    # lines.append((tag, (len(points), 1)))
    # tag+=1

    # model.geo.addLine(len(points), 1, tag)
    # lines.append((tag, (len(points), 1)))
    # tag+=1

    # model.geo.addCurveLoop(list(range(1, tag)), 1)
    # model.geo.addPlaneSurface([1], 1)

    # gmsh.model.geo.mesh.setTransfiniteCurve(1, int(2*c_h / 1e-3))
    # gmsh.model.geo.mesh.setTransfiniteCurve(7, int(2*c_h / 1e-3))
    # gmsh.model.geo.mesh.setTransfiniteCurve(8, int(2*c_w / 1e-3))

    model.geo.synchronize()
    

    # # add domains 
    # # for ic in enumerate(border_conditions):
    # border_conditions = {i: [] for i in [BC_L, BC_A, BC_W]}
    # for tag, (p1,p2) in lines:
    #     print(ccss[p1-1], ccss[p2-1])
    #     assert ccss[p1-1][1] == ccss[p2-1][0]
    #     border_conditions[ccss[p2-1][0]].append(tag)
    # print(border_conditions)
    # for k, lis in border_conditions.items():
    #     # c = border_conditions[k]
    #     gmsh.model.addPhysicalGroup(1, lis, k, name=names[k]) # boundary
    # gmsh.model.addPhysicalGroup(2, [1], 1000, name="domain") # domain

    # generate 
    model.mesh.generate(2)
    model.mesh.generate(3)

    return model

    
if __name__ == "__main__":
    gmsh.initialize()

    model = gmsh_generate_domain(d_w=0.02, d_h=0.05, c_w=10e-3,c_h=50e-3, l = 0.2, l_cnt = 100)
    # os.makedirs("workdir", exist_ok=True)
    gmsh.write(f"mesh.msh")
    if "-nopopup" not in sys.argv:
        gmsh.fltk.run()
        while gmsh.fltk.isAvailable() and checkForEvent():
            gmsh.fltk.wait()

    gmsh.finalize()
