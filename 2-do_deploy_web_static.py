#!/usr/bin/python3
"""
This module contains the function do_deploy that distributes an archive
to your web servers.
"""

from fabric.api import env, put, run
import os

# Define the IPs of your web servers
env.hosts = ['3.91.244.104', '204.236.213.151']

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    Args:
        archive_path (str): The path to the archive to distribute.
    Returns:
        bool: True if all operations have been done correctly, otherwise False.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        
        # Extract the archive filename without extension
        archive_file = archive_path.split("/")[-1]
        archive_folder = "/data/web_static/releases/" + archive_file.split(".")[0]

        # Create the directory to uncompress the archive
        run("mkdir -p {}".format(archive_folder))

        # Uncompress the archive
        run("tar -xzf /tmp/{} -C {}".format(archive_file, archive_folder))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_file))

        # Move contents out of web_static
        run("mv {}/web_static/* {}/".format(archive_folder, archive_folder))
        run("rm -rf {}/web_static".format(archive_folder))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server
        run("ln -s {} /data/web_static/current".format(archive_folder))

        return True

    except Exception:
        return False
