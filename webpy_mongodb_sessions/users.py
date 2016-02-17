## -*- coding: utf-8 -*-
import web
import hashlib
import uuid

#Must be set by the thing importing this module
collection = None
session = None
#TODO: put a real salt in an env variable
SALT = "aslkjw32immSDK9kwer9sFDk8asdg"

def get_user():
    try:
        u = collection.find_one({'_id':session._user_id})
        return u
    except AttributeError:
        return None

def authenticate(username, password):
    user = collection.find_one({'username':username})
    if user and user.get("password") == pswd(password, user.get("username"), user.get("email")):
        return user
    return None

def login(user):
    session._user_id = user['_id']
    session.username = user['username']
    return user

def logout():
    session.kill()

def register(**kwargs):
    user = collection.save(kwargs)
    return user

def pswd(password, username, email):
    seasoned = get_salt(username, email)
    seasoned = seasoned.encode('utf-8')
    return hashlib.sha256(seasoned).hexdigest()

def login_required(function, login_page='/login/'):
    def inner(*args, **kwargs):
        if get_user():
            return function(*args, **kwargs)
        else:
            return web.seeother(login_page+'?next=%s' % web.ctx.get('path','/'))
    return inner

def get_salt(username, email):
    return "{0}{1}{2}".format(email, SALT, username,)
