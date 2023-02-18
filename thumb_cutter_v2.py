import os
import base64
import re
import time
import configparser
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith('.gcode'):
            with open(event.src_path, 'r') as f:
                data = f.read()

            pattern = r'; thumbnail begin 500x500 \d{5,}(.+); thumbnail end'
            match = re.search(pattern, data, re.DOTALL)
            if match:
                thumbnail_data = match.group(1).strip()
                thumbnail_data = re.sub(r'^; ', '', thumbnail_data, flags=re.MULTILINE)
                thumbnail_data = base64.b64decode(thumbnail_data)

                # Set the output filename to a fixed string or read from the config file
                output_path = os.path.join(output_dir, f'{filename}.png')

                with open(output_path, 'wb') as f:
                    f.write(thumbnail_data)
                print(f'Saved thumbnail as {output_path}')

                # Copy the file to the remote server using scp

                scp_command = ['scp', '-P', port, output_path, f'{username}@{server}:{remote_dir}']
                subprocess.run(scp_command)


if __name__ == '__main__':
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get the variables from the configuration file
    input_dir = config.get('directories', 'input_dir')
    output_dir = config.get('directories', 'output_dir')
    username = config.get('remote', 'username')
    server = config.get('remote', 'server')
    remote_dir = config.get('remote', 'remote_dir')
    port = config.get('remote', 'port', fallback='22')
    filename = config.get('output', 'filename', fallback='thumbnail')
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
