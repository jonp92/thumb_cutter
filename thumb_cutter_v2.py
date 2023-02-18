import os
import base64
import re
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        if event.src_path.endswith('.gcode'):
            with open(event.src_path, 'r') as f:
                data = f.read()
            
            pattern = r'thumbnail begin 500x500(.+?)thumbnail end'
            match = re.search(pattern, data, re.DOTALL)
            if match:
                thumbnail_data = match.group(1).strip()
                thumbnail_data = re.sub(r'^;', '', thumbnail_data, flags=re.MULTILINE)
                thumbnail_data = base64.b64decode(thumbnail_data)
                
                pattern = r';filename: (.+?)/'
                match = re.search(pattern, data)
                if match:
                    filename = match.group(1).strip()
                    output_path = os.path.join('/home/pi/printer_data/gcodes/thumbs', filename + '.png')
                    
                    with open(output_path, 'wb') as f:
                        f.write(thumbnail_data)
                    print(f'Saved thumbnail as {output_path}')

if __name__ == '__main__':
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, '/home/pi/printer_data/gcodes', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
