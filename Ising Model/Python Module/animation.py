from configuration import ini_creator
from shapes import *
from user_questions import *
from povray import *
import multiprocessing
import os

def start(file_info,directory,res=[640,480]):
    """
    Version 1.3
    This function must intake 2 parameter:
    
    file_info: The name of the file the information is found on.
    All of the following lines should contain information about the spin objects at certain
    positions in the Lattice. After the script has encountered enough spin objects to fill the
    lattice it will assume the rest of the objects belong on following frames.

    directory: The desired name for the directory of all the files to be outputted in.
    All the files in the directory will have a similar name with different extensions.
    name but with varying extensions.
    
    The optional parameter determines the resolution of the images created. The default is 640x480.
    To view the other options please call the function: poss_resolutions().
    It must be entered in the form: [W,H]. Where W and H are integers (image witdth and height)
    when the different resolutions are printed they are in the form WxH.
    If a valid resolution is not entered, the default will be used.
    """
    
    #Gather information about the lattice size
    Lx,Ly,Lz=dimensions_q()
    
    #The files which will be accessed during the script
    f_i=open(file_info,'r')


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

    #Gather more information from the user:
    offset=offset_q()
    cam=cam_q()
    form=format_q()
    image=image_q()
    spinrep=spinrep_q(form)
    trans=transparency_q()
    processors=processors_q(multiprocessing.cpu_count())   
    res=[640,480] if res not in resolutions() else res
    processors=1 if form=='average'else processors
    
    #Create a directory to store all the files as well as a .pov file:
    if os.name=='posix': #Different os systems have different path names
        sc='/'
    else:
        sc='\\'
    D=os.getcwd()+sc+directory
    os.mkdir(D)
    pov=open(D+sc+directory+'.pov','w')
    exe=open(D+sc+'execute','w')
        
    #Create all of the .ini files:
    ratio=counter/processors
    for i in range(1,processors+1):
        first_frame=1+counter*(i-1)/processors
        final_frame=counter*i/processors
        
        tmp=open(D+sc+directory+" - "+str(i)+'.ini','w')
        tmp.write(ini_creator(first_frame,final_frame,res,image,directory+'.pov'))
        exe.write("povray '%s' +I'%s' &\n" %(directory+' - '+str(i)+'.ini',directory+'.pov',))
        tmp.close()
    exe.close()
    
    #Create the .pov file
    #First add greneral and camera info about the camera
    pov.write(general_info())
    pov.write(camera_info(cam,offset,Lx,Ly,Lz))
    
    #Add the sphapes to the image
    if form=='animation':
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
                    
                if spinrep=='colours':
                    temp=Sphere_C(Lattice[pos][frame-1],(pos[0],pos[1],pos[2]),t_factor)
                    pov.write(temp.msg())
                elif spinrep=='arrows':
                    temp=Arrow(Lattice[pos][frame-1],(pos[0],pos[1],pos[2]),t_factor)
                    pov.write(temp.msg())
                else:
                    temp=Arrow_C(Lattice[pos][frame-1],(pos[0],pos[1],pos[2]),t_factor)
                    pov.write(temp.msg())
            pov.write("#end\n")
            frame+=1
    elif form=='average':
        pov.write("#if (frame_number = 1)\n")
        for pos in Lattice:
            if trans=="yes" and cam=='x' and Lx>1:
                t_factor=0.5-pos[0]*0.5/Lx
            elif trans=="yes" and cam=='y' and Ly>1:
                t_factor=0.5-pos[1]*0.5/Ly
            elif trans=="yes" and cam=='z' and Lz>1:
                t_factor=0.5-pos[2]*0.5/Lz
            else:
                t_factor=0
            
            avg=sum(filter(lambda i: i==1, Lattice[pos]))/float(counter)
            
            if spinrep=='colours':
                temp=Sphere_C(avg,(pos[0],pos[1],pos[2]),t_factor)
                pov.write(temp.msg())
            else:
                temp=Arrow_C(avg,(pos[0],pos[1],pos[2]),t_factor)
                pov.write(temp.msg())
        pov.write("#end\n")
        
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