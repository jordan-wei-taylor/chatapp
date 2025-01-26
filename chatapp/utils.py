from flask import request
# from chatapp import sql

import yaml

def CONFIG():
    """ Loads default parameters from config.yaml """
    with open('config.yaml') as file:
        return yaml.safe_load(file)
    
# def check_user():
#     cookie = request.cookies.get('esther-cookie')
#     user = sql.cookie2user(cookie)
#     if user is None:
#         return None, None, None
#     treatment, option = sql.fetch_user_treatment(user)
#     return user, treatment, option