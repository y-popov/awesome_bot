import os
import pytest
from dadata import Dadata

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    print("Skip setting env variables from .env")


@pytest.fixture(scope='module')
def dadata():
    dadata_token = os.getenv('DADATA_TOKEN')
    dadata_secret = os.getenv('DADATA_SECRET')
    return Dadata(dadata_token, dadata_secret)


@pytest.mark.parametrize('name, gender', [
    ("Срегей владимерович иванов", 'М'),
    ("Rita Rizh", 'Ж')
])
def test_dadata_male(dadata, name, gender):
    res = dadata.clean(name="name", source=name)
    assert res['gender'] == gender
