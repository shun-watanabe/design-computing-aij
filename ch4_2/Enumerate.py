# -*- coding: utf-8 -*-

import copy
import math
import bpy

def make_path(c,e):
    c.append(e)

def search(a,e,i,m,comp,c,n):
    if len(e)==n-1:
        b=copy.deepcopy(e)
        make_path(c,b)
    for j in range(i,m):
        a_0=a[j][0]#head
        a_1=a[j][1]#tail
        if comp[a_0]!=comp[a_1]:
            comp2=copy.deepcopy(comp)
            e.append(j)
            t=min(comp[a_0],comp[a_1])
            s=max(comp[a_0],comp[a_1])
            for k in range(len(comp)):
                if comp[k]==s:
                    comp[k]=t
            search(a,e,j+1,m,comp,c,n)
            comp=comp2
            e.pop()

def make_edges(c,a,d,n):
    for i in range(len(c)):
        f=[]
        for j in range(n-1):
            f.append(a[c[i][j]])
        d.append(f)

def make_verts(verts_n,n,k):
    p=k//10+1
    for l in range(9):
        verts_i=copy.deepcopy(verts_n[-1])
        for i in range(n):
            verts_i[i][0]+=15
        verts_n.append(verts_i)
    verts_m=copy.deepcopy(verts_n)
    verts_m_0=copy.deepcopy(verts_m)
    for j in range(p):
        for q in range(10):
            for i in range(n):
                verts_m_0[q][i][1]+=15*(j+1)
        for i in range(10):
            verts_n.append(verts_m_0[i])
        verts_m_0=copy.deepcopy(verts_m)

def Cylinder(o0, o1):

    #Location
    x0 = o0[0]
    y0 = o0[1]
    z0 = o0[2]
    x1 = o1[0]
    y1 = o1[1]
    z1 = o1[2]

    #Center
    xc = x0 + ((x1-x0)/2)
    yc = y0 + ((y1-y0)/2)
    zc = z0 + ((z1-z0)/2)

    xt = x1-xc
    yt = y1-yc
    zt = z1-zc

    r = math.sqrt( (xt*xt) + (yt*yt) + (zt*zt) )
    theta = math.acos( zt/r )
    phi = math.atan2( (yt), (xt) )

    bpy.ops.mesh.primitive_cylinder_add(location = (xc, yc, zc),depth = r*2,radius = 0.2,rotation = (0, theta, phi))

#################################################
# tetrahedron

verts=[[-5,-5,-5],
[-5,5,5],
[5,-5,5],
[5,5,-5]
]

a = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]

#################################################
# cube

# verts=[[0,0,0],
# [10,0,0],
# [10,10,0],
# [0,10,0],
# [0,0,10],
# [10,0,10],
# [10,10,10],
# [0,10,10]]

# a = [(0,1),(1,2),(2,3),(0,3),
# (0,4),(1,5),(2,6),(3,7),
# (4,5),(5,6),(6,7),(4,7)]

#################################################

n=len(verts)
m=len(a)

comp=[i for i in range(n)]

#add_edges
e=[]

#all_spanning_tree
c=[]

d=[]

search(a,e,0,m,comp,c,n)

make_edges(c,a,d,n)

verts_n=[verts]

k=len(c)

make_verts(verts_n,n,k)

for j in range(p):
    e=d[j]
    for i in range(n-1):
        Cylinder(verts_n[j][e[i][0]],verts_n[j][e[i][1]])
