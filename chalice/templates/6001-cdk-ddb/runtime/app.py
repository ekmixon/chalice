import os
import boto3
from chalice import Chalice


app = Chalice(app_name='{{app_name}}')
dynamodb = boto3.resource('dynamodb')
dynamodb_table = dynamodb.Table(os.environ.get('APP_TABLE_NAME', ''))


@app.route('/users', methods=['POST'])
def create_user():
    request = app.current_request.json_body
    item = {
        'PK': f"User#{request['username']}",
        'SK': f"Profile#{request['username']}",
    }

    item |= request
    dynamodb_table.put_item(Item=item)
    return {}


@app.route('/users/{username}', methods=['GET'])
def get_user(username):
    key = {'PK': f'User#{username}', 'SK': f'Profile#{username}'}
    item = dynamodb_table.get_item(Key=key)['Item']
    del item['PK']
    del item['SK']
    return item
