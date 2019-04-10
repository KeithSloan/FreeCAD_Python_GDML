# FreeCAD_Python_GDML

FreeCAD python Importer & Exporter for GDML files.

Note: Sister development https://github.com/KeithSloan/FreeCAD_Geant4

## Current stable version of FreeCAD is 18.01 which uses Python3

As having to make a lot of changes to work with Python3 the
development branch <workbench> has now been merged with the <master> branch

## Installation Linux

To incorporate into FreeCAD linux.

Assumes you already have FreeCAD and git installed

1) Install lmxl - sudo apt-get install python3-lxml

2) Clone repository **git clone https://github.com/KeithSloan/FreeCAD_Python_GDML.git**

3) cd FreeCAD_Python_GDML

4) Check paths in softLinks script

5) make sure softLink script is executable - chmod +x softLinks

6) Run softLink script to soft link the module into FreeCAD and FreeCAD-daily systems

## Installation Window

1) Contents of Mod directory should be copied to a sub directory named
GDML in the windows FreeCAD Mod directory

2) A correct version of lxml for your version of windows should be downloaded and installed.
   
## GDML Workbench

If you switch to the GDML workbench a number of icons are available
in the Workbench bar, clicking on one the icons will create a GDML
object with default values. You can then edit the properties via the properties window. The parameters should be the same as in the GDML user guide.

GDML objects supported in this 
GDMLBox
GDMLCone
GDMLElTube
GDMLEllipsoid
GDMLSphere
GDMLTrap
GDMLTube

The first icon on the workbench bar is different. If you select a object
via the Combo view - Model - Labels & Attributes and then click on the icon
it will cycle the display mode of the selected object and all its children.
The cycle is Solid -> WireFrame -> Not Displayed -> Solid

## SampleFiles

This directory contains some sample gdml files. 

One in particular is lhcbvelo.gdml. This file takes a LONG time to import/open, but does eventually load. You might have to okay the odd wait.

If when it is displayed you go down the Volumes tree  ...

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
* DeepSOIC
* ickby

## Feedback

To contact the author email keith[at]sloan-home.co.uk

