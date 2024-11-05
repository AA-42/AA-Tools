# -*- coding: utf-8 -*-
__title__ = "Remove All CAD Imports"
__author__ = "Andreea ADAM"
__version__ = 'Version: 1.0.0'
__doc__ = """Version = 1.0.0
Date    = 31.10.2024
Description:
Batch rename Revit element types based on a predefined mapping dictionary.

Last update:
- [31.10.2024]
Author: Andreea ADAM - https://github.com/AA-42
Repository URL: https://github.com/AA-42/pyRevitBatchReplaceWords
"""

# IMPORTS
#====================================================================================================
from pyrevit import script
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    RevitLinkInstance,
    RevitLinkType,
    CADLinkType,
    Transaction
)

# VARIABLES
#====================================================================================================
# Get the Revit document
doc = __revit__.ActiveUIDocument.Document

# FUNCTION
#====================================================================================================
# Start a PyRevit transaction
with Transaction(doc, "Remove All Links") as t:
    t.Start()

    # Collect all Revit link instances and types in the model
    revit_link_instances = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
    revit_link_types = FilteredElementCollector(doc).OfClass(RevitLinkType).ToElements()
    
    # Collect all CAD link types in the model
    cad_link_types = FilteredElementCollector(doc).OfClass(CADLinkType).ToElements()

    # Remove all Revit link instances
    for link_instance in revit_link_instances:
        doc.Delete(link_instance.Id)
    
    # Remove all Revit link types
    for link_type in revit_link_types:
        doc.Delete(link_type.Id)

    # Remove all CAD link types
    for cad_type in cad_link_types:
        doc.Delete(cad_type.Id)

    t.Commit()

# Notify the user
script.get_logger().info("All Revit and CAD links have been removed from the model.")
