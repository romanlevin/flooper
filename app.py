from flask import Flask
import os

DEBUG = bool(os.getenv('DEBUG'))

app = Flask(u'Flooper')

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

    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run(
        port=port,
        host=host,
        debug=DEBUG,
        )

