#!/usr/bin/python

"""Backend, separating ssh-code from frontend"""

import ssh
import os
import shutil

import system

PASSWORD = ""

def clean_working_dir():
    for f in os.listdir(system.WORKING_DIR):
        path = os.path.join(system.WORKING_DIR, f)

        if os.path.isfile(path):
            os.unlink(path)

def download():
    connection = ssh.RemarkableConnection(PASSWORD)
    connection.dump_templates(system.WORKING_DIR)

def upload(path_list):
    connection = ssh.RemarkableConnection(PASSWORD)
    connection.purge_templates()
    connection.upload_templates(path_list)

    clean_working_dir()


