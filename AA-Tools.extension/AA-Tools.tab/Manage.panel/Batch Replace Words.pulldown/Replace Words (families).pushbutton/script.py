# -*- coding: utf-8 -*-
__title__ = "Batch Rename Families"
__author__ = "Andreea ADAM"
__version__ = 'Version: 1.0.0'
__doc__ = """Version = 1.0.0
Date    = 28.10.2024
Description:
Batch rename Revit families based on a predefined mapping dictionary.

Last update:
- [31.10.2024]
Author: Andreea ADAM - https://github.com/AA-42
Repository URL: https://github.com/AA-42/pyRevitBatchReplaceWords
"""

# IMPORTS
#====================================================================================================
from Autodesk.Revit.DB import FilteredElementCollector, Transaction
import re
from System import Exception  # General Exception to catch errors in IronPython

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
# Function to replace words with whole word matching
def replace_words(text, replacements):
    for old_word, new_word in replacements.items():
        # Use a regex pattern to replace only whole words
        pattern = r'\b' + re.escape(old_word) + r'\b'
        if new_word == '-':
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        else:
            text = re.sub(pattern, new_word, text, flags=re.IGNORECASE)
    return text.strip()

# Function to validate name (avoiding prohibited characters like '[]{}:;,' in Revit)
def is_valid_name(name):
    prohibited_chars = '[]{}:;,'  # Add any other prohibited characters here
    return not any(char in name for char in prohibited_chars)

doc = __revit__.ActiveUIDocument.Document

# Begin transaction
with Transaction(doc, "Batch Rename Families") as trans:
    trans.Start()

    elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()

    # Function to rename with error handling
    def safe_rename(element, new_name):
        try:
            if is_valid_name(new_name):  # Check if the new name is valid
                element.Name = new_name
                return True
            else:
                print("Invalid name for element ID " + str(element.Id) + ": " + new_name)
                return False
        except Exception as e:
            print("Error renaming element ID " + str(element.Id) + ": " + str(e))
            return False

    # Rename elements
    for element in elements:
        if hasattr(element, "Name"):
            original_name = element.Name
            new_name = replace_words(original_name, replacements)
            if new_name != original_name:
                if safe_rename(element, new_name):
                    print('Renamed: {} -> {}'.format(original_name, new_name))
                else:
                    print("Skipping element ID " + str(element.Id))

    trans.Commit()