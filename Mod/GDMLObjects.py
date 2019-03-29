import FreeCAD, FreeCADGui, Part
from pivy import coin


# Get angle in Radians
def getAngle(aunit,angle) :
   if aunit == 1 :   # 0 radians 1 Degrees
      return(angle*180/math.pi)
   else :
      return angle

class GDMLBox :
   def __init__(self, obj, x, y, z, lunits, material):
      '''Add some custom properties to our Box feature'''
      print "GDMLBox init"
      obj.addProperty("App::PropertyLength","x","GDMLBox","Length x").x=x
      obj.addProperty("App::PropertyLength","y","GDMLBox","Length y").y=y
      obj.addProperty("App::PropertyLength","z","GDMLBox","Length z").z=z
      obj.addProperty("App::PropertyString","lunits","GDMLBox","lunits").lunits=lunits
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
                lunits, material):
      '''Add some custom properties to our Cone feature'''
      obj.addProperty("App::PropertyDistance","rmin1","GDMLCone","Min Radius 1").rmin1=rmin1
      obj.addProperty("App::PropertyDistance","rmax1","GDMLCone","Max Radius 1").rmax1=rmax1
      obj.addProperty("App::PropertyDistance","rmin2","GDMLCone","Min Radius 2").rmin2=rmin2
      obj.addProperty("App::PropertyDistance","rmax2","GDMLCone","Max Radius 2").rmax2=rmax2
      obj.addProperty("App::PropertyLength","z","GDMLCone","Height of Cone").z=z
      obj.addProperty("App::PropertyFloat","startphi","GDMLCone","Start Angle").startphi=startphi
      obj.addProperty("App::PropertyFloat","deltaphi","GDMLCone","Delta Angle").deltaphi=deltaphi
      obj.addProperty("App::PropertyEnumeration","aunit","GDMLCone","aunit")
      obj.aunit=["Rad", "Deg"]
      obj.aunit=0
      obj.addProperty("App::PropertyString","lunits","GDMLCone","lunits").lunits=lunits
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

class GDMLSphere :
   def __init__(self, obj, rmin, rmax, startphi, deltaphi, starttheta, \
                deltatheta, aunit, lunits, material):
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
      obj.aunit=["Rad", "Deg"]
      obj.aunit=0
      obj.addProperty("App::PropertyString","lunits","GDMLSphere", \
                      "lunits").lunits=lunits
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


class GDMLTube :
   def __init__(self, obj, rmin, rmax, z, startphi, deltaphi, aunit,  \
                lunits, material):
      '''Add some custom properties to our Tube feature'''
      obj.addProperty("App::PropertyLength","rmin","GDMLTube","Inside Radius").rmin=rmin
      obj.addProperty("App::PropertyLength","rmax","GDMLTube","Outside Radius").rmax=rmax
      obj.addProperty("App::PropertyLength","z","GDMLTube","Length z").z=z
      obj.addProperty("App::PropertyFloat","startphi","GDMLTube","Start Angle").startphi=startphi
      obj.addProperty("App::PropertyFloat","deltaphi","GDMLTube","Delta Angle").deltaphi=deltaphi
      obj.addProperty("App::PropertyEnumeration","aunit","GDMLTube","aunit")
      obj.aunit=["Rad", "Deg"]
      obj.aunit=0
      obj.addProperty("App::PropertyString","lunits","GDMLTube","lunits").lunits=lunits
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

