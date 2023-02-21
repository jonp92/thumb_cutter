![Flexi-Rex-improved](https://user-images.githubusercontent.com/35941065/220163684-c806fe24-13ac-4221-b86e-5c6fe68b9d73.png)
# thumb_cutter
A small Python program to strip thumbnails from .gcode files and save them as a .png. Then it will upload to a server using SCP.

The purpose of this program for me is to enable notifications to be sent to my phone when starting a new print with a .gcode thumbnail attachment. Using a URL pointing to my webserver, it host the .png image of the .gcode file to be printed.

So far this is only tested using PrusaSlicer and Klipper/Moonraker.

To allow the program to find the filename for matching purposes added the following to your Start G-code exactly.

;filename:{input_filename_base}/

config.conf will also need to be present in the working directory and configured for the application to run correctly.
