# -*- coding: utf8 -*-
#**************************************************************************
#*                                                                        *
#*   Copyright (c) 2017 Keith Sloan <keith@sloan-home.co.uk>              *
#*                                                                        *
#*   This program is free software; you can redistribute it and/or modify *
#*   it under the terms of the GNU Lesser General Public License (LGPL)   *
#*   as published by the Free Software Foundation; either version 2 of    *
#*   the License, or (at your option) any later version.                  *
#*   for detail see the LICENCE text file.                                *
#*                                                                        *
#*   This program is distributed in the hope that it will be useful,      *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of       *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
#*   GNU Library General Public License for more details.                 *
#*                                                                        *
#*   You should have received a copy of the GNU Library General Public    *
#*   License along with this program; if not, write to the Free Software  *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 *
#*   USA                                                                  *
#*                                                                        *
#*   Acknowledgements :                                                   *
#*                                                                        *
#*                                                                        *
#**************************************************************************
__title__="FreeCAD - GDML importer"
__author__ = "Keith Sloan <keith@sloan-home.co.uk>"
__url__ = ["https://github.com/KeithSloan/FreeCAD_GDML"]

printverbose = False

import FreeCAD 
import os, io, sys, re, math
import Part, PartGui

##########################
# Globals Dictionarys    #
##########################
#global setup, define, materials, solids, structure
#globals constDict, filesDict 

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
    docname = os.path.splitext(os.path.basename(filename))[0]
    doc = FreeCAD.newDocument(docname)
    if filename.lower().endswith('.gdml'):
        processGDML(filename)
    return doc

def insert(filename,docname):
    "called when freecad imports a file"
    global doc
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
    print (vval)

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

# get ref e.g name world, solidref, materialref
def getRef(ptr, name) :
    wrk = ptr.find(name)
    if wrk != None :
       ref = wrk.get('ref')
       print (name + ' : ' + ref)
       return ref
    return wrk

def processPlacement(base,rot) :
    # Different Objects will have adjusted base GDML-FreeCAD
    # rot is rotation or None if default 
    # set angle & axis in case not set by rotation attribute
    axis = FreeCAD.Vector(1,0,0) 
    angle = 0
    if rot != None :
        print ("Rotation : ")
        print (rot.attrib)
        if 'y' in rot.attrib :
            axis = FreeCAD.Vector(0,1,0) 
            angle = float(rot.attrib['y'])
        if 'x' in rot.attrib :
       	    axis = FreeCAD.Vector(1,0,0) 
            angle = float(rot.attrib['x'])
        if 'z' in rot.attrib :
            axis = FreeCAD.Vector(0,0,1) 
            angle = float(rot.attrib['z'])
    print (angle) 
    place = FreeCAD.Placement(base,axis,angle)
    return place

# Return a FreeCAD placement for positionref & rotateref
def getPlacementFromRefs(ptr) :
    print ("getPlacementFromRef")
    pos = define.find("position[@name='%s']" % getRef(ptr,'positionref'))
    print (pos)
    rot = define.find("rotation[@name='%s']" % getRef(ptr,'rotationref'))
    base = FreeCAD.Vector(0.0,0.0,0.0)
    if pos != None :    
       print (pos.attrib)
       x = getVal(pos,'x')
       print (x)
       y = getVal(pos,'y')
       z = getVal(pos,'z')
       base = FreeCAD.Vector(x,y,z)
    return(processPlacement(base,rot))   

def setDisplayMode(obj,mode):
    print ("setDisplayMode")
    if mode == 2 :
       obj.ViewObject.DisplayMode = 'Hide'

    if mode == 3 :
       obj.ViewObject.DisplayMode = 'Wireframe'

def createBox(volObj,solid,material,px,py,pz,rot,displayMode) :
    from GDMLObjects import GDMLBox, ViewProvider
    print ("CreateBox : ")
    print (solid.attrib)
    #mycube=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","GDMLBox")
    mycube=volObj.newObject("Part::FeaturePython","GDMLBox")
    x = getVal(solid,'x')
    y = getVal(solid,'y')
    z = getVal(solid,'z')
    lunit = getText(solid,'lunit',"mm")
    GDMLBox(mycube,x,y,z,lunit,material)
    ViewProvider(mycube.ViewObject)
    print ("Logical Position : "+str(px)+','+str(py)+','+str(pz))
    base = FreeCAD.Vector(px-x/2,py-y/2,pz-z/2)
    mycube.Placement = processPlacement(base,rot)
    print (mycube.Placement.Rotation)
    setDisplayMode(mycube,displayMode)
    return mycube

