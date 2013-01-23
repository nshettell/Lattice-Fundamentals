class Sphere_C:
    def __init__(self,spin,pos,trans_factor):
        self.colour='Red' if spin==1 else 'Blue'
        self.trans=trans_factor
        self.i=pos[0]
        self.j=pos[1]
        self.k=pos[2]
    def msg(self):
        return """sphere {<%d,%d,%d>, 0.25
texture{pigment{color %s} finish{phong 1}}
transmit %f}
""" %(self.i,self.j,self.k,self.colour,self.trans)
################################################################################
class Arrow:
    def __init__(self,spin,pos,trans_factor):
        self.rotate='<45,-45,0>' if spin==1 else '<-45,135,0>'
        self.trans=trans_factor
        self.i=pos[0]
        self.j=pos[1]
        self.k=pos[2]
    def msg(self):
        return """union {
cylinder{
    <0,0,0.25>,<0,0,-0.25>,0.17
    texture{pigment{color Green} finish{phong 1}}}
cone{
    <0,0,-0.25>, 0.28
    <0,0,-0.5>, 0
    texture{pigment{color Green} finish{phong 1}}}
rotate %s
transmit %f
translate <%d,%d,%d>}
""" %(self.rotate,self.trans,self.i,self.j,self.k)
################################################################################
class Arrow_C:
    def __init__(self,spin,pos,trans_factor):
        self.rotate='<45,-45,0>' if spin==1 else '<-45,135,0>'
        self.colour='Red' if spin==1 else 'Blue'
        self.trans=trans_factor
        self.i=pos[0]
        self.j=pos[1]
        self.k=pos[2]
    def msg(self):
        return """union {
cylinder{
    <0,0,0.25>,<0,0,-0.25>,0.17
    texture{pigment{color %s} finish{phong 1}}}
cone{
    <0,0,-0.25>, 0.28
    <0,0,-0.5>, 0
    texture{pigment{color %s} finish{phong 1}}}
rotate %s
transmit %f
translate <%d,%d,%d>}
""" %(self.colour,self.colour,self.rotate,self.trans,self.i,self.j,self.k)
################################################################################
################################################################################
def resolutions():
    R=[[128,128],[160,120],[320,200],[320,240],[512,384],[640,480],[800,600],[1024,768],[1280,1024],[1600,1200]]
    print "The possible resolutions are:"
    for r in R:
        print "%dx%d" %(r[0],r[1])
################################################################################
def _ini_creator(res,image,frames,filename):
    if image=="jpeg":
        code="J"
    elif image=="png":
        code="N"
    else:
        code="B"
    return """
;POV-Ray animation ini file
;Visual Representation of an Ising model Square Lattice
;Version 1.2
;Author: Nathan Shettell

Antialias=Off
Antialias_Threshold=0.1
Antialias_Depth=2
Display=Off
+W%d
+H%d

Input_File_Name='%s'
Output_File_Type=%s

Initial_Frame=1
Final_Frame=%d
Initial_Clock=0
Final_Clock=1

Cyclic_Animation=on
Pause_when_Done=off    
""" %(res[0],res[1],filename,code,frames)
################################################################################
def _pov_creator(axis,offset,Lx,Ly,Lz):
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
//Visual Representation of an Ising model Square Lattice
//Version 1.2
//Author: Nathan Shettell

#include "shapes.inc"
#include "textures.inc"
#include "colors.inc"

global_settings { assumed_gamma 1}
    
camera {
    location %s
    look_at %s}

background {rgb <1,1,1>}
""" %(loc,look)
################################################################################
def start(file_info,file_out,res=[640,480]):
    """
    Version 1.2
    This function must intake 2 parameter:
    
    file_info: The name of the file the information is found on.
    All of the following lines should contain information about the spin objects at certain
    positions in the Lattice. After the script has encountered enough spin objects to fill the
    lattice it will assume the rest of the objects belong on following frames.

    file_out: The desired file name used to render the image.
    Should be of the form .ini. All associated files will be created with the same
    name but with varying extensions.
    
    The optional parameter determines the resolution of the images created. The default is 640x480.
    To view the other options please call the function: resolutions().
    It must be entered in the form: [W,H]. Where W and H are integers (image witdth and height)
    when the different resolutions are printed they are in the form WxH.
    If a valid resolution is not entered, the default will be used.
    """
    #Gather information about the lattice size
    while True:
        try:
            Lx=raw_input("Please enter the size of the lattice in the x-direction (a positive integer): ")
            Lx=int(Lx)
            if Lx<=0:
                print "That was not a valid entry, please try again"
            else:
                break
        except ValueError:
            print "That was not a valid entry, please try again"
    
    while True:
        try:
            Ly=raw_input("Please enter the size of the lattice in the y-direction (a positive integer): ")
            Ly=int(Ly)
            if Ly<=0:
                print "That was not a valid entry, please try again"
            else:
                break
        except ValueError:
            print "That was not a valid entry, please try again"
    
    while True:
        try:
            Lz=raw_input("Please enter the size of the lattice in the z-direction (a positive integer): ")
            Lz=int(Lz)
            if Lz<=0:
                print "That was not a valid entry, please try again"
            else:
                break
        except ValueError:
            print "That was not a valid entry, please try again"
            
    #The files which will be accessed during the script
    f_i=open(file_info,'r')
    ini=open(file_out,'w')
    pov=open(file_out[:-4]+'.pov','w')

    Lattice={(i,j,k):[] for i in range(Lx) for j in range(Ly) for k in range(Lz)}
    #Note:
    #Lattice is a dictionary where (i,j) will represent the location of the object on the lattice
    #And the value will represent a list of all spins at that location.
    
    counter=0 #A counter to determine how many frames are needed
    info=filter(lambda i: i!='\n', f_i.readlines())
    info=[i.split() for i in info]
    
    j,k=0,0
    for spins in info:
        if j==Ly:
            j=0
            k+=1
        if k==Lz:
            k=0
            counter+=1
        i=0
        for spin in spins:
            Lattice[(i,j,k)]+=[int(spin)]
            i+=1
        j+=1
    counter+=1 #Doesn't update the last frame

    #After the for-loop has finished running all of the data has been analyzed
    #Hence the information file can be closed:
    f_i.close()

    #Gather more information:
    print """
