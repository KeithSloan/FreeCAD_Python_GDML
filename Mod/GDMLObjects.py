import FreeCAD, FreeCADGui
from pivy import coin

class RefineShapeFeature:
    def IsActive(self):
        return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        import Part,OpenSCADFeatures
        selection=FreeCADGui.Selection.getSelectionEx()
        for selobj in selection:
            newobj=selobj.Document.addObject("Part::FeaturePython",'refine')
            OpenSCADFeatures.RefineShape(newobj,selobj.Object)
            OpenSCADFeatures.ViewProviderTree(newobj.ViewObject)
            newobj.Label='refine_%s' % selobj.Object.Label
            selobj.Object.ViewObject.hide()
        FreeCAD.ActiveDocument.recompute()
    def GetResources(self):
        return {'Pixmap'  : 'OpenSCAD_RefineShapeFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('OpenSCAD_RefineShapeFeature',\
                'Refine Shape Feature'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('OpenSCAD_RefineShapeFeature',\
                'Create Refine Shape Feature')}


class GDMLCone :
   def __init__(self, obj):
      '''Add some custom properties to our Cone feature'''
      obj.addProperty("App::PropertyDistance","rmin1","Cone","Min Radius 1").rmin1=1.0
      obj.addProperty("App::PropertyDistance","rmax1","Cone","Max Radius 1").rmax1=1.0
      obj.addProperty("App::PropertyDistance","rmin2","Cone","Min Radius 2").rmin2=1.0
      obj.addProperty("App::PropertyDistance","rmax2","Cone","Max Radius 2").rmax2=1.0
      obj.addProperty("App::PropertyLength","z","Cone","Height of Cone").z=1.0
      obj.addProperty("App::PropertyAngle","startphi","Cone","Start Angle").startphi=0
      obj.addProperty("App::PropertyAngle","deltaphi","Cone","Delta Angle").deltaphi=0
      obj.addProperty("App::PropertyStringList","units","Cone","Units").units="rad"
      obj.addProperty("Part::PropertyPartShape","Shape","GDMLCone", "Shape of the Cone")
      obj.Proxy = self


   def onChanged(self, fp, prop):
       '''Do something when a property has changed'''
       FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

   def execute(self, fp):
       '''Do something when doing a recomputation, this method is mandatory'''
       #from Part import makeCone
       import Part
       #solid=Part.makeCone(fp.rmax1,fp.rmax2,fp.z)
       cone1 = Part.makeCone(10,20,40)
       cone2 = Part.makeCone(9,19,40)
       cone3 = cone1.cut(cone2)
       fp.Shape = cone3
       FreeCAD.Console.PrintMessage("Recompute GDML Cone Object \n")


class ViewProviderCone:
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

def makeCone():
    #FreeCAD.newDocument()
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","GDMLCone")
    GDMLCone(a)
    ViewProviderCone(a.ViewObject)

#makeCone()    
