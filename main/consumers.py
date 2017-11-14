from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
#import command

# user to session
user_shells = {}

@channel_session_user_from_http
def ws_connect(message):
    #Group("users").add(message.reply_channel)
    message.reply_channel.send({"accept":True})
    shell = command.create_connection()
    (shell.makefile("r"))
    user_shells[message.user.username]

@channel_session_user
def ws_recieve(message):
    print(message.user)
    # could be improved to be fault tolerant
    sh = user_shells[message.user.username]
    sh

@channel_session_user
def ws_disconnect(message):
    #Group("users").discard(message.reply_channel)
    user_shells[message.user.username]
    del user_shells[message.user.username]
