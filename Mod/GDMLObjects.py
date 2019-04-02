import FreeCAD, FreeCADGui, Part
from pivy import coin


# Get angle in Radians
def getAngle(aunit,angle) :
   if aunit == 1 :   # 0 radians 1 Degrees
      return(angle*180/math.pi)
   else :
      return angle

class GDMLBox :
   def __init__(self, obj, x, y, z, lunit, material):
      '''Add some custom properties to our Box feature'''
      print "GDMLBox init"
      obj.addProperty("App::PropertyLength","x","GDMLBox","Length x").x=x
      obj.addProperty("App::PropertyLength","y","GDMLBox","Length y").y=y
      obj.addProperty("App::PropertyLength","z","GDMLBox","Length z").z=z
      obj.addProperty("App::PropertyString","lunit","GDMLBox","lunit").lunit=lunit
      obj.addProperty("App::PropertyString","material","GDMLBox","Material").material=material
      obj.addProperty("Part::PropertyPartShape","Shape","GDMLBox", "Shape of the Box")
      obj.Proxy = self
      self.Type = 'GDMLBox'

   def onChanged(self, fp, prop):
       '''Do something when a property has changed'''
       if not hasattr(fp,'onchange') or not fp.onchange : return
       self.execute(fp)
       FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

   def execute(self, fp):
       '''Do something when doing a recomputation, this method is mandatory'''
       # Need to add code to check values make a valid cone
       box = Part.makeBox(fp.x,fp.y,fp.z)
       fp.Shape = box
       FreeCAD.Console.PrintMessage("Recompute GDML Box Object \n")

class GDMLCone :
   def __init__(self, obj, rmin1,rmax1,rmin2,rmax2,z,startphi,deltaphi,aunit, \
                lunit, material):
      '''Add some custom properties to our Cone feature'''
      obj.addProperty("App::PropertyDistance","rmin1","GDMLCone","Min Radius 1").rmin1=rmin1
      obj.addProperty("App::PropertyDistance","rmax1","GDMLCone","Max Radius 1").rmax1=rmax1
      obj.addProperty("App::PropertyDistance","rmin2","GDMLCone","Min Radius 2").rmin2=rmin2
      obj.addProperty("App::PropertyDistance","rmax2","GDMLCone","Max Radius 2").rmax2=rmax2
      obj.addProperty("App::PropertyLength","z","GDMLCone","Height of Cone").z=z
      obj.addProperty("App::PropertyFloat","startphi","GDMLCone","Start Angle").startphi=startphi
      obj.addProperty("App::PropertyFloat","deltaphi","GDMLCone","Delta Angle").deltaphi=deltaphi
      obj.addProperty("App::PropertyEnumeration","aunit","GDMLCone","aunit")
      obj.aunit=["rad", "deg"]
      obj.aunit=0
      obj.addProperty("App::PropertyString","lunit","GDMLCone","lunit").lunit=lunit
      obj.addProperty("Part::PropertyPartShape","Shape","GDMLCone", \
                      "Shape of the Cone")
      obj.addProperty("App::PropertyStringList","material","GDMLCone", \
                       "Material").material=material
      self.Type = 'GDMLCone'
      obj.Proxy = self

   def onChanged(self, fp, prop):
       '''Do something when a property has changed'''
       if not hasattr(fp,'onchange') or not fp.onchange : return
       self.execute(fp)
       FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

   def execute(self, fp):
       '''Do something when doing a recomputation, this method is mandatory'''

       # Need to add code to check variables will make a valid cone
       # i.e.max > min etc etc
       #print("execute cone")
       #print fp.rmax1
       #print fp.rmax2
       #print fp.z

       cone1 = Part.makeCone(fp.rmax2,fp.rmax1,fp.z)
       if (fp.rmin1 != 0.0 and fp.rmin2 != 0.0) :
          cone2 = Part.makeCone(fp.rmin2,fp.rmin1,fp.z)
          cone3 = cone1.cut(cone2)
          fp.Shape = cone3
       else :   
          fp.Shape = cone1
       FreeCAD.Console.PrintMessage("Recompute GDML Cone Object \n")

