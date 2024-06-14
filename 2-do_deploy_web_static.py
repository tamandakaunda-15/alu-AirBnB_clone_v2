#!/usr/bin/python3

from fabric.api import env, put, run
import os

env.hosts = ["3.91.244.104", "204.236.213.151"]

def do_deploy(archive_path):
    if not os.path.isfile(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        archive_filename = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_filename)[0]
        release_dir = f"/data/web_static/releases/{archive_no_ext}"

        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder
        run(f"mkdir -p {release_dir}")
        run(f"tar -xzf /tmp/{archive_filename} -C {release_dir}")

        # Remove the archive from the web server
        run(f"rm /tmp/{archive_filename}")

        # Delete the symbolic link
        run("rm -f /data/web_static/current")

        # Create a new symbolic link
        run(f"ln -s {release_dir} /data/web_static/current")

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Example usage
if __name__ == "__main__":
    archive_path = "versions/web_static_20210615000000.tgz"
    if do_deploy(archive_path):
        print("Deployment succeeded.")
    else:
        print("Deployment failed.")

