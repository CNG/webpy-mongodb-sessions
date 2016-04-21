## -*- coding: utf-8 -*-
import web
import hashlib
import uuid

# must be set after importing
collection = None
session    = None
SALT       = "aslkjw32immSDK9kwer9sFDk8asdg"

def get_user():
    try:
        u = collection.find_one({'_id': session._user_id})
        return u
    except AttributeError:
        return None

def authenticate(username, password):
    user = collection.find_one({'username': username})
    if user and user.get("password") == pswd(password, user.get("username")):
        return user
    return None

def login(user):
    session._user_id = user['_id']
    session.username = user['username']
    return user

def logout():
    session.kill()

def register(**kwargs):
    collection.replace_one({'username': kwargs["username"]}, kwargs, upsert=True)
    user = collection.find_one({'username': kwargs["username"]})
    return user

def pswd(password, username):
    seasoned = get_salt(username)
    seasoned = seasoned.encode('utf-8')
    return hashlib.sha256(seasoned).hexdigest()

def login_required(function, login_page='/login/'):
    def inner(*args, **kwargs):
        if get_user():
            return function(*args, **kwargs)
        else:
            return web.seeother(login_page+'?next=%s' % web.ctx.get('path','/'))
    return inner

def get_salt(username):
    return "{0}{1}".format(username, SALT)
