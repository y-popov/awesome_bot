import pytest
dotenv = pytest.importorskip('dotenv')

dotenv.load_dotenv()

from main import users
from main import generate_awesome_message


@pytest.mark.skip(reason='prod credentials needed')
def test_generate_awesome_message():
    for user in users:
        generate_awesome_message(user)