def createCone(volObj,solid,material,px,py,pz,rot,displayMode) :
    from GDMLObjects import GDMLCone, ViewProvider
    print ("CreateCone : ")
    print (solid.attrib)
    rmin1 = getVal(solid,'rmin1')
    rmax1 = getVal(solid,'rmax1')
    rmin2 = getVal(solid,'rmin2')
    rmax2 = getVal(solid,'rmax2')
    z = getVal(solid,'z')
    startphi = getVal(solid,'startphi')
    deltaphi = getVal(solid,'deltaphi')
    aunit = getText(solid,'aunit','rad')
    lunit = getText(solid,'lunit',"mm")
    mycone=volObj.newObject("Part::FeaturePython","GDMLCone")
    GDMLCone(mycone,rmin1,rmax1,rmin2,rmax2,z, \
             startphi,deltaphi,aunit,lunit,material)
    print ("CreateCone : ")
    print ("Position : "+str(px)+','+str(py)+','+str(pz))
    base = FreeCAD.Vector(px,py,pz-z/2)
    mycone.Placement = processPlacement(base,rot)
    print (mycone.Placement.Rotation)
    setDisplayMode(mycone,displayMode)
    ViewProvider(mycone.ViewObject)
    return(mycone)

def createElcone(volObj,solid,material,px,py,pz,rot,displayMode) :
    from GDMLObjects import GDMLElCone, ViewProvider
    print ("CreateElCone : ")
    dx = getVal(solid,'dx')
    dy = getVal(solid,'dy')
    zmax = getVal(solid,'zmax')
    zcut = getVal(solid,'zcut')
    lunit = getText(solid,'lunit',"mm")
    myelcone=volObj.newObject("Part::FeaturePython","GDMLElCone")
    GDMLElCone(myelcone,dx,dy,zmax,zcut,lunit,material)
    print ("CreateElCone : ")
    print ("Position : "+str(px)+','+str(py)+','+str(pz))
    base = FreeCAD.Vector(px,py,pz-zmax/2)
    myelcone.Placement = processPlacement(base,rot)
    print (myelcone.Placement.Rotation)
    setDisplayMode(myelcone,displayMode)
    ViewProvider(myelcone.ViewObject)
    return(myelcone)

def createEllipsoid(volObj,solid,material,px,py,pz,rot,displayMode) :
    from GDMLObjects import GDMLEllipsoid, ViewProvider
    print ("CreateElTube : ")
    print (solid.attrib)
    ax = getVal(solid,'ax')
    by = getVal(solid,'by')
    cz = getVal(solid,'cz')
    zcut1 = getVal(solid,'zcut1')
    zcut2 = getVal(solid,'zcut2')
    lunit = getText(solid,'lunit',"mm")
    myelli=volObj.newObject("Part::FeaturePython","GDMLEllipsoid")
    # cuts 0 for now
    GDMLEllipsoid(myelli,ax, by, cz,zcut1,zcut2,lunit,material)
    print ("CreateEllipsoid : ")
    print ("Position : "+str(px)+','+str(py)+','+str(pz))
    base = FreeCAD.Vector(px,py,pz)
    #base = FreeCAD.Vector(px,py,pz-z/2)
    myelli.Placement = processPlacement(base,rot)
    print (myelli.Placement.Rotation)
    setDisplayMode(myelli,displayMode)
    ViewProvider(myelli.ViewObject)
    return myelli

def createEltube(volObj,solid,material,px,py,pz,rot,displayMode) :
    from GDMLObjects import GDMLElTube, ViewProvider
    print ("CreateElTube : ")
    print (solid.attrib)
    dx = getVal(solid,'dx')
    dy = getVal(solid,'dy')
    dz = getVal(solid,'dz')
    lunit = getText(solid,'lunit',"mm")
    myeltube=volObj.newObject("Part::FeaturePython","GDMLElTube")
    GDMLElTube(myeltube,dx, dy, dz,lunit,material)
    print ("CreateElTube : ")
    print ("Position : "+str(px)+','+str(py)+','+str(pz))
    base = FreeCAD.Vector(px,py,pz)
    #base = FreeCAD.Vector(px,py,pz-z/2)
    myeltube.Placement = processPlacement(base,rot)
    print (myeltube.Placement.Rotation)
    setDisplayMode(myeltube,displayMode)
    ViewProvider(myeltube.ViewObject)
    return myeltube

