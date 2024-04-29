import pytest

from mono_citizen.version import Version


@pytest.fixture
def sample_version():
    return Version(2, 4, 6)


def test_version_string():
    v = Version.from_string("1.2.3")

    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 3
    assert v.rc is False


def test_version_string_rc():
    v = Version.from_string("1.2.3.rc")

    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 3
    assert v.rc is True


def test_new_patch(sample_version):
    v = sample_version.new_patch()

    assert v.major == sample_version.major
    assert v.minor == sample_version.minor
    assert v.patch == sample_version.patch + 1


def test_new_minor(sample_version):
    v = sample_version.new_minor()

    assert v.major == sample_version.major
    assert v.minor == sample_version.minor + 1
    assert v.patch == 0


def test_new_major(sample_version):
    v = sample_version.new_major()

    assert v.major == sample_version.major + 1
    assert v.minor == 0
    assert v.patch == 0
