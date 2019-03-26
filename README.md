# FreeCAD_Python_GDML

FreeCAD python Importer & Exporter for GDML files.

Note: Sister development https://github.com/KeithSloan/FreeCAD_Geant4

## Installation Linux

To incorporate into FreeCAD linux.

Assumes you already have FreeCAD and git installed

1) Install lmxl - sudo apt-get install python-lxml

2) Clone repository **git clone https://github.com/KeithSloan/FreeCAD_Python_GDML.git**

3) For workbench **git checkout workbench**
   (if workbench not present **git checkout -b workbench origin/workbench )

4) cd FreeCAD_Python_GDML

5) Check paths in softLinks script

6) make sure softLink script is executable - chmod +x softLinks

7) Run softLink script to soft link the module into FreeCAD and FreeCAD-daily systems

## Branch - materials

There is a new branch 'materials' that on an import makes
the GDML  Material definitions available in FreeCAD document
( Only limited testing hence the ability to switch in and our via git branch )
( There is currently no checking the validity of any changed parameters )

   **git checkout -b materials origin/materials**

   You can then switch between branch with **git checkout** 

## Workbench

Adds support for GDMLBox, GDMLCone, GDMLCylinder, GDMLSphere, GDMLTube

## Exporter

GDMLObjects are output as straight GDML solids

The following FreeCAD objects are output as GDML equivalents

1) Cube     ( GDML - Box )
2) Cone     ( GDML - Cone )
3) Cylinder ( GDML - Tube )
4) Sphere   ( GDML - Sphere )

If not handled as above then objects shapes are checked  to see if planar,
if yes converts to Tessellated Solid with 3 or 4 vertex as appropriate.
If not creates a mesh and then a Tessellated solid with 3 vertex. 
 
## Future Development Road Map

  * Workbench Dialog for initial GDML Object values(?)
  * Handle different Positioning between GDML & FreeCAD
  * Sort out handling of degrees radians
  * Add support for quantity
  * Add further GDML Objects
  * Design icons for workbench

* Workbench
  * Analize FreeCAD file for direct conversion of object to GDML solid
  * Display mesh for objects that will not directly convert
  * Provide options to control meshing objects that will be Tessellated
  * Icons to Analize and Export
* Tidy softLink script
* Make FreeCAD installable workbench 
* Documentation
* Investigate handling of Materials

## For NIST Materials database see http://physics.nist.gov/PhysRefData

## Need to sort out AIR definition

## Acknowledgements

Thanks to

* Wouter Deconnick

and the following FreeCAD forum members

* wmayer
* Joel_graff
* chrisb

## Feedback

To contact the Author email keith[at]sloan-home.co.uk

