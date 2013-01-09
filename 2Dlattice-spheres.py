"""
This script will generate a 2d lattice of spheres with given dimensions to be 
rendered by povray
"""
def sphere_rep(i,j,colour):
    if colour==0:
        return "sphere{<%d,%d,0>, 0.5 texture{pigment{color Red} finish{phong 1}}}\n" %(i,j)
    else:
        return "sphere{<%d,%d,0>, 0.5 texture{pigment{color Blue} finish{phong 1}}}\n" %(i,j)
    
def start(Lx,Ly,filename):
    f=open(filename,'w')
    f.write("""
//2D Square Lattice Simulation with spheres
//Version 1.0
//Nathan Shettell

#include "shapes.inc"
#include "textures.inc"
#include "colors.inc"

global_settings {
    assumed_gamma 1}
    
camera {
    location <"""+str(-0.75*Lx)+","+str(-0.75*Ly)+","+str(min(Lx,Ly))+""">
    look_at <"""+str(Lx/2.)+","+str(Ly/2.)+""",0>}
    
light_source {
    <"""+str(0.75*Lx)+","+str(0.75*Ly)+","+str(max(-Lx,-Ly))+""">
    color White
    parallel
    point_at <"""+str(Lx/2.)+","+str(Ly/2.)+""",0>}
\n""")
    from random import randint
    spheres=[]
    j=0
    while j<Ly:
        spheres+=[(2*i,2*j,randint(0,1)) for i in Range(Lx)]
        j+=1
    """
    Spheres is a list of tuples, where each tuple is of the form (i,j,colour).
    (i,j) is the position of each sphere on the xy plane and the number in the colour position
    determines the random colour associated with the sphere (red or blue).
    """
    
    #Adds the spheres to the image
    for s in spheres:
        f.write(sphere_rep(s[0],s[1],s[2]))
    
    #Adds the cylinders ('bonds') to the image
    i,j=0,0
    while j<Ly:
        i=0
        while i<Lx-1:
            s="cylinder{<%d,%d,0>,<%d,%d,0>,0.2 texture{pigment{color NewTan} finish{phong 1}}}\n" %(2*i,2*j,2*i+2,2*j)
            f.write(s)
            i+=1
        j+=1
    i,j=0,0
    
    while i<Lx:
        j=0
        while j<Ly-1:
            s="cylinder{<%d,%d,0>,<%d,%d,0>,0.2 texture{pigment{color NewTan} finish{phong 1}}}\n" %(2*i,2*j,2*i,2*j+2)
            f.write(s)
            j+=1
        i+=1
    f.close()