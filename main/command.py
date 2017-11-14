import subprocess
import paramiko
from django.conf import settings
import os
import psutil
import time
import datetime

# All hostnames w/ open connections
connections = {}
# Last time of tunnel check
last_check = datetime.datetime(year=1970,month=1,day=1)

def ensure_tunnel():
    global last_check
    # check if tunnel is already open
    if last_check + datetime.timedelta(seconds=30) > datetime.datetime.now():
        return
    last_check = datetime.datetime.now()
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
            if settings.USE_TUNNEL:
                ensure_tunnel()
                connection.connect(hostname, key_filename = keyfile, username = username, sock = paramiko.ProxyCommand("nc -x localhost:6536 " + hostname + " 22"), timeout = 3)
            else:
                connection.connect(hostname, key_filename = keyfile, username = username, timeout = 3)
        except:
            connection.close()
            raise
    return connection

def run_command(hostname, command, username = 'pi'):
    connection = create_connection(hostname, username)
    stdin, stdout, stderr = connection.exec_command(command)
    return stdout.read()

def is_online(hostname):
    if settings.USE_TUNNEL:
        output = run_command("ras1.tjhsst.edu", 'ping6 -c 1 -W 1 ' + hostname, "2019djones")
        if b'1 received' in output:
            return True
        output = run_command("ras1.tjhsst.edu", 'ping -c 1 -W 1 ' + hostname, "2019djones")
        print(output)
        if b'1 received' in output:
            return True
        return False
    else:
        proc = subprocess.Popen(['ping', '-c', '1', '-W', '1', hostname], stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        return b'1 received' in stdout

