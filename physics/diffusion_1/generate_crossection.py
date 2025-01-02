import gmsh
import numpy as np

import enum 
import os
import sys


def gmsh_generate_domain(d_w, d_h, c_w, c_h, w_w, a, s1=0.25*1e-3):
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
        [BC_W, BC_W],
        [BC_W, BC_W],
        [BC_W, BC_A],
        [BC_A, BC_A]
    ]

    r_part = np.array([
        [c_w/2, c_h- a, s1],
        [c_w/2, c_h, s1],
        [c_w/2 + w_w, c_h, s1],
        [c_w/2 + w_w, 0, s2],
        [d_w/2, 0, s2],
        [d_w/2, d_h, s2]
    ])

    l_part = r_part.copy()[::-1]; l_part[:, 0] *= -1

    points = np.vstack([r_part, l_part])
    ccss = ccs + [c[::-1] for c in ccs[::-1]]
    # print(ccss)

    # add points
    for pi, p in enumerate(points):
        model.geo.addPoint(p[0], p[1], 0, p[2], pi+1)
    # l_tags = range()
    lines = []
    tag = 1
    for pi in range(1, len(points)):
        model.geo.addLine(pi, pi+1, tag)
        lines.append((tag, (pi, pi+1)))
        tag += 1
    model.geo.addLine(len(points), 1, tag)
    lines.append((tag, (len(points), 1)))
    tag+=1

    model.geo.addCurveLoop(list(range(1, tag)), 1)
    model.geo.addPlaneSurface([1], 1)

    model.geo.synchronize()
    

    # add domains 
    # for ic in enumerate(border_conditions):
    border_conditions = {i: [] for i in [BC_L, BC_A, BC_W]}
    for tag, (p1,p2) in lines:
        print(ccss[p1-1], ccss[p2-1])
        assert ccss[p1-1][1] == ccss[p2-1][0]
        border_conditions[ccss[p2-1][0]].append(tag)
    print(border_conditions)
    for k, lis in border_conditions.items():
        # c = border_conditions[k]
        gmsh.model.addPhysicalGroup(1, lis, k, name=names[k]) # boundary
    gmsh.model.addPhysicalGroup(2, [1], 1000, name="domain") # domain

    # generate 
    model.mesh.generate(2)

    return model

    
if __name__ == "__main__":
    gmsh.initialize()

    model = gmsh_generate_domain(d_w=0.2, d_h=0.2, c_h=5e-3, c_w=5e-3, w_w=1e-3, a=3e-3)
    os.makedirs("workdir", exist_ok=True)
    gmsh.write(f"workdir/mesh.msh")

    gmsh.fltk.run()
    gmsh.finalize()
