import os
import json
import shutil

import gkeepapi
import requests
import wget

from config import USERNAME, PASSWORD, DOWNLOAD_URL, DOWNLOAD_FOLDER

if __name__ == '__main__':
    # Create the Keep client
    keep = gkeepapi.Keep()

    # Log into the app account
    success = keep.login(USERNAME, PASSWORD)

    # Fetch all the available notes
    notes = keep.find(archived=False, trashed=False, pinned=False)

    # Iterate through notes
    for note in notes:
        filetime = note.timestamps.created
        # Format the time as YYYYMMDD_HHMMSS
        filetimestring = filetime.strftime('%Y%m%d_%H%M%S')

        # Get the attachment count for this note
        attachment_count = len(note.images)

        # Iterate through images in the note
        for i, image in enumerate(note.images):
            # Generate unique image name based on the note's creation date, index, and attachment count
            image_name = f"{filetimestring}_{i + 1}"
            if attachment_count > 1:
                image_name += f"_{attachment_count}"

            # Add the file extension
            image_name += ".png"

            # Create the full URL for the image
            image_url = DOWNLOAD_URL + image_name

            # Create the full path for saving the image
            image_path = os.path.join(DOWNLOAD_FOLDER, image_name)

            # Check if the image already exists, and skip download if it does
            if not os.path.exists(image_path):
                try:
                    blob = note.images[i]
                    keepimagelink = keep.getMediaLink(blob)
                    wget.download(keepimagelink, image_path)
                    print(f"Downloaded: {image_name}")
                except Exception as e:
                    print(f"Failed to download: {image_name} (Error: {str(e)})")
            else:
                print(f"Image already exists: {image_name}")
