#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to the web servers
"""
from fabric import task
from fabric.api import env
from datetime import datetime
from os.path import exists, isdir

# Replace these with your actual server IP addresses and SSH credentials
env.hosts = ["100.27.4.102","54.165.197.71","54.90.21.58"]
user = "ubuntu"
key_path = "/path/to/your/private/key.pem"
remote_app_path = "/home/ubuntu/"
gunicorn_service_name = "cariba_app"

@task
def deploy(c):
    # Step 1: Archive the app folder
    archive_path = archive_app(c)
    
    # Step 2: Check that archive exists
    if exists(archive_path) is False:
        return False
    
    # Loop through the servers and deploy to each one
    for host in env.hosts:
        c.host = "{}@{}".format(user, host)
        c.connect_kwargs.key_filename = [key_path]
        
        try:
            file_n = archive_path.split("/")[-1]
            no_ext = file_n.split(".")[0]
            
            # Step 3: Copy the app archive to the remote host
            copy_archive_app_to_remote(c, archive_path)
            
            # Step 4: Stop gunicorn app
            stop_gunicorn(c)
            
            # Step 5: Delete previous gunicorn app path if and recreate it
            create_remote_directory(c, no_ext)

            # Step 6: Extract the app archive on the remote host
            extract_app(c, file_n, remote_app_path, no_ext)
            
            # Step 7: Remove the app archive on the remote host
            remove_app_archive(c, file_n)

            # Step 8: Restart the Gunicorn service
            start_gunicorn(c)

            # Step 9: Reload Nginx configuration
            reload_nginx(c)
            
            return True
        except:
            return False

@task
def archive_app(c):
    # Archive the app folder
    """generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            c.local("mkdir versions")
        file_name = "versions/cariba_{}.tgz".format(date)
        c.local("tar -cvzf {} app".format(file_name))
        return file_name
    except:
        return None

@task
def remove_app_archive(c, file_n):
    # Copy the app archive to the remote host
    c.run('rm /tmp/{}'.format(file_n))
    
@task
def create_remote_directory(c, no_ext):
    # Copy the app archive to the remote host
    c.run('rm -rf {}{}/'.format(remote_app_path, no_ext))
    c.run('mkdir -p {}{}/'.format(remote_app_path, no_ext))

@task
def copy_archive_app_to_remote(c, archive_path):
    # Copy the app archive to the remote host
    c.put(archive_path, '/tmp/')

@task
def extract_app(c, file_n, path, no_ext):
    # Extract the app archive on the remote server
    c.run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
    
@task
def remove_extract_app(c, file_n):
    # Extract the app archive on the remote server
    c.run('rm /tmp/{}'.format(file_n))

@task
def start_gunicorn(c):
    # Restart the Gunicorn service on the remote server
    c.sudo(f"systemctl start {gunicorn_service_name}", pty=True)

@task
def stop_gunicorn(c):
    # Restart the Gunicorn service on the remote server
    c.sudo(f"systemctl stop {gunicorn_service_name}", pty=True)

@task
def reload_nginx(c):
    # Reload Nginx configuration on the remote server
    c.sudo("systemctl reload nginx", pty=True)
