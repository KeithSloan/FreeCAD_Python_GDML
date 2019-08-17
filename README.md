# FreeCAD_Python_GDML

FreeCAD python Importer & Exporter for GDML files.

Note: Sister development https://github.com/KeithSloan/FreeCAD_Geant4

## Current stable version of FreeCAD is 18.01 which uses Python3

As I had to make a lot of changes to get things working with Python3 the
development branch <workbench> has now been merged with the master branch

## Installation Linux

To incorporate into FreeCAD linux.

Assumes you already have FreeCAD and git installed

1) Install lmxl - sudo apt-get install python3-lxml

2) Clone repository **git clone https://github.com/KeithSloan/FreeCAD_Python_GDML.git**

3) cd FreeCAD_Python_GDML

4) Check paths in softLinks script

5) make sure softLink script is executable - chmod +x softLinks

6) Run softLink script to soft link the module into FreeCAD and FreeCAD-daily systems

## Installation Windows

1) Contents of Mod directory should be copied to a sub directory named
GDML in the windows FreeCAD Mod directory

2) A correct version of lxml for your version of windows should be downloaded and installed.
   
# GDML Workbench

## GDML Solids

GDML Solids are implemented as FreeCAD Python Objects and have the same properties as defined by GDML. By selecting an Object the properties can be changed
via the FreeCAD properties windows and the resulting changes displayed

## Opening a new file when the GDML workbench is active will load a Default file.
The Default file is defined in GDML/Mod/Resources/Default.gdml.

New GDML object have the material set to SSteel0x56070ee87d10 so the Default file should define this material. Other materials can be set by editing the FreeCAD parmeters of the object after creation.

## GDML Object creation

Switching to the GDML workbench a number of icons are then available on the Workbench bar,
clicking on one the icons will create a GDML object with default values.
You can then edit the properties via the properties window. The parameters should be the same as in the GDML user guide.

GDML objects supported in this

1. GDMLBox
2. GDMLCone
3. GDMLElTube
4. GDMLEllipsoid
5. GDMLSphere
6. GDMLTrap
7. GDMLTube

## GDML Import

On opening of a GDML file the appropriate FreeCAD implemented python Object
is created for each solid

## Viewing Volumes

The first icon on the workbench bar is different. If you select a object by one of the following methods

1. A volume via the Combo view - Model - Labels & Attributes.

   Then click on the icon it will cycle the display mode of the selected Volume and all its children.
   The cycle is Solid -> WireFrame -> Not Displayed -> Solid

2. In the main display - select a face by <ctrl> <left mouse>
   
   Then click on the icon it will cycle the display mode of the selected object
   

## SampleFiles

This directory contains some sample gdml files. 

One in particular is lhcbvelo.gdml. This file takes a LONG LONG time to import/open, over a minute on my system, but does eventually load. On my system I have to okay one wait. When it finally does display you will want to zoom in.

If when it is displayed you go down the Volumes tree to VelovVelo under the World volume then click on the toggle icon ( 1st GDML icon in the workbench) Again wait patiently and the display will change to wireframe. You can
then decend further down the Volumes tree, select one and again use the toggle icon and that volume and children will change to Solid. In this way various parts in different volumes can be examined.

## Exporter

### GDML Objects
GDMLObjects are output as straight GDML solids

### FreeCAD Objects

The following FreeCAD objects are output as GDML equivalents

1. Cube     ( GDML - Box )
2. Cone     ( GDML - Cone )
3. Cylinder ( GDML - Tube )
4. Sphere   ( GDML - Sphere )

If not handled as above then objects shapes are checked  to see if planar,
if yes converts to Tessellated Solid with 3 or 4 vertex as appropriate.
If not creates a mesh and then a Tessellated solid with 3 vertex. 

### Constants / Isotopes / Elements / Materials

Importing a GDML will create FreeCAD objects for the above and export should
create the same GDML definitions as imported.

The Ability to change to change these maybe implemented in the future.
 
## Preferences
There is now an option to toggle Printverbose flag to reduce printing to the python console.

## Future Development Road Map

  * Workbench Dialog for initial GDML Object values(?)
  * Handle different Positioning between GDML & FreeCAD
  * Add support for quantity
  * Add further GDML Objects
  * Add facility to add Volume
  * Add facility to edit Materials
  * Add facility to edit Isotopes
  * Add facility to edit Elements 

* Workbench
  * Analize FreeCAD file for direct conversion of object to GDML solid
  * Display mesh for objects that will not directly convert
  * Provide options to control meshing objects that will be Tessellated
  * Icons to Analize and Export
* Tidy softLink script
* Make FreeCAD an installable workbench 
* Documentation
* Investigate handling of Materials

## For NIST Materials database see http://physics.nist.gov/PhysRefData

## Need to sort out AIR definition

## Graphic Icons 

GDML Shapes designed by Jim Austin jmaustpc
Cycle icon by Flaticon see www.flaticon.com

Thanks to

* Wouter Deconnick

and the following FreeCAD forum members

* wmayer
* Joel_graff
* chrisb
* DeepSOIC
* ickby
* looo

## Feedback

To contact the author email keith[at]sloan-home.co.uk

