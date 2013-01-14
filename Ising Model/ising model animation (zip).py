from zipfile import ZipFile

def start_ising(Lx,Ly,file_zip,file_out):
    """
    This intakes 4 parameter:
    Lx,Ly: The dimensions of the 2D square lattice the data will be represented on.
    file_zip: The name of the main file which contains texts files regarding
    spin configuration for the ising model. This file must be a zip file.
    file_out: The desired file name used to render the image.
    Should be of the form .ini. All associated files will be created with the same
    name but with varying extensions.
    """
    Lattice={(i,j):[] for i in range(Lx) for j in range(Ly)}
    #Note:
    #Lattice is a dictionary where (i,j) will represent the location of the object on the lattice
    #And the value will represent a list of all spins at that location.
    
    fz=ZipFile(file_zip,'r')
    ini=open(file_out,'w')
    
    n=file_out[:-4]
    rm=open(n+'_Readme.txt','w')
    pov=open(n+'.pov','w')
    
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
    counter=0 #A counter to determine how many files there are
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
                    Lattice[(i,j)]+=[1]
                else:
                    Lattice[(i,j)]+=[-1]
                i+=1
            j+=1
    #After the for-loop has finished running all of the data has been analyzed
    #Hence the zip file can be closed:
    fz.close()
    
    #Write helpful message to the readme file:
    rm.write("""
Two main files will help render the animation of the Lattice, one with a .pov
extension and one with a .ini extension. To create and view the animation open the .ini file
and select run, this will create several .bmp files, which is a snapshot of the animation
at every frame.
For a better quality animation with less lag it is recommended to place the .bmp files
in an animation program (ex: windows movie maker (Windows) Final cut pro (Apple)).
Running the .ini file will created a lot of .bmp files so it is recommended to create a new folder or .zip file.
""")
    rm.close()
    ini.write("""
;POV-Ray animation ini file
;Visual Representation of a Ising model 2D Square Lattice
;Version 1.0
;Author: Nathan Shettell

Antialias=Off
Antialias_Threshold=0.1
Antialias_Depth=2

Input_File_Name='"""+file_out[:-4]+""".pov'

Initial_Frame=1
Final_Frame="""+str(counter)+"""
Initial_Clock=0
Final_Clock=1

Cyclic_Animation=on
Pause_when_Done=off    
""")
    ini.close()
    
    pov.write("""
//Visual Representation of a Ising model 2D Square Lattice
//Version 1.0
//Author: Nathan Shettell

//Each sphere in the lattice will have a colour assoicated its spin at a current frame.

#include "shapes.inc"
#include "textures.inc"
#include "colors.inc"

global_settings { assumed_gamma 1}
    
camera {
    location <"""+str(-0.25*Lx)+","+str(-0.25*Ly)+","+str(0.75*min(Lx,Ly))+""">
    look_at <"""+str(Lx/2.)+","+str(Ly/2.)+""",0>}
    
light_source {
    <"""+str(0.25*Lx)+","+str(0.25*Ly)+","+str(0.75*max(-Lx,-Ly))+""">
    color White
    parallel
    point_at <"""+str(Lx/2.)+","+str(Ly/2.)+""",0>}

sky_sphere{ pigment{color rgb<1,1,1>}}
\n""")
    
    #Add the spheres to the image
    frame=1
    while frame<=counter:
        pov.write("#if (frame_number = %d)\n" %(frame))
        for pos in Lattice:
            i=pos[0]
            j=pos[1]
            c=Lattice[pos][frame-1]
            if c==1:
                colour="<1,0,0>"
            else:
                colour="<0,0,1>"
            msg="sphere{<%d,%d,0>, 0.25 texture{pigment{color rgb %s} finish{phong 1}}}\n" %(i,j,colour)
            pov.write(msg)
        pov.write("#end\n")
        frame+=1
        
    #Adds the cylinders ('bonds') to the image
    i,j=0,0
    while j<Ly:
        i=0
        while i<Lx-1:
            s="cylinder{<%d,%d,0>,<%d,%d,0>,0.07 texture{pigment{color NewTan} finish{phong 1}}}\n" %(i,j,i+1,j)
            pov.write(s)
            i+=1
        j+=1
    i,j=0,0  
    while i<Lx:
        j=0
        while j<Ly-1:
            s="cylinder{<%d,%d,0>,<%d,%d,0>,0.07 texture{pigment{color NewTan} finish{phong 1}}}\n" %(i,j,i,j+1)
            pov.write(s)
            j+=1
        i+=1
    pov.close()