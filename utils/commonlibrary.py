import random
import time
import pytest
from test.conftest import logger
from datetime import datetime
import os
from faker import Faker


class CommonLibrary:
    def __init__(self, page):
        self.page = page
        self.generated_names = set()  # Track previously generated names

        self.demo = False  # Set to True to bypass time.sleep in demo mode

        # Override time.sleep if demo is True
        if self.demo:
            time.sleep = lambda x: None

    @pytest.fixture(scope="session", autouse=True)
    def setup_demo_mode(self):
        demo = True  # Set to True to bypass time.sleep
        if demo:
            logger.info("Enabling demo mode: bypassing time.sleep")
            time.sleep = lambda x: None
        else:
            logger.info("Disabling demo mode: restoring time.sleep")
            time.sleep = time.__dict__['sleep']
        yield

    def generate_random_name(self, prefix="Section"):

        random_number = random.randint(100, 999)
        fake_name = f"{prefix} {random_number}"

        while fake_name in self.generated_names:
            random_number = random.randint(100, 999)
            fake_name = f"{prefix} {random_number}"

        self.generated_names.add(fake_name)
        return fake_name

    def after_edit_product_validate_pricebook(self, product_edit_value, section_edit_value, service_name,
                                              sub_section_name):
        time.sleep(5)
        self.page.click('.navbar-toggler.navbar-toggler.align-self-center')
        time.sleep(5)
        self.page.locator("#NewPricebook").click()
        time.sleep(3)
        if service_name == "Flat Roofing":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(5)
            self.page.locator(f'[data-servicename="FlatRoofing"]').click()
            time.sleep(3)
            service_class_name = "FlatRoofing"
            self.edit_product_validations(service_class_name, product_edit_value, section_edit_value, service_name,
                                          sub_section_name)
        elif service_name == "Pitched Roofing":
            service_class_name = "PitchedRoofing"
            self.edit_product_validations(service_class_name, product_edit_value, section_edit_value, service_name,
                                          sub_section_name)
        elif service_name == "Windows":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Windows"]').click()
            time.sleep(3)
            service_class_name = "Windows"
            self.edit_product_validations(service_class_name, product_edit_value, section_edit_value, service_name,
                                          sub_section_name)
        elif service_name == "Exterior Paint":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="ExteriorPaint"]').click()
            time.sleep(3)
            service_class_name = "ExteriorPaint"
            self.edit_product_validations(service_class_name, product_edit_value, section_edit_value, service_name,
                                          sub_section_name)
        elif service_name == "Doors":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Doors"]').click()
            time.sleep(3)
            service_class_name = "Doors"
            self.edit_product_validations(service_class_name, product_edit_value, section_edit_value, service_name,
                                          sub_section_name)
        elif service_name == "Siding":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Siding"]').click()
            time.sleep(3)
            service_class_name = "Siding"
            self.edit_product_validations(service_class_name, product_edit_value, section_edit_value, service_name,
                                          sub_section_name)
        elif service_name == "Interior Paint":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="InteriorPaint"]').click()
            time.sleep(3)
            service_class_name = "InteriorPaint"
            self.edit_product_validations(service_class_name, product_edit_value, section_edit_value, service_name,
                                          sub_section_name)
        elif service_name == "Carpentry":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Carpentry"]').click()
            time.sleep(3)
            service_class_name = "Carpentry"
            self.edit_product_validations(service_class_name, product_edit_value, section_edit_value, service_name,
                                          sub_section_name)
        elif service_name == "Miscellaneous":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Miscellaneous"]').click()
            time.sleep(3)
            service_class_name = "Miscellaneous"
            self.edit_product_validations(service_class_name, product_edit_value, section_edit_value, service_name,
                                          sub_section_name)

    def after_delete_product_validate_pricebook(self, section_name, product_name, service_name, sub_section_name):
        time.sleep(5)
        self.page.click('.navbar-toggler.navbar-toggler.align-self-center')
        time.sleep(3)
        self.page.locator("#NewPricebook").click()
        time.sleep(3)
        if service_name == "Flat Roofing":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="FlatRoofing"]').click()
            time.sleep(3)
            service_class_name = "FlatRoofing"
            self.delete_product_validations(service_class_name, product_name, section_name, service_name,
                                            sub_section_name)
        elif service_name == "Pitched Roofing":
            service_class_name = "PitchedRoofing"
            self.delete_product_validations(service_class_name, product_name, section_name, service_name,
                                            sub_section_name)
        elif service_name == "Windows":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Windows"]').click()
            time.sleep(3)
            service_class_name = "Windows"
            self.delete_product_validations(service_class_name, product_name, section_name, service_name,
                                            sub_section_name)
        elif service_name == "Doors":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Doors"]').click()
            time.sleep(3)
            service_class_name = "Doors"
            self.delete_product_validations(service_class_name, product_name, section_name, service_name,
                                            sub_section_name)
        elif service_name == "Siding":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Siding"]').click()
            time.sleep(3)
            service_class_name = "Siding"
            self.delete_product_validations(service_class_name, product_name, section_name, service_name,
                                            sub_section_name)
        elif service_name == "Interior Paint":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="InteriorPaint"]').click()
            time.sleep(3)
            service_class_name = "InteriorPaint"
            self.delete_product_validations(service_class_name, product_name, section_name, service_name,
                                            sub_section_name)
        elif service_name == "Exterior Paint":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="ExteriorPaint"]').click()
            time.sleep(3)
            service_class_name = "ExteriorPaint"
            self.delete_product_validations(service_class_name, product_name, section_name, service_name,
                                            sub_section_name)
        elif service_name == "Carpentry":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Carpentry"]').click()
            time.sleep(3)
            service_class_name = "Carpentry"
            self.delete_product_validations(service_class_name, product_name, section_name, service_name,
                                            sub_section_name)
        elif service_name == "Miscellaneous":
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Miscellaneous"]').click()
            time.sleep(3)
            service_class_name = "Miscellaneous"
            self.delete_product_validations(service_class_name, product_name, section_name, service_name,
                                            sub_section_name)

    def edit_product_validations(self, service_class_name, product_edit_value, section_edit_value, service_name,
                                 sub_section_name):
        time.sleep(3)
        total_sections = self.page.locator(f".{service_class_name}-accordion").count()
        for k in range(total_sections):
            pf_section = self.page.locator(
                f".{service_class_name}-accordion.sections.sections-index-{k}").locator(".card-header").locator(
                ".align-items-center").inner_text()
            if pf_section == section_edit_value:
                if sub_section_name == "" or sub_section_name == "Select":
                    if service_name == "Flat Roofing":
                        self.page.locator(f"#FlatRoofing-tr-section-{k}-product-0").locator(
                            f'[data-id="Sections_{k}__Products_0__ProductId"]').click()
                    else:
                        self.page.locator(f'[data-id="Sections_{k}__Products_0__ProductId"]').click()
                else:
                    sub_section_count = self.page.locator(
                        f".{service_class_name}-accordion.sections.sections-index-{k}").locator(
                        ".card-body").locator(
                        ".align-items-center").locator(".text-prim").count()
                    for i in range(sub_section_count):
                        ss_name = self.page.locator(
                            f".{service_class_name}-accordion.sections.sections-index-{k}").locator(
                            ".card-body").locator(
                            ".align-items-center").locator(".text-prim").nth(i).inner_text()
                        if ss_name == sub_section_name:
                            self.page.locator(f"#{service_class_name}-tr-section-{k}-product-0").locator(
                                f'[data-id="Sections_{k}__Subsection_{i}__Products_0__ProductId"]').click()

                time.sleep(2)
                product_elements = self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").all()
                product_list = []
                for pitem in product_elements:
                    product = pitem.inner_text()
                    if product != "Select":
                        product_list.append(product)

                if product_edit_value in product_list:
                    print(f"{product_edit_value} Product Edit Done Successfully")

                else:
                    print(f"{product_edit_value} Product Edit Not done Successfully")
                break

        self.page.locator(".btn.btn-outline-light").nth(0).click()
        time.sleep(2)
        self.page.locator("#urpiceProducts").click()
        time.sleep(2)
        self.page.locator(".nav-item").locator(f'[data-name="{service_name}"]').click()
        time.sleep(2)

    def delete_product_validations(self, service_class_name, product_name, section_name, service_name,
                                   sub_section_name):
        time.sleep(3)
        total_sections = self.page.locator(f".{service_class_name}-accordion").count()
        for k in range(total_sections):
            pf_section = self.page.locator(
                f".{service_class_name}-accordion.sections.sections-index-{k}").locator(".card-header").locator(
                ".align-items-center").inner_text()
            if pf_section == section_name:
                if sub_section_name == "":
                    if service_name == "Flat Roofing":
                        self.page.locator(f"#FlatRoofing-tr-section-{k}-product-0").locator(
                            f'[data-id="Sections_{k}__Products_0__ProductId"]').click()
                    else:
                        self.page.locator(f'[data-id="Sections_{k}__Products_0__ProductId"]').click()
                else:
                    sub_section_count = self.page.locator(
                        f".{service_class_name}-accordion.sections.sections-index-{k}").locator(
                        ".card-body").locator(
                        ".align-items-center").locator(".text-prim").count()
                    for i in range(sub_section_count):
                        ss_name = self.page.locator(
                            f".{service_class_name}-accordion.sections.sections-index-{k}").locator(
                            ".card-body").locator(
                            ".align-items-center").locator(".text-prim").nth(i).inner_text()
                        if ss_name == sub_section_name:
                            self.page.locator(f"#{service_class_name}-tr-section-{k}-product-0").locator(
                                f'[data-id="Sections_{k}__Subsection_{i}__Products_0__ProductId"]').click()
                time.sleep(2)
                product_elements = self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").all()
                product_list = []
                for pitem in product_elements:
                    product = pitem.inner_text()
                    if product != "Select":
                        product_list.append(product)

                if product_name in product_list:
                    print(f"{product_name} Product Not deleted Successfully")
                else:
                    print(f"{product_name} Product Delete Successfully")
                break
        self.page.locator(".btn.btn-outline-light").nth(0).click()
        time.sleep(2)
        self.page.locator("#urpiceProducts").click()
        time.sleep(2)
        self.page.locator(".nav-item").locator(f'[data-name="{service_name}"]').click()
        time.sleep(2)

    def add_product_validations(self, service_class_name, search_value, section_name, service_name, sub_section_name):
        total_sections = self.page.locator(f".{service_class_name}-accordion").count()
        for k in range(total_sections):
            pf_section = self.page.locator(
                f".{service_class_name}-accordion.sections.sections-index-{k}").locator(".card-header").locator(
                ".align-items-center").inner_text()
            if pf_section == section_name:
                if sub_section_name == "":
                    if service_name == "Flat Roofing":
                        self.page.locator(f"#FlatRoofing-tr-section-{k}-product-0").locator(
                            f'[data-id="Sections_{k}__Products_0__ProductId"]').click()
                    else:
                        self.page.locator(f'[data-id="Sections_{k}__Products_0__ProductId"]').click()
                else:
                    sub_section_count = self.page.locator(
                        f".{service_class_name}-accordion.sections.sections-index-{k}").locator(
                        ".card-body").locator(
                        ".align-items-center").locator(".text-prim").count()
                    for i in range(sub_section_count):
                        ss_name = self.page.locator(
                            f".{service_class_name}-accordion.sections.sections-index-{k}").locator(
                            ".card-body").locator(
                            ".align-items-center").locator(".text-prim").nth(i).inner_text()
                        if ss_name == sub_section_name:
                            self.page.locator(f"#{service_class_name}-tr-section-{k}-product-0").locator(
                                f'[data-id="Sections_{k}__Subsection_{i}__Products_0__ProductId"]').click()

                time.sleep(2)
                product_elements = self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").all()
                product_list = []
                for pitem in product_elements:
                    product = pitem.inner_text()
                    if product != "Select":
                        product_list.append(product)
                if search_value in product_list:
                    print(f"{search_value} Product added in Pricebook successfully")
                else:
                    print(f"{search_value} Product not added in Pricebook successfully")
                break

        self.page.locator(".btn.btn-outline-light").nth(0).click()
        time.sleep(2)
        self.page.locator("#urpiceProducts").click()
        time.sleep(2)
        self.page.locator(".nav-item").locator(f'[data-name="{service_name}"]').click()
        time.sleep(2)

    def add_section_validation(self, section_name, service_name, service_class_name):
        time.sleep(5)
        total_sections = self.page.locator(f".{service_class_name}-accordion").count()
        print(section_name)
        for k in range(total_sections):
            pf_section = self.page.locator(
                f".{service_class_name}-accordion.sections").nth(k).locator(".card-header").locator(
                ".align-items-center").inner_text()
            time.sleep(2)
            print(pf_section)
            if pf_section == section_name:
                print(f"{section_name} Section added in Pricebook successfully")
                break

        self.page.locator(".btn.btn-outline-light").nth(0).click()
        time.sleep(2)
        self.page.locator("#upriceSection").click()
        time.sleep(2)
        if service_name != "Pitched Roofing":
            self.page.locator(".nav-item").locator(".nav-link.service-name").filter(has_text=f"{service_name}").click()
            time.sleep(2)

    def add_sub_section_validation(self, section_name, service_name, service_class_name, sub_section_name, action):
        time.sleep(5)
        section_elements = self.page.locator(f'.{service_class_name}-accordion.sections.subsections').all()
        for x, item in enumerate(section_elements):
            pf_section = item.locator(".card-header").locator(".align-items-center").inner_text()
            if pf_section == section_name:
                sub_section_elements = item.locator('[data-parent="#accordion-line-pricewindows"]').locator(
                    ".text-prim").all()
                sub_section_names = [sub.inner_text() for sub in sub_section_elements]
                if sub_section_name in sub_section_names:
                    print(f"{sub_section_name} Sub Section {action} in {section_name} in Price Book")
                    logger.info(f"{sub_section_name} Sub Section {action} in {section_name} in Price Book")
                else:
                    print(f"{sub_section_name} Sub Section not {action} in {section_name} in Price Book")
                    logger.info(f"{sub_section_name} Sub Section not {action} in {section_name} in Price Book")

        self.page.locator(".btn.btn-outline-light").nth(0).click()
        time.sleep(2)
        self.page.locator("#upriceSubSection").click()
        time.sleep(2)
        if service_name != "Pitched Roofing":
            self.page.locator(".nav-item").locator(".nav-link.service-name").filter(has_text=f"{service_name}").click()
            time.sleep(2)

    def after_add_sub_section_validate_pricebook(self, section_name, sub_section_name, service_class_name, service_name,
                                                 action):

        time.sleep(5)
        if action == "Edited":
            self.page.click('.navbar-toggler.navbar-toggler.align-self-center')
        else:
            self.page.click('.navbar-toggler.navbar-toggler.align-self-center')
            self.page.click('.navbar-toggler.navbar-toggler.align-self-center')

        time.sleep(5)
        self.page.locator("#NewPricebook").click()
        time.sleep(3)
        self.page.locator("#PricebookName").fill("test")
        time.sleep(3)
        self.page.locator(f'[data-servicename="{service_class_name}"]').click()
        time.sleep(3)
        self.add_sub_section_validation(section_name, service_name, service_class_name, sub_section_name, action)

    def uprice_add_section_validation(self, section_name, service_name, service_class_name):
        time.sleep(5)
        self.page.click('.navbar-toggler.navbar-toggler.align-self-center')
        self.page.click('.navbar-toggler.navbar-toggler.align-self-center')
        time.sleep(5)
        self.page.locator("#NewPricebook").click()
        time.sleep(3)
        self.page.locator("#PricebookName").fill("test")
        time.sleep(3)
        self.page.locator(f'[data-servicename="{service_class_name}"]').click()
        time.sleep(3)
        self.add_section_validation(section_name, service_name, service_class_name)

    def edit_section_validation(self, service_name, section_name, service_class_name):
        time.sleep(5)
        total_sections = self.page.locator(f".{service_class_name}-accordion").count()

        for k in range(total_sections):
            pf_section = self.page.locator(
                f".{service_class_name}-accordion.sections").nth(k).locator(".card-header").locator(
                ".align-items-center").inner_text()

            if pf_section == section_name:
                print(f"{section_name} Section Edited done in Pricebook successfully")
                break

        self.page.locator(".btn.btn-outline-light").nth(0).click()
        time.sleep(2)
        self.page.locator("#upriceSection").click()
        time.sleep(2)
        if service_name != "Pitched Roofing":
            self.page.locator(".nav-item").locator(".nav-link.service-name").filter(has_text=f"{service_name}").click()
            time.sleep(2)

    def uprice_edit_section_validation(self, section_name, service_name, service_class_name):
        time.sleep(5)
        self.page.click('.navbar-toggler.navbar-toggler.align-self-center')
        self.page.click('.navbar-toggler.navbar-toggler.align-self-center')
        time.sleep(5)
        self.page.locator("#NewPricebook").click()
        time.sleep(3)
        self.page.locator("#PricebookName").fill("test")
        time.sleep(3)
        self.page.locator(f'[data-servicename="{service_class_name}"]').click()
        time.sleep(3)
        self.edit_section_validation(service_name, section_name, service_class_name)

    def delete_section_validation(self, section_name, service_class_name, service_name):
        time.sleep(3)
        total_sections = self.page.locator(f".{service_class_name}-accordion").count()
        section_list = []
        for k in range(total_sections):
            pf_section = self.page.locator(
                f".{service_class_name}-accordion.sections").nth(k).locator(".card-header").locator(
                ".align-items-center").inner_text()
            section_list.append(pf_section)
        if section_name in section_list:
            print(f"{section_name} Section Not deleted Successfully")
        else:
            print(f"{section_name} Section Delete Successfully")

        self.page.locator(".btn.btn-outline-light").nth(0).click()
        time.sleep(2)
        self.page.locator("#upriceSection").click()
        time.sleep(2)
        if service_name != "Pitched Roofing":
            self.page.locator(".nav-item").locator(".nav-link.service-name").filter(has_text=f"{service_name}").click()
            time.sleep(2)

    def uprice_deleted_section_validation(self, section_name, service_class_name, service_name):
        time.sleep(3)
        self.page.click('.navbar-toggler.navbar-toggler.align-self-center')
        # self.page.click('.navbar-toggler.navbar-toggler.align-self-center')
        time.sleep(5)
        self.page.locator("#NewPricebook").click()
        time.sleep(3)
        self.page.locator("#PricebookName").fill("test")
        time.sleep(3)
        self.page.locator(f'[data-servicename="{service_class_name}"]').click()
        time.sleep(3)
        self.delete_section_validation(section_name, service_class_name, service_name)

    def delete_sub_section_validation(self, section_name, service_class_name, service_name, sub_section_name):
        time.sleep(5)
        section_elements = self.page.locator(f'.{service_class_name}-accordion.sections.subsections').all()
        for x, item in enumerate(section_elements):
            pf_section = item.locator(".card-header").locator(".align-items-center").inner_text()
            if pf_section == section_name:
                sub_section_elements = item.locator('[data-parent="#accordion-line-pricewindows"]').locator(
                    ".text-prim").all()
                sub_section_names = [sub.inner_text() for sub in sub_section_elements]
                if sub_section_name in sub_section_names:
                    print(f"{sub_section_name} Sub Section created in {section_name} in Price Book")
                    logger.info(f"{sub_section_name} Sub Section created in {section_name} in Price Book")
                else:
                    print(f"{sub_section_name} Sub Section deleted {section_name} in Price Book")
                    logger.info(f"{sub_section_name} Sub Section deleted in {section_name} in Price Book")

        self.page.locator(".btn.btn-outline-light").nth(0).click()
        time.sleep(2)
        self.page.locator("#upriceSubSection").click()
        time.sleep(2)
        if service_name != "Pitched Roofing":
            self.page.locator(".nav-item").locator(".nav-link.service-name").filter(has_text=f"{service_name}").click()
            time.sleep(2)

    def after_delete_sub_section_validate_pricebook(self, section_name, sub_section_name, service_name,
                                                    service_class_name):
        time.sleep(3)
        self.page.click('.navbar-toggler.navbar-toggler.align-self-center')
        time.sleep(5)
        self.page.locator("#NewPricebook").click()
        time.sleep(3)
        self.page.locator("#PricebookName").fill("test")
        time.sleep(3)
        self.page.locator(f'[data-servicename="{service_class_name}"]').click()
        time.sleep(3)
        self.delete_sub_section_validation(section_name, service_class_name, service_name, sub_section_name)

    def after_add_product_validate_pricebook(self, section_name, search_value, service_name, sub_section_name):
        time.sleep(5)
        self.page.click('.navbar-toggler.navbar-toggler.align-self-center')
        self.page.click('.navbar-toggler.navbar-toggler.align-self-center')
        time.sleep(5)
        self.page.locator("#NewPricebook").click()
        time.sleep(3)
        if service_name == "Flat Roofing":
            service_class_name = "FlatRoofing"
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="FlatRoofing"]').click()
            time.sleep(3)
            self.add_product_validations(service_class_name, search_value, section_name, service_name, sub_section_name)
        elif service_name == "Pitched Roofing":
            service_class_name = "PitchedRoofing"
            self.add_product_validations(service_class_name, search_value, section_name, service_name, sub_section_name)
        elif service_name == "Windows":
            service_class_name = "Windows"
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Windows"]').click()
            time.sleep(3)
            self.add_product_validations(service_class_name, search_value, section_name, service_name, sub_section_name)
        elif service_name == "Doors":
            service_class_name = "Doors"
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Doors"]').click()
            time.sleep(3)
            self.add_product_validations(service_class_name, search_value, section_name, service_name, sub_section_name)
        elif service_name == "Siding":
            service_class_name = "Siding"
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Siding"]').click()
            time.sleep(3)
            self.add_product_validations(service_class_name, search_value, section_name, service_name, sub_section_name)
        elif service_name == "Interior Paint":
            service_class_name = "InteriorPaint"
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="InteriorPaint"]').click()
            time.sleep(3)
            self.add_product_validations(service_class_name, search_value, section_name, service_name, sub_section_name)
        elif service_name == "Exterior Paint":
            service_class_name = "ExteriorPaint"
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="ExteriorPaint"]').click()
            time.sleep(3)
            self.add_product_validations(service_class_name, search_value, section_name, service_name, sub_section_name)
        elif service_name == "Carpentry":
            service_class_name = "Carpentry"
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Carpentry"]').click()
            time.sleep(3)
            self.add_product_validations(service_class_name, search_value, section_name, service_name, sub_section_name)
        elif service_name == "Miscellaneous":
            service_class_name = "Miscellaneous"
            self.page.locator("#PricebookName").fill("test")
            time.sleep(3)
            self.page.locator(f'[data-servicename="Miscellaneous"]').click()
            time.sleep(3)
            self.add_product_validations(service_class_name, search_value, section_name, service_name, sub_section_name)

    @staticmethod
    def on_success_flow_take_screenshot(page, ss_name):
        screenshots_dir = "./success_screenshot"
        os.makedirs(screenshots_dir, exist_ok=True)
        # Save the screenshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(screenshots_dir, f"{ss_name}_{timestamp}.png")
        page.screenshot(path=screenshot_path)

    def faker_data(self, page):
        self.fake = Faker()
        fake_data = {
            "c_name": self.fake.user_name(),
            "f_name": self.fake.first_name(),
            "l_name": self.fake.last_name(),
            "title": self.fake.name(),
            "p_no": self.fake.phone_number(),
            "e_mail": self.fake.email(),
            "s_name": self.fake.first_name(),
            "user_name": self.fake.user_name(),
            "add": self.fake.address(),
            "zip": self.fake.zipcode(),
            "i_mail": self.fake.email(),
            "city": self.fake.city(),
            "city1": self.fake.city(),
            "zip1": self.fake.zipcode(),
            "add1": self.fake.address(),
            "role": self.fake.word().capitalize(),
            "plan": self.fake.company(),
            "company": self.fake.company(),
            "plan2": self.fake.building_number(),
            "plan3": self.fake.building_number(),
            "contact_name": self.fake.last_name(),
            "contact_email": self.fake.email(),
            "c_no": self.fake.phone_number(),
            "plan_name": self.fake.name(),
            "description": self.fake.words()
        }
        print("Fake Data Generated: ", fake_data)
        return fake_data

    @staticmethod
    def get_all_toaster_messages(page):
        # Select the toast container with class .toast-top-right
        toaster_selector = '#toast-container.toast-top-right .toast'

        try:
            # Wait for the toaster container to become visible
            page.wait_for_selector(toaster_selector, state='visible', timeout=50000)
        except Exception as e:
            print("Toaster messages container not visible:", e)
            return []

        # Get all toaster elements inside the toast container
        toaster_elements = page.locator(toaster_selector).element_handles()

        messages = []

        # Loop through each toaster element and extract the message text
        for toaster in toaster_elements:
            try:
                # Extract the message from the .toast-message element
                message_element = toaster.query_selector('.toast-message')

                # Get the text inside the toast-message element or use a default if not found
                message_text = message_element.inner_text() if message_element else 'No message'

                # Store the extracted message
                messages.append(message_text)
            except Exception as e:
                print(f"Error processing toaster message: {e}")
                continue

        # Return the collected toaster messages
        return messages


    # # Get all toaster messages
    # @staticmethod
    # def get_all_toaster_messages(page):
    #     toaster_selector = '.p-toast-message'
    #
    #     try:
    #         page.wait_for_selector(toaster_selector, state='visible', timeout=50000)
    #     except Exception as e:
    #         return []
    #
    #     toaster_elements = page.locator(toaster_selector).element_handles()
    #
    #     messages = []
    #
    #     for toaster in toaster_elements:
    #         try:
    #             summary = toaster.query_selector('.p-toast-summary')
    #             detail = toaster.query_selector('.p-toast-detail')
    #
    #             summary_text = summary.inner_text() if summary else 'No summary'
    #             detail_text = detail.inner_text() if detail else 'No detail'
    #
    #             message = f"Summary: {summary_text}, Detail: {detail_text}"
    #             messages.append(message)
    #         except Exception as e:
    #             print(f"Error processing toaster message: {e}")
    #             continue
    #     return messages