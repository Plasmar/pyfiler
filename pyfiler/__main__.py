from pyfiler.setup_worker import SetupWorker
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import os
import json
import time


class MyHandler(FileSystemEventHandler):
    """subclass of FileSystemEventHandler, implements on_modified()."""
    def on_modified(self, event):
        new_files = os.listdir(watch_dir)
        prefix_options = config_obj.keys()

        for new_file in new_files:
            new_file = str(new_file)
            for prefix in prefix_options:
                prefix = str(prefix)
                if new_file.startswith(prefix):
                    srcpath = watch_dir + '/' + new_file
                    dstpath = config_obj[prefix] + '/' + new_file
                    os.rename(srcpath, dstpath)
                    print("[*] successfully renamed:")
                    print("[*] src: " + srcpath)
                    print("[*] dest:  " + dstpath)



def main():
    """the start of the program."""
    # specify the source dir to watch over
    watch_dir = '/Users/cameron.merrick/Downloads'

    # load in the config file with the filetypes and routes defined
    with open("./data/config.json", "r") as read_file:
        config_obj = json.load(read_file)

    # create the object that scans the filesystem and creates necessary dirs from the config
    setupworker = SetupWorker(config_obj)
    needed_dirs = setupworker.exec_setup_process(dry_run=True) # defaults to true to be safe
    setupworker.create_missing_dirs(needed_dirs)
    print("[*] made it through the main method successfully.")

    # now set up the wathdog worker to watch over the directory for changes (new downloaded files)
    myhandler = MyHandler()
    observer = Observer()

    # next give the observer the MyHandler object which is subclass of Filesystemeventhandler
    observer.schedule(myhandler, watch_dir, recursive=False)
    # start it up
    observer.start()

    # create the loop that will enable the watchdog worker to remain alive
    # try:
        # while True:
            # # make it poll the watch_dir every 10 seconds
            # time.sleep(10)
    # except KeyboardInterrupt:
        # observer.stop()
    # observer.join




if __name__ == '__main__':
    main()