class GDMLEllipsoid :
   def __init__(self, obj, ax, by, cz, zcut1, zcut2, lunit, material) :
      '''Add some custom properties to our Elliptical Tube feature'''
      obj.addProperty("App::PropertyDistance","ax","GDMLEllipsoid", \
                       "x semi axis1").ax=ax
      obj.addProperty("App::PropertyDistance","by","GDMLEllipsoid", \
                       "y semi axis1").by=by
      obj.addProperty("App::PropertyDistance","cz","GDMLEllipsoid", \
                       "z semi axis1").cz=cz
      obj.addProperty("App::PropertyDistance","zcut1","GDMLEllipsoid", \
                       "z semi axis1").zcut1=zcut1
      obj.addProperty("App::PropertyDistance","zcut2","GDMLEllipsoid", \
                       "z semi axis1").zcut2=zcut2
      obj.addProperty("App::PropertyString","lunit","GDMLEllipsoid","lunit"). \
                        lunit=lunit
      obj.addProperty("Part::PropertyPartShape","Shape","GDMLEllipsoid", \
                      "Shape of the Ellipsoid")
      obj.addProperty("App::PropertyStringList","material","GDMLEllipsoid", \
                       "Material").material=material
      obj.addProperty("Part::PropertyPartShape","Shape","GDMLEllipsoid", \
                      "Shape of the Ellipsoid")
      self.Type = 'GDMLEllipsoid'
      obj.Proxy = self

   def onChanged(self, fp, prop):
       '''Do something when a property has changed'''
       if not hasattr(fp,'onchange') or not fp.onchange : return
       self.execute(fp)
       FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

   def execute(self, fp):
       '''Do something when doing a recomputation, this method is mandatory'''
       ellipsoid = Part.makeSphere(100)
       mat = FreeCAD.Matrix()
       mat.unity()
       mat.A11 = fp.ax / 100
       mat.A22 = fp.by / 100
       mat.A33 = fp.cz / 100
       mat.A44 = 100
       #print mat
       newellipsoid = ellipsoid.transformGeometry(mat) 
       fp.Shape = newellipsoid
       FreeCAD.Console.PrintMessage("Recompute GDML Ellipsoid Object \n")

class GDMLElTube :
   def __init__(self, obj, dx, dy, dz, lunit, material) :
      '''Add some custom properties to our Elliptical Tube feature'''
      obj.addProperty("App::PropertyDistance","dx","GDMLElTube", \
                       "x semi axis1").dx=dx
      obj.addProperty("App::PropertyDistance","dy","GDMLElTube", \
                       "y semi axis1").dy=dy
      obj.addProperty("App::PropertyDistance","dz","GDMLElTube", \
                       "z semi axis1").dz=dz
      obj.addProperty("App::PropertyString","lunit","GDMLElTube","lunit"). \
                        lunit=lunit
      obj.addProperty("Part::PropertyPartShape","Shape","GDMLElTube", \
                      "Shape of the Cone")
      obj.addProperty("App::PropertyStringList","material","GDMLElTube", \
                       "Material").material=material
      obj.addProperty("Part::PropertyPartShape","Shape","GDMLElTube", \
                      "Shape of the ElTube")
      self.Type = 'GDMLElTube'
      obj.Proxy = self

   def onChanged(self, fp, prop):
       '''Do something when a property has changed'''
       if not hasattr(fp,'onchange') or not fp.onchange : return
       self.execute(fp)
       FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

   def execute(self, fp):
       '''Do something when doing a recomputation, this method is mandatory'''
       tube = Part.makeCylinder(100,100)
       mat = FreeCAD.Matrix()
       mat.unity()
       mat.A11 = fp.dx / 100
       mat.A22 = fp.dy / 100
       mat.A33 = fp.dz / 100
       mat.A44 = 100
       #print mat
       newtube = tube.transformGeometry(mat) 
       fp.Shape = newtube
       FreeCAD.Console.PrintMessage("Recompute GDML ElTube Object \n")

