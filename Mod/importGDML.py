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

class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

def checkConstant(vval):
    print vval

def getVal(cdict,ptr,var) :
    # get value for var variable var 
    from math import pi
    print ptr.attrib
    # is the variable defined in passed attribute
    if var in ptr.attrib :
       # if yes get its value 
       vval = ptr.attrib.get(var)
       #print "vval"
       #print vval
       # check if defined as a constant
       if vval in cdict :
          c = cdict.get(vval)
          #print c
          return(eval(c))
       
       else :
          return float(eval(ptr.attrib.get(var)))
    else :
       return (0.0)

def getText(ptr,var,default) :
    if var in ptr :
       return (ptr.attrib.get(var))
    else :
       return default

def processPlacement(base,rot) :
    print "Rotation : "
    print rot.attrib
    if 'y' in rot.attrib :
	axis = FreeCAD.Vector(0,1,0) 
        angle = float(rot.attrib['y'])
    if 'x' in rot.attrib :
	axis = FreeCAD.Vector(1,0,0) 
        angle = float(rot.attrib['x'])
    if 'z' in rot.attrib :
	axis = FreeCAD.Vector(0,0,1) 
        angle = float(rot.attrib['z'])
    print angle 
    place = FreeCAD.Placement(base,axis,angle)
    return place

def createBox(solid,cdict,volref,lx,ly,lz,rot) :
    from GDMLObjects import GDMLBox, ViewProvider
    print "CreateBox : "
    print solid.attrib
    #mycube=doc.addObject('Part::Box',volref.get('ref')+'_'+solid.get('name')+'_')
    mycube=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","GDMLBox")
    x = getVal(cdict,solid,'x')
    y = getVal(cdict,solid,'y')
    z = getVal(cdict,solid,'z')
    GDMLBox(mycube,x,y,z,"mm","SSteel")
    ViewProvider(mycube.ViewObject)
    print "Logical Position : "+str(lx)+','+str(ly)+','+str(lz)
    base = FreeCAD.Vector(lx-x/2,ly-y/2,lz-z/2)
    mycube.Placement = processPlacement(base,rot)
    print mycube.Placement.Rotation
    #mycube.ViewObject.DisplayMode = 'Wireframe'

def createCylinder(solid,cdict,r) :
    #mycyl = doc.addObject('Part::Cylinder',solid.get('name')+'_')
    mycyl=doc.addObject("Part::FeaturePython","GDMLCyl")
    z = getVal(cdict,solid,'z')
    r = getVal(cdict,solid,'r')
    aunit = getText(solid,'aunit','rad')
    deltaphi = getVal(define,solid,'deltaphi')
    if ('aunit' == 'rad') :
       deltaphi = (180 * deltaphi) / math.pi
    GDMLCyl(mycyl,r,z,deltaphi,aunit,"SSteel")   
    return mycyl

def createSphere(solid,cdict,volref,lx,ly,lz,rot) :
    from GDMLObjects import GDMLSphere, ViewProvider
    print "CreateSphere : "
    print solid.attrib
    rmin = getVal(cdict,solid,'rmin')
    rmax = getVal(cdict,solid,'rmax')
    startphi = getVal(cdict,solid,'startphi')
    deltaphi = getVal(cdict,solid,'deltaphi')
    aunit = getText(solid,'aunit','rad')
    lunits = getText(solid,'lunits',"mm")
    mysphere=doc.addObject("Part::FeaturePython","GDMLSphere")
    GDMLSphere(mysphere,rmin,rmax,startphi,deltaphi,0,3.00,aunit,lunits,"SSteel")
    print "Position : "+str(lx)+','+str(ly)+','+str(lz)
    base = FreeCAD.Vector(lx,ly,lz)
    mysphere.Placement = processPlacement(base,rot)
    print mysphere.Placement.Rotation
    ViewProvider(mysphere.ViewObject)


