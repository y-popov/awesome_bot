import pytest
from utils import dump_users, load_users


@pytest.fixture(scope='module')
def user():
    return {
        'id': 12345678,
        'first_name': 'Иван'
    }


@pytest.fixture(scope='module')
def user_list(user):
    return [user]


def test_dump_users(s3, dadata, user_list, bucket):
    dump_users(user_list, s3=s3, dadata=dadata)
    s3_users = load_users(s3=s3)
    assert isinstance(s3_users, list)
    assert len(s3_users) == len(user_list)
