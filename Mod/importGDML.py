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

from HTMLParser import HTMLParser

##########################
# Globals Dictionarys    #
##########################
#constDict = {}
#filesDict = {}
#currentTag = None
#currentString = ""
#global setup, define, materials, solids, structure
#globals constDict, filesDict, currentString

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

def getVal(ptr,var) :
    # get value for var variable var 
    from math import pi
    #print ptr.attrib
    # is the variable defined in passed attribute
    if var in ptr.attrib :
       # if yes get its value 
       vval = ptr.attrib.get(var)
       #print "vval"
       #print vval
       if vval[0] == '&' :  # Is this refering to an HTML entity constant
          chkval = vval[1:]
       else : 
          chkval = vval
       # check if defined as a constant
       if vval in constDict :
          c = constDict.get(vval)
          #print c
          return(eval(c))
       
       else :
          return(float(eval(chkval)))
    else :
       return (0.0)

def getText(ptr,var,default) :
    if var in ptr :
       return (ptr.attrib.get(var))
    else :
       return default

def processPlacement(base,rot) :
    # rot is rotation or None if default 
    # set angle & axis in case not set by rotation attribute
    axis = FreeCAD.Vector(1,0,0) 
    angle = 0
    if rot != None :
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

def createBox(solid,px,py,pz,rot) :
    from GDMLObjects import GDMLBox, ViewProvider
    print "CreateBox : "
    print solid.attrib
    mycube=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","GDMLBox")
    x = getVal(solid,'x')
    y = getVal(solid,'y')
    z = getVal(solid,'z')
    GDMLBox(mycube,x,y,z,"mm","SSteel")
    ViewProvider(mycube.ViewObject)
    print "Logical Position : "+str(px)+','+str(py)+','+str(pz)
    base = FreeCAD.Vector(px-x/2,py-y/2,pz-z/2)
    mycube.Placement = processPlacement(base,rot)
    print mycube.Placement.Rotation
    #mycube.ViewObject.DisplayMode = 'Wireframe'
    return mycube

def createCylinder(solid) :
    #mycyl = doc.addObject('Part::Cylinder',solid.get('name')+'_')
    mycyl=doc.addObject("Part::FeaturePython","GDMLCyl")
    z = getVal(solid,'z')
    r = getVal(solid,'r')
    aunit = getText(solid,'aunit','rad')
    deltaphi = getVal(solid,'deltaphi')
    if ('aunit' == 'rad') :
       deltaphi = (180 * deltaphi) / math.pi
    GDMLCyl(mycyl,r,z,deltaphi,aunit,"SSteel")   
    return mycyl

def createSphere(solid,px,py,pz,rot) :
    from GDMLObjects import GDMLSphere, ViewProvider
    print "CreateSphere : "
    print solid.attrib
    rmin = getVal(solid,'rmin')
    rmax = getVal(solid,'rmax')
    startphi = getVal(solid,'startphi')
    deltaphi = getVal(solid,'deltaphi')
    aunit = getText(solid,'aunit','rad')
    lunits = getText(solid,'lunits',"mm")
    mysphere=doc.addObject("Part::FeaturePython","GDMLSphere")
    GDMLSphere(mysphere,rmin,rmax,startphi,deltaphi,0,3.00,aunit,lunits,"SSteel")
    print "Position : "+str(px)+','+str(py)+','+str(pz)
    base = FreeCAD.Vector(px,py,pz)
    mysphere.Placement = processPlacement(base,rot)
    print mysphere.Placement.Rotation
    ViewProvider(mysphere.ViewObject)
    return mysphere


