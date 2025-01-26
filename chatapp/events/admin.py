from chatapp.objects import socket
from chatapp import sql
import base64
import os

def verify_admin(password):

    # 2 layer encoding
    hidden           = base64.b85encode(password.encode())
    encoded_password = base64.b85encode(hidden + hidden)

    with open('secret', 'rb') as file:
        return file.read() == encoded_password
    
@socket.on('client-admin-login')
def admin_login(password):
    check    = verify_admin(password)
    cookie   = sql.generate_cookie('admin') if check else None
    response = dict(check = check, cookie = cookie)
    socket.emit('server-admin-login', response)
    
@socket.on('client-fetch-records')
def fetch_records(data):
    page   = int(data['page'])
    limit  = int(data['limit'])
    offset = (page - 1) * limit
    records, total_count = sql.fetch_records(limit, offset)
    socket.emit('server-fetch-records', dict(records = records, totalCount = total_count, page = page, limit = limit))

@socket.on('client-generate-users')
def generate_users(data):
    number  = int(data['number'])
    treatment = data['treatment']
    option = data['option']
    users   = sql.generate_users(number, treatment, option)
    with open('users.txt', 'w') as file:
        print(users, file = file)

@socket.on('client-get-treatments')
def get_treatments():
    treatments = os.listdir('pages/user/treatments')
    socket.emit('server-get-treatments', treatments)

@socket.on('client-get-options')
def get_options(treatment):
    options = os.listdir(f'pages/user/treatments/{treatment}')
    socket.emit('server-get-options', options)

@socket.on('client-add-study')
def add_study(data):
    sql.add_study(data)

@socket.on('client-get-studies')
def get_studies():
    socket.emit('server-get-studies', sql.get_studies())

@socket.on('client-get-study')
def get_study(code):
    socket.emit('server-get-study', sql.get_study(code))

@socket.on('client-update-study')
def update_study(data):
    print(data)
    sql.update_study(**data)

@socket.on('client-get-treatments-2')
def get_treatments2():
    socket.emit('server-get-treatments-2', os.listdir('pages/user/treatments'))