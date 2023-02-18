import os
import base64
import time

# Path to folder to monitor
folder_path = '/home/pi/printer_data/gcodes/test'

# Path to folder to save output files
output_path = '/home/pi/printer_data/gcodes/thumbs'

# Extension to monitor

ext = '.gcode'

# Start monitoring folder for changes
while True:
    for file_name in os.listdir(folder_path):
        if file_name.endswith(ext):
            # Read the contents of the file
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r") as f:
                contents = f.read()

            # Find the thumbnail data between "thumbnail begin 500x500" and "thumbnail end"
            start_index = contents.find("thumbnail begin 500x500 ?????")
            end_index = contents.find("thumbnail end")
            if start_index != -1 and end_index != -1:
                thumbnail_data = contents[start_index:end_index]
                thumbnail_data = thumbnail_data.replace(";", "")
                thumbnail_data = thumbnail_data.encode("utf-8")

                # Decode the thumbnail data using base64
                thumbnail_data = base64.b64decode(thumbnail_data)

                # Generate filename for output file
                start_index = contents.find(";filename:")
                end_index = contents.find("/", start_index)
                file_name = contents[start_index+len(";filename:"):end_index]

                # Save the decoded thumbnail as a PNG file
                output_file_path = os.path.join(output_path, file_name + ".png")
                with open(output_file_path, "wb") as f:
                    f.write(thumbnail_data)

    # Wait for a few seconds before checking again
    time.sleep(5)
