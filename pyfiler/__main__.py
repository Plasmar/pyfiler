from pyfiler.setup_worker import SetupWorker
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import os
import json
import argparse
import time

class MyHandler(FileSystemEventHandler):
    """subclass of FileSystemEventHandler, implements on_modified()."""

    def __init__(self, watch_dir, config_obj):
        self.watch_dir = watch_dir
        self.config_obj = config_obj

    def on_modified(self, event):
        """a method triggered when a file is saved or moved into the dir"""
        prefix_options = self.config_obj.keys()

        for new_file in os.listdir(self.watch_dir):
            new_file = str(new_file)
            for prefix in prefix_options:
                prefix = str(prefix)
                if new_file.startswith(prefix):
                    srcpath = self.watch_dir + '/' + new_file
                    dstpath = self.config_obj[prefix] + '/' + new_file
                    os.rename(srcpath, dstpath)
                    print("[*] successfully renamed:")
                    print("[*] src: " + srcpath)
                    print("[*] dest:  " + dstpath)

def main(args):
    # specify the source dir to watch over
    if args.watch_dir is not None:
        watch_dir = args.watch_dir
    else:
        watch_dir = "/Users/cameron.merrick/Downloads/test"

    # load in the config file with the filetypes and routes defined
    with open("/Users/cameron.merrick/code/pyfiler/pyfiler/data/config.json", "r") as read_file:
        config_obj = json.load(read_file)

    # create the object that scans the filesystem and creates necessary dirs from the config
    setupworker = SetupWorker(config_obj)
    needed_dirs = setupworker.exec_setup_process(dry_run=args.dry) # defaults to true to be safe
    setupworker.create_missing_dirs(needed_dirs)
    print("[*] made it through the main method successfully.")

    # now set up the wathdog worker to watch over the directory for changes (new downloaded files)
    myhandler = MyHandler(watch_dir, config_obj)
    observer = Observer()

    # next give the observer the MyHandler object which is subclass of Filesystemeventhandler
    observer.schedule(myhandler, watch_dir, recursive=True)
    # start it up
    observer.start()

    # create the loop that will enable the watchdog worker to remain alive
    try:
        while True:
            # poll watch_dir every 10 sec unless default changed in CLI args
            time.sleep(int(args.interval))
    except KeyboardInterrupt:
        observer.stop()
    observer.join



if __name__ == '__main__':
    """the start of the program."""
    # create the argparser and create some optional arguments
    parser = argparse.ArgumentParser(description='main method to invoke pyfiler', add_help=True)
    parser.add_argument('-w', '--watch_dir', type=str, help='specify a  directory to monitor', metavar='')
    parser.add_argument('-d', '--dry', action='store_true', help='toggle the script to run in dry_run mode')
    parser.add_argument('-i', '--interval', type=int, default=10, help='interval (seconds) between poll requests by the watcher', metavar='')

    # add an output volume control M.E. argument group
    me_group = parser.add_mutually_exclusive_group()
    me_group.add_argument('-v', '--verbose', action='store_true', help='toggle verbose outputs to stdout')
    me_group.add_argument('-q', '--quiet', action='store_true', help='redirect stdout messages to log file')

    # now collect all the arguments and pass the object to main()
    args = parser.parse_args()
    main(args)
