import os
from flooper_api import flooper_api
from flooper_ui import flooper_ui
from flask import Flask


flooper = Flask(u'Flooper')
flooper.secret_key = os.getenv('SECRET_KEY', 'super secret')
flooper.debug = int(os.getenv('DEBUG', 0))
flooper.debug = True


flooper.register_blueprint(flooper_api)
flooper.register_blueprint(flooper_ui)

if __name__ == '__main__':
    flooper.run()
