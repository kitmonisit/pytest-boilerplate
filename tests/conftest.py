import logging
import sys
from copy import deepcopy
from pathlib import Path
from unittest import mock

import pytest

log = logging.getLogger(__name__)


def _add_src_to_sys_path(session: pytest.Session):
    src = Path(session.path) / "src"
    mocked_sys_path = deepcopy(sys.path)
    mocked_sys_path.insert(0, str(src))
    return mock.patch(target="sys.path", new=mocked_sys_path)


def _has_marker(item: pytest.Item, marker_name: str):
    return marker_name in (marker.name for marker in item.own_markers)


@pytest.hookimpl(wrapper=True)
def pytest_collection(session: pytest.Session):
    with _add_src_to_sys_path(session):
        yield


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    result: pytest.TestReport = yield

    if _has_marker(item, "skip") and call.when == "setup":
        # A test decorated with @pytest.mark.skip will never get to a state where call.when == "call"
        assert result.failed == False and result.outcome == "skipped", (
            "If a test is decorated with @pytest.mark.skip, result.failed =="
            f" False and result.outcome == 'skipped', but we have {result.failed} and"
            f" '{result.outcome}' respectively. Something is wrong here."
        )
        log.warning("SKIPPED")

    if call.when == "call":
        if result.failed:
            log.error("FAILED")
        elif result.failed == False:
            log.info("PASSED")

    return result
