## -*- coding: utf-8 -*-
import web
import hashlib
import uuid

#Must be set by the thing importing this module
collection = None
session = None

def get_user():
    try:
        u = collection.find_one({'_id':session._user_id}) 
        return u
    except AttributeError:
        return None

def authenticate(username, password):
    user = collection.find_one({'username':username})
    if user and user.get("password") == pswd(password, user.get("salt")):
        return user
    return None

def login(user):
    session._user_id = user['_id']
    session.username = user['username']
    return user

def logout():
    session.kill()

def register(**kwargs):
    salt = str(uuid.uuid4())
    kwargs['salt'] = salt
    kwargs['password'] = pswd(kwargs['password'], salt)
    user = collection.save(kwargs)
    return user
    
def pswd(password, salt):
    seasoned = password + salt
    seasoned = seasoned.encode('utf-8')
    return hashlib.sha256(seasoned).hexdigest()

def login_required(function, login_page='/login/'):
    def inner(*args, **kwargs):
        if get_user():
            return function(*args, **kwargs)
        else:
            return web.seeother(login_page+'?next=%s' % web.ctx.get('path','/'))
    return inner
