def general_info():
    return """
//Visual Representation of an Ising model Square Lattice
//Version 1.3
//Author: Nathan Shettell

#include "shapes.inc"
#include "textures.inc"
#include "colors.inc"

global_settings { assumed_gamma 1}
background {rgb <1,1,1>}"""
################################################################################
def camera_info(axis,offset,Lx,Ly,Lz):
    if axis=='x':
        if offset=='none':
            loc="<%f,%f,%f>" %(-max(Ly,Lz),0.5*Ly,0.5*Lz)
        elif offset=='small':
            loc="<%f,%f,%f>" %(-max(Ly,Lz),0.8*Ly,0.8*Lz)
        else:
            loc="<%f,%f,%f>" %(-1.5*max(Ly,Lz),1.2*Ly,1.2*Lz)
    elif axis=='y':
        if offset=='none':
            loc="<%f,%f,%f>" %(0.5*Lx,-max(Lx,Lz),0.5*Lz)
        elif offset=='small':
            loc="<%f,%f,%f>" %(0.8*Lx,-max(Lx,Lz),0.8*Lz)
        else:
            loc="<%f,%f,%f>" %(1.2*Lx,-1.5*max(Lx,Lz),1.2*Lz)
    elif axis=='z':
        if offset=='none':
            loc="<%f,%f,%f>" %(0.5*Lx,0.5*Ly,-max(Lx,Ly))
        elif offset=='small':
            loc="<%f,%f,%f>" %(0.8*Lx,0.8*Ly,-max(Lx,Ly))
        else:
            loc="<%f,%f,%f>" %(1.2*Lx,1.2*Ly,-1.6*max(Lx,Ly))
    look="<%f,%f,%f>" %(0.5*Lx,0.5*Ly,0.5*Lz)
    return """
camera {
    location %s
    look_at %s}""" %(loc,look)