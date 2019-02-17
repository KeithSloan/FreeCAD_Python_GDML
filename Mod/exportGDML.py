
#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2019 Keith Sloan <keith@sloan-home.co.uk>               *
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
#***************************************************************************
__title__="FreeCAD - GDML exporter Version"
__author__ = "Keith Sloan <keith@sloan-home.co.uk>"
__url__ = ["https://github.com/KeithSloan/FreeCAD_Geant4"]

import FreeCAD, os, Part, math
from FreeCAD import Vector

# xml handling
import argparse
import xml.etree.ElementTree as ET

#################################
# Globals
global gdml

try: import FreeCADGui
except ValueError: gui = False
else: gui = True

#***************************************************************************
# Tailor following to your requirements ( Should all be strings )          *
# no doubt there will be a problem when they do implement Value
if open.__module__ in ['__builtin__', 'io']:
    pythonopen = open # to distinguish python built-in open function from the one declared here

#################################
# Switch functions
################################
class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))


#################################
#  Setup GDML environment
#################################
def GDMLstructure() :
     global gdml, define, materials, structure, setup
     gdml = ET.Element('gdml', {
          'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
          'xsi:noNamespaceSchemaLocation': "http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd"
})
     define = ET.SubElement(gdml, 'define')
     materials = ET.SubElement(gdml, 'materials')
     solids = ET.SubElement(gdml, 'solids')
     structure = ET.SubElement(gdml, 'structure')
     setup = ET.SubElement(gdml, 'setup', {'name': 'Default', 'version': '1.0'})
     ET.SubElement(setup, 'world', {'ref': 'worldLogical'})


def DefineMaterials():
    x = 1
    # Materials from DataBase 
    #nist = G4NistManager.Instance()
    #air = nist.FindOrBuildMaterial("G4_AIR")
    #global air
   
    # Our defined Materials 
    #Fe = G4Element(G4String("Iron"),G4String("Fe"),"z=26.","55.845*g/mole")
    #Fe = G4Element(G4String("Iron"),G4String("Fe"),26.0,55.845*g/mole)
    #Cr = G4Element(G4String("Chromium"),G4String("Cr"),"z=24.","51.9961*g/mole")
    #Cr = G4Element(G4String("Chromium"),G4String("Cr"),24.0,51.9961*g/mole)
    #Ni = G4Element(G4String("Nickel"),G4String("Ni"),"z=28.","58.6934*g/mole")
    #Ni = G4Element(G4String("Nickel"),G4String("Ni"),28.0,58.6934*g/mole)

    #global SSteel,Fe,Cr,Ni
    #SSteel = G4Material("SSteel","density=8.03*g/cm3",components)
    #SSteel = G4Material("SSteel",8.03,3)
    #SSteel.AddElement(Fe,"74*perCent")
    #SSteel.AddElement(Fe,0.74)
    #SSteel.AddElement(Cr,"18*perCent")
    #SSteel.AddElement(Cr,0.18)
    #SSteel.AddElement(Ni,"8*perCent")
    #SSteel.AddElement(Ni,0.08)
   
def DefineBoundingBox(exportList,bbox):
    x = 1
    # Does not work if just a mesh`
    #for obj in exportList :
    #    print("{} + {} = ".format(bbox, obj.Shape.BoundBox))
    #    bbox.add(obj.Shape.BoundBox)
    #    print(bbox)


def ConstructWorld():
    x = 1
    # Python has automatic garbage collection system.
    # Geometry objects must be defined as GLOBAL not to be deleted.
    #global sld_world, lv_world, pv_world, va_world

    #sld_world= G4Box("world", 1.*m, 1.*m, 1.*m)
    #lv_world= G4LogicalVolume(sld_world, air, "world")
    #pv_world= G4PVPlacement(G4Transform3D(), lv_world, "world",
    #                        None, False, 0)

    #va_world= G4VisAttributes()
    #va_world.SetVisibility(False)
    #lv_world.SetVisAttributes(va_world)

    # solid object (dummy)
    #    global sld_brep_box, sld_sld, lv_sld, pv_sld

    #solidBox = G4Box("dummy", 10.*cm, 10.*cm, 10.*cm)
    #lvBox = G4LogicalVolume(solidBox,SSteel,"box")

    #pos_x = G4double(-1.0*meter)
    #pos_x = -1.0
    #pos_y = G4doule(0.0*meter)
    #pos_y = 0.0
    #pos_z = G4double(0.0*meter)
    #pos_z = 0.0

    # Look for better constructor options for G4PVPlacement
    #pvBox = G4PVPlacement(G4RotationMatrix(),  # no rotaion \
    #                  G4ThreeVector(pos_x, pos_y, pos_z),   \
    #                  G4String("Box"),         # its name   \ 
    #                  lvBox,                   # its logical volume \
    #                  pv_world,                # its mother (physical) volume \
    #                  False,0)


    #    p1 = G4ThreeVector(0.0,0.0,0.0)
    #    p2 = G4ThreeVector(0.0,50.0,0.0)

    #    return(pv_world)

