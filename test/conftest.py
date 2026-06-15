import pytest
import yaml
from playwright.sync_api import sync_playwright

from pages.login import LoginPage
from utils.logger import setup_logger
from datetime import datetime, timedelta
import os

# Expose a logger instance
logger = setup_logger()


def pytest_html_results_table_header(cells):
    cells.insert(2, '<th class="sortable" data-column-type="module">Module</th>')


def pytest_html_results_table_row(report, cells):
    module_name = getattr(report, "module_name", "Unknown")
    cells.insert(2, f'<td>{module_name}</td>')

    # Modify Test column to show only test function name
    test_full_name = cells[1].text_content() if hasattr(cells[1], "text_content") else cells[1]
    if "::" in test_full_name:
        test_name_only = test_full_name.split("::")[-1]
        cells[1] = f'<td>{test_name_only}</td>'


def attach_module_name(report, item):
    # """
    # Attach module name to the report.
    # Supports both function-level and class-level @pytest.mark.module("...").
    # """
    # Check function-level marker first
    module_marker = item.get_closest_marker("module") or item.get_closest_marker("modules")
    if module_marker and module_marker.args:
        report.module_name = module_marker.args[0]
        return

    # Check class-level marker
    if hasattr(item, "cls"):
        class_markers = getattr(item.cls, "pytestmark", [])
        for marker in class_markers:
            if marker.name in ("module", "modules") and marker.args:
                report.module_name = marker.args[0]
                return

    # Fallback
    report.module_name = "Unknown"

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    attach_module_name(report, item)


    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")  # Access the "page" fixture, assuming it's used in tests
        if page:

            # Create a screenshots directory if it doesn't exist
            screenshots_dir = "./screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

            # Save the screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshots_dir, f"{item.name}_{timestamp}.png")
            page.screenshot(path=screenshot_path)

            # Attach the screenshot to the report
            report.extra = getattr(report, "extra", [])
            report.extra.append(f"Screenshot: {screenshot_path}")

@pytest.fixture(scope="session")
def input_config():
    relative_path = './data/inputdata.yaml'
    absolute_path = os.path.abspath(relative_path)
    with open(absolute_path, "r") as file:
        config_data = yaml.safe_load(file)
        return config_data

# Load the yaml Config file
# @pytest.fixture(scope="session")
# def input_config():
#     relative_path = 'C:/Users/sivarama.krishna/Documents/uhe_phase3/data/inputdata.yaml'
#     absolute_path = os.path.abspath(relative_path)
#     with open(absolute_path, "r") as file:
#         config_data = yaml.safe_load(file)
#         return config_data




@pytest.fixture(scope="function")
def page1():
    # Initialize Playwright resources
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(args=['--start-maximized'], headless=False)  # Use headless=True for CI
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    yield page  # Provide the `page` to the test
    page.close()
    context.close()
    browser.close()
    playwright.stop()


# def input_config():
#     project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     config_file_path = os.path.join(project_root, 'data', 'inputdata.yaml')
#
#     if not os.path.exists(config_file_path):
#         raise FileNotFoundError(f"Config file not found at: {config_file_path}")
#
#     with open(config_file_path, "r") as file:
#         return yaml.safe_load(file)


@pytest.fixture(scope="session")
def login_user_phase3():
    """Logs in once per session and reuses the Playwright page."""
    with sync_playwright() as playwright:
        #browser = p.chromium.launch(headless=False, slow_mo=50)
        browser = playwright.chromium.launch(args=['--start-maximized'], headless=False)  # Use headless=True for CI
        # ✅ Load existing session state if available
        try:
            #context = browser.new_context(storage_state="state.json")
            context = browser.new_context(no_viewport=True, storage_state="state.json")
            print("✅ Loaded existing session.")
        except:
            context = browser.new_context()
            print("🔐 No saved session found, logging in...")

        page = context.new_page()
        config = input_config_value()
        url = config["base_url2"]
        page.goto(url)

        # Check if already logged in

        if page.locator("#profileDropdown-navbar").is_visible():
            print("✅ Already logged in, reusing session.")
        else:
            username = config['User_name']
            password = config['user_password3']
            login_page=LoginPage(page)
            login_page.login_app(username,password)
            page.locator("#profileDropdown-navbar").wait_for(state="visible", timeout=50000)
            print("✅ Successfully logged in!")
            # ✅ Save session state after login
            context.storage_state(path="state.json")
        yield page, context  # Return the logged-in page for reuse
        browser.close()  # Close the browser after all tests