class GDMLSphere :
   def __init__(self, obj, rmin, rmax, startphi, deltaphi, starttheta, \
                deltatheta, aunit, lunit, material):
      '''Add some custom properties to our Sphere feature'''
      print "GDMLSphere init"
      obj.addProperty("App::PropertyLength","rmin","GDMLSphere", \
              "Inside Radius").rmin=rmin
      obj.addProperty("App::PropertyLength","rmax","GDMLSphere", \
              "Outside Radius").rmax=rmax
      obj.addProperty("App::PropertyFloat","startphi","GDMLSphere", \
              "Start Angle").startphi=startphi
      obj.addProperty("App::PropertyFloat","deltaphi","GDMLSphere", \
             "Delta Angle").deltaphi=deltaphi
      obj.addProperty("App::PropertyFloat","starttheta","GDMLSphere", \
             "Start Theta pos").starttheta=starttheta
      obj.addProperty("App::PropertyFloat","deltatheta","GDMLSphere", \
             "Delta Angle").deltatheta=deltatheta
      obj.addProperty("App::PropertyEnumeration","aunit","GDMLSphere","aunit")
      obj.aunit=["rad", "deg"]
      obj.aunit=0
      obj.addProperty("App::PropertyString","lunit","GDMLSphere", \
                      "lunit").lunit=lunit
      obj.addProperty("App::PropertyString","material","GDMLSphere", \
                       "Material").material=material
      obj.addProperty("Part::PropertyPartShape","Shape","GDMLSphere", \
                      "Shape of the Sphere")
      obj.Proxy = self
      self.Type = 'GDMLSphere'

   def onChanged(self, fp, prop):
       '''Do something when a property has changed'''
       if not hasattr(fp,'onchange') or not fp.onchange : return
       self.execute(fp)
       FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")


   def execute(self, fp):
       '''Do something when doing a recomputation, this method is mandatory'''
       import math
       # Need to add code to check values make a valid sphere
       cp = FreeCAD.Vector(0,0,0)
       axis_dir = FreeCAD.Vector(0,0,1)
       #sphere1 = Part.makeSphere(fp.rmin, cp, axis_dir, fp.startphi, \
       #            fp.startphi+fp.deltaphi, fp.deltatheta)
       #sphere2 = Part.makeSphere(fp.rmax, cp, axis_dir, fp.startphi, \
       #            fp.startphi+fp.deltaphi, fp.deltatheta)
       sphere2 = Part.makeSphere(fp.rmax, cp, axis_dir)
       
       #sphere3 = sphere2.cut(sphere1)
       fp.Shape = sphere2
       FreeCAD.Console.PrintMessage("Recompute GDML Sphere Object \n")

