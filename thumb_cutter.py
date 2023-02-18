import os
import base64

# Specify the folder to monitor and the folder to save the images
monitor_folder = "/home/pi/printer_data/gcodes/test"
save_folder = "/home/pi/printer_data/gcodes/thumbs"

while True:
    # Get a list of all the files in the monitor folder
    files = os.listdir(monitor_folder)

    # Check each file for .gcode extension
    for file in files:
        if file.endswith(".gcode"):
            # Open the file and read its contents
            with open(os.path.join(monitor_folder, file), "r") as f:
                data = f.read()

            # Find the thumbnail data between "thumbnail begin 500x500" and "thumbnail end"
            start_index = data.find("thumbnail begin 500x500 ?????") + len("thumbnail begin 500x500")
            end_index = data.find(";thumbnail end", start_index)
            thumb_data = data[start_index:end_index].strip()

            # Decode the thumbnail data using base64
            thumb_bytes = base64.b64decode(thumb_data)

            # Find the filename between ';filename: and /'
            start_index = data.find(";filename:") + len(";filename:")
            end_index = data.find("/", start_index)
            filename = data[start_index:end_index].strip()

            # Save the thumbnail as a .png file in the save folder
            with open(os.path.join(save_folder, filename + ".png"), "wb") as f:
                f.write(thumb_bytes)

    # Wait for 1 second before checking the folder again
    time.sleep(1)