def createTube(solid,px,py,pz,rot) :
    from GDMLObjects import GDMLTube, ViewProvider
    print "CreateTube : "
    print solid.attrib
    rmin = getVal(solid,'rmin')
    rmax = getVal(solid,'rmax')
    z = getVal(solid,'z')
    startphi = getVal(solid,'startphi')
    deltaphi = getVal(solid,'deltaphi')
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
    print "Position : "+str(px)+','+str(py)+','+str(pz)
    base = FreeCAD.Vector(px,py,pz)
    mytube.Placement = processPlacement(base,rot)
    print mytube.Placement.Rotation
    ViewProvider(mytube.ViewObject)
    return mytube

def createCone(solid,px,py,pz,rot) :
    print "CreateCone : "
    print solid.attrib

def parseBoolean(solid,objType,px,py,pz,rot) :
    from GDMLObjects import ViewProvider
    print solid.tag
    print solid.attrib
    if solid.tag in ["subtraction","union","intersection"] :
       print "Boolean : "+solid.tag
       name1st = getRef(solid,'first')
       base = solids.find("*[@name='%s']" % name1st )
       print "first : "+name1st
       #parseObject(root,base)
       name2nd = getRef(solid,'second')
       tool = solids.find("*[@name='%s']" % name2nd )
       print "second : "+name2nd
       #parseObject(root,tool)
       mybool = doc.addObject(objType,solid.tag)
       mybool.Base = createSolid(base,0,0,0,None)
       #mybool.Base = createSolid(base,px,py,pz,rot)
       mybool.Tool = createSolid(tool,0,0,0,None)
       #print "Position : "+str(px)+','+str(py)+','+str(pz)
       pos = FreeCAD.Vector(px,py,pz)
       mybool.Placement = processPlacement(pos,rot)
       #print mybool.Placement.Rotation
       #ViewProvider(mybool.ViewObject)
       return mybool

def createSolid(solid,px,py,pz,rot) :
    print solid.tag
    while switch(solid.tag) :
        if case('box'):
           return(createBox(solid,px,py,pz,rot)) 
           break

        if case('sphere'):
           return(createSphere(solid,px,py,pz,rot)) 
           break

        if case('tube'):
           return(createTube(solid,px,py,pz,rot)) 
           break
        #if case('cone'):
        #   createCone(solid,px,py,pz,rot) 
        #   break

        if case('intersection'):
           return(parseBoolean(solid,'Part::Common',px,py,pz,rot)) 
           break

        if case('union'):
           return(parseBoolean(solid,'Part::Fuse',px,py,pz,rot)) 
           break

        if case('subtraction'):
           return(parseBoolean(solid,'Part::Cut',px,py,pz,rot)) 
           break

        print "Solid : "+solid.tag+" Not yet supported"
        break

# get ref e.g name world, solidref, materialref
def getRef(ptr, name) :
    wrk = ptr.find(name)
    ref = wrk.get('ref')
    print "ref : " + ref
    return ref

def getVolSolid(name):
    print "Get Volume Solid"
    vol = structure.find("/volume[@name='%s']" % name )
    sr = vol.find("solidref")
    print sr.attrib
    name = getRef(sr)
    solid = solids.find("*[@name='%s']" % name )
    return solid

def parsePhysVol(physVol,solid,material):
    print "ParsePhyVol"

    posref = getRef(physVol,"positionref")
    if posref is not None :
       pos = define.find("position[@name='%s']" % posref )
       print pos.attrib
    else :
       pos = physvol.find("position")
    px = getVal(pos,'x')
    py = getVal(pos,'y')
    pz = getVal(pos,'z')
    rotref = getRef(physVol,"rotationref")
    if rotref is not None :
       rot = define.find("rotation[@name='%s']" % rotref )
    else :
       rot = physVol.find("rotation")

    volref = getRef(physVol,"volumeref")
    print "Volume ref : "+volref
    parseVolume(volref,px,py,pz,rot)

