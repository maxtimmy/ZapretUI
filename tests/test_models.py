from app.models.profile import Profile


def test_profile_to_dict():
    p = Profile(name='x', domains=['a', 'a'])
    d = p.to_dict()
    assert d['name'] == 'x'
    assert d['domains'] == ['a']
