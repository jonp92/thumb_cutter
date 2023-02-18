import os
import base64
import re
import time
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith('.gcode'):
            with open(event.src_path, 'r') as f:
                data = f.read()

            pattern = r'; thumbnail begin.* \d{5,}(.+); thumbnail end'
            match = re.search(pattern, data, re.DOTALL)
            if match:
                thumbnail_data = match.group(1).strip()
                thumbnail_data = re.sub(r'^; ', '', thumbnail_data, flags=re.MULTILINE)
                thumbnail_data = base64.b64decode(thumbnail_data)

                pattern = r';filename:(.+?)/'
                match = re.search(pattern, data)
                if match:
                    filename = match.group(1).strip()
                    output_path = os.path.join(output_dir, filename + '.png')

                    with open(output_path, 'wb') as f:
                        f.write(thumbnail_data)
                    print(f'Saved thumbnail as {output_path}')


if __name__ == '__main__':
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get the directory paths from the configuration file
    input_dir = config.get('directories', 'input_dir')
    output_dir = config.get('directories', 'output_dir')

    # Create the FileHandler and Observer objects
    event_handler = FileHandler()
    observer = Observer()

    # Schedule the observer to monitor the input directory
    observer.schedule(event_handler, input_dir, recursive=True)

    # Start the observer
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
