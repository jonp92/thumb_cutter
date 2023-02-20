# thumb_cutter
A small Python program to strip thumbnails from .gcode files and save them as a .png. Then it will upload to a server using SCP.

The purpose of this program for me is to allow me to send notification to my phone when starting a new print with an attachment URL pointing to my webserver. This url points to the .png image of the .gcode file to be printed.

So far this is only tested using PrusaSlicer and Klipper/Moonraker.

To allow the program to find the filename for matching purposes added the following to your Start G-code exactly.

;filename:{input_filename_base}/
