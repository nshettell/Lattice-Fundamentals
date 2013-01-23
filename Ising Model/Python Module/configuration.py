def ini_creator(first_frame,final_frame,res,image_type,pov_name):
    if image_type=="jpeg":
        image="J"
    elif image_type=="png":
        image="N"
    else:
        image="B"
        
    return """
;POV-Ray animation ini file
;Visual Representation of an Ising model Square Lattice
;Version 1.3
;Author: Nathan Shettell

Antialias=Off
Antialias_Threshold=0.1
Antialias_Depth=2
Display=Off
+W%d
+H%d

Input_File_Name='%s'
Output_File_Type=%s

Initial_Frame=%d
Final_Frame=%d
Initial_Clock=0
Final_Clock=1

Cyclic_Animation=on
Pause_when_Done=off    
""" %(res[0],res[1],pov_name,image,first_frame,final_frame)