def createPolycone(volObj,solid,material,px,py,pz,rot,displayMode) :
    from GDMLObjects import GDMLPolycone, GDMLzplane, \
            ViewProvider, ViewProviderExtension
    print ("Create Polycone : ")
    print (solid.attrib)
    startphi = getVal(solid,'startphi')
    deltaphi = getVal(solid,'deltaphi')
    aunit = getText(solid,'aunit','rad')
    lunit = getText(solid,'lunit',"mm")
    mypolycone=volObj.newObject("Part::FeaturePython","GDMLPolycone")
    mypolycone.addExtension("App::OriginGroupExtensionPython", None)
    GDMLPolycone(mypolycone,startphi,deltaphi,aunit,lunit,material)
    ViewProviderExtension(mypolycone.ViewObject)

    #mypolycone.ViewObject.DisplayMode = "Shaded"
    print (solid.findall('zplane'))
    for zplane in solid.findall('zplane') : 
        print (zplane)
        rmin = getVal(zplane,'rmin')
        rmax = getVal(zplane,'rmax')
        z = getVal(zplane,'z')
        myzplane=FreeCAD.ActiveDocument.addObject('App::FeaturePython','zplane') 
        mypolycone.addObject(myzplane)
        #myzplane=mypolycone.newObject('App::FeaturePython','zplane') 
        GDMLzplane(myzplane,rmin,rmax,z)
        ViewProvider(myzplane)

    print ("Position : "+str(px)+','+str(py)+','+str(pz))
    base = FreeCAD.Vector(px,py,pz)
    mypolycone.Placement = processPlacement(base,rot)
    print (mypolycone.Placement.Rotation)
    setDisplayMode(mypolycone,displayMode)
    return mypolycone

def createSphere(volObj,solid,material,px,py,pz,rot,displayMode) :
    from GDMLObjects import GDMLSphere, ViewProvider
    print ("CreateSphere : ")
    print (solid.attrib)
    rmin = getVal(solid,'rmin')
    rmax = getVal(solid,'rmax')
    startphi = getVal(solid,'startphi')
    deltaphi = getVal(solid,'deltaphi')
    aunit = getText(solid,'aunit','rad')
    lunit = getText(solid,'lunit',"mm")
    mysphere=volObj.newObject("Part::FeaturePython","GDMLSphere")
    GDMLSphere(mysphere,rmin,rmax,startphi,deltaphi,0,3.00,aunit, \
               lunit,material)
    print ("Position : "+str(px)+','+str(py)+','+str(pz))
    base = FreeCAD.Vector(px,py,pz)
    mysphere.Placement = prcessPlacement(base,rot)
    print (mysphere.Placement.Rotation)
    ViewProvider(mysphere.ViewObject)
    setDisplayMode(mysphere,displayMode)
    return mysphere

def createTrap(volObj,solid,material,px,py,pz,rot,displayMode) :
    from GDMLObjects import GDMLTrap, ViewProvider
    print ("CreateTrap : ")
    print (solid.attrib)
    z  = getVal(solid,'z')
    x1 = getVal(solid,'x1')
    x2 = getVal(solid,'x2')
    x3 = getVal(solid,'x3')
    x4 = getVal(solid,'x4')
    y1 = getVal(solid,'y1')
    y2 = getVal(solid,'y2')
    theta = getVal(solid,'theta')
    phi = getVal(solid,'phi')
    alpha = getVal(solid,'alpah1')
    aunit = getText(solid,'aunit','rad')
    lunit = getText(solid,'lunit',"mm")
    #print z
    mytrap=volObj.newObject("Part::FeaturePython","GDMLTrap")
    GDMLTrap(mytrap,z,theta,phi,x1,x2,x3,x4,y1,y2,alpha,aunit,lunit,material)
    print ("Position : "+str(px)+','+str(py)+','+str(pz))
    base = FreeCAD.Vector(px,py,pz)
    mytrap.Placement = processPlacement(base,rot)
    print (mytrap.Placement.Rotation)
    setDisplayMode(mytrap,displayMode)
    ViewProvider(mytrap.ViewObject)
    return mytrap

