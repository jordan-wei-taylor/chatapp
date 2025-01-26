from   datetime import datetime, timedelta
from   random   import randint, choice, shuffle
from   .utils   import CONFIG

import sqlite3
import secrets
import json
import os

config = CONFIG()

_create_records = \
"""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    module INT NOT NULL,
    cue_word TEXT NOT NULL,
    cue_text TEXT NOT NULL,
    user_text TEXT NOT NULL,
    user_valence INTEGER NOT NULL,
    gpt_prob FLOAT NOT NULL,
    gpt_memory TINYTEXT NOT NULL,
    amt_label TINYTEXT NOT NULL,
    amt_associate FLOAT NOT NULL,
    amt_categoric FLOAT NOT NULL,
    amt_extended FLOAT NOT NULL,
    amt_omission FLOAT NOT NULL,
    amt_specific FLOAT NOT NULL,
    esther_response TEXT NOT NULL,
    user_flag TEXT NOT NULL
)
"""

_create_users = \
"""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    treatment TEXT NOT NULL,
    option TEXT NOT NULL,
    completed INTEGER,
    generated TEXT NOT NULL,
    last_active TEXT
)
"""

_create_login = \
"""
CREATE TABLE IF NOT EXISTS login (
    cookie TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    expire TEXT NOT NULL
)
"""

_create_signup = \
"""
CREATE TABLE IF NOT EXISTS signup (
    email TINYTEXT PRIMARY KEY,
    dob TEXT NOT NULL,
    sex TINYTEXT NOT NULL
)
"""

_create_studies = \
"""
CREATE TABLE IF NOT EXISTS studies (
    code TEXT PRIMARY KEY,
    name TEXT,
    treatment TEXT,
    treatment_size INTEGER,
    control_size INTEGER
)
"""

_create_study = \
"""
CREATE TABLE IF NOT EXISTS {} (
    id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    gender TEXT,
    dob TEXT,
    category TEXT
)
"""
dt_fmt = r'%d-%m-%y %X'

def current(): 
    return datetime.now().replace(microsecond = 0)

def connect():
    # if bash variable `esther_deploy` is set, have database stored as a 'database.db'
    if os.environ.get('esther_deploy'):
        path = 'database.db'
    
    # otherwise, use 'database-dev.db' which is reset at program launch.
    else:
        path = 'database-dev.db'
        if os.path.exists(path):
            os.remove(path)
    return sqlite3.connect(path)

db = connect()

def execute(query, *args):
    with db:
        cursor = db.cursor()
        cursor.execute(query, args)

def fetchone(query, *args):
    with db:
        cursor = db.cursor()
        result = cursor.execute(query, args).fetchone()
        if result:
            return result[0] if len(result) == 1 else result
    
def fetchall(query, *args):
    with db:
        cursor = db.cursor()
        return cursor.execute(query, args).fetchall()
        
def authenticate(cookie, user = None):
    if user is None:
        expire_str = fetchone('SELECT expire FROM login WHERE cookie = ?', cookie)
    else:
        expire_str = fetchone('SELECT expire FROM login WHERE cookie = ? AND username = ?', cookie, user)
    if expire_str:
        now    = current()
        expire = datetime.strptime(expire_str, dt_fmt)
        if now < expire:
            new_expire = datetime.strftime(now + timedelta(minutes = config['timeout']), dt_fmt)
            execute('UPDATE login SET expire = ? WHERE cookie = ?', new_expire, cookie)
            last_active(now, cookie = cookie)
            return True, None
        else:
            invalidate(cookie = cookie)
            return False, "Session time-out"
    return False, "You have not logged in to view this page"

def invalidate(user = None, cookie = None):
    execute('DELETE FROM login WHERE cookie = ?', cookie)
    execute('DELETE FROM login WHERE username = ?', user)

def extend_cookie(cookie):
    now = current()
    expire = now + timedelta(minutes = config['timeout'])
    execute('UPDATE login SET expire = ? WHERE cookie = ?', expire.strftime(dt_fmt), cookie)
    return fetchone('SELECT username FROM login WHERE cookie = ?', cookie)

def generate_cookie(user):
    invalidate(user = user)
    cookie = secrets.token_hex() # generate a random cookie string
    now    = current()
    expire = now + timedelta(minutes = 5)
    execute('INSERT INTO login VALUES(?,?,?)', cookie, user, expire.strftime(dt_fmt))
    last_active(now.strftime(dt_fmt), user = user)
    return cookie

def last_active(now, user = None, cookie = None):
    if cookie is not None:
        user = fetchone('SELECT username FROM login WHERE cookie = ?', cookie)
    execute('UPDATE users SET last_active = ? WHERE username = ?', now, user)

def user_exists(user):
    return any([fetchone('SELECT COUNT(username) FROM users WHERE username = ?', user),
                fetchone('SELECT COUNT(email) FROM signup WHERE email = ?', user)])

def login(user):
    flag     = user in fetchall('SELECT DISTINCT username FROM records')
    memories = fetchall('SELECT gpt_memory FROM records WHERE username = ?', user)
    return flag, memories
    
def logout(cookie):
    now = current().strftime(dt_fmt)
    last_active(now, cookie = cookie)
    execute('DELETE FROM login WHERE cookie = ?', cookie)

def add_entry(args):
    execute('INSERT INTO records VALUES(NULL,?,?,?,?,?,?,?,?)', *args)

def fetch_records(limit, offset):
    records     = fetchall('SELECT * FROM users LIMIT ? OFFSET ?', limit, offset)
    total_count = fetchone('SELECT COUNT(*) FROM users')
    return records, total_count

def fetch_users():
    return fetchall('SELECT username FROM users')

