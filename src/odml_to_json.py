import os
import json
from odml import load, save

# Create the json_templates folder if it doesn't exist
folder_path = 'templates-json/in2pb-templates'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Convert all odml files to JSONs
odml_folder = 'templates-odml/in2pb-templates'
for filename in os.listdir(odml_folder):
    if filename.endswith('.xml'):
        try:
            odml_path = os.path.join(odml_folder, filename)
            json_path = os.path.join(folder_path, os.path.splitext(filename)[0] + '.json')
            odml_doc = load(odml_path)
            save(odml_doc, json_path, "JSON")
            print(f"Converted {filename} to JSON.")
        except Exception as e:
            print(f"Error converting {filename} to JSON: {e}")

print("All odml files have been converted to JSONs successfully!")