def createTube(solid,cdict,volref,lx,ly,lz,rot) :
    from GDMLObjects import GDMLTube, ViewProvider
    print "CreateTube : "
    print solid.attrib
    rmin = getVal(cdict,solid,'rmin')
    rmax = getVal(cdict,solid,'rmax')
    z = getVal(cdict,solid,'z')
    startphi = getVal(cdict,solid,'startphi')
    deltaphi = getVal(cdict,solid,'deltaphi')
    aunit = getText(solid,'aunit','rad')
    lunits = getText(solid,'lunits',"mm")
    #if ( rmin is None or rmin == 0 ) :
    #   mytube = makeCylinder(solid,rmax)
    #else :
    #   mytube = doc.addObject('Part::Cut','Tube_'+solid.get('name')+'_')
    #   mytube.Base = makeCylinder(solid,rmax)
    #   mytube.Tool = makeCylinder(solid,rmin)
    print "Tube parameters"
    print rmin
    print rmax
    print z
    mytube=doc.addObject("Part::FeaturePython","GDMLTube")
    GDMLTube(mytube,rmin,rmax,z,startphi,deltaphi,aunit,lunits,"SSteel")
    print "Position : "+str(lx)+','+str(ly)+','+str(lz)
    base = FreeCAD.Vector(lx,ly,lz)
    mytube.Placement = processPlacement(base,rot)
    print mytube.Placement.Rotation
    ViewProvider(mytube.ViewObject)

def createCone(solid,cdict,volref,lx,ly,lz,rot) :
    print "CreateCone : "
    print solid.attrib

def createSolid(solid,cdict,volref,lx,ly,lz,rot) :
    while switch(solid.tag):
        if case('box'):
           createBox(solid,cdict,volref,lx,ly,lz,rot) 
           break

        if case('sphere'):
           createSphere(solid,cdict,volref,lx,ly,lz,rot) 
           break

        if case('tube'):
           createTube(solid,cdict,volref,lx,ly,lz,rot) 
           break
        #if case('cone'):
        #   createCone(solid,cdict,volref,lx,ly,lz,rot) 
        #   break
        print "Solid : "+solid.tag+" Not yet supported"
        break


def getRef(ptr) :
    ref = ptr.get('ref')
    print "ref : " + ref
    return ref

def parseObject(root,ptr) :
    print ptr.tag
    print ptr.attrib
    if ptr.tag in ["subtraction","union","intersection"] :
       print "Boolean : "+ptr.tag
       base = ptr.find('first')
       name = getRef(base)
       base = root.find("solids/*[@name='%s']" % name )
       parseObject(root,base)
       tool = ptr.find('second')
       name = getRef(tool)
       tool = root.find("solids/*[@name='%s']" % name )
       parseObject(root,tool)

def getVolSolid(root,name):
    print "Get Volume Solid"
    vol = root.find("structure/volume[@name='%s']" % name )
    sr = vol.find("solidref")
    print sr.attrib
    name = getRef(sr)
    solid = root.find("solids/*[@name='%s']" % name )
    return solid

def parsePhysVol(root,cdict,ptr,lx,ly,lz):
    print "ParsePhyVol"
    pos = ptr.find("positionref")
    if pos is not None :
       name = getRef(pos)
       pos = root.find("define/position[@name='%s']" % name )
       print pos.attrib
    else :
       pos = ptr.find("position")
    lx += getVal(cdict,pos,'x')
    ly += getVal(cdict,pos,'y')
    lz += getVal(cdict,pos,'z')
    rot = ptr.find("rotationref")
    if rot is not None :
       name = getRef(rot)
       rot = root.find("define/rotation[@name='%s']" % name )
    else :
       rot = ptr.find("rotation")
    volref = ptr.find("volumeref")
    name = getRef(volref)
    solid = getVolSolid(root,name)
    if ((pos is not None) and (rot is not None)) :
       createSolid(solid,cdict,volref,lx,ly,lz,rot)
    parseVolume(root,cdict,name,lx,ly,lz)

# ParseVolume 
def parseVolume(root,cdict,name,lx,ly,lz) :
    print "ParseVolume : "+name
    vol = root.find("structure/volume[@name='%s']" % name )
    print vol.attrib
    for pv in vol.findall('physvol') : 
        parsePhysVol(root,cdict,pv,lx,ly,lz)

def processConstants(root):
    print "Process Constants"
    dict = {}
    define = root.find('define')
    for cdefine in root.findall('define/constant') :
        #print cdefine.attrib
        name  = cdefine.attrib.get('name')
        #print name
        value = cdefine.attrib.get('value')
        #print value
        dict[name] = value
    print "Constant Dictionary"    
    print dict
    return(dict)

def processGDML(filename):
    FreeCAD.Console.PrintMessage('Import GDML file : '+filename+'\n')
    if printverbose: print ('ImportGDML Version 0.1')

    import xml.etree.ElementTree as ET
    tree = ET.parse(filename)
    root = tree.getroot()
    cdict = processConstants(root)
    for setup in root.find('setup'):
        print setup.attrib
        ref = getRef(setup)
        parseVolume(root,cdict,ref,0,0,0)

    doc.recompute()
    if printverbose:
        print('End ImportGDML')
    FreeCAD.Console.PrintMessage('End processing GDML file\n')