This program will now gather information on how you would like to view the lattice.
Note: user input is case sensative.

The first option allows the viewer to choose whether they want the camera to look at the center
with an offset angle from 0 degrees. The available options are: none, small, large.

The second option allows the user to choose what axis the camera should be located. The options
are: x, y, z. For example, if it was a 2D lattice, the best option would be the z axis.\

The third option allows the user to choose the file type of the images created. The options
are: jpeg, png, bmp.

The fourth option allows the user to choose the method which the data is represented. The
options are: colours, arrows, arrows+colours.

The fifth option allows the user to choose whether or not some objects appear transparent or not,
if yes then the objects at the front will appear transparent. The options are: yes, no.
"""
    while True:
        offset=raw_input("Please enter the offset value: ")
        if offset!='none' and offset!='small' and offset!='large':
            print "You did not input an available option, please enter: none, small or large."
        else:
            break
    while True:
        cam=raw_input("Please enter the camera-axis value: ")
        if cam!='x' and cam!='y' and cam!='z':
            print "You did not input an available option, please enter: x, y or z."
        else:
            break
    while True:
        image=raw_input("Please enter the desired image type: ")
        if image!='jpeg' and image!='png' and image!='bmp':
            print "You did not input an available option, please enter: jpeg, png or bmp."
        else:
            break
    while True:
        rep=raw_input("Please enter the desired representation type: ")
        if rep!='colours' and rep!='arrows' and rep!='arrows+colours':
            print "You did not input an available option, please enter: colours, arrows or arrows+colours."
        else:
            break
    while True:
        trans=raw_input("Please enter if transparency is wanted: ")
        if trans!='yes' and trans!='no':
            print "You did not input an available option, please enter: yes or no."
        else:
            break
        
    resolutions=[[128,128],[160,120],[320,200],[320,240],[512,384],[640,480],[800,600],[1024,768],[1280,1024],[1600,1200]]
    if res not in resolutions:
        res=[640,480]
    
    ini.write(_ini_creator(res,image,counter,file_out[:-4]+'.pov'))
    ini.close()
    pov.write(_pov_creator(cam,offset,Lx,Ly,Lz))
    
    #Add the sphapes to the image
    frame=1
    while frame<=counter:
        pov.write("#if (frame_number = %d)\n" %(frame))
        for pos in Lattice:
            if trans=="yes" and cam=='x' and Lx>1:
                t_factor=0.5-pos[0]*0.5/Lx
            elif trans=="yes" and cam=='y' and Ly>1:
                t_factor=0.5-pos[1]*0.5/Ly
            elif trans=="yes" and cam=='z' and Lz>1:
                t_factor=0.5-pos[2]*0.5/Lz
            else:
                t_factor=0
            
            if rep=='colours':
                temp=Sphere_C(Lattice[pos][frame-1],(pos[0],pos[1],pos[2]),t_factor)
                pov.write(temp.msg())
            elif rep=='arrows':
                temp=Arrow(Lattice[pos][frame-1],(pos[0],pos[1],pos[2]),t_factor)
                pov.write(temp.msg())
            else:
                temp=Arrow_C(Lattice[pos][frame-1],(pos[0],pos[1],pos[2]),t_factor)
                pov.write(temp.msg())
        pov.write("#end\n")
        frame+=1
        
    #Adds the cylinders ('bonds') to the image
    Bx=[(i,j,k) for i in range(Lx-1) for j in range(Ly) for k in range(Lz)]
    By=[(i,j,k) for i in range(Lx) for j in range(Ly-1) for k in range(Lz)]
    Bz=[(i,j,k) for i in range(Lx) for j in range(Ly) for k in range(Lz-1)]
    for bond in Bx:
        i=bond[0]
        j=bond[1]
        k=bond[2]
        s="cylinder{<%d,%d,%d>,<%d,%d,%d>,0.07 texture{pigment{color NewTan} finish{phong 1}}}\n" %(i,j,k,i+1,j,k)
        pov.write(s)
    for bond in By:
        i=bond[0]
        j=bond[1]
        k=bond[2]
        s="cylinder{<%d,%d,%d>,<%d,%d,%d>,0.07 texture{pigment{color NewTan} finish{phong 1}}}\n" %(i,j,k,i,j+1,k)
        pov.write(s)
    for bond in Bz:
        i=bond[0]
        j=bond[1]
        k=bond[2]
        s="cylinder{<%d,%d,%d>,<%d,%d,%d>,0.07 texture{pigment{color NewTan} finish{phong 1}}}\n" %(i,j,k,i,j,k+1)
        pov.write(s)
    pov.close()