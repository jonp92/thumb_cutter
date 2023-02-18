import os
import base64

WATCH_FOLDER = '/home/pi/printer_data/gcodes/test'
OUTPUT_FOLDER = 'home/pi/printer_data/gcodes/thumbs'

def decode_thumbnail(data):
    lines = data.split('\n')
    decoded_lines = []
    for line in lines:
        if line.startswith(';'):
            line = line[1:].strip()
            decoded_line = base64.b64decode(line)
            decoded_lines.append(decoded_line)
    return b'\n'.join(decoded_lines)

def extract_filename(gcode_file):
    with open(gcode_file, 'r') as f:
        for line in f:
            if ';filename:' in line:
                start = line.index(';filename:') + len(';filename:')
                end = line.index('/', start)
                filename = line[start:end].strip()
                return filename
    return None

def process_gcode_file(gcode_file):
    with open(gcode_file, 'r') as f:
        data = f.read()
    start = data.find('thumbnail begin 500x500 ?????')
    if start == -1:
        return
    start += len('thumbnail begin 500x500 ?????')
    end = data.find('thumbnail end', start)
    if end == -1:
        return
    thumbnail_data = data[start:end].strip()
    decoded_data = decode_thumbnail(thumbnail_data)
    filename = extract_filename(gcode_file)
    if filename is None:
        return
    output_file = os.path.join(OUTPUT_FOLDER, filename + '.png')
    with open(output_file, 'wb') as f:
        f.write(decoded_data)
    print('Saved thumbnail from', gcode_file, 'to', output_file)

def monitor_folder():
    files = set(os.listdir(WATCH_FOLDER))
    while True:
        new_files = set(os.listdir(WATCH_FOLDER)) - files
        for new_file in new_files:
            if new_file.endswith('.gcode'):
                gcode_file = os.path.join(WATCH_FOLDER, new_file)
                process_gcode_file(gcode_file)
        files = set(os.listdir(WATCH_FOLDER))

if __name__ == '__main__':
    monitor_folder()
