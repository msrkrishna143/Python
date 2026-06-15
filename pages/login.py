from playwright.sync_api import sync_playwright
import time
class LoginPage:
    def __init__(self, page):
        self.page = page


    def login(self, input_config):

        url = input_config.get('base_url')
        # url='http://uheph3qa.demo.aezion.com'
        self.page.goto(url, wait_until='load', timeout=60000)
        # self.page.goto(url, wait_until='load')
        # self.page.goto(url)
        # self.page.goto(url, timeout=60000)
        # self.page.get_by_placeholder("Email").fill("jaiprasanth.r@aezion.com")
        self.page.get_by_placeholder("Email").fill("anitha.kn@aezion.com")
        self.page.get_by_placeholder("Password").fill("Aezion@600")
        self.page.click("button[type='submit']")
        self.page.wait_for_load_state('networkidle')
        if self.page.title() == 'Proposals - UHE':
            return True
        else :
            return False

    def login_app(self, username, password):
        self.page.get_by_placeholder("Email").fill(username)
        self.page.get_by_placeholder("Password").fill(password)
        self.page.click("button[type='submit']")
        self.page.wait_for_load_state('networkidle')
        if self.page.title() == 'Proposals - UHE':
            return True
        else:
            return False


    def logout(self):
        time.sleep(3)
        self.page.locator("#profileDropdown-navbar").click()
        self.page.locator('[data-target="#confirm-logout"]').click()
        time.sleep(3)
        