@pytest.fixture(scope="session")
def login_sales_user_phase3():
    """Logs in once per session and reuses the Playwright page."""
    with sync_playwright() as playwright:
        #browser = p.chromium.launch(headless=False, slow_mo=50)
        browser = playwright.chromium.launch(args=['--start-maximized'], headless=False)  # Use headless=True for CI
        # ✅ Load existing session state if available
        try:
            #context = browser.new_context(storage_state="state.json")
            context = browser.new_context(no_viewport=True, storage_state="state.json")
            print("✅ Loaded existing session.")
        except:
            context = browser.new_context()
            print("🔐 No saved session found, logging in...")

        page = context.new_page()
        config = input_config_value()
        url = config["base_url2"]
        page.goto(url)

        # Check if already logged in

        if page.locator("#profileDropdown-navbar").is_visible():
            print("✅ Already logged in, reusing session.")
        else:
            username = config['sales_user_name']
            password = config['sales_pass_password']
            login_page=LoginPage(page)
            login_page.login_app(username,password)
            page.locator("#profileDropdown-navbar").wait_for(state="visible", timeout=50000)
            print("✅ Successfully logged in!")
            # ✅ Save session state after login
            context.storage_state(path="state.json")
        yield page, context  # Return the logged-in page for reuse
        browser.close()  # Close the browser after all tests


@pytest.fixture(scope="session")
def login_admin_user_phase3():
    """Logs in once per session and reuses the Playwright page."""
    with sync_playwright() as playwright:
        #browser = p.chromium.launch(headless=False, slow_mo=50)
        browser = playwright.chromium.launch(args=['--start-maximized'], headless=False)  # Use headless=True for CI
        # ✅ Load existing session state if available
        try:
            #context = browser.new_context(storage_state="state.json")
            context = browser.new_context(no_viewport=True, storage_state="state.json")
            print("✅ Loaded existing session.")
        except:
            context = browser.new_context()
            print("🔐 No saved session found, logging in...")

        page = context.new_page()
        config = input_config_value()
        url = config["base_url2"]
        page.goto(url)

        # Check if already logged in

        if page.locator("#profileDropdown-navbar").is_visible():
            print("✅ Already logged in, reusing session.")
        else:
            username = config['User_name']
            password = config['sales_pass_password']
            login_page=LoginPage(page)
            login_page.login_app(username,password)
            page.locator("#profileDropdown-navbar").wait_for(state="visible", timeout=50000)
            print("✅ Successfully logged in!")
            # ✅ Save session state after login
            context.storage_state(path="state.json")
        yield page, context  # Return the logged-in page for reuse
        browser.close()

def input_config_value():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file_path = os.path.join(project_root, 'data', 'inputdata.yaml')

    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Config file not found at: {config_file_path}")

    with open(config_file_path, "r") as file:
        return yaml.safe_load(file)

