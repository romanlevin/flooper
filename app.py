from flask import Flask
import os

app = Flask(u'Flooper')
app.secret_key = os.getenv('SECRET_KEY', 'super secret')
app.debug = int(os.getenv('DEBUG', 0))


@app.route('/')
def index():
    return u'Hello World!'


@app.route('/api/users/<user_id>')
def api_get_user(user_id):
    user_id = int(user_id)
    return u'You got a user! user_id: %r' % user_id


@app.route('/api/users/')
def api_get_users():
    return u'You got a bunch of users!'
