#!/usr/bin/python

import os

BACKUP_DIR = os.path.expanduser("~/.remarkable-tweak/backup/")
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

WORKING_DIR = os.path.expanduser("~/.remarkable-tweak/temp/")
if not os.path.exists(WORKING_DIR):
    os.makedirs(WORKING_DIR)

CONFIG_DIR = os.path.expanduser("~/.remarkable-tweak/config/")
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)
