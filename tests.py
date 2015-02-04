import flooper
import subprocess
import os
import json
import pytest
import logging
try:
    import local_settings
except ImportError:
    local_settings = None


TEST_DB = 'flooper_test'

fixture_users = (
    {
        'name': 'dude',
        'email': 'dude@email.com',
    },
    {
        'name': 'not dude',
        'email': 'not.dude@email.com',
    },)


def set_env():
    env = {'DEBUG': '1'}
    if local_settings:
        env['DATABASE_URL'] = 'postgres://%s:%s@%s:%s/%s' % (
            local_settings.database_user,
            local_settings.database_password,
            local_settings.database_host,
            local_settings.database_port,
            TEST_DB,
        )
    logging.error(env)
    os.environ.update(env)


@pytest.yield_fixture
def db():
    PIPE = subprocess.PIPE
    subprocess.call(['dropdb', TEST_DB], stderr=PIPE)
    subprocess.call(['createdb', TEST_DB], stderr=PIPE, stdout=PIPE)
    with open('setup_postgres.sql') as f:
        subprocess.call(['psql', TEST_DB, 'postgres'], stdin=f, stderr=PIPE, stdout=PIPE)
    yield
    subprocess.call(['dropdb', TEST_DB])


@pytest.yield_fixture
def api(db):
    set_env()
    flooper_api = flooper.flooper.test_client()
    flooper_api.testing = True
    yield flooper_api


def api_post(api, path, data):
    return api.post('/api/' + path, data=json.dumps(data), content_type='application/json')


def api_put(api, path, data):
    return api.put('/api/' + path, data=json.dumps(data), content_type='application/json')


def api_get(api, path):
    return api.get('/api/' + path)


def create_user(api, user=None, expected_status=200):
    user = user or fixture_users[0]
    rv = api_post(api, 'users/', user)
    assert rv.status_code == expected_status
    return json.loads(rv.data)['result']


def get_user(api, user_id, expected_status=200):
    rv = api_get(api, 'users/%d' % user_id)
    assert rv.status_code == expected_status
    assert rv.data
    return json.loads(rv.data)['result']


def test_post_user(api):
    user_data = fixture_users[0]
    persisted_user = create_user(api, user=user_data)
    for field in user_data:
        assert persisted_user[field] == user_data[field]


def test_post_users(api):
    for user_data in fixture_users:
        persisted_user = create_user(api, user=user_data)
        for field in user_data:
            assert persisted_user[field] == user_data[field]


def test_get_user(api):
    user_data = fixture_users[0]
    persisted_user = create_user(api, user_data)
    user_id = persisted_user['id']
    user = get_user(api, user_id)
    for field in user_data:
        assert user[field] == user_data[field]


def test_get_users(api):
    for user_data in fixture_users:
        create_user(api, user=user_data)
    rv = api_get(api, 'users/')
    assert rv.status_code == 200
    assert rv.data
    users = json.loads(rv.data)['result']
    for expected_user in fixture_users:
        user_found = False
        for user in users:
            if user['name'] == expected_user['name'] and user['email'] == expected_user['email']:
                user_found = True
                break
        assert user_found, 'User %r missing in response %r' % (expected_user, users)


def test_put_user(api):
    user_data = fixture_users[0]
    persisted_user = create_user(api, user_data)
    user_id = persisted_user['id']
    new_name = 'blah blah blah'
    rv = api_put(api, 'users/%d' % user_id, data={'name': new_name})
    assert rv.status_code == 200
    assert rv.data
    returned_user = json.loads(rv.data)['result']
    assert returned_user['email'] == user_data['email']
    assert returned_user['name'] == new_name
