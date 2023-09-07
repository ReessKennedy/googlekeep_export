import gkeepapi
import json
import os
from creds import USERNAME, PASSWORD

def convert_to_json_safe(data):
    if isinstance(data, (str, int, float, bool, type(None))):
        return data
    elif isinstance(data, dict):
        return {key: convert_to_json_safe(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_to_json_safe(item) for item in data]
    else:
        return str(data)  # Convert other types to strings

def debug_print_notes():
    try:
        # Create the Keep client
        keep = gkeepapi.Keep()

        # Logging into the app account
        success = keep.login(USERNAME, PASSWORD)

        # Fetch notes
        notes = keep.find(archived=False, trashed=False, pinned=False)

        debug_data = []

        for note in notes:
            note_dict = vars(note)

            # Include information about note.images
            note_dict['images'] = [vars(image) for image in note.images]

            # Include information about note.images.blob
            for image in note.images:
                if hasattr(image, 'blob'):
                    image.blob_info = vars(image.blob)
                else:
                    image.blob_info = None

            debug_data.append(convert_to_json_safe(note_dict))

        # Define the output file path
        output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debug_output.json')

        # Write the debug data to the JSON file with indentation for readability
        with open(output_file, 'w') as outfile:
            json.dump(debug_data, outfile, indent=4)

        # Sync with Google Keep
        keep.sync()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    debug_print_notes()
