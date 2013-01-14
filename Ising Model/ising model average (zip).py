from zipfile import ZipFile

def start_ising(Lx,Ly,file_zip,file_out):
    """
    This intakes 4 parameter:
    Lx,Ly: The dimensions of the 2D square lattice the data will be represented on.
    file_zip: The name of the main file which contains texts files regarding
    spin configuration for the ising model. This file must be a zip file.
    file_out: the desired file name used to render the image. Should be of the form .pov
    """
    Lattice={(i,j):0 for i in range(Lx) for j in range(Ly)}
    #Note:
    #Lattice is a dictionary where (i,j) will represent the location of the onject on the lattice
    #And the value will eventually represent the average spin (currently 0).
    
    fz=ZipFile(file_zip,'r')
    fo=open(file_out,'w')
    
    def sorter(a,b):
        if len(b)>len(a):
            return -1
        elif b>a:
            return -1
        elif a==b:
            return 0
        else:
            return 1
    
    L=sorted([info.filename for info in fz.infolist()], cmp=lambda a,b: sorter(a,b))
    counter=0 #keeps track of how many files there are (to take the average later)
    for n in L:
        if n[-4:]!=".txt":
            continue #Skips if this is not a .txt file
        counter+=1
        temp=fz.open(n,'r')
        info=temp.readlines()
        temp.close()
        j=0
        for line in info:
            i=0
            line=line.split()
            for data in line:
                if data=="1":
                    Lattice[(i,j)]+=1
                i+=1
            j+=1
    #After the for-loop has finished running all of the data has been analyzed
    #Hence the zip file can be closed:
    fz.close()
    
    #The data must be averaged. 
    for pos in Lattice.keys():
        Lattice[pos]/=float(counter)
    fo.write("""
//Visual Representation of a Ising model 2D Square Lattice
//Version 1.0
//Author: Nathan Shettell

/*
Each sphere in the lattice will have a colour assoicated to the average spin,
the colour given to each spin will be some combination of blue and red.
The more frequently a particle has a spin of 1, the more red the sphere will appear.
Similarly, the more frequently a particle has of -1, the more blue the sphere will appear.
*/

#include "shapes.inc"
#include "textures.inc"
#include "colors.inc"

global_settings {
    assumed_gamma 1}
    
camera {
    location <"""+str(-0.25*Lx)+","+str(-0.25*Ly)+","+str(0.75*min(Lx,Ly))+""">
    look_at <"""+str(Lx/2.)+","+str(Ly/2.)+""",0>}
    
light_source {
    <"""+str(0.25*Lx)+","+str(0.25*Ly)+","+str(0.75*max(-Lx,-Ly))+""">
    color White
    parallel
    point_at <"""+str(Lx/2.)+","+str(Ly/2.)+""",0>}
\n""")
    
    #Add the spheres to the image
    for pos in Lattice.keys():
        i=pos[0]
        j=pos[1]
        s=Lattice[pos]
        colour="<%f,0,%f>" %(s,1-s)
        msg="sphere{<%d,%d,0>, 0.25 texture{pigment{color rgb %s} finish{phong 1}}}\n" %(i,j,colour)
        fo.write(msg)
        
    #Adds the cylinders ('bonds') to the image
    i,j=0,0
    while j<Ly:
        i=0
        while i<Lx-1:
            s="cylinder{<%d,%d,0>,<%d,%d,0>,0.07 texture{pigment{color NewTan} finish{phong 1}}}\n" %(i,j,i+1,j)
            fo.write(s)
            i+=1
        j+=1
    i,j=0,0  
    while i<Lx:
        j=0
        while j<Ly-1:
            s="cylinder{<%d,%d,0>,<%d,%d,0>,0.07 texture{pigment{color NewTan} finish{phong 1}}}\n" %(i,j,i,j+1)
            fo.write(s)
            j+=1
        i+=1
    fo.close()