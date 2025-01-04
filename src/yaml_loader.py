import os
import yaml

def load_yaml_files(directory):
    yaml_data = {}
    
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.yaml'):
            file_path = os.path.join(directory, filename)
            
            # Open and parse each YAML file
            with open(file_path, 'r') as file:
                try:
                    # Load the YAML content
                    yaml_content = yaml.safe_load(file)
                    
                    # Store it in the dictionary with the filename as the key (w/o the extension)
                    yaml_data[os.path.splitext(filename)[0]] = yaml_content
                except yaml.YAMLError as err:
                    print(f"Error parsing YAML file {filename}: {err}")
    
    return yaml_data
