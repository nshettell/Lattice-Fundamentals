"""
This script will generate a 2d kagome lattice of arrows connected by ellipsoids
with given dimensions to be rendered by povray.
Th arrows have randomly generated direction.
"""

def ellipsoid_rep(i,j,rot,colour):
    if colour==0:
        c="Red"
    else:
        c="Blue"
    return """
sphere{
    0,1 scale <1,0.25,0.25>
    rotate <0,0,"""+str(rot)+""">
    translate <"""+str(i)+","+str(j)+""",0>     
    texture{pigment{color """+c+"""}
    finish{phong 1}}}\n"""

def arrow_rep(i,j,orientation):
    if orientation==0:
        k1,k2="-0.6","-1"
    else:
        k1,k2="0.6","1"
    return """
cylinder{<"""+str(i)+","+str(j)+",-0.6>,<"+str(i)+","+str(j)+""",0.6>,0.2 texture{pigment{color Green} finish{phong 1}}}
cone{
    <"""+str(i)+","+str(j)+","+k1+""">, 0.3
    <"""+str(i)+","+str(j)+","+k2+""">,0
    texture{pigment{color Green}
    finish{phong 1}}}\n"""
   
def start(Lx,Ly,filename):
    f=open(filename,'w')
    f.write("""
//2D Kagome Lattice Simulation with ellipsoids and arrows
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
    #Genereate ellipsoids
    from random import randint
    from math import floor, ceil, sqrt
    ellipsoids_x=[]
    ellipsoids_rot1=[]
    ellipsoids_rot2=[]
    j=0
    while j<Ly:
        ellipsoids_x+=[(2*i+1,sqrt(3)*j,0,randint(0,1)) for i in range(Lx-1)]
        j+=2
    for e in ellipsoids_x:
        i=e[0]
        j=e[1]
        p=int(j/sqrt(3))
        if p%4==0:
            if i%4==1:            
                ellipsoids_rot1+=[(i-0.5,j+sqrt(3)/2,60,randint(0,1))]
                ellipsoids_rot2+=[(i+0.5,j+sqrt(3)/2,120,randint(0,1))]
            else:
                ellipsoids_rot1+=[(i+0.5,j-sqrt(3)/2,60,randint(0,1))]
                ellipsoids_rot2+=[(i-0.5,j-sqrt(3)/2,120,randint(0,1))]
        else:
            if i%4==1:
                ellipsoids_rot1+=[(i+0.5,j-sqrt(3)/2,60,randint(0,1))]
                ellipsoids_rot2+=[(i-0.5,j-sqrt(3)/2,120,randint(0,1))]
            else:
                ellipsoids_rot1+=[(i-0.5,j+sqrt(3)/2,60,randint(0,1))]
                ellipsoids_rot2+=[(i+0.5,j+sqrt(3)/2,120,randint(0,1))]
    """
    Every list of ellipsoids contains tuples of the form (i,j,theta,colour)
    where (i,j) is the location of the center of the ellipse, theta represents the
    rotation of the ellipsoid along the x axis and colour is the colour given to the ellipse
    on the image (0=red,1=blue).
    """
    #Adds the ellipsoids to the image
    for e in ellipsoids_x+ellipsoids_rot1+ellipsoids_rot2:
        f.write(ellipsoid_rep(e[0],e[1],e[2],e[3]))
 
    #Generate the arrows:
    arrows=[]
    j=-1
    while j<Ly:
        if j%4==3:
            arrows+=[(i,sqrt(3)*j,randint(0,1)) for i in range(3,2*Lx-1,4)]
        elif j%4==1:
            arrows+=[(i,sqrt(3)*j,randint(0,1)) for i in range(1,2*Lx,4)]
        elif j%2==0:
            arrows+=[(i,sqrt(3)*j,randint(0,1)) for i in range(0,2*Lx,2)]
        j+=1

    """
    Every element in the list of ellipsoids contains tuples of the form (i,j,orientation)
    where (i,j) is the location of the arrow on xy-plane (the arrows are parallel to the z-plane)
    center of the ellipse, the orientation is randomly generated where 0 represents down and 1 represents up.
    """
    #Adds the arrows to the image
    for a in arrows:
        f.write(arrow_rep(a[0],a[1],a[2]))
 
    f.close()