# FreeCAD_Python_GDML

FreeCAD python importer & Exporter for GDML files.

Note: Sister devlopment https://github.com/KeithSloan/FreeCAD_Geant4

## Installation Linux

To incorporate into FreeCAD linux.

Assumes you already have FreeCAD and git installed

1) Clone repository **git clone https://github.com/KeithSloan/FreeCAD_Python_GDML.git**

2) cd FreeCAD_Python_GDML

3) make sure softLink script is executable

4) Run softLink script to soft link the module into FreeCAD and FreeCAD-daily systems
   
   
## Exporter

Current version converts all FreeCAD objects containing shapes to a mesh and then to a GDML Tessellated Solid.

## Future Development Road Map

* Implement Booleans operations
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

## Feedback

To contact the Author email keith[at]sloan-home.co.uk

