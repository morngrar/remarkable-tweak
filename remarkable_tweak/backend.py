#!/usr/bin/python

"""Backend, separating ssh-code from frontend"""

import os

from remarkable_tweak import ssh
from remarkable_tweak import system


def clean_working_dir():
    for f in os.listdir(system.WORKING_DIR):
        path = os.path.join(system.WORKING_DIR, f)

        if os.path.isfile(path):
            os.unlink(path)

def download():
    connection = ssh.RemarkableConnection(password())
    connection.dump_templates(system.WORKING_DIR)

def upload(path_list):
    connection = ssh.RemarkableConnection(password())
    connection.purge_templates()
    connection.upload_templates(path_list)

    clean_working_dir()

def update_password(password):
    path = os.path.join(system.CONFIG_DIR, "password.cfg")

    if os.path.isfile(path):
        os.unlink(path)

    with open(path, "w+") as f:
        f.write(password)

def password():
    path = os.path.join(system.CONFIG_DIR, "password.cfg")

    with open(path, "r") as f:
        password = f.read()

    return password


