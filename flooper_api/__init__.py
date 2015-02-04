from flask import Blueprint, views, request, jsonify, abort
from db import transaction
from werkzeug.exceptions import BadRequest
import logging


flooper_api = Blueprint('flooper_api', __name__, url_prefix='/api')


def wrap_result(result=None):
    wrapper = {}
    if result:
        wrapper['result'] = result
    return wrapper


def api_response(result=None):
    return jsonify(wrap_result(result))


class UserCollectionAPI(views.MethodView):
    def get(self):
        with transaction() as cursor:
            cursor.execute('SELECT * FROM flooper_user')
            users = cursor.fetchall()
        return api_response(users)

    def post(self):
        values = request.get_json()
        try:
            assert values, 'Must provide user data'
            assert 'name' in values, 'User must have a name'
            assert 'email' in values, 'User must have an email address'
        except AssertionError as e:
            logging.exception(e)
            raise BadRequest(e.args[0])
        with transaction() as cursor:
            try:
                cursor.execute('INSERT INTO flooper_user (email, name)'
                               'VALUES (%(email)s, %(name)s) RETURNING *', values)
            except Exception as e:
                logging.exception(e)
            user = cursor.fetchone()
        return api_response(user)


class UserAPI(views.MethodView):
    def get(self, user_id):
        with transaction() as cursor:
            cursor.execute('SELECT * FROM flooper_user WHERE id=%s', (user_id,))
            user = cursor.fetchone()
            if not user:
                abort(404)
        return api_response(user)

    def put(self, user_id):
        values = request.get_json()
        set_values = ','.join(column + '=%(' + column + ')s' for column in values.iterkeys())
        sql = 'UPDATE flooper_user SET {set_values} WHERE id=%(id)s RETURNING *'.format(set_values=set_values)
        values['id'] = user_id
        with transaction() as cursor:
            cursor.execute(sql, values)
            user = cursor.fetchone()
        return api_response(user)


flooper_api.add_url_rule(
    '/users/',
    view_func=UserCollectionAPI.as_view('users'))
flooper_api.add_url_rule(
    '/users/<int:user_id>',
    view_func=UserAPI.as_view('user'))
