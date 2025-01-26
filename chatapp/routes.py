from flask import render_template, redirect, send_file, send_from_directory, abort, request
from chatapp.objects import app
from chatapp.utils   import CONFIG
from chatapp import sql
import json

import os

# non-user pages

@app.route('/')
def root():
    return redirect('/login')

@app.route('/login')
def login():
    jinja_vars = CONFIG()
    return render_template('login.html', **jinja_vars)

@app.route('/retrieve-username')
def retrieve_username():
    jinja_vars = CONFIG()
    return render_template('retrieve-username.html', **jinja_vars)

# helper function for authentication
def authenticate(path, cookie):
    """ Checks if cookie is authorised to access path - returns a response if unauthorised """
    user = sql.cookie2user(cookie)
    if user:
        if ('login' in path) or ('signup' in path):
            sql.invalidate(cookie)
            return user, None
        else:
            if request.cookies.get('esther-auth-reject') is None:
                valid, message = sql.authenticate(cookie, user)
                if not valid:
                    response = redirect('/login')
                    response.set_cookie('esther-auth-reject', message, path = '/')
                    return user, response
    else:
        if 'login' not in path:
            response = redirect('/login')
            response.set_cookie('esther-auth-reject', 'Could not validate your cookie. Please log in again.', path = '/')
            return user, response
    return user, None

# admin pages
def route_admin(path):
    jinja_vars = CONFIG()
    if 'study' in path:
        code = path.split('/')[-1]
        name = sql.get_study_name(code)
        return render_template('admin.html', css = f'admin/study.css', js = 'admin/study.js', page = 'study.html', name = name, code = code, **jinja_vars)
    return render_template('admin.html', css = f'admin/{path}.css', js = f'admin/{path}.js', page = f'{path}.html', **jinja_vars)

@app.route('/<path:path>')
def route(path):
    cookie = request.cookies.get('esther-cookie')
    user, response = authenticate(path, cookie)
    if user == 'admin':
        return route_admin(path)
    elif user:
        return route_user(path, user, cookie)
    return template(path, cookie)

def template(path, cookie, support = None, **kwargs):

    # default jinja variables (from config.yaml)
    jinja_vars = CONFIG()

    # extends the time the cookie is active for, and returns the user
    user = sql.extend_cookie(cookie)
    if (user is not None) and ('login' not in path) and ('signup' not in path):
        jinja_vars['user'] = user
        if user == 'admin':
            full_path              = f'admin/{path}'
            jinja_vars['subtitle'] = jinja_vars['header_subtitle'] = 'Admin Area'
        elif ('chat' in path) or ('home' in path):
            full_path              = f'user/{path}'
        else:
            # treatment, group       = sql.fetch_user_treatment(user)
            full_path              = f'user/{path}'
    else:
        full_path = path
    jinja_vars['back'] = 'home' not in path

    # if page does not have an associated markdown file, return 404 page not found
    if not os.path.exists(f'pages/{full_path}.md'):
        print(f'could not find "pages/{full_path}.md" - redirecting to 404...')
        return abort(404)

    # open markdown contents
    with open(f'pages/{full_path}.md') as file:
        jinja_vars['md'] = file.read()

    # update jinja variables (js and css)
    for s in ['js', 'css']:
        if support and os.path.exists(f'chatapp/static/{s}/{support}.{s}'):
            jinja_vars[s] = f'{support}.{s}'
            continue
        
        if os.path.exists(f'chatapp/static/{s}/user/{path}.{s}'):
            jinja_vars[s] = f'user/{path}.{s}'
        else:
            jinja_vars[s] = f'user/module-intro.{s}'

    # update jinja variables provided by kwargs
    jinja_vars.update(kwargs)

    # substitute all jinja variables into template.html and render
    return render_template(f'template.html', **jinja_vars)

# 404 page not found error handler
@app.errorhandler(404)
def page_not_found_error(e):
    return redirect('/404')

@app.route('/404')
def page_not_found():
    with open(f'pages/404.md') as file:
        md = file.read()
    jinja = CONFIG()
    jinja.update(md = md, logout = False, css = '404.css', js = False)
    return render_template('template.html', **jinja), 404

# login route
# @app.route('/login')
# def login():
#     cookie = request.cookies.get('esther-cookie')
#     return template('login', cookie = cookie, header = False, footer = False, subtitle = 'Login')

# @app.route('/signup')
# def signup():
#     cookie = request.cookies.get('esther-cookie')
#     return template('signup', cookie = cookie, header = False, footer = False, subtitle = 'Signup')

# generic routing logic if nothing below catches
# @app.route('/<path:path>')
# def route(path):

#     # to make the following code easier...
#     if path.startswith('/'): path = path[1:]

#     cookie = request.cookies.get('esther-cookie')

#     # check if client cookie is authorised (no authorisation required at login page)
#     user, unauthorised = authenticate(path, cookie)
#     if unauthorised:
#         return unauthorised
    
#     if user == 'admin':
#         return template(path, cookie, footer_right = False)
#     return route_user(path, user, cookie)

def route_user(path, user, cookie):
    treatment, option = sql.fetch_user_treatment(user)
    temp = f'treatments/{treatment}/{option}'
    if 'home' in path:
        return template(path, cookie, user = user, back = False, subtitle = 'Home')
    elif 'module' in path:
        if 'chat' in path:
            return template('chat', cookie, 'user/chat', subtitle = 'Chat', back = True)
        else:
            module = os.path.basename(path).replace('module-', '')
            return template(f'{temp}/{module}', cookie, 'module-intro', subtitle = 'Module Introduction')
    elif any(subpath in path for subpath in ['welcome', 'free-recall']):
        print(f'{temp}/{os.path.basename(path)}')
        return template(f'{temp}/{os.path.basename(path)}', cookie, 'module-intro', subtitle = 'Module Introduction')
    else:
        return redirect('/404')
    


# @app.route('/home')
# def user_home():
#     user, treatment, option = check_user()
#     if user is None: return abort(404)
#     return template('home', subtitle = 'user', user = user)

# # user welcome module
# @app.route('/welcome')
# def user_welcome():
#     user, treatment, option = check_user()
#     if user is None: return abort(404)
#     return template(f'treatments/{treatment}/{option}/welcome', support = 'module-intro', subtitle = 'user', user = user, back = True)

# # user free-recall module
# @app.route('/free-recall')
# def user_free_recall():
#     user, treatment, option = check_user()
#     if user is None: return abort(404)
#     return template(f'treatments/{treatment}/{option}/free-recall', support = 'module-intro', subtitle = 'user', user = user, back = True)

# # user main modules
# @app.route('/module-<module>')
# def user_modules(module):
#     user, treatment, option = check_user()
#     if user is None: return abort(404)
#     return template(f'treatments/{treatment}/{option}/{module}', user = user, module = module, support = 'module-intro', subtitle = 'user')

# @app.route('/module-<module>/chat')
# def chat(module):
#     user, treatment, option = check_user()
#     if user is None: return abort(404)
#     return template('chat', user = user, module = module, support = 'user/chat', subtitle = 'chat', back = True)


# REDIRECTS




# download (upon admin generating new users)
@app.route('/admin/download=<cookie>', methods = ['GET'])
def download(cookie):
    valid, message = sql.authenticate(cookie, 'admin')
    if valid:
        return send_file('../users.txt', as_attachment = True)
    return abort(404)
