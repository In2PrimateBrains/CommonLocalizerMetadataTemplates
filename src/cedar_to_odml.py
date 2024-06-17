import json
import odml
from odml.tools.xmlparser import XMLWriter
from pathlib import Path
import os

def convert_properties(properties, prop_ui, section):
    if 'order' not in prop_ui:
        return
    
    for prop in prop_ui['order']:
        prop_details = properties.get(prop, {})
        prop_label = prop_ui['propertyLabels'].get(prop, prop)
        prop_desc = prop_ui['propertyDescriptions'].get(prop, "No description available.")
        
        my_section = odml.Section(name=prop_label, definition=prop_desc)
        
        if prop_details.get('type') == "array":
            prop_details = prop_details['items']
            
        sub_ui = prop_details.get('_ui', {})
        if 'order' in sub_ui:
            for subprop in sub_ui['order']:
                subprop_label = sub_ui['propertyLabels'].get(subprop, subprop)
                subprop_desc = sub_ui['propertyDescriptions'].get(subprop, "No description available.")
                subprop_details = prop_details.get('properties', {}).get(subprop, {})
                # value_type = subprop_details.get('properties', {}).get('@value', {}).get('type', ['string'])[0]
                pref_label = subprop_details.get('skos:prefLabel') or subprop_details.get('items', {}).get('skos:prefLabel', 'Label not found')
                my_section.append(odml.Property(name=subprop_label, value="", definition=subprop_desc))

        else:
            section.append(odml.Property(name=prop_label, value="", definition=prop_desc))
        
        section.append(my_section)



def process_template_folder(input_folder, output_folder=None):
    # Create the output folder based on the input folder name
    if output_folder is None:
        output_folder = f"{input_folder}-odml"
    Path(output_folder).mkdir(exist_ok=True)
    
    # List all JSON files in the specified input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            # Construct the full path for both input and output files
            input_path = os.path.join(input_folder, file_name)
            output_file_name = os.path.splitext(file_name)[0] + ".xml"
            output_path = os.path.join(output_folder, output_file_name)
            
            # Create a new odML Document
            odml_doc = odml.Document(author="Reema Gupta", version="1.0")
            
            # Load the JSON template
            with open(input_path, 'r') as file:
                cedar_template = json.load(file)
                
            # Initialize the main section
            main_section = odml.Section(file_name.replace("-template.json", ""), definition=cedar_template.get("description", ""))
            
            # Convert the CEDAR template properties
            convert_properties(cedar_template["properties"], cedar_template["_ui"], main_section)
            
            # Add the main section to the odML document
            odml_doc.append(main_section)
            
            # Save the odML document to a file
            XMLWriter(odml_doc).write_file(output_path, local_style=True)
            
            print(f"Processed {file_name} -> {output_file_name}")

if __name__ == "__main__":

    input_folder_path = "templates-cedar/in2pb-templates/"
    output_folder_path = "templates-odml/in2pb-templates/"
    print(f"Input folder: {input_folder_path}")
    print(f"Output folder: {output_folder_path}")

    process_template_folder(input_folder_path, output_folder_path)
