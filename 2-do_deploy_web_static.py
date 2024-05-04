#!/usr/bin/python3
""" Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.user = "ubuntu"
env.hosts = ['52.73.243.18', '35.153.57.40']


def do_deploy(archive_path):
    """Distributes an archive to a web server.
       Returns True if successful otherwise false
    """
    if os.path.isfile(archive_path) is False:
        return False
    fullFile = archive_path.split("/")[-1]
    folder = fullFile.split(".")[0]

    if put(archive_path, "/tmp/{}".format(fullFile)).failed is True:
        print("Uploading archive to /tmp/ failed")
        return False

    if run("rm -rf /data/web_static/releases/{}/".
           format(folder)).failed is True:
        print("Deleting folder with archive(if already exists) failed")
        return False

    if run("mkdir -p /data/web_static/releases/{}/".
           format(folder)).failed is True:
        print("Creating new archive folder failed")
        return False

    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(fullFile, folder)).failed is True:
        print("Uncompressing archive to failed")
        return False

    if run("rm /tmp/{}".format(fullFile)).failed is True:
        print("Deleting archive from /tmp/ directory dailed")
        return False

    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".
           format(folder, folder)).failed is True:
        print("Moving content to archive folder before deletion failed")
        return False

    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(folder)).failed is True:
        print("Deleting web_static folder failed")
        return False

    if run("rm -rf /data/web_static/current").failed is True:
        print("Deleting 'current' folder failed")
        return False

    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(folder)).failed is True:
        print("Creating new symbolic link to new code version failed")
        return False

    print("New version deployed!")
    return True
