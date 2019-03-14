__title__="FreeCAD GDML Workbench - GUI Commands"
__author__ = "Keith Sloan"
__url__ = ["http://www.freecadweb.org"]

'''
This Script includes the GUI Commands of the GDML module
'''

import FreeCAD,FreeCADGui
from PySide import QtCore, QtGui

class ConeFeature:
    def IsActive(self):
        return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from GDMLObjects import GDMLCone, ViewProvider
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","GDMLCone")
        print("GDMLCone Object - added")
        #  obj,rmin1,rmax1,rmin2,rmax2,z,startphi,deltaphi,units,material
        GDMLCone(a,1,3,4,7,10.0,0,2,"rads","SSteal")
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

class BoxFeature:
    def IsActive(self):
        return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from GDMLObjects import GDMLBox, ViewProvider
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","GDMLBox")
        print("GDMLBox Object - added")
        GDMLBox(a)
        print("GDMLBox initiated")
        ViewProvider(a.ViewObject)
        print("GDMLBox ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()

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


class TubeFeature:
    def IsActive(self):
        return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from GDMLObjects import GDMLTube, ViewProvider
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","GDMLTube")
        print("GDMLTube Object - added")
        GDMLTube(a)
        print("GDMLTube initiated")
        ViewProvider(a.ViewObject)
        print("GDMLTube ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()

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


FreeCADGui.addCommand('BoxCommand',BoxFeature())
FreeCADGui.addCommand('ConeCommand',ConeFeature())
FreeCADGui.addCommand('TubeCommand',TubeFeature())
