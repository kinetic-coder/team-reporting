import json

def get_settings(filename: str):

    # Open the settings/secrets.json file in read mode
    with open(filename, 'r') as f:
        
        # Load the JSON data from the file into a Python dictionary
        secrets = json.load(f)

        return secrets