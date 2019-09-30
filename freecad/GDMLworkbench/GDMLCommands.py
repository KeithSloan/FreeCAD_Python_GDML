__title__="FreeCAD GDML Workbench - GUI Commands"
__author__ = "Keith Sloan"
__url__ = ["http://www.freecadweb.org"]

'''
This Script includes the GUI Commands of the GDML module
'''

import FreeCAD,FreeCADGui
from PySide import QtCore, QtGui

class BoxFeature:
    #    def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from GDMLObjects import GDMLBox, ViewProvider
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","GDMLBox")
        print("GDMLBox Object - added")
        # obj, x, y, z, lunits, material
        GDMLBox(a,10.0,10.0,10.0,"mm",0)
        print("GDMLBox initiated")
        ViewProvider(a.ViewObject)
        print("GDMLBox ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLBoxFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLBoxFeature',\
                'Box Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLBoxFeature',\
                'Box Object')}

class ConeFeature:
    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from GDMLObjects import GDMLCone, ViewProvider
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","GDMLCone")
        print("GDMLCone Object - added")
        #  obj,rmin1,rmax1,rmin2,rmax2,z,startphi,deltaphi,aunit,lunits,material
        GDMLCone(a,1,3,4,7,10.0,0,2,"rads","mm",0)
        print("GDMLCone initiated")
        ViewProvider(a.ViewObject)
        print("GDMLCone ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLConeFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLConeFeature',\
                'Cone Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLConeFeature',\
                'Cone Object')}

class EllispoidFeature:
    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from GDMLObjects import GDMLEllipsoid, ViewProvider
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython", \
                  "GDMLEllipsoid")
        print("GDMLEllipsoid Object - added")
        #  obj,ax, by, cz, zcut1, zcut2, lunit,material
        GDMLEllipsoid(a,10,20,30,0,0,"mm",0)
        print("GDMLEllipsoid initiated")
        ViewProvider(a.ViewObject)
        print("GDMLEllipsoid ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLEllipsoidFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLEllipsoidFeature',\
                'Ellipsoid Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLEllipsoidFeature',\
                'Ellipsoid Object')}

class ElliTubeFeature:
    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from GDMLObjects import GDMLElTube, ViewProvider
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython", \
                  "GDMLElTube")
        print("GDMLElTube Object - added")
        #  obj,dx, dy, dz, lunit, material
        GDMLElTube(a,10,20,30,"mm",0)
        print("GDMLElTube initiated")
        ViewProvider(a.ViewObject)
        print("GDMLElTube ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLElTubeFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLElTubeFeature',\
                'ElTube Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLElTubeFeature',\
                'ElTube Object')}

class SphereFeature:
    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from GDMLObjects import GDMLSphere, ViewProvider
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","GDMLSphere")
        print("GDMLSphere Object - added")
        # obj, rmin, rmax, startphi, deltaphi, starttheta, deltatheta,
        #       aunit, lunits, material
        GDMLSphere(a,10.0, 20.0, 0.0, 2.02, 0.0, 2.02,"rad","mm",0)
        print("GDMLSphere initiated")
        ViewProvider(a.ViewObject)
        print("GDMLSphere ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLSphereFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLSphereFeature',\
                'Sphere Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLSphereFeature',\
                'Sphere Object')}

class TrapFeature:
    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from GDMLObjects import GDMLTrap, ViewProvider
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","GDMLTrap")
        print("GDMLTrap Object - added")
        # obj z, theta, phi, x1, x2, x3, x4, y1, y2,
        # pAlp2, aunits, lunits, material
        GDMLTrap(a,10.0,0.0,0.0,6.0,6.0,6.0,6.0,7.0,7.0,0.0,"rad","mm",0)
        print("GDMLTrap initiated")
        ViewProvider(a.ViewObject)
        print("GDMLTrap ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLTrapFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLTrapFeature',\
                'Trap Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLTrapFeature',\
                'Trap Object')}


class TubeFeature:
    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from GDMLObjects import GDMLTube, ViewProvider
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","GDMLTube")
        print("GDMLTube Object - added")
        # obj, rmin, rmax, z, startphi, deltaphi, aunit, lunits, material
        GDMLTube(a,5.0,8.0,10.0,0.52,1.57,"rad","mm",0)
        print("GDMLTube initiated")
        ViewProvider(a.ViewObject)
        print("GDMLTube ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLTubeFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLTubeFeature',\
                'Tube Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLTubeFeature',\
                'Tube Object')}

class CycleFeature :

    def Activated(self) :
       
        def toggle(obj) :
            #print ("Toggle "+obj.Label)
            #print (obj.ViewObject.DisplayMode)
            #print (obj.ViewObject.Visibility)
            if obj.ViewObject.Visibility == False :
               obj.ViewObject.DisplayMode = 'Shaded'
               obj.ViewObject.Visibility = True
            else :
               if obj.ViewObject.DisplayMode == 'Shaded' :
                  obj.ViewObject.DisplayMode = 'Wireframe'
               else :
                  obj.ViewObject.Visibility = False 


        def cycle(obj) :
            #print ("Toggle : "+ obj.Label)
            #print (dir(obj))
            #print("TypeId : "+str(obj.TypeId))
            if obj.TypeId == "App::Part" :
               for i in obj.OutList :
                   #print(i)
                   #print(dir(i))
                   #print (i.TypeId)
                   if i.TypeId != "App::Origin" :
                      cycle(i) 
            elif obj.TypeId =="App::Origin" :
                return
            #print obj.isDerivedFrom('App::DocumentObjectGroupPython')
            # Is this a genuine group i.e. Volumes
            # Not Parts with Groups i.e. GDMLPolycone
            elif obj.isDerivedFrom('App::DocumentObjectGroupPython') :
               #print "Toggle Group" 
               for s in obj.Group :
                   #print s
                   cycle(s)

            # Cycle through display options
            elif hasattr(obj,'ViewObject') :
               toggle(obj)

            if hasattr(obj,'Base') and hasattr(obj,'Tool') :
               print ("Boolean") 
               cycle(obj.Base)
               cycle(obj.Tool)
            

        for obj in FreeCADGui.Selection.getSelection():
            #if len(obj.InList) == 0: # allowed only for for top level objects
            cycle(obj)


    def GetResources(self):
        return {'Pixmap'  : 'GDML_Cycle', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDML_CycleGroup',\
                'Cycle Group'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDML_CycleGroup', \
                'Cycle Object and all children display')}    

FreeCADGui.addCommand('CycleCommand',CycleFeature())
FreeCADGui.addCommand('BoxCommand',BoxFeature())
FreeCADGui.addCommand('EllipsoidCommand',EllispoidFeature())
FreeCADGui.addCommand('ElTubeCommand',ElliTubeFeature())
FreeCADGui.addCommand('ConeCommand',ConeFeature())
FreeCADGui.addCommand('SphereCommand',SphereFeature())
FreeCADGui.addCommand('TrapCommand',TrapFeature())
FreeCADGui.addCommand('TubeCommand',TubeFeature())
