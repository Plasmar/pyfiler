# pyfiler
## Python Directory Secretary

### Overview

This is a seemingly trivial little automation utility, however the potential use cases and possibilities that it unlocks are virtually limitless.

On face value, it is a command line utility that handles filesystem automation (copying and moving files from directory to directory, potentially renaming, appending dates, compressing, etc).  It comes fully packaged with [setup.py](http://setup.py) and is left intentionally somewhat-barebones in a deliberate attempt to signal an invitation for others to collaborate.

### How it Works

The way it works is by leveraging the `watchdog` library.  Specifically the `watchdog.observer.Observer` class and the `watchdog.events.FileSystemEventHandler` classes.  These enable you to monitor specified directories and specify various surveillance configurations for what to do when change events (CRUD) occur.

I designed the initial version of `pyfiler` to look for "rules" in a json configuration file and you will see an example of how it looks in the screenshot.

You can define the directories you wish to use in your config file, and a `setup_worker` class runs before directory monitoring  + filing begins which goes and creates the dirs if they do not exist (but checks if they do first)

Note* there is a -d —dry option to enable dry-runs if you dont want the `setup_worker` to create dirs (also depicted in the screenshot).

### Prefixes

Here is where it gets kick ass.  Set up directories that you often move files to after they are saved to, say, your Downloads folder (the value), and define a matching prefix (the key) to construct your configuration json file.

Now, whenever you click on that PDF, or that image and want to save it, whatever it is related to just prefix it with the appropriate characters you defined and as soon as it hits your downloads folder (or wherever you have defined as the `watch_dir` (defaults to Downloads) it will be instantly filed.  Like a 24 hour round the clock filing secretary that never sleeps and keeps your  filesystem spotlessly clean.

### Possibilities

Ideas for Improvement:

- append/prepend a datetime stamp to each file in addition to the filing operations
- instead of by prefix, sort by filetype
- enable recursion - have it sweep the whole filesystem instead of a single directory to watch. 

Inline-style: 
![alt text](https://github.com/Plasmar/pyfiler/blob/master/pyfiler_usage.png "pyfiler_usage.png")