class GDMLTrap :
   def __init__(self, obj, z, theta, phi, x1, x2, x3, x4, y1, y2, alpha, \
                aunit, lunit, material):
      '''Add some custom properties to our Tube feature'''
      obj.addProperty("App::PropertyLength","z","GDMLTrap","z").z=z
      obj.addProperty("App::PropertyFloat","theta","GDMLTrap","theta"). \
                       theta=theta
      obj.addProperty("App::PropertyFloat","phi","GDMLTrap","phi").phi=phi
      obj.addProperty("App::PropertyLength","x1","GDMLTrap", \
                      "Length x at y= -y1 face -z").x1=x1
      obj.addProperty("App::PropertyLength","x2","GDMLTrap", \
                      "Length x at y= +y1 face -z").x2=x2
      obj.addProperty("App::PropertyLength","x3","GDMLTrap", \
                      "Length x at y= -y1 face +z").x3=x3
      obj.addProperty("App::PropertyLength","x4","GDMLTrap", \
                      "Length x at y= +y1 face +z").x4=x4
      obj.addProperty("App::PropertyLength","y1","GDMLTrap", \
                      "Length y at face -z").y1=y1
      obj.addProperty("App::PropertyLength","y2","GDMLTrap", \
                      "Length y at face +z").y2=y2
      obj.addProperty("App::PropertyFloat","alpha","GDMLTrap","alpha"). \
                     alpha=alpha
      obj.addProperty("App::PropertyEnumeration","aunit","GDMLTrap","aunit")
      obj.aunit=["rad", "deg"]
      obj.aunit=0
      obj.addProperty("App::PropertyString","lunit","GDMLTrap","lunit"). \
                       lunit=lunit
      obj.addProperty("App::PropertyString","material","GDMLTrap","Material"). \
                       material=material
      obj.addProperty("Part::PropertyPartShape","Shape","GDMLTrap", \
                      "Shape of the Trap")
      obj.Proxy = self
      self.Type = 'GDMLTrap'

   def onChanged(self, fp, prop):
       '''Do something when a property has changed'''
       if not hasattr(fp,'onchange') or not fp.onchange : return
       self.execute(fp)
       FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
   
   def make_face4(self,v1,v2,v3,v4):
       # helper mehod to create the faces
       wire = Part.makePolygon([v1,v2,v3,v4,v1])
       face = Part.Face(wire)
       return face

   def execute(self, fp):
       '''Do something when doing a recomputation, this method is mandatory'''
       import math
       # Define six vetices for the shape
       alpha = getAngle(fp.aunit,fp.alpha)
       theta = getAngle(fp.aunit,fp.theta)
       phi   = getAngle(fp.aunit,fp.phi)
       dx = fp.y1*math.sin(alpha)
       dy = fp.y1*(1.0 - math.cos(alpha))
       print "Delta adjustments"
       print "dx : "+str(dx)+" dy : "+str(dy)
       y1m = dy - fp.y1
       y1p = dy + fp.y1
       x1m = dx - fp.x1
       x1p = dx + fp.x1
       z    = fp.z
       print "y1m : "+str(y1m)
       print "y1p : "+str(y1p)
       print "z   : "+str(z)
       print "x1  : "+str(fp.x1)
       print "x2  : "+str(fp.x2)

       v1    = FreeCAD.Vector(x1m, y1m, -z)
       v2    = FreeCAD.Vector(x1p, y1m, -z)
       v3    = FreeCAD.Vector(x1p, y1p, -z)
       v4    = FreeCAD.Vector(x1m, y1p, -z)

       # x,y of centre of top surface
       dr = z*math.tan(theta)
       tx = dr*math.cos(phi)
       ty = dr*math.cos(phi)
       print "Coord of top surface centre"
       print "x : "+str(tx)+" y : "+str(ty)
       py2 = ty + fp.y2
       my2 = ty - fp.y2
       px3 = tx + fp.x3
       mx3 = tx - fp.x3
       px4 = tx + fp.x4
       mx4 = tx - fp.x4
       print "px3 : "+str(px3)
       print "py2 : "+str(py2)
       print "my2 : "+str(my2)

       v5 = FreeCAD.Vector(mx3, my2, z)
       v6 = FreeCAD.Vector(px3, my2, z)
       v7 = FreeCAD.Vector(px3, py2, z)
       v8 = FreeCAD.Vector(mx3, py2, z)

       # Make the wires/faces
       f1 = self.make_face4(v1,v2,v3,v4)
       f2 = self.make_face4(v1,v2,v6,v5)
       f3 = self.make_face4(v2,v3,v7,v6)
       f4 = self.make_face4(v3,v4,v8,v7)
       f5 = self.make_face4(v1,v4,v8,v5)
       f6 = self.make_face4(v5,v6,v7,v8)
       shell=Part.makeShell([f1,f2,f3,f4,f5,f6])
       solid=Part.makeSolid(shell)

       #solid = Part.makePolygon([v1,v2,v3,v4,v5,v6,v7,v1])

       fp.Shape = solid
       FreeCAD.Console.PrintMessage("Recompute GDML Trap Object \n")