def report_object(obj) :
    
    print("Report Object")
    print(obj)
    print("Name : "+obj.Name)
    print("Type : "+obj.TypeId) 
    print("Placement")
    print("Pos   : "+str(obj.Placement.Base))
    print("axis  : "+str(obj.Placement.Rotation.Axis))
    print("angle : "+str(obj.Placement.Rotation.Angle))
    
    while switch(obj.TypeId) :

      if case("Part::Sphere") :
         print("Sphere Radius : "+str(obj.Radius))
         break
           
      if case("Part::Box") : 
         print("cube : ("+ str(obj.Length)+","+str(obj.Width)+","+str(obj.Height)+")")
         break

      if case("Part::Cylinder") : 
         print("cylinder : Height "+str(obj.Height)+ " Radius "+str(obj.Radius))
         break
   
      if case("Part::Cone") :
         print("cone : Height "+str(obj.Height)+ " Radius1 "+str(obj.Radius1)+" Radius2 "+str(obj.Radius2))
         break

      if case("Part::Torus") : 
         print("Torus")
         print(obj.Radius1)
         print(obj.Radius2)
         break

      if case("Part::Prism") :
         print("Prism")
         break

      if case("Part::RegularPolygon") :
         print("RegularPolygon")
         break

      if case("Part::Extrusion") :
         print("Extrusion")
         break

      if case("Circle") :
         print("Circle")
         break

      if case("Extrusion") : 
         print("Wire extrusion")
         break

      print("Other")
      print(obj.TypeId)
      break

def fc2g4Vec(v) :
    print(str(v[0])+" : "+str(v[1])+" : "+str(v[2]))
    #    return(G4ThreeVector(int(v[0]),int(v[1]),int(v[2])))

def createFacet(v0,v1,v2) :
    global facet
    print("Create Facet : ")
    print(str(v0)+" : "+str(v1)+" : "+str(v2))
# following should work but does not wait for weyner response in forum
#    facet = MyG4TriangularFacet(v0,v1,v2)
    v0g4 = fc2g4Vec(v0)
    v1g4 = fc2g4Vec(v1)
    v2g4 = fc2g4Vec(v2)
    print(str(v0g4)+" : "+str(v1g4)+" : "+str(v2g4))
    #facet = MyG4TriangularFacet(v0g4,v1g4,v2g4)
    print("Facet constructed")
#   facet = G4VFacet() cannot be initiated from python
#   G4TrianglerFacet needs to be constructed with all three vectors
#   otherwise Isdefined is false and one gets an error 
# need to convert FreeCAD base.Vector to Geant4 vector Hep3Vector
    #print("Number Vert   : "+str(facet.GetNumberOfVertices()))
    #print("Area          : "+str(facet.GetArea()))
    #print("Is defined    : "+str(bool(facet.IsDefined)))
    #print(facet.GetVertex(0))
    #print(facet.GetVertex(1))
    #print(facet.GetVertex(2))
    #return(facet)

#    Add XML for TessellateSolid
def mesh2Tessellate(mesh) :
     print "mesh"
     print mesh
     print dir(mesh)
     print "Facets"
     print mesh.Facets
     print "mesh topology"
     print dir(mesh.Topology)
     print mesh.Topology

#     add name of TessellateSolid
#     tessellate = G4TessellatedSolid()
#    mesh.Topology[0] = points
#    mesh.Topology[1] = faces
     for fc_facet in mesh.Topology[1] : 
         print(fc_facet)
         g4_facet = createFacet(mesh.Topology[0][fc_facet[0]],
                                mesh.Topology[0][fc_facet[1]],
                                mesh.Topology[0][fc_facet[2]])
         #print(g4_facet.GetVertex(0))
         #print(g4_facet.GetVertex(1))
         #print(g4_facet.GetVertex(2))

         print("Adding Facet")
         #tessellate.AddFacet(g4_facet)
         #print("Facet added")
     #return(tessellate)

