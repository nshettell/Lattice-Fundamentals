class Sphere_C:
    def __init__(self,spin,pos,trans_factor):
        self.colour='<%f,0,%f>' %(spin,1-spin)
        self.trans=trans_factor
        self.i=pos[0]
        self.j=pos[1]
        self.k=pos[2]
    def msg(self):
        return """sphere {<%d,%d,%d>, 0.25
texture{pigment{color %s transmit %f} finish{phong 1}}}
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
    <0,0,-0.5>, 0}
texture{pigment{color Green transmit %f} finish{phong 1}}
rotate %s
translate <%d,%d,%d>}
""" %(self.trans,self.rotate,self.i,self.j,self.k)
################################################################################
class Arrow_C:
    def __init__(self,spin,pos,trans_factor):
        self.rotate='<45,-45,0>' if spin==1 else '<-45,135,0>'
        self.colour='<%f,0,%f>' %(spin,1-spin)
        self.trans=trans_factor
        self.i=pos[0]
        self.j=pos[1]
        self.k=pos[2]
    def msg(self):
        return """union {
cylinder{
    <0,0,0.25>,<0,0,-0.25>,0.17}
cone{
    <0,0,-0.25>, 0.28
    <0,0,-0.5>, 0}
texture{pigment{color %s transmit %f} finish{phong 1}}
rotate %s
translate <%d,%d,%d>}
""" %(self.colour,self.trans,self.rotate,self.i,self.j,self.k)