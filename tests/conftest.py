import sys
from copy import deepcopy
from pathlib import Path
from unittest import mock

import pytest


def _add_src_to_sys_path(session: pytest.Session):
    src = Path(session.path) / "src"
    mocked_sys_path = deepcopy(sys.path)
    mocked_sys_path.insert(0, str(src))
    return mock.patch(target="sys.path", new=mocked_sys_path)


@pytest.hookimpl(wrapper=True)
def pytest_collection(session: pytest.Session):
    with _add_src_to_sys_path(session):
        yield