def createTrd(volObj,solid,material,px,py,pz,rot,displayMode) :
    from GDMLObjects import GDMLTrd, ViewProvider
    print ("CreateTrd : ")
    print (solid.attrib)
    z  = getVal(solid,'z')
    x1 = getVal(solid,'x1')
    x2 = getVal(solid,'x2')
    y1 = getVal(solid,'y1')
    y2 = getVal(solid,'y2')
    lunit = getText(solid,'lunit',"mm")
    #print z
    mytrd=volObj.newObject("Part::FeaturePython","GDMLTrd")
    GDMLTrd(mytrd,z,x1,x2,y1,y2,lunit,material)
    print ("Position : "+str(px)+','+str(py)+','+str(pz))
    base = FreeCAD.Vector(px,py,pz)
    mytrd.Placement = processPlacement(base,rot)
    print (mytrd.Placement.Rotation)
    ViewProvider(mytrd.ViewObject)
    setDisplayMode(mytrd,displayMode)
    return mytrd

def createTube(volObj,solid,material,px,py,pz,rot,displayMode) :
    from GDMLObjects import GDMLTube, ViewProvider
    print ("CreateTube : ")
    print (solid.attrib)
    rmin = getVal(solid,'rmin')
    rmax = getVal(solid,'rmax')
    z = getVal(solid,'z')
    startphi = getVal(solid,'startphi')
    deltaphi = getVal(solid,'deltaphi')
    aunit = getText(solid,'aunit','rad')
    lunit = getText(solid,'lunit',"mm")
    print (rmin)
    print (rmax)
    print (z)
    mytube=volObj.newObject("Part::FeaturePython","GDMLTube")
    GDMLTube(mytube,rmin,rmax,z,startphi,deltaphi,aunit,lunit,material)
    print ("Position : "+str(px)+','+str(py)+','+str(pz))
    base = FreeCAD.Vector(px,py,pz)
    mytube.Placement = processPlacement(base,rot)
    print (mytube.Placement.Rotation)
    ViewProvider(mytube.ViewObject)
    setDisplayMode(mytube,displayMode)
    return mytube

def parseBoolean(volObj,solid,objType,material,px,py,pz,rot,displayMode) :
    from GDMLObjects import ViewProvider
    print (solid.tag)
    print (solid.attrib)
    if solid.tag in ["subtraction","union","intersection"] :
       print ("Boolean : "+solid.tag)
       name1st = getRef(solid,'first')
       base = solids.find("*[@name='%s']" % name1st )
       print ("first : "+name1st)
       #parseObject(root,base)
       name2nd = getRef(solid,'second')
       tool = solids.find("*[@name='%s']" % name2nd )
       print ("second : "+name2nd)
       #parseObject(root,tool)
       mybool = volObj.newObject(objType,solid.tag)
       mybool.Base = createSolid(volObj,base,material,0,0,0,None,displayMode)
       #mybool.Base = createSolid(base,px,py,pz,rot)
       # second solid is placed at position and rotation relative to first
       mybool.Tool = createSolid(volObj,tool,material,0,0,0,None,displayMode)
       mybool.Tool.Placement= getPlacementFromRefs(solid) 
       # Okay deal with position of boolean
       print ("Position : "+str(px)+','+str(py)+','+str(pz))
       base = FreeCAD.Vector(px,py,pz)
       mybool.Placement = processPlacement(base,rot)
       #ViewProvider(mybool.ViewObject)
       return mybool

def createSolid(volObj,solid,material,px,py,pz,rot,displayMode) :
    print (solid.tag)
    while switch(solid.tag) :
        if case('box'):
           return(createBox(volObj,solid,material,px,py,pz,rot,displayMode)) 
           break

        if case('cone'):
           return(createCone(volObj,solid,material,px,py,pz,rot,displayMode)) 
           break

        if case('elcone'):
           return(createElcone(volObj,solid,material,px,py,pz,rot,displayMode)) 
           break

        if case('ellipsoid'):
           return(createEllipsoid(volObj,solid,material,px,py,pz,rot,displayMode)) 
           break

        if case('eltube'):
           return(createEltube(volObj,solid,material,px,py,pz,rot,displayMode)) 
           break

        if case('polycone'):
           return(createPolycone(volObj,solid,material,px,py,pz,rot,displayMode)) 
           break

        if case('sphere'):
           return(createSphere(volObj,solid,material,px,py,pz,rot,displayMode)) 
           break

        if case('trap'):
           return(createTrap(volObj,solid,material,px,py,pz,rot,displayMode)) 
           break

        if case('trap_dimensions'):
           return(createTrap(volObj,solid,material,px,py,pz,rot,displayMode)) 
           break

        if case('trd'):
           return(createTrd(volObj,solid,material,px,py,pz,rot,displayMode)) 
           break

        if case('tube'):
           return(createTube(volObj,solid,material,px,py,pz,rot,displayMode)) 
           break

        if case('intersection'):
            return(parseBoolean(volObj,solid,'Part::Common', \
                  material,px,py,pz,rot,displayMode)) 
            break

        if case('union'):
            return(parseBoolean(volObj,solid,'Part::Fuse', \
                  material,px,py,pz,rot,displayMode)) 
            break

        if case('subtraction'):
            return(parseBoolean(volObj,solid,'Part::Cut', \
                  material,px,py,pz,rot,displayMode)) 
            break

        print ("Solid : "+solid.tag+" Not yet supported")
        break

