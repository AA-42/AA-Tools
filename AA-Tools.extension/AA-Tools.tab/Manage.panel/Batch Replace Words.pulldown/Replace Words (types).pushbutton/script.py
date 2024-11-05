# -*- coding: utf-8 -*-
__title__ = "Batch Rename FamilyTypes"
__author__ = "Andreea ADAM"
__version__ = 'Version: 1.0.0'
__doc__ = """Version = 1.0.0
Date    = 29.10.2024
Description:
Batch rename Revit element types based on a predefined mapping dictionary.

Last update:
- [31.10.2024]
Author: Andreea ADAM - https://github.com/AA-42
Repository URL: https://github.com/AA-42/AA-Tools.git
"""

# IMPORTS
#====================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import RailingType, HandRailType, StairsType
from Autodesk.Revit.DB.Mechanical import FlexDuctType, DuctSystemType, DuctType, DuctInsulationType, MechanicalSystemType
from Autodesk.Revit.DB.Plumbing import FlexPipeType, PipingSystemType, PipeInsulationType, PipeType
from Renaming.BaseClass_FindReplace import BaseRenaming
from Snippets._context_manager import ef_Transaction, try_except
import re  # Import regular expressions module

# VARIABLES
#====================================================================================================
uidoc = __revit__.ActiveUIDocument
doc   = __revit__.ActiveUIDocument.Document

# REPLACEMENT DICTIONARY
#====================================================================================================
replacement_dict = {
    'ROYAL': '-',
    'PRINCE': '-',
    'CPPA': 'THE CLIENT',
    'CPPO': 'THE CLIENT',
    'INVITED PERSONS': 'VIP GUESTS',
    'FRIENDS': 'VIP GUESTS',
    'INHABITED CANYON USERS': 'GUESTS',
    'INHABITED CANYONS USERS': 'GUESTS',
    'CLUB': 'LOUNGE AREA',
    'DISCOTHEQUE': 'ENTERTAINMENT AREA',
    'DANCING AREA': 'GATHERING SPACE',
    'NIGHTCLUB': 'GATHERING SPACE',
    'MUSIC STAGE': 'PERFORMANCE STAGE',
    'DANCING': '-',
    'JUICE BAR': 'REFRESHMENT AREA',
    'BAR': 'REFRESHMENT AREA',
    'COCKTAIL BAR': 'REFRESHMENT AREA',
    'COCKTAIL': 'REFRESHMENT AREA',
    'DRINKS': 'BEVERAGES',
    'MUSIC LOUNGE': 'GATHERING SPACE',
    'MUSIC': '-',
    'DJ': 'TECHNICAL STATION',
    'RESTAURANT': 'DINING AREA',
    # Case-insensitive mappings
    'royal': '-',
    'Royal': '-',
    'prince': '-',
    'Prince': '-',
    'cppa': 'THE CLIENT',
    'Cppa': 'THE CLIENT',
    'cppo': 'THE CLIENT',
    'Cppo': 'THE CLIENT',
    'invited persons': 'VIP GUESTS',
    'Invited persons': 'VIP GUESTS',
    'Invited Persons': 'VIP GUESTS',
    'friends': 'VIP GUESTS',
    'Friends': 'VIP GUESTS',
    'inhabited canyon users': 'GUESTS',
    'Inhabited canyon users': 'GUESTS',
    'Inhabited Canyon Users': 'GUESTS',
    'inhabited canyons users': 'GUESTS',
    'Inhabited canyons users': 'GUESTS',
    'Inhabited Canyons Users': 'GUESTS',
    'club': 'LOUNGE AREA',
    'Club': 'LOUNGE AREA',
    'discotheque': 'ENTERTAINMENT AREA',
    'Discotheque': 'ENTERTAINMENT AREA',
    'dancing area': 'GATHERING SPACE',
    'Dancing area': 'GATHERING SPACE',
    'Dancing Area': 'GATHERING SPACE',
    'nightclub': 'GATHERING SPACE',
    'Nightclub': 'GATHERING SPACE',
    'music stage': 'PERFORMANCE STAGE',
    'Music stage': 'PERFORMANCE STAGE',
    'Music Stage': 'PERFORMANCE STAGE',
    'dancing': '-',
    'Dancing': '-',
    'juice bar': 'REFRESHMENT AREA',
    'Juice bar': 'REFRESHMENT AREA',
    'Juice Bar': 'REFRESHMENT AREA',
    'bar': 'REFRESHMENT AREA',
    'Bar': 'REFRESHMENT AREA',
    'cocktail bar': 'REFRESHMENT AREA',
    'Cocktail bar': 'REFRESHMENT AREA',
    'Cocktail Bar': 'REFRESHMENT AREA',
    'cocktail': 'REFRESHMENT AREA',
    'Cocktail': 'REFRESHMENT AREA',
    'drinks': 'BEVERAGES',
    'Drinks': 'BEVERAGES',
    'music lounge': 'GATHERING SPACE',
    'Music lounge': 'GATHERING SPACE',
    'Music Lounge': 'GATHERING SPACE',
    'music': '-',
    'Music': '-',
    'dj': 'TECHNICAL STATION',
    'Dj': 'TECHNICAL STATION',
    'restaurant': 'DINING AREA',
    'Restaurant': 'DINING AREA'
}

# CLASS
#====================================================================================================
class BatchRenameFamilyTypes:
    def __init__(self):
        self.all_types = []  # Initialize list for all types
        self.get_all_types()  # Automatically get all types
        print("Found {} types to rename.".format(len(self.all_types)))  # Using format for string

    def get_all_types(self):
        """Get all element types from the document."""
        all_types = FilteredElementCollector(doc).WhereElementIsElementType().ToElements()
        incl_types = [FamilySymbol, WallType, FloorType, CeilingType, RoofType,
                      FilledRegionType, TextNoteType, AnnotationSymbolType, AnnotationSymbol,
                      DimensionType, SpotDimensionType, GridType, CurtainSystemType, MullionType, GroupType,
                      FlexPipeType, FlexDuctType, RailingType, HandRailType, DuctSystemType, DuctType,
                      MechanicalSystemType, DuctInsulationType, PipingSystemType, PipeInsulationType, PipeType,
                      StairsType, BeamSystemType]

        # Filter all types based on included types
        self.all_types = [typ for typ in all_types if type(typ) in incl_types]

    def rename_elements(self):
        """Function to batch rename all FamilyTypes based on a mapping dictionary."""
        with ef_Transaction(doc, __title__):
            for typ in self.all_types:
                with try_except():
                    current_name = typ.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString().strip()  # Ensure no leading/trailing spaces

                    # Skip if current name is empty
                    if not current_name:
                        print("Skipping empty name.")
                        continue
                    
                    # Get the new name without forcing lowercase
                    new_name = self.get_new_name(current_name)  # Pass the original name

                    if new_name and new_name != current_name:  # Only rename if the name changes
                        typ.Name = new_name
                        print("Renamed '{}' to '{}'.".format(current_name, new_name))
                    else:
                        print("No change for '{}'.".format(current_name))

    def get_new_name(self, current_name):
        """Get the new name based on the replacement dictionary with word boundary matching."""
        for key, replacement in replacement_dict.items():
            # Use regular expression to match whole words only
            pattern = r'\b' + re.escape(key) + r'\b'  # Match only standalone instances of the key
            current_name = re.sub(pattern, replacement, current_name)

        return current_name  # Return the updated name

# MAIN
#====================================================================================================
if __name__ == '__main__':
    renamer = BatchRenameFamilyTypes()  # Instantiate the renamer
    renamer.rename_elements()  # Call rename method