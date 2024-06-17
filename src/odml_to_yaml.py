import os
from odml import load, save

# Create the yaml_templates folder if it doesn't exist
folder_path = 'templates-yaml/in2pb-templates'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Convert all odml files to YAMLs
odml_folder = 'templates-odml/in2pb-templates'
for filename in os.listdir(odml_folder):
    if filename.endswith('.xml'):
        try:
            odml_path = os.path.join(odml_folder, filename)
            yaml_path = os.path.join(folder_path, os.path.splitext(filename)[0] + '.yaml')
            odml_doc = load(odml_path)
            save(odml_doc, yaml_path, "YAML")
            print(f"Converted {filename} to YAML.")
        except Exception as e:
            print(f"Error converting {filename} to YAML: {e}")

print("All odml files have been converted to YAMLs successfully!")