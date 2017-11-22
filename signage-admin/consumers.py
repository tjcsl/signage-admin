from channels import Group
from . import command
from channels.auth import channel_session_user, channel_session_user_from_http
from threading import Thread
#import command

# user to session
user_shells = {}

@channel_session_user_from_http
def ws_connect(message):
    # make sure the user is actually logged in
    if not message.user.is_authenticated():
        message.reply_channel.send({'close': True})
        return
    # accept the connection
    message.reply_channel.send({"accept":True})
    # the last part of the URL is the hostname
    hostname = message.content['path'].split('/')[-1]
    # setup the shell
    shell = command.create_connection(hostname).invoke_shell(term='xterm-256color')
    shell.settimeout(1)
    shell.setblocking(True)
    shell.set_combine_stderr(True)
    stdout = shell.makefile("r")
    stdin = shell.makefile("wb")
    # put the shell in the global cache
    user_shells[message.user.username] = (stdout, stdin, shell)
    # start the receiving thread
    Thread(target=recv_thread, args=(message.reply_channel, stdout, shell)).start()

@channel_session_user
def ws_receive(message):
    # could be improved to be fault tolerant
    stdout, stdin, shell = user_shells[message.user.username]
    try:
        stdin.write(message.content['text'])
    except:
        message.reply_channel.send({"close": True})
        shell.close()
    stdin.flush()

@channel_session_user
def ws_disconnect(message):
    if message.user.username == '':
        return
    user_shells[message.user.username][2].close()
    del user_shells[message.user.username]

def recv_thread(replier, stdout, shell):
    while True:
        try:
            b = stdout.read(1)
        except:
            print("IS CLOSE\n\n\n\n")
        while shell.recv_ready():
            b += stdout.read(1)
        try:
            replier.send({"text": b.decode("UTF-8")})
        except:
            print("socket is ded")
            break
