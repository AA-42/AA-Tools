# -*- coding: utf-8 -*-
__title__ = "Batch Rename Areas, Rooms, Views, Sheets, and Schedules"
__author__ = "Andreea ADAM"
__version__ = 'Version: 1.0.0'
__doc__ = """Version = 1.0.0
Date    = 28.10.2024
Description:
Batch rename Revit elements based on a predefined mapping dictionary.

Last update:
- [04.11.2024]
Author: Andreea ADAM - https://github.com/AA-42
Repository URL: https://github.com/AA-42/AA-Tools.git
"""

# IMPORTS
#====================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms, script
import re  # Import the regular expressions module

# VARIABLES
#====================================================================================================
# Get the active Revit document
doc = __revit__.ActiveUIDocument.Document

# REPLACEMENT DICTIONARY
#====================================================================================================
replacements = {
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

# FUNCTION
#====================================================================================================
# Function to replace words in a given string
def replace_words(original_text, replacements):
    for old_word, new_word in replacements.items():
        if new_word == "-":  # Remove the word if the replacement is "-"
            # Use regex to match whole words and replace them
            original_text = re.sub(r'\b' + re.escape(old_word) + r'\b', '', original_text, flags=re.IGNORECASE)
        else:
            # Use regex to match whole words and replace them
            original_text = re.sub(r'\b' + re.escape(old_word) + r'\b', new_word, original_text, flags=re.IGNORECASE)
    return original_text

# TRANSACTION
#====================================================================================================
# Transaction to modify the document
with Transaction(doc, "Batch Replace Words") as trans:
    trans.Start()
    
    # Set a flag to check if any modifications were made
    modifications_made = False

    # Collect elements from different categories
    categories_to_check = [
        BuiltInCategory.OST_Views,
        BuiltInCategory.OST_Sheets,
        BuiltInCategory.OST_Schedules
    ]
    
    # Iterate over each category except rooms and areas
    for category in categories_to_check:
        collector = FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType()
        for elem in collector:
            if hasattr(elem, 'Name') and elem.IsValidObject:
                original_name = elem.Name
                new_name = replace_words(original_name, replacements)
                if new_name != original_name:
                    try:
                        elem.Name = new_name
                        modifications_made = True
                    except Exception as e:
                        print("Cannot change name for {0}: {1}".format(elem.Id, e))
    
    # Additional check for rooms and areas
    room_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType()
    for room in room_collector:
        if room.IsValidObject:
            original_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
            new_name = replace_words(original_name, replacements)
            if new_name != original_name:
                try:
                    room.get_Parameter(BuiltInParameter.ROOM_NAME).Set(new_name)
                    modifications_made = True
                except Exception as e:
                    print("Cannot change name for room {0}: {1}".format(room.Id, e))
                
    area_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Areas).WhereElementIsNotElementType()
    for area in area_collector:
        if area.IsValidObject:
            original_name = area.LookupParameter("Name").AsString()
            new_name = replace_words(original_name, replacements)
            if new_name != original_name:
                try:
                    area.LookupParameter("Name").Set(new_name)
                    modifications_made = True
                except Exception as e:
                    print("Cannot change name for area {0}: {1}".format(area.Id, e))

    # Commit only if modifications were made
    if modifications_made:
        trans.Commit()
    else:
        trans.RollBack()

# Notify user that the operation is complete
forms.alert("Batch replace operation completed!")