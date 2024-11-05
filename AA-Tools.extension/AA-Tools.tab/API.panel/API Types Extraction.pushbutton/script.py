# -*- coding: utf-8 -*-
__title__ = "Remove All CAD Imports"
__author__ = "Andreea ADAM"
__version__ = 'Version: 1.0.0'
__doc__ = """Version = 1.0.0
Date    = 28.10.2024
Description:
Batch rename Revit element types based on a predefined mapping dictionary.

Last update:
- [29.10.2024]
Author: Andreea ADAM - https://github.com/AA-42
Repository URL: https://github.com/AA-42/pyRevitBatchReplaceWords
"""

# Import necessary Revit API classes
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

# Get the current document
doc = __revit__.ActiveUIDocument.Document

# List of all built-in categories
categories = [category for category in BuiltInCategory.GetValues(BuiltInCategory) if category != BuiltInCategory.INVALID]

# Loop through all built-in categories and collect element types
for category in categories:
    try:
        # Get element types for the current category
        element_types = FilteredElementCollector(doc) \
            .OfCategory(category) \
            .WhereElementIsElementType() \
            .ToElements()

        # Print out the names of all element types for this category
        if element_types:
            for typ in element_types:
                type_name = typ.Name
                print("Category: '{}' | Type Name: '{}'".format(category.ToString(), type_name))
        else:
            print("Category: '{}' has no element types.".format(category.ToString()))
    
    except Exception as e:
        print("Error processing category '{}': {}".format(category, e))
