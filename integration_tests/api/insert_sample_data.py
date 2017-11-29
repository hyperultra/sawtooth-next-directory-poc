
# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

import re
import json
import dredd_hooks as hooks
from requests import request


API_PATH = 'api'

USER = {
    'name': 'Bob Bobson',
    'password': '12345'
}

EXTRA_USER = {
    'name': 'Suzie Suzerson',
    'password': '67890'
}

ROLE = {
    'name': 'Test Administrator',
    'owners': [],  # USER will be appended
    'administrators': []  # USER will be appended
}

TASK = {
    'name': 'test-user-permissions',
    'owners': [],
    'administrators': []
}


seeded_data = {}


def get_base_api_url(txn):
    protocol = txn.get('protocol', 'http:')
    host = txn.get('host', 'localhost')
    port = txn.get('port', '8000')
    return '{}//{}:{}/{}/'.format(protocol, host, port, API_PATH)

def api_request(method, base_url, path, body=None, auth=None):
    url = base_url + path

    auth = auth or seeded_data.get('auth', None)
    headers = {'Authorization': auth} if auth else None

    response = request(method, url, json=body, headers=headers)
    response.raise_for_status()

    parsed = response.json()
    return parsed.get('data', parsed)


def api_submit(base_url, path, resource, auth=None):
    return api_request('POST', base_url, path, body=resource, auth=auth)


def patch_body(txn, update):
    old_body = json.loads(txn['request']['body'])

    new_body = {}
    for key, value in old_body.items():
        new_body[key] = value
    for key, value in update.items():
        new_body[key] = value

    txn['request']['body'] = json.dumps(new_body)


def sub_nested_strings(dct, pattern, replacement):
    for key in dct.keys():
        if isinstance(dct[key], dict):
            sub_nested_strings(dct[key], pattern, replacement)
        elif isinstance(dct[key], str):
            dct[key] = re.sub(pattern, replacement, dct[key])


@hooks.before_all
def initialize_sample_resources(txns):
    base_url = get_base_api_url(txns[0])
    submit = lambda p, r, a=None: api_submit(base_url, p, r, a)

    # Create USER
    user_response = submit('users', USER)
    seeded_data['auth'] = user_response['authorization']
    seeded_data['user'] = user_response['user']

    # Create ROLE
    ROLE['owners'].append(seeded_data['user']['id'])
    ROLE['administrators'].append(seeded_data['user']['id'])
    seeded_data['role'] = submit('roles', ROLE)

    # Create TASK
    TASK['owners'].append(seeded_data['user']['id'])
    TASK['administrators'].append(seeded_data['user']['id'])
    seeded_data['task'] = submit('tasks', TASK)

    # Create EXTRA_USER
    extra_response = submit('users', USER)
    seeded_data['extra_auth'] = extra_response['authorization']
    seeded_data['extra_user'] = extra_response['user']

    # Create a proposal
    proposal_path = 'roles/{}/owners'.format(seeded_data['role']['id'])
    proposal_body = {'id': seeded_data['extra_user']['id']}
    proposal_auth = seeded_data['extra_auth']

    proposal_response = submit(proposal_path, proposal_body, proposal_auth)
    seeded_data['proposal'] = {'id': proposal_response['proposal_id']}

    # Get head block id
    head_id = api_request('GET', base_url, 'blocks/latest')['id']

    # Add USER's auth token and current head to all transactions
    for txn in txns:
        txn['request']['headers']['Authorization'] = seeded_data['auth']
        sub_nested_strings(txn, '[0-9a-f]{128}', head_id)


@hooks.before('/api/authorization > POST > 200 > application/json')
def add_credentials(txn):
    patch_body(txn, {
        'id': seeded_data['user']['id'],
        'password': USER['password']
    })


@hooks.before('/api/roles > POST > 200 > application/json')
def add_owners_and_admins(txn):
    patch_body(txn, {
        'administrators': [seeded_data['user']['id']],
        'owners': [seeded_data['user']['id']]
    })


@hooks.before('/api/roles/{id}/admins > POST > 200 > application/json')
def add_user_id(txn):
    patch_body(txn, {'id': seeded_data['user']['id']})