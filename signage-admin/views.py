from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import condition
from time import sleep

import threading
import datetime

from . import models, command, consumers

# Create your views here.

# cache of hostname : (screenshot data, time last updated)
screenshots = {}

@login_required
def index(request):
    class Wrappa():
        def __init__(self, sign):
            self.online = command.is_online(sign.hostname)
            self.name = sign.name
            self.hostname = sign.hostname
            self.landscape = sign.landscape
    signs = []
    threads = []
    command.ensure_tunnel() # initalize tunnel to prevent race conditions
    set
    for sign in models.Sign.objects.all():
        #signs.append(Wrappa(sign))
        def func(sig):
            signs.append(Wrappa(sig))
        threads.append(threading.Thread(target=func, args = (sign,)))
        threads[-1].start()
    for thread in threads:
        thread.join()
    signs.sort(key = lambda x: x.name)
    return render(request, "signage-admin/index.html", { 'all_signs' : signs }) 

@login_required
def reboot(request):
    hostname = request.path.split('/')[-1]
    if hostname == '':
        return HttpResponseBadRequest('Bad Request<br><a href="/">Back to main page</a>')
    connection = command.create_connection(hostname)
    connection.exec_command('sudo reboot')
    connection.close()
    sleep(3)
    return redirect("/", permanent = False)

@login_required
def screenshot(request):
    hostname = request.GET.get('hostname', '')
    if hostname == '':
        return HttpResponseNotFound('404 Not Found')
    #if hostname in screenshots and datetime.datetime.now() - screenshots[hostname][1] < datetime.timedelta(minutes = 1):
    #    return HttpResponse(screenshots[hostname][0], content_type = 'image/png')
    #png_data = command.run_command(hostname, 'DISPLAY=:0 XAUTHORITY=/home/pi/.Xauthority scrot scrot.png; cat scrot.png; rm scrot.png')
    png_data = command.run_command(hostname, "cd ~/raspi2png; ./raspi2png; cat ./snapshot.png; rm snapshot.png")
    screenshots[hostname] = (png_data, datetime.datetime.now())
    return HttpResponse(png_data, content_type = 'image/png')

@login_required
def terminal(request):
    hostname = request.path.split('/')[-1]
    if hostname == '':
        return HttpResponseNotFound("404 Not Found")
    return render(request, "signage-admin/terminal.html", { 'hostname': hostname  })

@login_required
def term_resize(request):
    rows = request.GET.get("rows", "")
    cols = request.GET.get("cols", "")
    uname = request.user.username
    if rows == '' or cols == '' or uname == '':
        return HttpResponseBadRequest("plz2fix")
    shell = consumers.user_shells[uname][2]
    shell.resize_pty(rows=rows, cols=cols)
