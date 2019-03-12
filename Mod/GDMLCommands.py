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
        from GDMLObjects import GDMLCone, ViewProviderCone
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","GDMLCone")
        print("GDMLCone Object - added")
        GDMLCone(a)
        print("GDMLCone initiated")
        ViewProviderCone(a.ViewObject)
        print("GDMLCone ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()

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


FreeCADGui.addCommand('ConeCommand',ConeFeature())
