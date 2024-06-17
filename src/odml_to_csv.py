import os
from odmltables import OdmlCsvTable

# Define the paths for input (odml_templates) and output (csv_templates) folders
input_folder = 'templates-odml/in2pb-templates'
output_folder = 'templates-csv/in2pb-templates/'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List all files in the input folder
input_files = os.listdir(input_folder)

# Iterate through each file and convert to CSV format
for file in input_files:
    # Check if the file is an odML file 
    if file.endswith('.xml'):
        # Load the odML file
        odml_file_path = os.path.join(input_folder, file)
        my_table = OdmlCsvTable()
        my_table.load_from_file(odml_file_path)

        # Create the corresponding CSV file in the output folder
        csv_file_path = os.path.join(output_folder, file[:-5] + '.csv')
        my_table.write2file(csv_file_path)