# ParseVolume name - structure is global
# We get passed position and rotation
def parseVolume(name,px,py,pz,rot) :
    print "ParseVolume : "+name
    vol = structure.find("volume[@name='%s']" % name )
    solidref = getRef(vol,"solidref")
    solid  = solids.find("*[@name='%s']" % solidref )
    print solid.tag
    materialref = getRef(vol,"materialref")
    print "Material : "+materialref
    material = materials.find(materialref)
    createSolid(solid,px,py,pz,rot)
    # Volume may or maynot contain physvol's
    for pv in vol.findall('physvol') : 
        # create solids at pos & rot in physvols
        parsePhysVol(pv,solid,material)

def processConstants():
    print "Process Constants"
    for cdefine in define.findall('constant') :
        #print cdefine.attrib
        name  = cdefine.attrib.get('name')
        #print name
        value = cdefine.attrib.get('value')
        #print value
        constDict[name] = value
    print "Constant Dictionary"    
    print constDict
    return(constDict)

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag
        global currentTag
        currentTag = tag

    def handle_decl(self, decl):    
        # This gets called when the entity is declared
        print "Encountered a declaration ", decl
        words = decl.split()
        wlen  = len(words)
        print words
        if words[3] == "<!ENTITY":
           while switch(wlen):
              if case(7):
                 # const that refers to a file
                 print words[4]
                 print words[6]
                 filesDict[words[4]] = words[6].split('"')[1]
                 break

              if case(6) :
                 # Constant definition - Add to dict 
                 print words[4]
                 print words[5]
                 constDict[words[4]] = words[5]
                 break

              print "Not yet handled : "+str(words[1])
              break

        else :
          print "Not Handled - Not an Entity"
    
    def handle_entityref(self, name):
        # This gets called when the entity is referenced
        print "Entity reference : "+ name
        tag = self.get_starttag_text()
        print "Current Section  : "+ tag
        print self.getpos()
        search = "&"+name
        print "Search : "+search
        print "Include file "
        insertFile = str(filesDict[name])
        print insertFile
        f = pythonopen(insertFile)
        insertString = f.read()
        lsearch = len(search)+1 # trailing ;
        print lsearch
        global currentString
        l = currentString.find(search)
        print "Pos in string    : "+str(l)
        newString = currentString[:l] + insertString + currentString[l+lsearch:]
        currentString = newString

#    def handle_endtag(self, tag):
#        print "Encountered an end tag :", tag

#    def handle_data(self, data):
#        print "Encountered some data  :", data

    def unknown_decl(data):
        print "Encountered unknown data  :", data

def preProcessHTML(filename) :
    # instantiate the parser and fed it some HTML
    f = pythonopen(filename)
    global constDict, filesDict, currentString
    constDict = {}
    filesDict = {}
    currentString = f.read()
    parser = MyHTMLParser()
    parser.feed(currentString)
    g = pythonopen("/tmp/dumpString","w")
    g.write(currentString)
    g.close

def processGDML(filename):

    FreeCAD.Console.PrintMessage('Import GDML file : '+filename+'\n')
    if printverbose: print ('ImportGDML Version 0.1')
    
    global currentString, filesDict

    # PreProcessHTML file - sets currentString & filesDict
    preProcessHTML(filename)
    print "Files dictionary"
    print filesDict
   
    # Add files object so user can change to organise files
    #from GDMLObjects import GDMLFiles, ViewProvider
    #myfiles = doc.addObject("Part::FeaturePython","GDMLFiles")
    #ViewProvider(myfiles.ViewObject)

    #import xml.etree.ElementTree as ET
    #tree = ET.parse(filename)
    #root = tree.getroot()

    global setup, define, materials, solids, structure
   
    from lxml import etree
    root = etree.fromstring(currentString)
    setup     = root.find('setup')
    define    = root.find('define')
    materials = root.find('materials')
    solids    = root.find('solids')
    structure = root.find('structure')

    constDict = processConstants()
    print setup.attrib
    world = getRef(setup,"world")
    parseVolume(world,0,0,0,None)

    doc.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    if printverbose:
        print('End ImportGDML')
    FreeCAD.Console.PrintMessage('End processing GDML file\n')
