from .setup_worker import SetupWorker
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import os
import json

config_obj = json.loads('./data/config.json')
watch_dir = '/Users/cameron.merrick/Downloads'

class my_handler(FileSystemEventHandler):
    """subclass of FileSystemEventHandler, implements on_modified()."""
    def on_modified(self, event):
        new_files = os.listdir(watch_dir)
        prefix_options = config_obj.keys()

        for new_file in new_files:
            new_file = str(new_file)
            for prefix in prefix_options:
                prefix = str(prefix)
                if new_file.startswith(prefix):
                    pass
                    # TRUE! then we move it to its corresponding destination

def main():
    setupworker = SetupWorker(config_obj)
    needed_dirs = setupworker.exec_setup_process(dry_run=True)
    setupworker.create_missing_dirs(needed_dirs)
    print("[*] made it through the main method successfully.")

if __name__ == '__main__':
    main()
