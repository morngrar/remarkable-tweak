#!/usr/bin/python3

"""This module handles ssh connections to the remarkable."""

import paramiko   # dependency installable from pip

class SSHCommandError(Exception):
    pass

def output_exec(client, command):
    """Wraps exec_command, raises exception on error, returns output."""

    stdin, stdout, stderr = client.exec_command(command)
    error_content = stderr.read()

    if error_content:
        raise SSHCommandError(error_content)

    return stdout.readlines()


class RemarkableConnection():
    """Class for ssh-connections to the reMarkable."""

    def __init__(self, password, on_wifi=False):
        self.password = password
        self.on_wifi = on_wifi
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )
        self._connect()
        self.template_directory = "/usr/share/remarkable/templates/"


    def _connect(self):
        if self.on_wifi:
            host = "remarkable"
        else:
            host = "10.11.99.1"

        self.ssh_client.connect(
            hostname=host,
            username="root",
            password=self.password
        )

    def get_template_list(self):
        """Returns a list of filenames of templates on the remarkable."""

        template_list = output_exec(
            ssh_client,
            "ls /usr/share/remarkable/templates"
        )
        template_list = [e.strip() for e in template_list]

        return template_list

    def make_template_paths(self, filenames):
        """Takes list of filenames, and returns list of full paths
        for templates on the remarkable.
        """

        paths_list = [      # The format function takes care of whitespace
            "'{0}'".format( # in filenames
                "".join((self.template_directory, e))
            )
            for e in filenames
        ]

        return paths_list

    def dump_templates(self, local_directory):
        """Downloads all templates from the reMarkable to local dir."""

        template_names = self.get_template_list()
        templates = 
        with self.ssh_client.open_sftp() as ftp_client:
            pass
