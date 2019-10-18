# FreeCAD_Python_GDML

FreeCAD python Importer & Exporter for GDML files.

Note: Sister development https://github.com/KeithSloan/FreeCAD_Geant4

Includes **experimental branch compound** to facilitate use of __FreeCAD FEM__ with GDML Files.
For more details see Experimental branch section.
   
Includes **experimental branch scan** to facilitate processing large GDML files like Alice   

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
   
   sudo ./softLinks

## Installation Windows

1) Contents of Mod directory should be copied to a sub directory named
GDML in the windows FreeCAD Mod directory

2) A correct version of lxml for your version of windows should be downloaded and installed.
   
# GDML Workbench

## GDML Solids

GDML Solids are implemented as FreeCAD Python Objects and have the same properties as defined by GDML. By selecting an Object the properties can be changed via the FreeCAD properties windows and the resulting changes displayed.

## To created a new GDML design

1) Start FreeCAD
2) Select the GDML workbench (Selecting a workbench varies with different versions of FreeCAD)
3) Via the **File** menu select **New** 
   This will load the Default GDML File with materials and create a World Volume.
   ( The Default GDML file is located GDML/Mod/Resources/Default.gdml )

4) Create 1-n Volumes in the World Volume by

   * Clicking on the Part icon ( Yellow blockish icon)
   * Then draging the created **Part** to the World Volume in the **Tree** window
   * **Part** maybe renamed vi right click on __Part__ and selected rename
   
5) Create GDML Solids by

   * Clicking on the corresponding icon of thw workbench.
   * Drag the GDML object to the appropriate **Part** again via the **Tree** window
   * You can then change the attributes by selecting the GDMLObject in the **Tree** window
     then changing the properties in the **Property View**
      
  So a valid structure for a GDML file is

   * Single World Volume (Part)
   * A number of Volumes (Parts) under the World Volume
   * A number of GDML Objects can exist in one Part ( GDML Logical Volume)
 
 6) To Export to GDML
           
    1. Select the 'World' Volume ( Default Name WorldVol )
    2. File export
    3. Select filetype as GDML ( Bottom Box of **Export file** window)
    4. Select Destination and file name with **GDML** as file extension 
     
## Opening a new file when the GDML workbench is active will load a Default file.
The Default file is defined in GDML/Mod/Resources/Default.gdml.

New GDML object have the material set to SSteel0x56070ee87d10 i.e. the first material in the Default file.
Other materials can be set by editing the material property via the FreeCAD parmeters View of the Object after creation.

## GDML Object creation

Switching to the GDML workbench a number of icons are then available on the Workbench bar.
clicking on one the icons will create a GDML object with default values.
It should then be dragged to the appropriate __Part__ ( GDML Logical Volume )
You can then edit the properties via the properties window. The parameters should be the same as in the GDML user guide.
If the Object is part of a Boolean you will have to use the **recompute** facility of FreeCAD to see the change to the Boolean

GDML objects currently supported in this

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

## GDML Objects Exporter 

To export to GDML 

1. Select the 'world' Volume, should be first Part in Design
2. File export
3. Select GDML as filetype
4. Make sure file has GDML as file extension

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

## Experimental branches

### compound

   **To use the branch**
   
   * git fetch compound
   * git checkout compound
   
   A new icon/command is added to the GDML workbench ( Currently an X )
   
   **To use** select a volume/Part i.e. The first Part which is the GDML world volume
   click on the compound icon ( Currently an X ) this will 
    
     1. Create an object named Compound under the selected Volume
     2. Create an FEM Analysis Object.
     3. All the materials of the objects in the Volume/Part/Compound are added to the Analysis Object.
     
     You can then switch to the FEM ( Finite Element ) Workbench and proceed with an analysis which would
     include
     
     1) Double click on each of the materials to edit their properties
     2) From the FEM workbench select the Compound Object and click on the icon to create a Mesh.
     3) Rest would depend on what analysys and what solver it is intended to use.
     
     Also as an experiment thermal parameters have been added to the GDMLmaterial object so these could
     be changed before creating a compound. One option to be would be to add elements to GDML files to enable
     loading and exporting, but then they would **NOT** be standard GDML files (maybe a different file extension)
     What do people think? see https://github.com/KeithSloan/FreeCAD_Python_GDML/issues/30


### scan

    **To use**
    Large files like Alice.GDML are not handled well as they take too long to load.
    The scan branch does a limit volume depth scan where volume names are determined but not processed.
    For unprocessed volume the names are preceeded by 'NOT_Expanded' so a volume name is 'NOT_Expanded_<VolumeName>
    
    Un expanded Volumes can be expanded by 
     1) Switching to the GDML workbench.
     2)Selecting a volume in the 'labels & attributes Window'
     3)clicking on the Expand Volume icon currently an X
    
   **To use the branch**
   
   * git fetch scan
   * git checkout scan
   
   A new icon/command is added to the GDML workbench ( Currently an X )

   The branch is experimental and I would appreciate feedback see https://github.com/KeithSloan/FreeCAD_Python_GDML/issues/29
   
   It could be that files like Alic.gdml do not load with the master branch due to a bug(s). So if you do find a volume
   that will not expand then please report this so things can be debugged.
   
   
   
    
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
* Hilden Timo

and the following FreeCAD forum members

* wmayer
* Joel_graff
* chrisb
* DeepSOIC
* ickby
* looooo
* easyw-fc
* bernd

OpenCascade Forum members

* Sergey Slyadnev

## Feedback

To contact the author email keith[at]sloan-home.co.uk

* Please report bugs
* I am always on the look out for test gdml files ( Small to medium size )XXXX# FreeCAD_Python_GDML

