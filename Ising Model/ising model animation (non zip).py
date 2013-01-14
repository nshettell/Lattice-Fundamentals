def start_ising(file_info,file_out):
    """
    This intakes 2 parameter:
    
    file_info: The name of the file the information is found on. The first two lines
    of the file should contain the size of the lattice and the temperature (in that order).
    All of the following lines should contain information about the spin objects at certain
    positions in the Lattice. After the script has encountered enough spin objects to fill the
    lattice it will assume the rest of the objects belong on following frames.

    file_out: The desired file name used to render the image.
    Should be of the form .ini. All associated files will be created with the same
    name but with varying extensions.
    """
    
    f_i=open(file_info,'r')
    ini=open(file_out,'w')
    
    n=file_out[:-4]
    rm=open(n+'_Readme.txt','w')
    pov=open(n+'.pov','w')
    
    L=int(f_i.readline().split()[0])
    T=float(f_i.readline().split()[0])

    Lattice={(i,j):[] for i in range(L) for j in range(L)}
    #Note:
    #Lattice is a dictionary where (i,j) will represent the location of the object on the lattice
    #And the value will represent a list of all spins at that location.
    
    counter=0 #A counter to determine how many frames are needed
    info=filter(lambda i: i!='\n', f_i.readlines())
    info=[i.split() for i in info]

    j=0
    for spins in info:
        if j==L:
            j=0
            counter+=1
        i=0
        for spin in spins:
            Lattice[(i,j)]+=[int(spin)]
            i+=1
        j+=1
    counter+=1 #Doesn't update the last frame

    #After the for-loop has finished running all of the data has been analyzed
    #Hence the zip file can be closed:
    f_i.close()
    
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
Display=Off

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
//Visual Representation of an Ising model 2D Square Lattice
//Version 1.0
//Author: Nathan Shettell

//Each sphere in the lattice will have a colour assoicated its spin at a current frame.

#include "shapes.inc"
#include "textures.inc"
#include "colors.inc"

global_settings { assumed_gamma 1}
    
camera {
    location <"""+str(0.5*L)+","+str(0.5*L)+","+str(-1.5*L)+""">
    look_at <"""+str(0.5*L)+","+str(0.5*L)+""",0>}

background {rgb<1,1,1>}
text {
    ttf "timrom.ttf"
    "Ising model: T="""+str(T)+""", L="""+str(L)+""""
    0.1,0
    pigment { Black }
    translate """+str(L+1)+"""*y
    }
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
    while j<L:
        i=0
        while i<L-1:
            s="cylinder{<%d,%d,0>,<%d,%d,0>,0.07 texture{pigment{color NewTan} finish{phong 1}}}\n" %(i,j,i+1,j)
            pov.write(s)
            i+=1
        j+=1
    i,j=0,0  
    while i<L:
        j=0
        while j<L-1:
            s="cylinder{<%d,%d,0>,<%d,%d,0>,0.07 texture{pigment{color NewTan} finish{phong 1}}}\n" %(i,j,i,j+1)
            pov.write(s)
            j+=1
        i+=1
    pov.close()