import pytest
from pages.login import LoginPage
from test.conftest import logger

@pytest.fixture(scope="function")
def login_page(login_user):
    pages, context = login_user
    return LoginPage(pages)


@pytest.mark.login
def test_filter(page, input_config):
    login_page = LoginPage(page)
    logger.info("______________________test_leads_filter_________________________")
    login_page.login(input_config)
    logger.info("Logged in successfully")