def process_Mesh(wv,obj) :

    tessellate = mesh2Tessellate(obj.Mesh)
    pos_x = 0.0
    pos_y = 0.0
    pos_z = 0.0

    print("Create Tessellate Logical Volume")
    #lvTess = G4LogicalVolume(tessellate,SSteel,"Tessellate")
    print("Add Logical Volume to Physical Volume")
    #pvTess = G4PVPlacement(G4RotationMatrix(),         # no rotaion     \
    #                  G4ThreeVector(pos_x, pos_y, pos_z),               \
    #                  G4String("Tessellated"),         # its name       \
    #                  lvTess,                 # its logical volume      \
    #                  wv,                # its mother (physical) volume \
    #                  False,0)


    #dir   = G4ThreeVector(0.,1.,0.)
    #axis  = G4ThreeVector(0.,1.,0.)
    #point = G4Point3D(0.,0.,0.)
    #point = G4ThreeVector(0.,0.,0.)
    #G4FPlane(dir,axis,point,1)
    #return(tessellate)

def shape2Mesh(shape) :
     import MeshPart
     return (MeshPart.meshFromShape(Shape=shape, Deflection = 0.0))
#            Deflection= params.GetFloat('meshdeflection',0.0)) 

def process_Object_Shape(wv,obj) :
    print("Process Object Shape")
    print(obj)
    print(obj.PropertiesList)
    shape = obj.Shape
    print shape
    print(shape.ShapeType)
    while switch(shape.ShapeType) : 

         if case("Mesh::Feature") :
            print("Mesh - Should not occur should have been handled")
            #print("Mesh")
	    #tessellate = mesh2Tessellate(mesh) 
            #return(tessellate)
            #break

	 print("ShapeType Not handled")
         print(shape.ShapeType)
         break

#   Dropped through to here
#   Need to check has Shape
    print("Faces")
    for f in shape.Faces :
        print f
#        print dir(f)

# Virtual function    G4solid = myG4VSolid()
# G4solid = G4BREPSolid() G4BREPSolid depreciated

# Create Mesh from shape & then Process Mesh to create Tessellated Solid in Geant4
    process_Mesh(wv,shape2Mesh(shape))


def process_box_object(wv, obj) :
    x = 1
    #solidBox = G4Box("dummy", 10.*cm, 10.*cm, 10.*cm)
    #lvBox = G4LogicalVolume(solidBox,SSteel,"box")

    #pos_x = -1.0
    #pos_y = 0.0
    #pos_z = 0.0

    # Look for better constructor options for G4PVPlacement
    #pvBox = G4PVPlacement(G4RotationMatrix(),  # no rotaion \
    #                  G4ThreeVector(pos_x, pos_y, pos_z),   \
    #                  G4String("Box"),         # its name   \
    #                  lvBox,                   # its logical volume \
    #                  wv,                # its mother (physical) volume \
    #                  False,0)


def process_object(wv, obj) :
   
    print("\nProcess Object")
    while switch(obj.TypeId) :

#      if case("Part::Box") :
#         print("Box")
#         process_Object_Box(wv, obj)
#         break

      if case("Part::Cut") :
         print("Cut")
         break

      if case("Part::Fuse") :
         print("Union")
         break

      if case("Part::Common") :
         print("intersection")
         break

      if case("Part::MultiFuse") :
         print("Multifuse") 
         break

      if case("Part::MultiCommon") :
         print("Multi Common / intersection")
         break

      if case("Mesh::Feature") :
         print("Mesh Feature") 
         process_Mesh(wv,obj)
         break

# Dropped through so treat object as a shape
# Need to check obj has attribute Shape
# Create a mesh & tessellate
      process_Object_Shape(wv, obj)
      break

def export(exportList,filename) :
    "called when FreeCAD exports a file"
   
    # process Objects
    print("\nStart GDML Export 0.1")

    GDMLstructure()
    DefineMaterials()

    bbox = FreeCAD.BoundBox()
    DefineBoundingBox(exportList,bbox)
    world_volume = ConstructWorld()
    for obj in exportList :
        report_object(obj)
        process_object(world_volume,obj)

    # write GDML file              
    print("Write to GDML file")
    #navigator= gTransportationManager.GetNavigatorForTracking()
    ##world_volume= navigator.GetWorldVolume()

    ET.ElementTree(gdml).write(filename, 'utf-8', True)

    #gdml_parser = G4GDMLParser()
    #print(filename)
    #print(type(filename))
    #gdml_parser.Write(G4String(str(filename)), world_volume)
    
    FreeCAD.Console.PrintMessage("successfully exported "+filename)