@pytest.fixture(scope="session")
def login_user():
    """Logs in once per session and reuses the Playwright page."""
    with sync_playwright() as playwright:
        #browser = p.chromium.launch(headless=False, slow_mo=50)
        browser = playwright.chromium.launch(args=['--start-maximized'], headless=False)  # Use headless=True for CI
        # ✅ Load existing session state if available
        try:
            #context = browser.new_context(storage_state="state.json")
            context = browser.new_context(no_viewport=True, storage_state="state.json")
            print("✅ Loaded existing session.")
        except:
            context = browser.new_context()
            print("🔐 No saved session found, logging in...")

        page = context.new_page()
        config = input_config_value()
        url = config["base_url"]
        page.goto(url)

        # Check if already logged in

        if page.locator("#profileDropdown-navbar").is_visible():
            print("✅ Already logged in, reusing session.")
        else:
            username = config['User_name']
            password = config['pass_password']
            login_page=LoginPage(page)
            login_page.login_app(username,password)
            page.locator("#profileDropdown-navbar").wait_for(state="visible", timeout=50000)
            print("✅ Successfully logged in!")
            # ✅ Save session state after login
            context.storage_state(path="state.json")
        yield page, context  # Return the logged-in page for reuse
        browser.close()  # Close the browser after all tests



@pytest.fixture(scope="session")
def login_marketing_manager_user_phase3():
    """Logs in once per session and reuses the Playwright page."""
    with sync_playwright() as playwright:
        #browser = p.chromium.launch(headless=False, slow_mo=50)
        browser = playwright.chromium.launch(args=['--start-maximized'], headless=False)  # Use headless=True for CI
        # ✅ Load existing session state if available
        try:
            #context = browser.new_context(storage_state="state.json")
            context = browser.new_context(no_viewport=True, storage_state="state.json")
            print("✅ Loaded existing session.")
        except:
            context = browser.new_context()
            print("🔐 No saved session found, logging in...")

        page = context.new_page()
        config = input_config_value()
        url = config["base_url2"]
        page.goto(url)

        # Check if already logged in

        if page.locator("#profileDropdown-navbar").is_visible():
            print("✅ Already logged in, reusing session.")
        else:
            username = config['marketing_manger_user']
            password = config['marketing_manger_password']
            login_page=LoginPage(page)
            login_page.login_app(username,password)
            page.locator("#profileDropdown-navbar").wait_for(state="visible", timeout=50000)
            print("✅ Successfully logged in!")
            # ✅ Save session state after login
            context.storage_state(path="state.json")
        yield page, context  # Return the logged-in page for reuse
        browser.close()  # Close the browser after all tests




logger = setup_logger()
SESSION_DIR = "./session"
os.makedirs(SESSION_DIR, exist_ok=True)

SESSION_FILE = os.path.join(SESSION_DIR, "session.json")
SESSION_MAX_AGE = timedelta(hours=7)

@pytest.fixture(scope="session")
def browser_context_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        if is_session_valid():
            # Reuse existing session
            context = browser.new_context(
                storage_state=SESSION_FILE,
                no_viewport=True,
            )

        else:
            context = browser.new_context(no_viewport=True)

        context.new_page()
        yield context
        context.close()

# loads each time u call the page it checks email visibility for each test case
@pytest.fixture(scope="function")
def page(browser_context_session, input_config):
    page = browser_context_session.new_page()
    if is_session_valid():
        url = input_config["session_url"]
    else:
        url = input_config["base_url"]

    page.goto(url, wait_until='load', timeout=150001)

    email_loc = page.get_by_placeholder("Email")

    # --- Auto-renew login if session expired or file missing ---
    if email_loc.is_visible():
        logger.warning("Session expired or no session. Re-logging in...")
        login_page = LoginPage(page)
        login_page.login_app(input_config["username"], input_config["password"])

        # Save new session
        browser_context_session.storage_state(path=SESSION_FILE)
        logger.info("Re-login successful, session renewed and saved.")

    yield page
    page.close()



def is_session_valid():
    if not os.path.exists(SESSION_FILE):
        return False
    file_time = datetime.fromtimestamp(os.path.getmtime(SESSION_FILE))
    now = datetime.now()
    age = now - file_time
    logger.info(f" Session file last updated: {file_time}")
    logger.info(f" Session age: {age}")
    return age < SESSION_MAX_AGE

