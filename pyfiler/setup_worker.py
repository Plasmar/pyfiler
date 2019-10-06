import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



class SetupWorker:
    """Uses cconfig to prep  filesystem  structure and support potential future mods."""
    def __init__(self, conf_dict):
        if conf_dict is None:
            raise Exception("[*] no configuration dict provided")

        self.conf_dict = conf_dict

    def exec_setup_process(self, dry_run=False):
        """Orchestrates the remaining setup steps accounting for dry_run."""
        self.missing_dirs = []

        if dry_run is False or dry_run == '':
            self.dry_run = False
        elif dry_run is not True or False:
                raise Exception("[*] dry run can only be a boolean value")
        else:
            self.dry_run = dry_run

        # check each dest path in case it exists to avoid duplicatiaon
        for self.dest_dir in self.conf_dict.values():
            if not os.path.isdir(self.dest_dir):
                self.missing_dirs.append(self.dest_dir)
                print("[*] missing dir at path: " + self.dest_dir)

        print("[*] filesystem prep complete. " + str(len(self.missing_dirs)) + " new dirs needed")

        # reset missing dirs to empty list if dry run
        if self.dry_run is True:
            print("[*] dry run - returning empty list of missing dirs")
            self.missing_dirs = []

        return self.missing_dirs


    def create_missing_dirs(self, dir_list):
        """Self explanatory."""
        try:
            for dir in dir_list:
                os.mkdir(dir)
                print("[*] successfully created dir at {}".format(dir))
        except(OSError) as e:
            print(e)

        return



if __name__ == '__main__':
    """the start of the program."""
    with open("./data/config.json", "r") as read_file:
        config_obj = json.load(read_file)

    setup_worker = SetupWorker(config_obj)
    needed_dirs = setup_worker.exec_setup_process(dry_run=True)
    setup_worker.create_missing_dirs(needed_dirs)

