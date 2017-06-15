# -*- coding: utf8 -*-

#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2017 Keith Sloan <keith@sloan-home.co.uk>               *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         * 
#*   Acknowledgements :                                                    *
#*                                                                         *
#*                                                                         *
#***************************************************************************
__title__="FreeCAD - GDML importer"
__author__ = "Keith Sloan <keith@sloan-home.co.uk>"
__url__ = ["https://github.com/KeithSloan/FreeCAD_GDML"]

printverbose = False

import FreeCAD, os, sys, re, math
import Part, PartGui

if FreeCAD.GuiUp:
    import FreeCADGui
    gui = True
else:
    if printverbose: print("FreeCAD Gui not present.")
    gui = False


import Part


if open.__module__ == '__builtin__':
    pythonopen = open # to distinguish python built-in open function from the one declared here


#try:
#    _encoding = QtGui.QApplication.UnicodeUTF8
#    def translate(context, text):
#        "convenience function for Qt translator"
#        from PySide import QtGui
#        return QtGui.QApplication.translate(context, text, None, _encoding)
#except AttributeError:
#    def translate(context, text):
#        "convenience function for Qt translator"
#        from PySide import QtGui
#        return QtGui.QApplication.translate(context, text, None)

def open(filename):
    "called when freecad opens a file."
    global doc
    global pathName
    docname = os.path.splitext(os.path.basename(filename))[0]
    doc = FreeCAD.newDocument(docname)
    if filename.lower().endswith('.gdml'):
        processGDML(filename)
    return doc

def insert(filename,docname):
    "called when freecad imports a file"
    global doc
    global pathName
    groupname = os.path.splitext(os.path.basename(filename))[0]
    try:
        doc=FreeCAD.getDocument(docname)
    except NameError:
        doc=FreeCAD.newDocument(docname)
    if filename.lower().endswith('.gdml'):
        processGDML(filename)

def getRef(ptr,name) :
    ref = ptr.get('ref')
    print name + " : " + ref
    return ref

def parsePhysVol(ptr) :
    print "ParsePhyVol"
    for vr in ptr.findall("volumeref") :
        ref = getRef(vr,"volumeref")
        parseVolume(ref) 

def parseVolume(name) :
    print "ParseVolume : "+name
    vol = root.find("structure/volume[@name='%s']" % name )
    print vol.attrib
    solid = vol.find('solidref')
    ref = getRef(solid,'solidref')
    for pv in vol.findall('physvol') : 
        parsePhysVol(pv)
    return


def processGDML(filename):
    global doc
    global root

    FreeCAD.Console.PrintMessage('Import GDML file : '+filename+'\n')
    if printverbose: print ('ImportGDML Version 0.1')

    import xml.etree.ElementTree as ET
    tree = ET.parse(filename)
    root = tree.getroot()
 
    print root.tag
    for setup in root.find('setup'):
        print setup.attrib
        ref = setup.get('ref')
        print ref        
        parseVolume(ref)

    # f = pythonopen(filename, 'r')
    #with pythonopen(filename,'rb') as f:
    #   while True:
    #      line=f.readline()
    #      if not line: break
    #      processLine(line)
    #f.close()
    #p = doc.addObject("Part::Polygon","GPS_Track")   
    #p.Nodes=nodes
    #v = doc.getObject("GPS_Track")
    #print v.ShapeColor
    #v.ShapeColor = (1.0,0,0)
    #doc.recompute()
    if printverbose:
        print('End ImportGDML')
    FreeCAD.Console.PrintMessage('End processing GDML file\n')

#class switch(object):
#    value = None
#    def __new__(class_, value):
#        class_.value = value
#        return True

#def case(*args):
#    return any((arg == switch.value for arg in args))

#def processLine(line):
#    while switch(line[0]):
#        if case('A'):
#           processA(line) 
#           break