class GDMLTube :
   def __init__(self, obj, rmin, rmax, z, startphi, deltaphi, aunit,  \
                lunit, material):
      '''Add some custom properties to our Tube feature'''
      obj.addProperty("App::PropertyLength","rmin","GDMLTube","Inside Radius").rmin=rmin
      obj.addProperty("App::PropertyLength","rmax","GDMLTube","Outside Radius").rmax=rmax
      obj.addProperty("App::PropertyLength","z","GDMLTube","Length z").z=z
      obj.addProperty("App::PropertyFloat","startphi","GDMLTube","Start Angle").startphi=startphi
      obj.addProperty("App::PropertyFloat","deltaphi","GDMLTube","Delta Angle").deltaphi=deltaphi
      obj.addProperty("App::PropertyEnumeration","aunit","GDMLTube","aunit")
      obj.aunit=["rad", "deg"]
      obj.aunit=0
      obj.addProperty("App::PropertyString","lunit","GDMLTube","lunit").lunit=lunit
      obj.addProperty("App::PropertyString","material","GDMLTube","Material").material=material
      obj.addProperty("Part::PropertyPartShape","Shape","GDMLTube", "Shape of the Tube")
      obj.Proxy = self
      self.Type = 'GDMLTube'

   def onChanged(self, fp, prop):
       '''Do something when a property has changed'''
       if not hasattr(fp,'onchange') or not fp.onchange : return
       self.execute(fp)
       FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

   def execute(self, fp):
       '''Do something when doing a recomputation, this method is mandatory'''
       import math
       # Need to add code to check values make a valid Tube
       # Define six vetices for the shape
       startphirad = getAngle(fp.aunit,fp.startphi)
       deltaphirad = getAngle(fp.aunit,fp.deltaphi)
       x1 = fp.rmax*math.sin(startphirad)
       y1 = fp.rmax*math.cos(startphirad)
       x2 = fp.rmax*math.sin(startphirad+deltaphirad)
       y2 = fp.rmax*math.cos(startphirad+deltaphirad)
       v1 = FreeCAD.Vector(0,0,0)
       v2 = FreeCAD.Vector(x1,y1,0)
       v3 = FreeCAD.Vector(x2,y2,0)
       v4 = FreeCAD.Vector(0,0,fp.z)
       v5 = FreeCAD.Vector(x1,y1,fp.z)
       v6 = FreeCAD.Vector(x2,y2,fp.z)

       # Make the wires/faces
       f1 = self.make_face3(v1,v2,v3)
       f2 = self.make_face4(v1,v3,v6,v4)
       f3 = self.make_face3(v4,v6,v5)
       f4 = self.make_face4(v5,v2,v1,v4)
       shell=Part.makeShell([f1,f2,f3,f4])
       solid=Part.makeSolid(shell)

       cyl1 = Part.makeCylinder(fp.rmax,fp.z)
       cyl2 = Part.makeCylinder(fp.rmin,fp.z)
       cyl3 = cyl1.cut(cyl2) 

       tube = cyl3.cut(solid)
       fp.Shape = tube
       FreeCAD.Console.PrintMessage("Recompute GDML Tube Object \n")

   def make_face3(self,v1,v2,v3):
       # helper mehod to create the faces
       wire = Part.makePolygon([v1,v2,v3,v1])
       face = Part.Face(wire)
       return face

   def make_face4(self,v1,v2,v3,v4):
       # helper mehod to create the faces
       wire = Part.makePolygon([v1,v2,v3,v4,v1])
       face = Part.Face(wire)
       return face

   def onChanged(self, fp, prop):
       '''Do something when a property has changed'''
       if not hasattr(fp,'onchange') or not fp.onchange : return
       self.execute(fp)
       FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

class GDMLFiles :
   def __init__(self,obj,FilesEntity,sectionDict) :
      '''Add some custom properties to our Cone feature'''
      print "GDML Files"
      print FilesEntity
      obj.addProperty("App::PropertyBool","active","GDMLFiles", \
                    "split option").active=FilesEntity
      obj.addProperty("App::PropertyString","define","GDMLFiles", \
                    "define section").define=sectionDict.get('define',"")
      obj.addProperty("App::PropertyString","materials","GDMLFiles", \
                    "materials section").materials=sectionDict.get('materials',"")
      obj.addProperty("App::PropertyString","solids","GDMLFiles", \
                    "solids section").solids=sectionDict.get('solids',"")
      obj.addProperty("App::PropertyString","structure","GDMLFiles", \
                    "sructure section").structure=sectionDict.get('structure',"")
      obj.Proxy = self

   def execute(self, fp):
      '''Do something when doing a recomputation, this method is mandatory'''

   def onChanged(self, fp, prop):
      '''Do something when a property has changed'''
      if not hasattr(fp,'onchange') or not fp.onchange : return
      self.execute(fp)
      FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

class GDMLmaterial :
   def __init__(self,obj,name) :
      # Add most properties later 
      obj.addProperty("App::PropertyString","name",name).name = name
      obj.Proxy = self
      self.Object = obj

