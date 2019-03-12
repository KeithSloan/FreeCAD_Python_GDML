import FreeCAD, FreeCADGui, Part
from pivy import coin

class GDMLBox :
   def __init__(self, obj):
      '''Add some custom properties to our Cone feature'''
      obj.addProperty("App::PropertyLength","x","GDMLBox","Length x").x=10.0
      obj.addProperty("App::PropertyLength","y","GDMLBox","Length y").y=10.0
      obj.addProperty("App::PropertyLength","z","GDMLBox","Length z").z=10.0
      obj.addProperty("App::PropertyString","material","GDMLBox","Material").material="SSteal"
      obj.addProperty("Part::PropertyPartShape","Shape","GDMLBox", "Shape of the Box")
      obj.Proxy = self

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
   def __init__(self, obj):
      '''Add some custom properties to our Cone feature'''
      obj.addProperty("App::PropertyDistance","rmin1","GDMLCone","Min Radius 1").rmin1=3.0
      obj.addProperty("App::PropertyDistance","rmax1","GDMLCone","Max Radius 1").rmax1=5.0
      obj.addProperty("App::PropertyDistance","rmin2","GDMLCone","Min Radius 2").rmin2=6.0
      obj.addProperty("App::PropertyDistance","rmax2","GDMLCone","Max Radius 2").rmax2=9.0
      obj.addProperty("App::PropertyLength","z","GDMLCone","Height of Cone").z=10.0
      obj.addProperty("App::PropertyAngle","startphi","GDMLCone","Start Angle").startphi=0
      obj.addProperty("App::PropertyAngle","deltaphi","GDMLCone","Delta Angle").deltaphi=0
      obj.addProperty("App::PropertyStringList","units","GDMLCone","Units").units="rad"
      obj.addProperty("App::PropertyString","material","GDMLCone","Material").material="SSteel"
      obj.addProperty("Part::PropertyPartShape","Shape","GDMLCone", "Shape of the Cone")
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
       cone1 = Part.makeCone(fp.rmax1,fp.rmax2,fp.z)
       cone2 = Part.makeCone(fp.rmin1,fp.rmin2,fp.z)
       cone3 = cone1.cut(cone2)
       fp.Shape = cone3
       FreeCAD.Console.PrintMessage("Recompute GDML Cone Object \n")

class GDMLTube :
   def __init__(self, obj):
      '''Add some custom properties to our Cone feature'''
      obj.addProperty("App::PropertyLength","rmin","GDMLTube","Inside Radius").rmin=5.0
      obj.addProperty("App::PropertyLength","rmax","GDMLTube","Outside Radius").rmax=8.0
      obj.addProperty("App::PropertyLength","z","GDMLTube","Length z").z=10.0
      obj.addProperty("App::PropertyAngle","startphi","GDMLTube","Start Angle").startphi="0.52"
      obj.addProperty("App::PropertyAngle","deltaphi","GDMLTube","Delta Angle").deltaphi="1.57"
      obj.addProperty("App::PropertyString","material","GDMLTube","Material").material="SSteal"
      obj.addProperty("Part::PropertyPartShape","Shape","GDMLTube", "Shape of the Box")
      obj.Proxy = self

   def onChanged(self, fp, prop):
       '''Do something when a property has changed'''
       if not hasattr(fp,'onchange') or not fp.onchange : return
       self.execute(fp)
       FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

   def execute(self, fp):
       '''Do something when doing a recomputation, this method is mandatory'''
       import math
       # Need to add code to check values make a valid cone
       #box = Part.makeBox(fp.x,fp.y,fp.z)
       # Define six vetices for the shape
       x1 = fp.rmax*math.sin(fp.startphi)
       y1 = fp.rmax*math.cos(fp.startphi)
       x2 = fp.rmax*math.sin(fp.startphi+fp.deltaphi)
       y2 = fp.rmax*math.cos(fp.startphi+fp.deltaphi)
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

       # helper mehod to create the faces
   def make_face3(self,v1,v2,v3):
       wire = Part.makePolygon([v1,v2,v3,v1])
       face = Part.Face(wire)
       return face

       # helper mehod to create the faces
   def make_face4(self,v1,v2,v3,v4):
       wire = Part.makePolygon([v1,v2,v3,v4,v1])
       face = Part.Face(wire)
       return face


   def onChanged(self, fp, prop):
       '''Do something when a property has changed'''
       if not hasattr(fp,'onchange') or not fp.onchange : return
       self.execute(fp)
       FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

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

def makeBox():
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","GDMLBox")
    GDMLBox(a)
    ViewProvider(a.ViewObject)

def makeCone():
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","GDMLCone")
    GDMLCone(a)
    ViewProvider(a.ViewObject)

def makeTube():
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","GDMLTube")
    GDMLTube(a)
    ViewProvider(a.ViewObject)

