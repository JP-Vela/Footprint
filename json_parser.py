import json

# Function to read and convert JSON file to a dictionary
def read_json_as_dict(file_path):
    try:
        # Open the JSON file
        with open(file_path, 'r') as file:
            # Load the JSON data into a Python dictionary
            data_dict = json.load(file)
        return data_dict
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Check the JSON file for errors.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")