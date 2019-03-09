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
        import GDMLsolids 
        a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","GDMLConeSolid")
        print("GDMLConeSolid Object - added")
        #`Box(a)
        #ViewProviderBox(a.ViewObject)
        #selection=FreeCADGui.Selection.getSelectionEx()
        #for selobj in selection:
        #    newobj=selobj.Document.addObject("Part::FeaturePython",'ConeSolid')
        #    OpenSCADFeatures.RefineShape(newobj,selobj.Object)
        #    OpenSCADFeatures.ViewProviderTree(newobj.ViewObject)
        #    newobj.Label='refine_%s' % selobj.Object.Label
        #    selobj.Object.ViewObject.hide()
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
