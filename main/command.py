import subprocess
import paramiko
from django.conf import settings
import os
import psutil
import time

# All hostnames w/ open connections
connections = {}

def init_tunnel():
    # check if tunnel is already open
    for conn in psutil.net_connections():
        if conn.laddr is not None and conn.laddr[1] == 6536:
            return
    subprocess.Popen("ssh -i " + os.path.join(settings.BASE_DIR, "id_rsa") + " -D 6536 -f -N 2019djones@remote.tjhsst.edu", shell = True)
    time.sleep(1)

def create_connection(hostname, username = 'pi'):
    if hostname in connections and connections[hostname].get_transport() is not None and connections[hostname].get_transport().is_active():
        connection = connections[hostname]
        print('using cached connection')
    else:
        print('new connection! ' + hostname)
        keyfile = os.path.join(settings.BASE_DIR, "id_rsa")
        connection = paramiko.SSHClient()
        connections[hostname] = connection
        connection.load_system_host_keys()
        connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            connection.connect(hostname, key_filename = keyfile, username = username, sock = paramiko.ProxyCommand("nc -x localhost:6536 " + hostname + " 22"))
        except:
            connection.close()
            raise
    return connection

def run_command(hostname, command, username = 'pi'):
    connection = create_connection(hostname, username)
    stdin, stdout, stderr = connection.exec_command(command)
    return stdout.read()