def getVolSolid(name):
    print ("Get Volume Solid")
    vol = structure.find("/volume[@name='%s']" % name )
    sr = vol.find("solidref")
    print (sr.attrib)
    name = getRef(sr)
    solid = solids.find("*[@name='%s']" % name )
    return solid

def parsePhysVol(volGrp,physVol,solid,material,displayMode):
    print ("ParsePhyVol")

    posref = getRef(physVol,"positionref")
    if posref is not None :
       pos = define.find("position[@name='%s']" % posref )
       print (pos.attrib)
    else :
       pos = physVol.find("position")
    if posref is not None :
       px = getVal(pos,'x')
       py = getVal(pos,'y')
       pz = getVal(pos,'z')
    else :
       px = py = pz = 0 
    rotref = getRef(physVol,"rotationref")
    if rotref is not None :
       rot = define.find("rotation[@name='%s']" % rotref )
    else :
       rot = physVol.find("rotation")

    volref = getRef(physVol,"volumeref")
    print ("Volume ref : "+volref)
    parseVolume(volGrp,volref,px,py,pz,rot,displayMode)

# ParseVolume name - structure is global
# We get passed position and rotation
# displayMode 1 normal 2 hide 3 wireframe
def parseVolume(parent,name,px,py,pz,rot,displayMode) :
    print ("ParseVolume : "+name)
    volgrp = parent.newObject("App::DocumentObjectGroupPython",name)
    vol = structure.find("volume[@name='%s']" % name )
    solidref = getRef(vol,"solidref")
    solid  = solids.find("*[@name='%s']" % solidref )
    print (solid.tag)
    # Material is the materialref value
    material = getRef(vol,"materialref")
    createSolid(volgrp,solid,material,px,py,pz,rot,displayMode)
    # Volume may or maynot contain physvol's
    displayMode = 1
    for pv in vol.findall('physvol') : 
        # create solids at pos & rot in physvols
        parsePhysVol(volgrp,pv,solid,material,displayMode)

def processConstants():
    global constDict
    constDict = {}
    print ("Process Constants")
    for cdefine in define.findall('constant') :
        #print cdefine.attrib
        name  = cdefine.attrib.get('name')
        #print name
        value = cdefine.attrib.get('value')
        #print value
        constDict[name] = value
    print ("Constant Dictionary")    
    print (constDict)
    return(constDict)

def getItem(element, attribute) :
    item = element.get(attribute)
    if item != None :
       return item
    else :
       return ""

