from app.models.profile import Profile
from app.models.settings import Settings


def test_profile_roundtrip():
    p = Profile(name="x", command="ping 1.1.1.1")
    q = Profile.from_dict(p.to_dict())
    assert q.name == "x"
    assert q.command == "ping 1.1.1.1"


def test_settings_roundtrip():
    s = Settings(default_profile="x", theme="light")
    t = Settings.from_dict(s.to_dict())
    assert t.default_profile == "x"
    assert t.theme == "light"
