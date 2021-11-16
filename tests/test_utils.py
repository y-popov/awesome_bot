import pytest
from utils import markdown_escape, admin_id
from utils import dump_users, load_users, send_message


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


@pytest.mark.skip(reason='Manual test')
@pytest.mark.parametrize('message', [
    'Я без ума от твоих волнительных сисек. Точнее - груди!'
])
def test_send_message(message):
    param = {'chat_id': admin_id,
             'text': message.translate(markdown_escape)}
    send_message(params=param)
