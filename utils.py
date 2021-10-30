import json
import logging
from typing import List
from dadata import Dadata
from botocore.client import BaseClient


def load_users(s3: BaseClient) -> List[dict]:
    resp = s3.get_object(Bucket='mad-bucket', Key='awesome_users.json')
    return json.load(resp['Body'])


def dump_users(user_list: List[dict], s3: BaseClient, dadata: Dadata):
    for user in user_list:
        if 'gender' not in user:
            name = f"{user.get('first_name', '')} {user.get('last_name', '')}"
            gender = get_dadata_gender(name=name, dadata=dadata)
            logging.info(f'Got gender {gender} for user {name}')
            user['gender'] = gender
    resp = s3.put_object(Bucket='mad-bucket', Key='awesome_users.json',
                         Body=json.dumps(user_list))
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200


# загружает текст из всех complements_ файлов
def load_complements(s3):
    complements = []
    keys = s3.list_objects_v2(Bucket='mad-bucket',
                              Prefix='complements_')
    for key in keys['Contents']:
        resp = s3.get_object(Bucket='mad-bucket', Key=key['Key'])
        text = resp['Body'].read().decode('utf8')
        complements.extend(json.loads(text))

    return complements


def get_dadata_gender(name: str, dadata: Dadata) -> str:
    res = dadata.clean(name="name", source=name)
    return res['gender']
