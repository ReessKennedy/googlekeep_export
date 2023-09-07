import json
import gkeepapi
import os
import logging
from pathlib import Path
from config import USERNAME, PASSWORD

# Define constants or configuration settings here
JSON_DIRECTORY = 'exported_json'
LOG_FILE = '_keep_export.log'

def setup_logging():
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def export_keep_notes():
    try:
        # Create the Keep client
        keep = gkeepapi.Keep()

        # Logging into the app account
        success = keep.login(USERNAME, PASSWORD)

        # Fetch notes
        notes = keep.find(archived=False, trashed=False, pinned=False)

        # Create a dictionary to store notes by date
        notes_by_date = {}

        for note in notes:
            filetime = note.timestamps.created
            note_date = filetime.date()

            # Create or append to the list of notes for this date
            if note_date not in notes_by_date:
                notes_by_date[note_date] = []

            # Initialize note data
            note_data = {
                'created_at': str(note.timestamps.created),
                'title': note.title,
                'body': note.text,
                'tags': [keep.getLabel(label).name for label, val in list(note.labels._labels.items())] if len(note.labels) > 0 else [],
            }

            # Initialize a list to store image data
            image_data_list = []

            # Iterate through images in the note
            for i, image in enumerate(note.images):
                # Generate unique image name based on the note's creation date and index
                image_name = f"{filetime.strftime('%Y%m%d_%H%M%S')}_{i + 1}"

                # Images Info
                image_mimetype = image.blob._mimetype if hasattr(image.blob, '_mimetype') else None
                image_width = image.blob._width if hasattr(image.blob, '_width') else None
                image_height = image.blob._height if hasattr(image.blob, '_height') else None
                image_byte_size = image.blob._byte_size if hasattr(image.blob, '_byte_size') else None
                image_extracted_text = image.blob._extracted_text if hasattr(image.blob, '_extracted_text') else None

                # Get the media link for the image
                blob = note.images[i]
                keepimagelink = keep.getMediaLink(blob)

                # Append image data to the list
                image_data_list.append({
                    'image_name': image_name,
                    'mimetype': image_mimetype,
                    'width': image_width,
                    'height': image_height,
                    'byte_size': image_byte_size,
                    'extracted_text': image_extracted_text,
                    'image_url': keepimagelink,
                })

            # Add image data to the note_data if it exists
            if image_data_list:
                note_data['images'] = image_data_list

            # Append the note_data to the list of notes for this date
            notes_by_date[note_date].append(note_data)

        # Ensure the output directory exists
        Path(JSON_DIRECTORY).mkdir(parents=True, exist_ok=True)

        # Iterate through notes by date and write to separate JSON files
        for date, note_list in notes_by_date.items():
            date_str = date.strftime('%Y_%m_%d')
            json_filename = os.path.join(JSON_DIRECTORY, f'{date_str}.json')

            # Create a JSON structure with metadata and notes
            json_data = {
                'metadata': {
                    'daily_total': len(note_list)
                },
                'notes': note_list
            }

            # Write the data to a JSON file with indentation for readability
            with open(json_filename, 'w') as outfile:
                json.dump(json_data, outfile, indent=4)

        # Sync with Google Keep
        keep.sync()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    setup_logging()
    export_keep_notes()
