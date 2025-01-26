from chatapp.objects import socket
from chatapp import sql


@socket.on('client-user-login')
def user_login(user):
    cookie = sql.generate_cookie(user)
    socket.emit('server-user-login', cookie)

@socket.on('client-logout')
def logout(cookie):
    sql.logout(cookie)

@socket.on('client-validate-user')
def validate_user(user, cookie):
    valid_user = sql.validate_user(user, cookie)
    socket.emit('server-validate-user', valid_user)

@socket.on('client-user-exists')
def user_exists(user):
    exists = sql.user_exists(user)
    socket.emit('server-user-exists', exists)

@socket.on('client-auth')
def authenticate(cookie):
    authenticate, message = sql.authenticate(cookie)
    socket.emit('server-auth', dict(authenticate = authenticate, message = message))

@socket.on('client-retrieve')
def retrieve(data):
    code  = data['code']
    email = data['email']
    user  = sql.retrieve(code, email)
    if user:
        message = f'Your username is {user}.'
        check   = True
    else:
        message = 'Check your input credentials and try again.'
        check   = False
    socket.emit('server-retrieve', dict(message = message, check = check))
