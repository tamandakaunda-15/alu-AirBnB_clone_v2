#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run

env.hosts = ["3.91.244.104", "204.236.213.151"]

def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isfile(archive_path):
        print("File does not exist: {}".format(archive_path))
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed:
        print("Failed to put file: {}".format(file))
        return False

    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
        print("Failed to remove old release directory: {}".format(name))
        return False

    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        print("Failed to create release directory: {}".format(name))
        return False

    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed:
        print("Failed to extract archive: {}".format(file))
        return False

    if run("rm /tmp/{}".format(file)).failed:
        print("Failed to remove temporary file: {}".format(file))
        return False

    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed:
        print("Failed to move files: {}".format(name))
        return False

    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed:
        print("Failed to remove web_static directory: {}".format(name))
        return False

    if run("rm -rf /data/web_static/current").failed:
        print("Failed to remove current symlink")
        return False

    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed:
        print("Failed to create new symlink")
        return False

    print("Deployment successful!")
    return True