def processMaterials() :
    from GDMLObjects import GDMLmaterial, GDMLfraction, \
                            GDMLcomposite, ViewProvider
    materialGrp = doc.addObject("App::DocumentObjectGroupPython","Materials")
    materialGrp.Label = "Materials"
    for material in materials.findall('material') :
        name = material.get('name')
        materialObj = materialGrp.newObject("App::DocumentObjectGroupPython", \
                      name)
        GDMLmaterial(materialObj,name)
        formula = material.get('formula')
        if formula != None :
           materialObj.addProperty("App::PropertyString",'formula', \
                      name).formula = formula
        D = material.find('D')
        if D != None :
           Dvalue = float(D.get('value'))
           Dunit = getItem(D,'unit')
        Z = material.get('Z')
        if Z != None :  
           materialObj.addProperty("App::PropertyString",'Z',name).Z = Z
        atom = material.find('atom')
        if atom != None :
           aVal = float(atom.get('value'))
           materialObj.addProperty("App::PropertyFloat",'atom',name).atom = aVal
        T = material.find('T')
        if T != None :
           Tunit = T.get('unit')
           Tvalue = float(T.get('value'))
           materialObj.addProperty("App::PropertyString",'Tunit',name).Tunit = Tunit
           materialObj.addProperty("App::PropertyFloat",'Tvalue',name).Tvalue = Tvalue
        MEE = material.find('MEE')
        if MEE != None :
           Munit = MEE.get('unit')
           Mvalue = float(MEE.get('value'))
           materialObj.addProperty("App::PropertyString",'MEEunit',name).MEEunit = Munit
           materialObj.addProperty("App::PropertyFloat",'MEEvalue',name).MEEvalue = Mvalue
        for fraction in material.findall('fraction') :
            n = float(fraction.get('n'))
            ref = fraction.get('ref')
            fractionObj = materialObj.newObject("App::DocumentObjectGroupPython", \
                                                 ref)
            GDMLfraction(fractionObj,ref,n)
            #fractionObj.Label = ref[0:5] +' : '+'{0:0.2f}'.format(n)
            fractionObj.Label = ref +' : '+'{0:0.2f}'.format(n)

        for composite in material.findall('composite') :
            n = int(composite.get('n'))
            ref = composite.get('ref')
            compositeObj = materialObj.newObject("App::DocumentObjectGroupPython", \
                                                 ref)
            GDMLcomposite(compositeObj,ref,n)
            compositeObj.Label = ref +' : '+str(n)

             
def processIsotopes() :
    from GDMLObjects import GDMLisotope, ViewProvider
    isotopesGrp  = doc.addObject("App::DocumentObjectGroupPython","Isotopes")
    for isotope in materials.findall('isotope') :
        N = int(isotope.get('N'))
        Z = int(float(isotope.get('Z')))    # annotated.gdml file has Z=8.0 
        name = isotope.get('name')
        atom = isotope.find('atom')
        #unit = atom.get('unit')
        value = float(atom.get('value'))
        #isoObj = isotopesGrp.newObject("App::FeaturePython",name)
        isoObj = isotopesGrp.newObject("App::DocumentObjectGroupPython",name)
        #GDMLisotope(isoObj,name,N,Z,unit,value)
        GDMLisotope(isoObj,name,N,Z,value)

def processElements() :
    from GDMLObjects import GDMLelement, GDMLfraction
    elementsGrp  = doc.addObject("App::DocumentObjectGroupPython","Elements")
    elementsGrp.Label = 'Elements'
    for element in materials.findall('element') :
        name = element.get('name')
        elementObj = elementsGrp.newObject("App::DocumentObjectGroupPython", \
                     name)
        GDMLelement(elementObj,name)
        for fraction in element.findall('fraction') :
            ref = fraction.get('ref')
            n = float(fraction.get('n'))
            #fractObj = elementObj.newObject("App::FeaturePython",ref)
            fractObj = elementObj.newObject("App::DocumentObjectGroupPython",ref)
            GDMLfraction(fractObj,ref,n)
            #fractObj.Label = ref[0:5]+' : ' + '{0:0.2f}'.format(n)
            fractObj.Label = ref+' : ' + '{0:0.2f}'.format(n)

def processGDML(filename):

    FreeCAD.Console.PrintMessage('Import GDML file : '+filename+'\n')
    if printverbose: print ('ImportGDML Version 0.1')
    
    global pathName
    pathName = os.path.dirname(os.path.normpath(filename))
    FilesEntity = False

    global setup, define, materials, solids, structure
  
  # Add files object so user can change to organise files
  #  from GDMLObjects import GDMLFiles, ViewProvider
  #  myfiles = doc.addObject("App::FeaturePython","Export_Files")
    #myfiles = doc.addObject("App::DocumentObjectGroupPython","Export_Files")
    #GDMLFiles(myfiles,FilesEntity,sectionDict)

    from lxml import etree
    #root = etree.fromstring(currentString)
    parser = etree.XMLParser(resolve_entities=True)
    root = etree.parse(filename, parser=parser)

    setup     = root.find('setup')
    define    = root.find('define')
    materials = root.find('materials')
    solids    = root.find('solids')
    structure = root.find('structure')

    processMaterials()
    processIsotopes()
    processElements()

    constDict = processConstants()
    print (setup.attrib)

    volumeGrp = doc.addObject("App::DocumentObjectGroupPython","Volumes")
    world = getRef(setup,"world")
    parseVolume(volumeGrp,world,0,0,0,None,3)

    doc.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    if printverbose:
        print('End ImportGDML')
    FreeCAD.Console.PrintMessage('End processing GDML file\n')
