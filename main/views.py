from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from time import sleep

import threading

from . import models, command

# Create your views here.

@login_required
def index(request):
    class Wrappa():
        def __init__(self, sign):
            self.online = True
            output = command.run_command("remote.tjhsst.edu", 'ping -c 1 -W 1 ' + sign.hostname, "2019djones")
            if b'0 received' in output:
                self.online = False
            self.name = sign.name
            self.hostname = sign.hostname
            self.landscape = sign.landscape
    signs = []
    threads = []
    command.init_tunnel() # initalize tunnel to prevent race conditions
    for sign in models.Sign.objects.all():
        signs.append(Wrappa(sign))
#        def func(sig):
#            signs.append(Wrappa(sig))
#        threads.append(threading.Thread(target=func, args = (sign,)))
#        threads[-1].start()
#    for thread in threads:
#        thread.join()
    signs.sort(key = lambda x: x.name)
    return render(request, "main/index.html", { 'all_signs' : signs }) 

@login_required
def reboot(request):
    hostname = request.GET.get('hostname', '')
    if hostname == '':
        return HttpResponseBadRequest('Bad Request<br><a href="/main/">Back to main page</a>')
    connection = command.create_connection(hostname)
    connection.exec_command('sudo reboot')
    connection.close()
    sleep(3)
    return redirect("/main/", permanent = False)
