import json
import boto3
import logging
import requests

from typing import List
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from botocore.client import BaseClient

load_dotenv()
logging.basicConfig(level='INFO')

s3 = boto3.session.Session().client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)


def parse_site() -> List[str]:
    url = "https://www.romanticcollection.ru/podarki/idei/krasivye-komplimenty-dlya-devushki"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")

    complements = []

    chapter3 = soup.find(id=3)
    for p in chapter3.parent.find_next_siblings(["p", "h2"]):
        if p.find('br'):
            complements.append(p.text)

    return complements


def upload_complements(complements: List[str], s3: BaseClient):
    text = json.dumps(complements)
    s3.put_object(Bucket='mad-bucket', Key='complements_romanticcollection.json', Body=text)


if __name__ == '__main__':
    complements = parse_site()
    logging.info(f'Получил {len(complements)} комплиментов')
    upload_complements( complements, s3=s3)
