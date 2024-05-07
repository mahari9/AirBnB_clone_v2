#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py) that creates and
distributes an archive to your web servers, using the function deploy
"""

from fabric.api import env, local, put, run
<<<<<<< HEAD
import os.path
=======
from os import path
>>>>>>> 32bf1265d6012c280df750f841b040cbeb5379c4
from datetime import datetime

env.hosts = ['52.73.243.18', '35.153.57.40']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

<<<<<<< HEAD

=======
>>>>>>> 32bf1265d6012c280df750f841b040cbeb5379c4
def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns the archive path if successful, None otherwise.
    """
    try:
<<<<<<< HEAD
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if os.path.isdir("versions") is False:
            local("mkdir versions")
        archive_path = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(archive_path))
=======
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_path = 'versions/web_static_{}.tgz'.format(now)
        local('mkdir -p versions')
        local('tar -cvzf {} web_static'.format(archive_path))
>>>>>>> 32bf1265d6012c280df750f841b040cbeb5379c4
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
<<<<<<< HEAD
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    print('New version deployed!')
    return True
=======
    if not path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        archive_file = archive_path.split('/')[-1]
        archive_folder = '/data/web_static/releases/' + archive_file[:-4]

        run('mkdir -p {}'.format(archive_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_file, archive_folder))
        run('rm /tmp/{}'.format(archive_file))
        run('mv {}/web_static/* {}'.format(archive_folder, archive_folder))
        run('rm -rf {}/web_static'.format(archive_folder))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(archive_folder))
        print('New version deployed!')
        return True
    except:
        return False
>>>>>>> 32bf1265d6012c280df750f841b040cbeb5379c4


def deploy():
    """
    Calls do_pack() function and store the path of the created archive.
    Returns False if no archive has been created.
<<<<<<< HEAD
    Calls do_deploy(archive_path) function using the new path of the new
    archive returns the return value of do_deploy.
=======
    Calls do_deploy(archive_path) function using the new path of the new archive.
    Returns the return value of do_deploy.
>>>>>>> 32bf1265d6012c280df750f841b040cbeb5379c4
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
