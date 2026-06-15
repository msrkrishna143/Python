import pytest
from pages.login import LoginPage
from test.conftest import logger

@pytest.fixture(scope="function")
def login_page(login_user):
    pages, context = login_user
    return LoginPage(pages)

@pytest.mark.logout
def test_logout_app(login_page):
    try:
        login_page.logout()

    except AssertionError as e:
        error_value = getattr(e, 'message', repr(e))
        logger.error(error_value)
        pytest.fail("Error message : " + error_value)


@pytest.mark.login
def test_filter(page, input_config):
    login_page = LoginPage(page)
    logger.info("______________________test_leads_filter_________________________")
    login_page.login(input_config)
    logger.info("Logged in successfully")
