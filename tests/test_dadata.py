import pytest


@pytest.mark.parametrize('name, gender', [
    ("Срегей владимерович иванов", 'М'),
    ("Rita Rizh", 'Ж')
])
def test_dadata_male(dadata, name, gender):
    res = dadata.clean(name="name", source=name)
    assert res['gender'] == gender
