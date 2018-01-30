#!/usr/bin/python

import os
import platform

class IncompatibleSystem(Exception):
    pass



if platform.system() == "Linux":
    _main_dir = os.path.expanduser("~/.remarkable-tweak/")
elif platform.system() == "Darwin":
    # iOS
    _main_dir = os.path.expanduser(
        "~/Library/Application support/remarkable-tweak/"
    )
elif platform.system() == "Windows":
    _main_dir = os.getenv("LOCALAPPDATA")
else:
    raise IncompatibleSystem


BACKUP_DIR = os.path.join(_main_dir, "backup/")
WORKING_DIR = os.path.join(_main_dir, "temp/")
CONFIG_DIR =  os.path.join(_main_dir, "config/")


if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

if not os.path.exists(WORKING_DIR):
    os.makedirs(WORKING_DIR)

if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)
