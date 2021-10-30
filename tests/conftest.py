import os
import boto3
import pytest

from moto import mock_s3
from dadata import Dadata

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    print("Skip setting env variables from .env")


@pytest.fixture(scope='module')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture(scope='module')
def s3(aws_credentials):
    with mock_s3():
        yield boto3.client('s3', region_name='us-east-1')


@pytest.fixture(scope='module')
def bucket(s3):
    s3.create_bucket(Bucket='mad-bucket')


@pytest.fixture(scope='module')
def dadata():
    dadata_token = os.getenv('DADATA_TOKEN')
    dadata_secret = os.getenv('DADATA_SECRET')
    return Dadata(dadata_token, dadata_secret)
