# FreeCAD_Python_GDML

FreeCAD python Importer & Exporter for GDML files.

Note: Sister development https://github.com/KeithSloan/FreeCAD_Geant4

## Branches ( git checkout "branch" )

* workbench - underdevelopment
  GDML workbench to Add GDML Objects as FreeCAD python Objects

   GDML Objects added

      * GDMLBox
      * GDMLCone
      * GDMLSphere
      * GDMLTube

* master - GDML import / export

## Installation - To incorporate into FreeCAD linux.

Assumes you already have FreeCAD and git installed

* Clone repository **git clone https://github.com/KeithSloan/FreeCAD_Python_GDML.git**

* cd FreeCAD_Python_GDML

* make sure softLink script is executable

* Run softLink script to soft link the module into FreeCAD and FreeCAD-daily systems
   
   
## Exporter

The following FreeCAD objects are output as GDML equivalents

* Cube     ( GDML - Box )
* Cone     ( GDML - Cone )
* Cylinder ( GDML - Tube )
* Sphere   ( GDML - Sphere )

If not handled as above then objects shapes are checked  to see if planar,
if yes converts to Tessellated Solid with 3 or 4 vertex as appropriate.
If not creates a mesh and then a Tessellated solid with 3 vertex. 

Booleans apart from MultiCommon are now implemented for export.
 
## Future Development Road Map

* Workbench
  * Analize FreeCAD file for direct conversion of object to GDML solid
  * Display mesh for objects that will not directly convert
  * Provide options to control meshing objects that will be Tessellated
  * Icons to Analize and Export
* Add function for objects that can be directly converted
* Use lxml rather than etree (Needs apt-get install python-lxml)
* Tidy softLink script
* Make FreeCAD installable workbench 
* Documentation
* Investigate handling of Materials

## For NIST Materials database see http://physics.nist.gov/PhysRefData

## Need to sort out AIR definition

## Feedback

To contact the Author email keith[at]sloan-home.co.uk

