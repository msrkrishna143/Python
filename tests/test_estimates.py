import pytest
from pages.Phase3.Estimates import Estimates
from test.conftest import logger


@pytest.fixture(scope="function")
def estimation_changes_flow(login_user_phase3):
    pages, context = login_user_phase3
    return Estimates(pages)


@pytest.mark.estimation
@pytest.mark.module("Estimations Module")
def test_view_deleted_estimate_full_flow(estimation_changes_flow):
    try:
        estimation_changes_flow.view_deleted_estimate_restore_validation()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)