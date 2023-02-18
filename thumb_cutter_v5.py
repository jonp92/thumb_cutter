import os
import base64
import time

WATCH_FOLDER = "/home/pi/printer_data/gcodes/test"
OUTPUT_FOLDER = "/home/pi/printer_data/gcodes/thumbs"

def extract_thumbnail(gcode_path):
    # Open gcode file and read contents
    with open(gcode_path, 'r') as gcode_file:
        gcode_content = gcode_file.read()

    # Find thumbnail data between "thumbnail begin 500x500" and "thumbnail end"
    start_index = gcode_content.find("thumbnail begin 500x500 32316")
    end_index = gcode_content.find(";thumbnail end", start_index)
    thumbnail_data = gcode_content[start_index:end_index]

    # Extract and decode thumbnail data
    thumbnail_data = thumbnail_data.replace("; ", "")
    thumbnail_data = thumbnail_data.replace("thumbnail begin 500x500", "")
    thumbnail_data = thumbnail_data.replace(";thumbnail end", "")
    thumbnail_data = base64.b64decode(thumbnail_data)

    # Find filename for output
    start_index = gcode_content.find(";filename:")
    end_index = gcode_content.find("/", start_index)
    filename = gcode_content[start_index+len(";filename:"):end_index]

    # Save thumbnail as .png file
    output_path = os.path.join(OUTPUT_FOLDER, filename + ".png")
    with open(output_path, "wb") as output_file:
        output_file.write(thumbnail_data)

def monitor_folder():
    while True:
        # Get list of files in watch folder
        files = os.listdir(WATCH_FOLDER)

        # Check for new .gcode files and extract thumbnails
        for file_name in files:
            if file_name.endswith(".gcode"):
                file_path = os.path.join(WATCH_FOLDER, file_name)
                extract_thumbnail(file_path)

        # Wait for 1 second before checking again
        time.sleep(1)

if __name__ == "__main__":
    monitor_folder()