class GDMLfraction :
   def __init__(self,obj,ref,n) :
      obj.addProperty("App::PropertyFloat",'n',ref).n = n 
      obj.Proxy = self
      self.Object = obj

class GDMLcomposite :
   def __init__(self,obj,ref,n) :
      obj.addProperty("App::PropertyInteger",'n',ref).n = n 
      obj.Proxy = self
      self.Object = obj

class GDMLelement :
   def __init__(self,obj,name) :
      obj.addProperty("App::PropertyString","name",name).name = name 
      obj.Proxy = self
      self.Object = obj

class GDMLisotope :
   def __init__(self,obj,name,N,Z,unit,value) :
      obj.addProperty("App::PropertyString","name",name).name = name 
      obj.addProperty("App::PropertyInteger","N",name).N=N
      obj.addProperty("App::PropertyInteger","Z",name).Z=Z
      obj.addProperty("App::PropertyString","unit",name).unit = unit 
      obj.addProperty("App::PropertyFloat","value",name).value = value 
      obj.Proxy = self
      self.Object = obj

# use general ViewProvider if poss
class ViewProvider:
   def __init__(self, obj):
       '''Set this object to the proxy object of the actual view provider'''
       obj.Proxy = self
 
   def updateData(self, fp, prop):
       '''If a property of the handled feature has changed we have the chance to handle this here'''
       # fp is the handled feature, prop is the name of the property that has changed
       #l = fp.getPropertyByName("Length")
       #w = fp.getPropertyByName("Width")
       #h = fp.getPropertyByName("Height")
       #self.scale.scaleFactor.setValue(float(l),float(w),float(h))
       pass
 
   def getDisplayModes(self,obj):
       '''Return a list of display modes.'''
       modes=[]
       modes.append("Shaded")
       modes.append("Wireframe")
       return modes
 
   def getDefaultDisplayMode(self):
       '''Return the name of the default display mode. It must be defined in getDisplayModes.'''
       return "Shaded"
 
   def setDisplayMode(self,mode):
       '''Map the display mode defined in attach with those defined in getDisplayModes.\
               Since they have the same names nothing needs to be done. This method is optional'''
       return mode
 
   def onChanged(self, vp, prop):
       '''Here we can do something when a single property got changed'''
       FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
       #if prop == "Color":
       #    c = vp.getPropertyByName("Color")
#    self.color.rgb.setValue(c[0],c[1],c[2])    

   def getIcon(self):
       '''Return the icon in XPM format which will appear in the tree view. This method is\
               optional and if not defined a default icon is shown.'''
       return """
           /* XPM */
           static const char * ViewProviderBox_xpm[] = {
           "16 16 6 1",
           "   c None",
           ".  c #141010",
           "+  c #615BD2",
           "@  c #C39D55",
           "#  c #000000",
           "$  c #57C355",
           "        ........",
           "   ......++..+..",
           "   .@@@@.++..++.",
           "   .@@@@.++..++.",
           "   .@@  .++++++.",
           "  ..@@  .++..++.",
           "###@@@@ .++..++.",
           "##$.@@$#.++++++.",
           "#$#$.$$$........",
           "#$$#######      ",
           "#$$#$$$$$#      ",
           "#$$#$$$$$#      ",
           "#$$#$$$$$#      ",
           " #$#$$$$$#      ",
           "  ##$$$$$#      ",
           "   #######      "};
           """
   def __getstate__(self):
       '''When saving the document this object gets stored using Python's json module.\
               Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
               to return a tuple of all serializable objects or None.'''
       return None

   def __setstate__(self,state):
       '''When restoring the serialized object from document we have the chance to set some internals here.\
               Since no data were serialized nothing needs to be done here.'''
       return None


#
#   Need to add variables to these functions or delete?
#
def makeBox():
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","GDMLBox")
    GDMLBox(a)
    ViewProvider(a.ViewObject)

def makeCone():
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","GDMLCone")
    GDMLCone(a)
    ViewProvider(a.ViewObject)

def makecSphere():
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","GDMLSphere")
    GDMLSphere(a)
    ViewProvider(a.ViewObject)

def makeTube():
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","GDMLTube")
    GDMLTube(a)
    ViewProvider(a.ViewObject)

