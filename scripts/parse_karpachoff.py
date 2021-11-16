import re
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
    url = "https://blog.karpachoff.com/komplimenty-muzhchine-spisok-iz-100-luchshih-fraz"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")

    complements = []

    h2_headers = soup.find_all("h2")
    complements_section = h2_headers[3]

    complements_subsections = complements_section.find_next_siblings(['h3'])
    for subsection in complements_subsections:
        logging.info(f'Parsing {subsection.text}')
        for p in subsection.find_next_siblings(['h3', 'p']):
            if p.name == 'h3':  # next subsection
                break
            if re.match(r'^\d+\. ', p.text):  # starts with number
                try:
                    complement = re.search(r'«(.+)»', p.text).group(1)
                    if '(свой вариант)' not in complement:
                        complements.append(complement)
                except AttributeError:
                    pass

    return complements


def upload_complements(complements: List[str], s3: BaseClient):
    text = json.dumps(complements)
    s3.put_object(Bucket='mad-bucket', Key='complements_male_karpachoff.json', Body=text)


if __name__ == '__main__':
    complements = parse_site()
    logging.info(f'Получил {len(complements)} комплиментов')
    upload_complements(complements, s3=s3)
