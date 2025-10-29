import domain
import pytest


def test_will_succeed():
    assert True


@pytest.mark.xfail
def test_will_succeed_unexpectedly():
    assert True


@pytest.mark.xfail
def test_will_fail_as_expected():
    assert False


@pytest.mark.xfail
def test_will_be_skipped_during_test_has_xfail():
    pytest.skip()
    assert False


@pytest.mark.skip
def test_will_be_skipped_as_marked():
    assert False


def test_will_be_skipped_during_test():
    pytest.skip()
    assert False


@pytest.mark.parametrize(
    ("value"),
    (
        True,
        False,
        pytest.param(False, marks=pytest.mark.xfail),
    ),
)
def test_parametrize(value):
    assert value
