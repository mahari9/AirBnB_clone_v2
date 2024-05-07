#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py) that creates and
distributes an archive to your web servers, using the function deploy
"""

from fabric.api import env, local, put, run
from os import path
from datetime import datetime

env.hosts = ['52.73.243.18', '35.153.57.40']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns the archive path if successful, None otherwise.
    """
    try:
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_path = 'versions/web_static_{}.tgz'.format(now)
        local('mkdir -p versions')
        local('tar -cvzf {} web_static'.format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
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


def deploy():
    """
    Calls do_pack() function and store the path of the created archive.
    Returns False if no archive has been created.
    Calls do_deploy(archive_path) function using the new path of the new archive.
    Returns the return value of do_deploy.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
