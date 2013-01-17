def resolutions():
    R=[[128,128],[160,120],[320,200],[320,240],[512,384],[640,480],[800,600],[1024,768],[1280,1024],[1600,1200]]
    for r in R:
        print "%dx%d" %(r[0],r[1])

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
;Version 1.1
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

def _pov_creator(axis,offset,shapes,Lx,Ly,Lz):
    if shapes=="colours":
        msg="/*Each sphere in the lattice has a varying colour (red or blue), the colour of the sphere in a certain\n\
        frame represents the current spin of the object (red=1, blue=-1)*/"
    elif shapes=="arrows":
        msg="/*Each arrow in the lattice has a varying direction (towards or away), the direction of the arrow\n\
        in a certain frame represents the current spin of the object (towards=1, away=-1)*/"
    else:
        msg="""/*
Each arrow in the lattice has a varying direction and colour (towards & red or away & blue),
the direction and colour of the arrow in a certain frame represents the current spin of the object
(towards & red=1, away & blue=-1)
*/"""
    if axis=='x':
        if offset=='none':
            loc="<%f,%f,%f>" %(-1.5*Lx,0.5*Ly,0.5*Lz)
        elif offset=='small':
            loc="<%f,%f,%f>" %(-1.5*Lx,0.8*Ly,0.8*Lz)
        else:
            loc="<%f,%f,%f>" %(-1.6*Lx,1.2*Ly,1.2*Lz)
    elif axis=='y':
        if offset=='none':
            loc="<%f,%f,%f>" %(0.5*Lx,-1.5*Ly,0.5*Lz)
        elif offset=='small':
            loc="<%f,%f,%f>" %(0.8*Lx,-1.5*Ly,0.8*Lz)
        else:
            loc="<%f,%f,%f>" %(1.2*Lx,-1.6*Ly,1.2*Lz)
    elif axis=='z':
        if offset=='none':
            loc="<%f,%f,%f>" %(0.5*Lx,0.5*Ly,-1.5*min(Lx,Ly))
        elif offset=='small':
            loc="<%f,%f,%f>" %(0.8*Lx,0.8*Ly,-1.5*Lz)
        else:
            loc="<%f,%f,%f>" %(1.2*Lx,1.2*Ly,-1.6*Lz)
    look="<%f,%f,%f>" %(0.5*Lx,0.5*Ly,0.5*Lz)
    return """
//Visual Representation of an Ising model Square Lattice
//Version 1.1
//Author: Nathan Shettell

%s

#include "shapes.inc"
#include "textures.inc"
#include "colors.inc"

global_settings { assumed_gamma 1}
    
camera {
    location %s
    look_at %s}

background {rgb <1,1,1>}
""" %(msg,loc,look)

def _arrow_declare(axis):
    if axis=='x':
        rot='<0,45,-45>'
        base='<0.3,0,0>'
        top1='<-0.3,0,0>'
        top2='<-0.4,0,0>'
    elif axis=='y':
        rot='<-45,0,45>'
        base='<0,0.3,0>'
        top1='<0,-0.3,0>'
        top2='<0,0.4,0>'
    else:
        rot='<45,-45,0>'
        base='<0,0,0.3>'
        top1='<0,0,-0.3>'
        top2='<0,0,-0.4>'
    return """
#declare shape = union {
cylinder{
    %s,%s,0.2
    texture{pigment{color Green} finish{phong 1}}}
cone{
    %s, 0.28
    %s, 0
    texture{pigment{color Green}
    finish{phong 1}}}
    rotate %s}
""" %(base,top1,top1,top2,rot)

def _shape_creator(spin,transparancy,axis,shapes,i,j,k,Lx,Ly,Lz):
    msg=""
    pos='<%d,%d,%d>' %(i,j,k)
    if shapes=='colours':
        msg+="sphere {\n%s, 0.25\n" %(pos)
    else:
        msg+="object {\nshape\n"
    if shapes!='arrows':
        if spin==1:
            msg+="texture{pigment{color Red} finish{phong 1}}\n"
        else:
            msg+="texture{pigment{color Blue} finish{phong 1}}\n"
    if transparancy=='yes':
        if axis=='x' and Lx>1:
            msg+="transmit %d\n" %(0.5-i*0.5/(Lx-1))
        elif axis=='y' and Ly>1:
            msg+="transmit %d\n" %(0.5-j*0.5/(Ly-1))
        elif axis=='z' and Lz>1:
            msg+="transmit %d\n" %(0.5-ik*0.5/(Lz-1))
    if spin==-1 and shapes!='colours':
        if axis=='x':
            msg+="rotate <0,180,180>\ntranslate %s\n" %(pos)
        elif axis=='y':
            msg+="rotate <180,0,180>\ntranslate %s\n" %(pos)
        else:
            msg+="rotate <180,180,0>\ntranslate %s\n" %(pos)
    if spin==1 and shapes!='colours':
        if axis=='x':
            msg+="translate %s\n" %(pos)
        elif axis=='y':
            msg+="translate %s\n" %(pos)
        else:
            msg+="translate %s\n" %(pos)
    msg+='}\n'            
    return msg

def start_ising(file_info,file_out,res=[640,480]):
    """
    Version 1.1
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
Note user input is case sensative.

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
    pov.write(_pov_creator(cam,offset,rep,Lx,Ly,Lz))
    if rep!='colours':
        pov.write(_arrow_declare(cam))
    
    #Add the sphapes to the image
    frame=1
    while frame<=counter:
        pov.write("#if (frame_number = %d)\n" %(frame))
        for pos in Lattice:
            m=_shape_creator(Lattice[pos][frame-1],trans,cam,rep,pos[0],pos[1],pos[2],Lx,Ly,Lz)
            pov.write(m)
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