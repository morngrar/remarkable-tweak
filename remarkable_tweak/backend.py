#!/usr/bin/python

"""Backend, separating ssh-code from frontend"""

import ssh
import system

PASSWORD = ""


def download():
    connection = ssh.RemarkableConnection(PASSWORD)
    connection.dump_templates(system.WORKING_DIR)

def upload(path_list):
    connection = ssh.RemarkableConnection(PASSWORD)
    connection.purge_templates()
    connection.upload_templates(path_list)
