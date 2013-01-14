"""
This script will generate a 2d lattice of arrows with given dimensions to be 
rendered by povray
"""
def arrow_rep(i,j,direction,theta,phi):
    rot="<%.5f,%.5f,0>" %(theta,phi)
    trans="<%d,%d,0>" %(i,j)
    if direction==0:
        base="<0,0,1>"
        top="<0,0,1.5>"
    else:
        base="<0,0,-1>"
        top="<0,0,-1.5>"
    return """
cylinder{
    <0,0,-1>,<0,0,1>,0.15
    rotate """+rot+"""
    translate """+trans+"""
    texture{pigment{color Green} finish{phong 1}}}
cone{
    """+base+""", 0.23
    """+top+""", 0
    rotate """+rot+"""
    translate """+trans+"""
    texture{pigment{color Green}
    finish{phong 1}}}\n"""
    
def start(Lx,Ly,filename):
    f=open(filename,'w')
    f.write("""
//2D Square Lattice Simulation with arrows
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
    from random import randint,random
    arrows=[]
    j=0
    while j<Ly:
        arrows+=[(2*i,2*j,randint(0,1),random()*30*randint(-1,1),random()*30*randint(-1,1)) for i in range(Lx)]
        j+=1
    """
    Arrows is a list of tuples where the tuples have the form (i,j,direction,theta,phi) where (i,j) is
    the location of the arrow on the xy plane. Direction is a number randomly generated where 0=up and 1=down
    theta and phi are angles between -30and 30 degrees which correspond to rotations about the x and y axis
    respectively.
    """
    
    #Adds the arrows to the image
    for a in arrows:
        f.write(arrow_rep(a[0],a[1],a[2],a[3],a[4]))
  
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