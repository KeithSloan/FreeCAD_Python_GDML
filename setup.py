from setuptools import setup
from GDMLworkbench import __version__

setup(name='freecad.GDMLworkbench',
      version=str(__version__),
      packages=['freecad',
                'freecad.GDMLworkbench'],
      maintainer="keithsloan52",
      maintainer_email="keith@sloan-home.co.uk",
      url="https://github.com/KeithSloan/FreeCAD_Python_GDML",
      description="FreeCAD GDML workbench",
      install_requires=['lxml'],
include_package_data=True)