def generate_users(num, treatment, option):
    existing = fetchall('SELECT username FROM users')
    users    = []

    for i in range(num):
        while True:
            user = randint(100000, 999999)
            if user not in existing: break
        users.append(user)
    
    now = current().strftime('%d-%m-%Y %X')
    for user in users:
        execute('INSERT INTO users VALUES(?,?,?,?,?,?)', user, treatment, option, -1, now, None)

    return '\n'.join(map(str, users))


def cookie2user(func_or_cookie):
    if isinstance(func_or_cookie, str) or (func_or_cookie is None):
        return fetchone('SELECT username FROM login WHERE cookie = ?', func_or_cookie)
    def inner(cookie, *args):
        user = fetchone('SELECT username FROM login WHERE cookie = ?', cookie)
        print(f'cookie2user:\n  user = {user}\n  cookie = {cookie}\n  *args = {args}')
        return func_or_cookie(user, *args)
    return inner

@cookie2user
def update_user_module(user, module):
    old = fetchone('SELECT completed FROM users WHERE username = ?', user)
    if old is not None:
        new = max(old, int(module))
    else:
        new = 0
    print(f'updating completed modules for user {user} from {old} to {new}')
    execute('UPDATE users SET completed = ? WHERE username = ?', new, user)

def check_user_cues(user, module):
    cues    = fetchall("SELECT cue FROM records WHERE username = ? AND module = ?", user, module)
    control = fetchone("SELECT control FROM users WHERE username = ?", user)
    return cues, control

def check_user_control(user):
    return fetchone("SELECT control FROM users WHERE username = ?", user)

def fetch_user_treatment(user):
    return fetchone("SELECT treatment, option FROM users WHERE username = ?", user)

@cookie2user
def fetch_modules_completed(user):
    number = fetchone("SELECT completed FROM users WHERE username = ?", user)
    if number is None: number = -1
    return number

@cookie2user
def fetch_cues(user, module):
    treatment, option = fetch_user_treatment(user)
    with open(f'pages/user/treatments/{treatment}/{option}/cues.json') as file:
        cues = json.load(file)[module]
        return cues

@cookie2user
def fetch_preamble(user, module):
    treatment, option = fetch_user_treatment(user)
    with open(f'pages/user/treatments/{treatment}/{option}/cues.json') as file:
        preamble = json.load(file)[module]['preamble']
    return preamble

@cookie2user
def fetch_cue(user, module):
    treatment, option = fetch_user_treatment(user)
    with open(f'pages/user/treatments/{treatment}/{option}/cues.json') as file:
        cues = json.load(file)[module]

    done   = fetchall("SELECT cue_word FROM records WHERE username = ? AND module = ?", user, module)
    if done:
        done = sum(done, tuple([]))
    random = set(cues['random']) - set(done)
    if len(random):
        i        = randint(0, len(random) - 1)
        cue_word = list(random)[i]
        cue      = cues['random'][cue_word]
        return cue_word, cue
    else:
        if 'last' in cues:
            if len(fetchall("SELECT cue_word FROM records WHERE username = ? AND module = ? AND cue_word = ?", user, module, 'N/A')):
                return 'N/A', 'N/A'
            else:
                return 'N/A', cues['last']
        else:
            return 'N/A', 'N/A'

@cookie2user
def submit_record(*args):
    execute("INSERT INTO records VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", *args)

def signup(email, dob, sex):
    if len(fetchall("SELECT email FROM signup WHERE email = ?", email)):
        valid = False
    else:
        valid = True
        execute('INSERT INTO signup VALUES(?,?,?)', email, dob, sex)
        execute('INSERT INTO users VALUES(?,?,?,-1,?,NULL)', email, 'MeST', 'feedback', current())
    return valid

@cookie2user
def get_option(user):
    return fetchone('SELECT option FROM users WHERE username = ?', user)

def add_study(args):
    execute('INSERT INTO studies VALUES(?,?,?,?,?)', *args)
    execute(_create_study.format(args[0]))
    treatment = fetchone('SELECT treatment FROM studies WHERE code = ?', args[0])
    groups = ['treatment'] * int(args[-2]) + ['control'] * int(args[-1])
    users  = fetchall('SELECT username FROM users')
    if users:
        users = set(range(100000, 1000000)) - set(sum(users, start = tuple([])))
    else:
        users = set(range(100000, 1000000))
    users = list(users)
    shuffle(users)
    shuffle(groups)
    for user, group in zip(users, groups):
        execute(f'INSERT INTO {args[0]} VALUES(?,?,?,?,?,?)', user, "", "", "", "", group)
        execute(f'INSERT INTO users VALUES(?,?,?,NULL,?,NULL)', user, treatment, group, current())

def get_studies():
    studies = fetchall("SELECT * FROM studies")[::-1]
    for i, study in enumerate(studies):
        emails = fetchall(f'SELECT email FROM {study[0]} WHERE email != ""')
        study += (len(emails),)
        studies[i] = study
    return studies

def get_study_name(code):
    return fetchone("SELECT name FROM studies WHERE code = ?", code)

def get_study(code):
    return fetchall(f"SELECT name, email, gender, dob FROM {code} ORDER BY id")

def update_study(code, data):
    ids = fetchall(f'SELECT id FROM {code}')
    for id, row in zip(ids, data):
        execute(f'UPDATE {code} SET name = ?, email = ?, gender = ?, dob = ? WHERE id = ?', *row, id[0])

def retrieve(code, email):
    if fetchone('SELECT ? FROM studies WHERE code = ?', code, code):
        return fetchone(f'SELECT id FROM {code} WHERE email = ?', email)
    
def check_user(user):
    return fetchone(f'SELECT treatment, option FROM users WHERE username = ?', user)

execute(_create_records)
execute(_create_users)
execute(_create_login)
execute(_create_signup)
execute(_create_studies)