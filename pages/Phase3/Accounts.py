import time
from test.conftest import logger
from test.conftest import input_config_value
import os
import pandas as pd
from utils.commonlibrary import CommonLibrary
import re


class Accounts:
    def __init__(self, page):
        self.page = page
        self.config = input_config_value()

    def account_other_filters(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        self.page.locator(".sidebar-click").click()
        time.sleep(2)
        self.page.locator('[data-id="filterOthers"]').click()
        time.sleep(5)
        elements = self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').all()
        time.sleep(2)
        others_lists = []
        for item in elements:
            other = item.inner_text()
            print(other)
            if other != "Select" and other != "":
                self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                    f"{other}",
                    exact=True).click()
                others_lists.append(other)
                time.sleep(2)
                self.page.locator("#applyFilter").click()
                time.sleep(2)
                if self.page.locator("#AccountPager").is_visible():
                    time.sleep(2)
                    count_text = self.page.locator("#AccountPager").locator(".px-3").inner_text()
                    value = int(count_text.split()[-2])
                    logger.info(f"Account Other Filters to value {other} and count : {value}")
                    print(f"Account Other Filters to value {other} and count : {value}")
                else:
                    value = 0
                    logger.info(f"Account Other Filters to value {other} and count : {value}")
                    print(f"Account Other Filters to value {other} and count : {value}")

                time.sleep(2)
                self.page.locator(".sidebar-click").click()
                time.sleep(2)
                self.page.locator('[data-id="filterOthers"]').click()
                time.sleep(2)
                self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                    f"{other}",
                    exact=True).click()
                time.sleep(2)
        self.page.locator(".mdi-close").click()
        time.sleep(2)

    def account_filer_state(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        self.page.locator(".sidebar-click").click()
        time.sleep(2)
        self.page.locator('[data-id="filterStates"]').click()
        time.sleep(2)
        time.sleep(5)
        elements = self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').all()
        time.sleep(2)
        state_lists = []
        for item in elements:
            state = item.inner_text()
            print(state)
            if state != "Select" and state != "":
                self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                    f"{state}",
                    exact=True).click()
                state_lists.append(state)
                time.sleep(2)
                self.page.locator("#applyFilter").click()
                time.sleep(2)
                if self.page.locator("#AccountPager").is_visible():
                    time.sleep(2)
                    count_text = self.page.locator("#AccountPager").locator(".px-3").inner_text()
                    value = int(count_text.split()[-2])
                    logger.info(f"Account State to value {state} and count : {value}")
                    print(f"Account State to value {state} and count : {value}")
                else:
                    value = 0
                    logger.info(f"Account State to value {state} and count : {value}")
                    print(f"Account State to value {state} and count : {value}")

                time.sleep(2)
                self.page.locator(".sidebar-click").click()
                time.sleep(2)
                self.page.locator('[data-id="filterStates"]').click()
                time.sleep(2)
                self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                    f"{state}",
                    exact=True).click()
                time.sleep(2)

        self.page.locator(".clear-filter").click()
        time.sleep(2)

    def account_filter_types(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        self.page.locator(".sidebar-click").click()
        time.sleep(2)
        self.page.locator('[data-id="filterLeadTypes"]').click()
        time.sleep(2)
        time.sleep(5)
        elements = self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').all()
        time.sleep(2)
        lead_types = []
        for item in elements:
            load_value = item.inner_text()
            print(load_value)
            if load_value != "Select" and load_value != "":
                self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                    f"{load_value}",
                    exact=True).click()
                lead_types.append(load_value)
                time.sleep(2)
                self.page.locator("#applyFilter").click()
                time.sleep(2)
                if self.page.locator("#AccountPager").is_visible():
                    time.sleep(2)
                    count_text = self.page.locator("#AccountPager").locator(".px-3").inner_text()
                    value = int(count_text.split()[-2])
                    logger.info(f"Account Types to value {load_value} and count : {value}")
                    print(f"Account Types to value {load_value} and count : {value}")
                else:
                    value = 0
                    logger.info(f"Account Types to value {load_value} and count : {value}")
                    print(f"Account Types to value {load_value} and count : {value}")

                time.sleep(2)
                self.page.locator(".sidebar-click").click()
                time.sleep(2)
                self.page.locator('[data-id="filterLeadTypes"]').click()
                time.sleep(2)
                self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                    f"{load_value}",
                    exact=True).click()
                time.sleep(2)

        self.page.locator(".clear-filter").click()
        time.sleep(2)

    def account_filter_date_from_to_date(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        self.page.locator(".sidebar-click").click()
        time.sleep(2)
        from_date = "09/15/2025"
        self.page.locator("#FromDate").type(f"{from_date}")
        time.sleep(2)
        end_date = "10/30/2025"
        self.page.locator("#ToDate").type(f"{end_date}")
        time.sleep(5)
        self.page.locator("#applyFilter").click()
        time.sleep(10)
        if self.page.locator("#AccountPager").is_visible():
            time.sleep(2)
            count_text = self.page.locator("#AccountPager").locator(".px-3").inner_text()
            value = int(count_text.split()[-2])
            logger.info(f"Account filter Date from {from_date} to  {end_date} and count : {value}")
            print(f"Account filter Date from {from_date} to  {end_date} and count : {value}")
        else:
            value = 0
            logger.info(f"Account filter Date from {from_date} to  {end_date} and count : {value}")
            print(f"Account filter Date from {from_date} to  {end_date} and count : {value}")

        self.page.locator(".sidebar-click").click()
        time.sleep(2)
        self.page.locator(".clear-filter").click()
        time.sleep(2)

    def account_contacts_action_call(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        tr_body_elements = tables.locator('tbody tr').all()
        i = 0
        for tr in tr_body_elements:
            tr.locator("td:nth-child(2)").click()
            time.sleep(2)
            # self.page.locator(".clear-tab-storage").nth(i).click()
            i += 1
            self.page.locator("#accountContactsTab").click()
            time.sleep(6)
            contact_tables = self.page.locator(".Usertable").locator(".custom-table")
            contact_first_tr = contact_tables.locator('tbody tr').first
            check_rows = contact_first_tr.locator("td:nth-child(1)").inner_text()
            if check_rows != "No data found":
                if self.page.locator(".px-1.py-1").nth(1).is_visible():
                    self.page.locator(".px-1.py-1").nth(1).click()
                    time.sleep(2)
                    if self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                            .get_by_text("Call", exact=True).nth(0).is_visible():
                        self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                            .get_by_text("Call", exact=True).nth(0).click()
                        time.sleep(5)
                        self.page.locator("#btnSaveCTMContacts").click()
                        time.sleep(2)
                        logger.info(f"Account Contacts Action Call Done Successfully")
                        print(f"Account Contacts Action Call Done Successfully")
                        self.page.click('button.swal-button.swal-button--confirm.btn.btn-primary')
                        time.sleep(2)
                        self.page.locator("#btnCloseDialModelPopup").click()
                        time.sleep(2)
                        self.page.locator(".backarrow").click()
                        time.sleep(2)
                        break
            else:
                self.page.locator(".backarrow").click()
                time.sleep(2)

    def account_contacts_action_dnc(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        tr_body_elements = tables.locator('tbody tr').all()
        i = 0
        for tr in tr_body_elements:
            tr.locator("td:nth-child(2)").click()
            i += 1
            time.sleep(2)
            self.page.locator("#accountContactsTab").click()
            time.sleep(6)
            contact_tables = self.page.locator(".Usertable").locator(".custom-table")
            contact_first_tr = contact_tables.locator('tbody tr').first
            check_rows = contact_first_tr.locator("td:nth-child(1)").inner_text()
            if check_rows != "No data found":
                if self.page.locator(".px-1.py-1").nth(1).is_visible():
                    contact_email = contact_first_tr.locator("td:nth-child(3)").inner_text()
                    match = re.search(r'[\w\.-]+@[\w\.-]+', contact_email)
                    contact_email = match.group(0)
                    #contact_email = contact_first_tr.locator("td:nth-child(4)").locator(".badge-danger").inner_text()
                    self.page.locator(".px-1.py-1").nth(1).click()
                    time.sleep(2)
                    self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                        .get_by_text("Mark as DNC", exact=True).nth(0).click()
                    time.sleep(5)
                    if self.page.locator("#DoNotContactSettings_0__IsPrimaryPhone_Donotcall").is_visible():
                        if contact_first_tr.locator("td:nth-child(4)").locator(".mb-1.p-1").is_visible():
                            time.sleep(2)
                        else:
                            self.page.locator("#DoNotContactSettings_0__IsPrimaryPhone_Donotcall").click()
                            time.sleep(2)
                            self.page.locator(
                                '[data-id="DoNotContactSettings_0__IsPrimaryPhone_Donotcall_ReasonId"]').click()
                            time.sleep(2)
                            self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                                .get_by_text("Deceased", exact=True).nth(0).click()

                    self.page.locator("#btn-save").click()
                    time.sleep(2)
                    if self.page.locator(".toast.toast-success").is_visible():
                        message = self.page.locator(".toast-message").inner_text()
                        print(message)
                        logger.info(f"{message}")
                        print(message)
                    tables = self.page.locator(".Usertable").locator(".custom-table")
                    first_tr = tables.locator('tbody tr').first
                    dnc_name = first_tr.locator("td:nth-child(4)").locator(".badge-danger").inner_text()
                    if dnc_name == "DNC/DNT":
                        logger.info(f"Account Contact DNC Action Validation Done Successfully")
                        print(f"Account Contact DNC Action Validation Done Successfully")
                    else:
                        logger.info(f"Account Contact DNC Action Validation failed")
                        print(f"Account Contact DNC Action Validation failed")

                    self.page.locator(".backarrow").click()
                    time.sleep(5)
                    self.page.locator("#CustomersMenu").click()
                    time.sleep(17)
                    self.page.locator("#searchContacts").fill(contact_email)
                    self.page.locator("#searchContacts").press("Enter")
                    time.sleep(17)
                    contact_table = self.page.locator(".custom-table.m-0")
                    contact_tr_body_elements = contact_table.locator('tbody tr').all()
                    for ctr in contact_tr_body_elements:
                        if ctr.locator("td:nth-child(4)").locator(".badge-danger").is_visible():
                            dnc_name = ctr.locator("td:nth-child(4)").locator(".badge-danger").inner_text()
                            if dnc_name == "DNC/DNT":
                                logger.info(f"Account Contact DNC Action Validation Done Successfully")
                                print(f"Account Contact DNC Action Validation Done Successfully")
                            else:
                                logger.info(f"Account Contact DNC Action Validation failed")
                                print(f"Account Contact DNC Action Validation failed")

                            self.page.locator("#searchContacts").fill("")
                            self.page.locator("#searchContacts").press("Enter")
                            time.sleep(10)
                            break

                    self.page.locator("#LeadsMenu").click()
                    time.sleep(17)
                    self.page.locator("#searchString").fill(contact_email)
                    self.page.locator("#searchString").press("Enter")
                    time.sleep(17)
                    lead_table = self.page.locator(".footable-loaded")
                    lead_tr_body_elements = lead_table.locator('tbody tr').all()
                    for ltr in lead_tr_body_elements:
                        dnc_name = ltr.locator("td:nth-child(3)").locator(".mb-1").nth(1).locator(".badge-danger").inner_text()
                        if dnc_name == "DNC/DNT":
                            logger.info(f"Account Contact DNC Action Validation Done Successfully in Leads module")
                            print(f"Account Contact DNC Action Validation Done Successfully in Leads module")
                        else:
                            logger.info(f"Account Contact DNC Action Validation failed in Leads module")
                            print(f"Account Contact DNC Action Validation failed in Leads module")

                        self.page.locator("#searchString").fill("")
                        self.page.locator("#searchString").press("Enter")
                        time.sleep(10)
                        break
                    break
            else:
                self.page.locator(".backarrow").click()
                time.sleep(2)

    def account_contact_send_email(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        tr_body_elements = tables.locator('tbody tr').all()
        i = 0
        for tr in tr_body_elements:
            tr.locator("td:nth-child(2)").click()
            time.sleep(2)
            # self.page.locator(".clear-tab-storage").nth(i).click()
            i += 1
            self.page.locator("#accountContactsTab").click()
            time.sleep(6)
            contact_tables = self.page.locator(".Usertable").locator(".custom-table")
            contact_first_tr = contact_tables.locator('tbody tr').first
            check_rows = contact_first_tr.locator("td:nth-child(1)").inner_text()
            if check_rows != "No data found":
                if self.page.locator(".px-1.py-1").nth(1).is_visible():
                    self.page.locator(".px-1.py-1").nth(1).click()
                    time.sleep(2)
                    self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                        .get_by_text("Send Email", exact=True).nth(0).click()
                    time.sleep(5)
                    # choose_func = CommonLibrary(self.page)
                    # fake_data = choose_func.faker_data(self.page)
                    # primary_email = fake_data["contact_email"]
                    # self.page.locator("#ToEmail").fill(f"{primary_email}")
                    time.sleep(1)
                    self.page.locator('[data-id="EmailTemplateId"]').click()
                    time.sleep(2)
                    self.page.locator(".dropdown-menu.show:not(.inner)").press('ArrowDown')
                    self.page.locator(".dropdown-menu.show:not(.inner)").press('ArrowDown')
                    self.page.locator(".dropdown-menu.show:not(.inner)").press('Enter')
                    time.sleep(2)
                    self.page.locator("#btnSend").click()
                    time.sleep(2)
                    if self.page.locator(".toast.toast-success").is_visible():
                        message = self.page.locator(".toast-message").inner_text()
                        print(message)
                        logger.info(f"{message}")
                        print(message)
                    self.page.locator(".backarrow").click()
                    time.sleep(2)
                    break
            else:
                self.page.locator(".backarrow").click()
                time.sleep(2)

    def account_contacts_action_delete(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        first_tr = tables.locator('tbody tr').first
        first_tr.locator("td:nth-child(2)").click()
        time.sleep(2)
        self.page.locator("#accountContactsTab").click()
        time.sleep(6)
        if self.page.locator(".px-1.py-1").nth(1).is_visible():
            tables = self.page.locator(".Usertable").locator(".custom-table")
            first_tr = tables.locator('tbody tr').first
            new_primary_email = first_tr.locator("td:nth-child(3)").inner_text()
            match = re.search(r'[\w\.-]+@[\w\.-]+', new_primary_email)
            new_primary_email = match.group(0)
            time.sleep(2)
            self.page.locator(".px-1.py-1").nth(1).click()
            time.sleep(2)
            self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                .get_by_text("Delete", exact=True).nth(0).click()
            time.sleep(5)
            self.page.locator("#btnDeleteContact").click()
            time.sleep(2)
            if self.page.locator(".toast.toast-success").is_visible():
                message = self.page.locator(".toast-message").inner_text()
                print(message)
                logger.info(f"{message}")
                print(message)

            if self.page.locator(".toast.toast-error").is_visible():
                message = self.page.locator(".toast-message").inner_text()
                print(message)
                logger.info(f"{message}")
                print(message)
                self.page.locator("#myModalContent").locator(".close").click()
                time.sleep(1)

            self.page.locator("#searchContacts").fill(new_primary_email)
            self.page.locator("#searchContacts").press("Enter")
            time.sleep(2)
            account_contact_tables = self.page.locator(".Usertable").locator(".custom-table")
            account_first_tr = account_contact_tables.locator('tbody tr').first
            contact_value = account_first_tr.locator("td:nth-child(1)").inner_text()
            if contact_value == "No data found":
                logger.info(f"Account Contact action delete validation done successfully.")
                print(f"Account Contact action delete validation done successfully.")
            else:
                logger.info(f"Account Contact action delete validation failed.")
                print(f"Account Contact action delete validation failed.")

            self.page.locator(".backarrow").click()
            time.sleep(5)
            self.page.locator("#CustomersMenu").click()
            time.sleep(13)
            self.page.locator("#searchContacts").fill(new_primary_email)
            self.page.locator("#searchContacts").press("Enter")
            time.sleep(16)
            contact_table = self.page.locator(".custom-table.m-0")
            contact_tr_body_elements = contact_table.locator('tbody tr').all()
            for ctr in contact_tr_body_elements:
                contact_value = ctr.locator("td:nth-child(1)").inner_text()

                if contact_value == "No data found":
                    logger.info(f"Account Contact Edit validation done successfully in Contact module.")
                    print(f"Account Contact Edit validation done successfully in Contact module.")
                else:
                    logger.info(f"Account Contact Edit validation failed in Contact module.")
                    print(f"Account Contact Edit validation failed in Contact module.")

                self.page.locator("#searchContacts").fill("")
                self.page.locator("#searchContacts").press("Enter")
                time.sleep(5)
                break

            self.page.locator("#LeadsMenu").click()
            time.sleep(17)
            self.page.locator("#searchString").fill(new_primary_email)
            self.page.locator("#searchString").press("Enter")
            time.sleep(17)
            lead_table = self.page.locator(".footable-loaded")
            lead_tr_body_elements = lead_table.locator('tbody tr').all()
            for ltr in lead_tr_body_elements:
                lead_value = ltr.locator("td:nth-child(1)").inner_text()

                if lead_value == "No active leads found":
                    logger.info(f"Account Contact Edit validation done successfully in Leads module.")
                    print(f"Account Contact Edit validation done successfully in Leads module.")
                else:
                    logger.info(f"Account Contact Edit validation failed in Leads module.")
                    print(f"Account Contact Edit validation failed in Leads module.")

                self.page.locator("#searchString").fill("")
                self.page.locator("#searchString").press("Enter")
                time.sleep(5)
                break

        else:
            self.page.locator(".backarrow").click()

    def account_contacts_action_edit(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        self.page.locator(".clear-tab-storage").nth(0).click()
        time.sleep(2)
        self.page.locator("#accountContactsTab").click()
        time.sleep(6)
        if self.page.locator(".px-1.py-1").nth(1).is_visible():
            self.page.locator(".px-1.py-1").nth(1).click()
            time.sleep(2)
            self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                .get_by_text("Edit", exact=True).nth(0).click()
            time.sleep(5)
            choose_func = CommonLibrary(self.page)
            fake_data = choose_func.faker_data(self.page)
            primary_email = fake_data["contact_email"]
            self.page.locator("#Email").fill(primary_email)
            time.sleep(2)
            self.page.locator("#btnUpdateContact").click()
            time.sleep(2)
            if self.page.locator(".toast.toast-error").nth(0).is_visible():
                message = self.page.locator(".toast-message").nth(0).inner_text()
                logger.info(message)
                print(message)

            if self.page.locator(".toast.toast-success").is_visible():
                message = self.page.locator(".toast-message").inner_text()
                print(message)
                logger.info(f"{message}")
                print(message)

            tables = self.page.locator(".Usertable").locator(".custom-table")
            first_tr = tables.locator('tbody tr').first
            new_primary_email = first_tr.locator("td:nth-child(3)").inner_text()
            match = re.search(r'[\w\.-]+@[\w\.-]+', new_primary_email)
            new_primary_email = match.group(0)

            if new_primary_email == primary_email:
                print(
                    f"Account Contacts Validation done Successfully and Email: {primary_email} and Old Email: {new_primary_email}")
                logger.info(
                    f"Account Contacts Validation done successfully and Email: {primary_email} and Old Email: {new_primary_email}")
            else:
                print(
                    f"Account Contacts Validation failed and Email: {primary_email} and Old Email: {new_primary_email}")
                logger.info(
                    f"Account Contacts Validation failed and Email: {primary_email} and Old Email: {new_primary_email}")

            self.page.locator(".backarrow").click()
            time.sleep(5)
            self.page.locator("#CustomersMenu").click()
            time.sleep(17)
            self.page.locator("#searchContacts").fill(new_primary_email)
            self.page.locator("#searchContacts").press("Enter")
            time.sleep(16)
            contact_table = self.page.locator(".custom-table.m-0")
            contact_tr_body_elements = contact_table.locator('tbody tr').all()
            for ctr in contact_tr_body_elements:
                contact_email = ctr.locator("td:nth-child(3)").inner_text()
                match = re.search(r'[\w\.-]+@[\w\.-]+', contact_email)
                contact_email = match.group(0)
                time.sleep(2)

                if contact_email == new_primary_email:
                    logger.info(
                        f"Account Contact Edit validation done successfully in Contact module. Contact Email:{contact_email} and Account Contact Email:{new_primary_email} ")
                    print(
                        f"Account Contact Edit validation done successfully in Contact module. Contact Email:{contact_email} and Account Contact Email:{new_primary_email} ")
                else:
                    logger.info(
                        f"Account Contact Edit validation failed in Contact module. Contact Email:{contact_email} and Account Contact Email:{new_primary_email}")
                    print(
                        f"Account Contact Edit validation failed in Contact module. Contact Email:{contact_email} and Account Contact Email:{new_primary_email} ")

                self.page.locator("#searchContacts").fill("")
                self.page.locator("#searchContacts").press("Enter")
                time.sleep(5)
                break
            self.page.locator("#LeadsMenu").click()
            time.sleep(17)
            self.page.locator("#searchString").fill(new_primary_email)
            self.page.locator("#searchString").press("Enter")
            time.sleep(17)
            lead_table = self.page.locator(".footable-loaded")
            lead_tr_body_elements = lead_table.locator('tbody tr').all()
            for ltr in lead_tr_body_elements:
                if ltr.locator("td:nth-child(3)").locator(".mb-1").nth(0).is_visible():
                    lead_email = ltr.locator("td:nth-child(3)").locator(".mb-1").nth(0).inner_text()
                    match = re.search(r'[\w\.-]+@[\w\.-]+', lead_email)
                    lead_email = match.group(0)

                    if lead_email == new_primary_email:
                        logger.info(
                            f"Account Contact Edit validation done successfully in Leads module. Leads Email:{lead_email} and Contact Email:{new_primary_email}")
                        print(
                            f"Account Contact Edit validation done successfully in Leads module. Leads Email:{lead_email} and Contact Email:{new_primary_email}")
                    else:
                        logger.info(
                            f"Account Contact Edit validation failed in Leads module. Leads Email:{lead_email} and Contact Email:{new_primary_email}")
                        print(
                            f"Account Contact Edit validation failed in Leads module. Leads Email:{lead_email} and Contact Email:{new_primary_email}")

                    self.page.locator("#searchString").fill("")
                    self.page.locator("#searchString").press("Enter")
                    time.sleep(5)
                    break



    def account_contacts_search(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        # tables = self.page.locator(".footable-loaded")
        # first_tr = tables.locator('tbody tr').first
        # first_tr.locator("td:nth-child(2)").click()
        self.page.locator(".clear-tab-storage").nth(0).click()
        time.sleep(2)
        self.page.locator("#accountContactsTab").click()
        time.sleep(6)
        search_info = self.config["account_contacts_search"]
        time.sleep(2)
        self.page.locator("#searchContacts").fill(search_info)
        time.sleep(2)
        self.page.locator("#searchContacts").press("Enter")
        time.sleep(2)
        if self.page.locator("#ContactPager").is_visible():
            time.sleep(2)
            count_text = self.page.locator("#ContactPager").locator(".px-3").inner_text()
            value = int(count_text.split()[-2])
            logger.info(f"Account Contact Search  value {search_info} and count : {value}")
            print(f"Account Contact Search  value {search_info}  and count : {value} ")
        else:
            value = 0
            logger.info(f"Account Contact Search  value {search_info} and count : {value}")
            print(f"Account Contact Search  value {search_info}  and count : {value} ")

        time.sleep(2)
        self.page.locator("#searchContacts").fill("")
        self.page.locator("#searchContacts").press("Enter")
        time.sleep(5)
        self.page.locator(".backarrow").click()
        time.sleep(2)

    def account_actions_create_contact(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        # tables = self.page.locator(".footable-loaded")
        # first_tr.locator("td:nth-child(2)").click()
        self.page.locator(".clear-tab-storage").nth(0).click()
        time.sleep(2)
        self.page.locator("#accountContactsTab").click()
        time.sleep(6)
        if self.page.locator("#ContactPager").is_visible():
            time.sleep(2)
            count_text = self.page.locator("#ContactPager").locator(".px-3").inner_text()
            value = int(count_text.split()[-2])
            if value > 0:
                logger.info(f"Accounts Contacts count {value}")
                print(f"Account Contacts count  {value} ")
                self.page.locator(".backarrow").click()
                time.sleep(2)
                if self.page.locator(".px-1.py-1").nth(0).is_visible():
                    self.page.locator(".px-1.py-1").nth(0).click()
                    time.sleep(2)
                    self.page.click("a.dropdown-item:has-text('Add Contact')")
                    time.sleep(5)
                    choose_func = CommonLibrary(self.page)
                    fake_data = choose_func.faker_data(self.page)
                    fname = fake_data["title"]
                    lname = fake_data["contact_name"]
                    cemail = fake_data["contact_email"]
                    cnumber = fake_data["c_no"]
                    # first_name = self.config["account_first_name"]
                    # last_name = self.config["account_last_name"]
                    # email_id = self.config["account_email_id"]
                    # mobile =self.config["account_mobile"]
                    # phone_number = self.config["account_phone_number"]
                    time.sleep(2)
                    self.page.locator("#FirstName").fill(fname)
                    time.sleep(2)
                    self.page.locator("#LastName").fill(lname)
                    time.sleep(2)
                    self.page.locator("#Email").fill(cemail)
                    time.sleep(2)
                    self.page.locator("#PrimaryPhone").fill(cnumber)
                    time.sleep(2)
                    self.page.locator('[data-id="RelationshipId"]').click()
                    time.sleep(5)
                    self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                        .get_by_text("Father", exact=True).nth(0).click()
                    self.page.check("#IsDecisionMaker")
                    time.sleep(1)
                    self.page.locator("#IsBilling").click()
                    time.sleep(1)
                    self.page.locator("#btnSaveContact").click()
                    time.sleep(2)
                    if self.page.locator(".toast.toast-error").nth(0).is_visible():
                        message = self.page.locator(".toast-message").nth(0).inner_text()
                        logger.info(message)
                        print(message)
                        time.sleep(2)
                        choose_func = CommonLibrary(self.page)
                        fake_data = choose_func.faker_data(self.page)
                        cnumber = fake_data["c_no"]
                        cemail = fake_data["contact_email"]
                        self.page.locator("#Email").fill(cemail)
                        time.sleep(2)
                        self.page.locator("#PrimaryPhone").fill(f"{cnumber}")
                        time.sleep(2)
                        self.page.locator("#btnSaveContact").click()
                        time.sleep(2)

                    if self.page.locator(".toast.toast-success").is_visible():
                        message = self.page.locator(".toast-message").inner_text()
                        print(message)
                        logger.info(f"{message}")
                        print(message)

                    tables = self.page.locator(".footable-loaded")
                    first_tr = tables.locator('tbody tr').first
                    first_tr.locator("td:nth-child(2)").click()
                    time.sleep(2)
                    self.page.locator("#accountContactsTab").click()
                    time.sleep(6)
                    if self.page.locator("#ContactPager").is_visible():
                        time.sleep(2)
                        count_text = self.page.locator("#ContactPager").locator(".px-3").inner_text()
                        new_value = int(count_text.split()[-2])
                        if new_value > value:
                            logger.info(
                                f"Account Contacts Validation done. New count {new_value} and old count {value}")
                            print(f"Account Contacts Validation done. New count {new_value} and old count {value}")
                        else:
                            logger.info(
                                f"Account Contacts Validation failed. New count {new_value} and old count {value}")
                            print(f"Account Contacts Validation failed. New count {new_value} and old count {value}")

                    self.page.locator(".backarrow").click()
                    time.sleep(2)

    def account_actions_log_activity(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        # tables = self.page.locator(".footable-loaded")
        # first_tr = tables.locator('tbody tr').first
        # first_tr.locator("td:nth-child(2)").click()
        self.page.locator(".clear-tab-storage").nth(0).click()
        time.sleep(8)
        self.page.locator("#accountActivitiesTab").click()
        time.sleep(6)
        if self.page.locator("#ActivityLogPager").is_visible():
            time.sleep(2)
            count_text = self.page.locator("#ActivityLogPager").locator(".px-3").inner_text()
            value = int(count_text.split()[-2])
            if value > 0:
                logger.info(f"Account Activity count {value}")
                print(f"Account Activity count  {value} ")
                self.page.locator(".backarrow").click()
                time.sleep(2)
                if self.page.locator(".px-1.py-1").nth(0).is_visible():
                    self.page.locator(".px-1.py-1").nth(0).click()
                    time.sleep(2)
                    self.page.click("a.dropdown-item:has-text('Log Activity')")
                    time.sleep(5)
                    self.page.locator('[data-id="ActivityTypeIds"]').click()
                    time.sleep(2)
                    self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text("Call",
                                                                                                               exact=True).click()
                    time.sleep(2)
                    self.page.locator("div.note-editable").evaluate(
                        "el => el.innerHTML = '<p><strong>Bold text</strong></p>'")
                    time.sleep(2)
                    self.page.locator("#btnSubmitActivityLog").click()
                    time.sleep(2)
                    if self.page.locator(".toast.toast-success").is_visible():
                        message = self.page.locator(".toast-message").inner_text()
                        print(message)
                        logger.info(f"{message}")
                        print(message)
                    self.page.locator(".clear-tab-storage").nth(0).click()
                    time.sleep(2)
                    self.page.locator("#accountActivitiesTab").click()
                    time.sleep(2)
                    if self.page.locator("#ActivityLogPager").is_visible():
                        time.sleep(2)
                        count_text = self.page.locator("#ActivityLogPager").locator(".px-3").inner_text()
                        new_value = int(count_text.split()[-2])
                        if new_value > value:
                            logger.info(
                                f"Account Log Activity validation done successfully New count: {new_value} and old count : {value}")
                            print(
                                f"Account Log activity validation done successfully New count: {new_value} and old count : {value}")
                        else:
                            logger.info(
                                f"Account Log Activity validation failed New count: {new_value} and old count : {value}")
                            print(
                                f"Account Log activity validation failed New count: {new_value} and old count : {value}")

                        self.page.locator(".backarrow").click()
                        time.sleep(2)

    def account_actions_delete(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        first_tr = tables.locator('tbody tr').first
        account_name = first_tr.locator("td:nth-child(2)").inner_text()
        time.sleep(8)
        if self.page.locator(".px-1.py-1").nth(0).is_visible():
            self.page.locator(".px-1.py-1").nth(0).click()
            time.sleep(2)
            self.page.click("a.dropdown-item:has-text('Delete')")
            time.sleep(5)
            self.page.locator("#btnDeleteAccount").nth(0).click()
            time.sleep(2)
            if self.page.locator(".toast.toast-success").is_visible():
                message = self.page.locator(".toast-message").inner_text()
                print(message)
                logger.info(f"{message}")
                print(message)
            tables = self.page.locator(".footable-loaded")
            first_tr = tables.locator('tbody tr').first
            account_new_name = first_tr.locator("td:nth-child(2)").inner_text()
            if account_new_name != account_name:
                logger.info(
                    f"Accounts module delete action validation done successfully. Account New Name : {account_new_name} and Account old name : {account_name}")
                print(
                    f"Accounts module delete action validation done successfully. Account New Name : {account_new_name} and Account old name : {account_name}")
            else:
                logger.info(
                    f"Account module delete action  validation failed. Account New Name : {account_new_name} and Account old name : {account_name}")
                print(
                    f"Account module delete action validation failed. Account New Name : {account_new_name} and Account old name : {account_name}")

    def account_actions_edit(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        first_tr = tables.locator('tbody tr').first
        account_name = first_tr.locator("td:nth-child(2)").inner_text()
        time.sleep(8)
        if self.page.locator(".px-1.py-1").nth(0).is_visible():
            self.page.locator(".px-1.py-1").nth(0).click()
            time.sleep(2)
            self.page.click("a.dropdown-item:has-text('Edit')")
            time.sleep(5)
            first_name = self.config["account_first_name"]
            time.sleep(2)
            last_name = self.config["account_last_name"]
            self.page.locator("#FirstName").fill(first_name)
            time.sleep(2)
            self.page.locator("#LastName").fill(last_name)
            # account_new_name = first_name+ " " + last_name
            time.sleep(2)  # DefaultHomeExpertId
            self.page.locator('[data-id="DefaultHomeExpertId"]').click()
            time.sleep(2)
            # self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text("Pallavi Hp",
            #                                                                                           exact=True).click()
            #
            self.page.locator(".dropdown-menu.show:not(.inner)").press('ArrowDown')
            self.page.locator(".dropdown-menu.show:not(.inner)").press('ArrowDown')
            self.page.locator(".dropdown-menu.show:not(.inner)").press('Enter')

            time.sleep(2)
            self.page.locator("#btnUpdateAccount").click()
            time.sleep(2)
            if self.page.locator(".toast.toast-success").is_visible():
                message = self.page.locator(".toast-message").inner_text()
                print(message)
                logger.info(f"{message}")
                print(message)

            time.sleep(5)
            tables = self.page.locator(".footable-loaded")
            first_tr = tables.locator('tbody tr').first
            account_new_name = first_tr.locator("td:nth-child(2)").inner_text()

            if account_new_name != account_name:
                logger.info(
                    f"Accounts module edit action validation done successfully. Account New Name : {account_new_name} and Account old name : {account_name}")
                print(
                    f"Accounts module action validation done successfully. Account New Name : {account_new_name} and Account old name : {account_name}")
            else:
                logger.info(
                    f"Account module edit action  validation failed. Account New Name : {account_new_name} and Account old name : {account_name}")
                print(
                    f"Account module edit action validation failed. Account New Name : {account_new_name} and Account old name : {account_name}")

    def account_bulk_actions(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        for i in range(0, 3):
            self.page.locator(".accountItem_checkbox").nth(i).click()
            time.sleep(1)
        self.page.locator("#accountsBulkSubmit").click()
        time.sleep(3)
        self.page.locator('[data-id="PrimaryHomeExpert"]').click()
        time.sleep(2)
        self.page.locator(".dropdown-menu.show:not(.inner)").press('ArrowDown')
        self.page.locator(".dropdown-menu.show:not(.inner)").press('ArrowDown')
        self.page.locator(".dropdown-menu.show:not(.inner)").press('ArrowDown')
        self.page.locator(".dropdown-menu.show:not(.inner)").press('Enter')
        # self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text("Pallavi Hp",
        #
        #                                                                                          exact=True).click()
        home_expert = self.page.locator('[data-id="PrimaryHomeExpert"]').inner_text()
        time.sleep(2)
        self.page.locator("#btnAddOrUpdateBulkActionAccount").click()
        time.sleep(2)
        if self.page.locator(".toast.toast-success").is_visible():
            message = self.page.locator(".toast-message").inner_text()
            print(message)
            logger.info(f"{message}")

        for i in range(0, 3):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(2)
            tables = self.page.locator(".table-bordered.m-0")
            first_tr = tables.locator('tbody tr').first
            assigned_name = first_tr.locator("td:nth-child(2)").inner_text()
            print(assigned_name)
            if assigned_name == home_expert:
                logger.info(f"Account Bulk Action Account {assigned_name} Validation done successfully")
                print(f"Account Bulk Action Account {assigned_name} Validation done successfully")
            else:
                logger.info(f"Account Bulk Action Account {assigned_name} Validation not done successfully")
                print(f"Account Bulk Action Account {assigned_name} Validation not done successfully")

            time.sleep(1)
            self.page.locator(".backarrow").click()
            time.sleep(1)

    def account_filter_category(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        self.page.locator(".sidebar-click").click()
        time.sleep(2)
        self.page.locator('[data-id="filterLeadCategories"]').click()
        time.sleep(5)
        elements = self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').all()
        time.sleep(2)
        category_list = []
        for item in elements:
            category = item.inner_text()
            print(category)
            if category != "Select" and category != "":
                self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                    f"{category}",
                    exact=True).click()
                category_list.append(category)
                time.sleep(2)
                self.page.locator("#applyFilter").click()
                time.sleep(2)
                if self.page.locator("#AccountPager").is_visible():
                    time.sleep(2)
                    count_text = self.page.locator("#AccountPager").locator(".px-3").inner_text()
                    value = int(count_text.split()[-2])
                    logger.info(f"Account Category to value {category} and count : {value}")
                    print(f"Account Category to value {category} and count : {value}")
                else:
                    value = 0
                    logger.info(f"Account Category to value {category} and count : {value}")
                    print(f"Account Category to value {category} and count : {value}")

                time.sleep(2)
                self.page.locator(".sidebar-click").click()
                time.sleep(2)
                self.page.locator('[data-id="filterLeadCategories"]').click()
                time.sleep(2)
                self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                    f"{category}",
                    exact=True).click()
                time.sleep(2)

        self.page.locator(".clear-filter").click()
        time.sleep(2)

    def account_filter_long_source(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        self.page.locator(".sidebar-click").click()
        time.sleep(2)
        self.page.locator('[data-id="filterLeadShortSource"]').click()
        time.sleep(2)
        self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
            f"Canvassing",
            exact=True).nth(0).click()
        time.sleep(2)
        self.page.locator('[data-id="filterLeadLongSource"]').click()
        time.sleep(2)
        elements = self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').all()
        time.sleep(2)
        long_source_list = []
        for item in elements:
            long_source = item.inner_text()
            if long_source != "Select" and long_source != "":
                long_source_list.append(long_source)

        self.page.locator(".mdi-close").click()
        time.sleep(2)
        self.page.locator(".sidebar-click").click()
        time.sleep(2)
        self.page.locator('[data-id="filterLeadLongSource"]').click()
        time.sleep(2)
        for long_source in long_source_list:
            self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                f"{long_source}",
                exact=True).nth(0).click()
            time.sleep(2)
            self.page.locator("#applyFilter").click()
            time.sleep(2)
            if self.page.locator("#AccountPager").is_visible():
                time.sleep(2)
                count_text = self.page.locator("#AccountPager").locator(".px-3").inner_text()
                value = int(count_text.split()[-2])
                logger.info(f"Account Long Source to value {long_source} and count : {value}")
                print(f"Account Long Source to value {long_source} and count : {value}")
            else:
                value = 0
                logger.info(f"Account Long Source to value {long_source} and count : {value}")
                print(f"Account Long Source to value {long_source} and count : {value}")

            self.page.locator(".sidebar-click").click()
            time.sleep(2)
            self.page.locator('[data-id="filterLeadLongSource"]').click()
            time.sleep(2)
            self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                f"{long_source}",
                exact=True).nth(0).click()
            time.sleep(2)
            self.page.locator("#applyFilter").click()
            self.page.locator(".sidebar-click").click()
            time.sleep(2)
            self.page.locator('[data-id="filterLeadLongSource"]').click()
            time.sleep(2)

        self.page.locator(".clear-filter").click()
        time.sleep(2)
        if self.page.locator(".mdi-close").is_visible():
            self.page.locator(".mdi-close").click()
            time.sleep(2)

    def account_filter_short_source(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        self.page.locator(".sidebar-click").click()
        time.sleep(2)
        self.page.locator('[data-id="filterLeadShortSource"]').click()
        time.sleep(2)
        elements = self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').all()
        time.sleep(2)
        short_source_list = []
        for item in elements:
            short_source = item.inner_text()
            if short_source != "Select" and short_source != "":
                short_source_list.append(short_source)

        self.page.locator(".mdi-close").click()
        time.sleep(2)
        self.page.locator(".sidebar-click").click()
        time.sleep(2)
        self.page.locator('[data-id="filterLeadShortSource"]').click()
        time.sleep(2)
        for short_source in short_source_list:
            self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                f"{short_source}",
                exact=True).nth(0).click()
            time.sleep(2)
            self.page.locator("#applyFilter").click()
            time.sleep(2)
            if self.page.locator("#AccountPager").is_visible():
                time.sleep(2)
                count_text = self.page.locator("#AccountPager").locator(".px-3").inner_text()
                value = int(count_text.split()[-2])
                logger.info(f"Account Short Source to value {short_source} and count : {value}")
                print(f"Account Short Source to value {short_source} and count : {value}")
            else:
                value = 0
                logger.info(f"Account Short Source to value {short_source} and count : {value}")
                print(f"Account Short Source to value {short_source} and count : {value}")

            self.page.locator(".sidebar-click").click()
            time.sleep(2)
            self.page.locator('[data-id="filterLeadShortSource"]').click()
            time.sleep(2)
        self.page.locator(".mdi-close").click()
        time.sleep(2)

    def account_filter_assigned(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        self.page.locator(".sidebar-click").click()
        time.sleep(5)
        self.page.locator('[data-id="filterAssigned"]').click()
        time.sleep(5)
        elements = self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').all()
        time.sleep(2)
        assignedto_list = []
        for item in elements:
            assignedto = item.inner_text()
            print(assignedto)
            if assignedto != "Select" and assignedto != "":
                self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                    f"{assignedto}",
                    exact=True).click()
                assignedto_list.append(assignedto)
                time.sleep(2)
                self.page.locator("#applyFilter").click()
                time.sleep(2)
                if self.page.locator("#AccountPager").is_visible():
                    time.sleep(2)
                    count_text = self.page.locator("#AccountPager").locator(".px-3").inner_text()
                    value = int(count_text.split()[-2])
                    logger.info(f"Account Assigned to value {assignedto} and count : {value}")
                    print(f"Account Assigned to value {assignedto} and count : {value}")
                else:
                    value = 0
                    logger.info(f"Account Assigned to value {assignedto} and count : {value}")
                    print(f"Account Assigned to value {assignedto} and count : {value}")

                time.sleep(2)
                self.page.locator(".sidebar-click").click()
                time.sleep(2)
                self.page.locator('[data-id="filterAssigned"]').click()
                time.sleep(2)
                self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                    f"{assignedto}",
                    exact=True).click()
                time.sleep(2)
        self.page.locator(".mdi-close").click()
        time.sleep(2)

    def accounts_export_phase3(self):
        self.page.locator("#AccountsMenu").click()
        self.page.wait_for_timeout(3000)

        with self.page.expect_download() as download_info:
            self.page.click('#exportAccounts', no_wait_after=True)
        self.page.wait_for_timeout(6000)

        download = download_info.value
        file_path = os.path.join(os.getcwd(), download.suggested_filename)
        download.save_as(file_path)
        print(f"✅ File downloaded: {file_path}")
        self.validate_downloaded_file(file_path)

    def validate_downloaded_file(self, file_path):
        df = pd.read_excel(file_path)
        assert not df.empty, "❌ Excel file is empty"
        print(f"✅ Excel file has {len(df)} rows")

        # Optional column check
        expected_cols = ["First Name", "Last Name", "Email", "Company Name", "Primary Phone", "Alternate Phone",
                         "Customer From", "Owner Salesrep Name", "Total Job Sold",
                         "Total Sales", "Open Balance", "Region", "District", "Region", "Area", "State",
                         "Property Address", "Billing Address"]

        missing = [col for col in expected_cols if col not in df.columns]
        assert not missing, f"❌ Missing columns: {missing}"
        print("✅ Excel columns are valid")
        logger.info("✅ Excel columns are valid")
        print("✅ Excel columns are valid")
        logger.info("✅ Excel columns are valid")
        print("✅ Excel columns are valid")
        logger.info("✅ Excel columns are valid")

    def account_search(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        searched_info = self.config["account_search"]
        time.sleep(2)
        self.page.locator("#SearchText").fill(searched_info)
        time.sleep(2)
        self.page.locator("#SearchText").press("Enter")
        time.sleep(2)
        if self.page.locator("#AccountPager").is_visible():
            time.sleep(2)
            count_text = self.page.locator("#AccountPager").locator(".px-3").inner_text()
            value = int(count_text.split()[-2])
            logger.info(f"\nAccount Search value {searched_info} and count : {value}")
            print(f"\nAccount Search value {searched_info} and count : {value}")
        time.sleep(2)
        self.page.locator("#SearchText").fill("")
        self.page.locator("#SearchText").press("Enter")
        time.sleep(5)

    def account_appointment_action_delete(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(10)
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()

        for i in range(0, tr_count):
            if self.page.locator(".clear-tab-storage").nth(i).is_visible():
                self.page.locator(".clear-tab-storage").nth(i).click()
                time.sleep(5)
                self.page.locator("#accountAppointmentsTab").click()
                time.sleep(6)
                if self.page.locator("#AppointmentsPager").is_visible():
                    time.sleep(2)
                    count_text = self.page.locator("#AppointmentsPager").locator(".px-3").inner_text()
                    value = int(count_text.split()[-2])
                    if value > 0:
                        self.page.locator("#tbl_Appoitments").locator(".px-1.py-1").nth(0).click()
                        time.sleep(5)
                        self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                            .get_by_text("Delete", exact=True).nth(0).click()
                        time.sleep(3)
                        self.page.locator("#btnDeleteAppointment").click()
                        time.sleep(4)
                        if self.page.locator(".toast.toast-success").is_visible():
                            message = self.page.locator(".toast-message").inner_text()
                            print(message)
                            logger.info(f"{message}")
                            print(message)
                        time.sleep(6)
                        self.page.locator(".backarrow").click()
                        time.sleep(2)
                        break
                    else:
                        self.page.locator(".backarrow").click()
                        time.sleep(2)



    def account_appointment_action_send_email(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()

        for i in range(0, tr_count):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(5)
            self.page.locator("#accountAppointmentsTab").click()
            time.sleep(6)
            if self.page.locator("#AppointmentsPager").is_visible():
                time.sleep(2)
                count_text = self.page.locator("#AppointmentsPager").locator(".px-3").inner_text()
                value = int(count_text.split()[-2])
                if value > 0:
                    self.page.locator("#tbl_Appoitments").locator(".px-1.py-1").nth(0).click()
                    time.sleep(5)
                    self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                        .get_by_text("Send Email", exact=True).nth(0).click()
                    time.sleep(3)
                    # self.page.locator("#ToEmail").fill("mskrishna.vtiger@gmail.com")
                    time.sleep(1)
                    # self.page.locator('[data-id="DepartmentId"]').click()
                    # time.sleep(2)
                    # self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                    #     .get_by_text("Administration", exact=True).nth(0).click()
                    # time.sleep(2)
                    self.page.locator('[data-id="EmailTemplateId"]').click()
                    time.sleep(1)
                    self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                        .get_by_text("Calc Email", exact=True).nth(0).click()
                    time.sleep(1)
                    self.page.locator("#btnSend").click()
                    time.sleep(4)
                    if self.page.locator(".toast.toast-success").is_visible():
                        message = self.page.locator(".toast-message").inner_text()
                        print(message)
                        logger.info(f"{message}")
                        print(message)
                    else:
                        self.page.locator("#SendEmailForm").locator(".close").nth(0).click()
                    time.sleep(6)

                    self.page.locator(".backarrow").click()
                    time.sleep(2)
                    break
                else:
                    self.page.locator(".backarrow").click()
                    time.sleep(2)
            else:
                self.page.locator(".backarrow").click()
                time.sleep(2)

    def account_appointment_action_record_outcome(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(10)
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()

        for i in range(0, tr_count):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(5)
            self.page.locator("#accountAppointmentsTab").click()
            time.sleep(6)
            if self.page.locator("#AppointmentsPager").is_visible():
                time.sleep(2)
                count_text = self.page.locator("#AppointmentsPager").locator(".px-3").inner_text()
                value = int(count_text.split()[-2])
                if value > 0:
                    if self.page.locator("#tbl_Appoitments").locator(".px-1.py-1").nth(0).is_visible():
                        self.page.locator("#tbl_Appoitments").locator(".px-1.py-1").nth(0).click()
                        time.sleep(5)
                        appointment_tables = self.page.locator("#tbl_Appoitments")
                        appointment_first_tr = appointment_tables.locator('tbody tr').first
                        lead_name = appointment_first_tr.locator("td:nth-child(1)").locator(
                            ".text-primary").nth(0).inner_text()
                        if self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                            .get_by_text("Record Outcome", exact=True).nth(0).is_visible():
                            self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                                .get_by_text("Record Outcome", exact=True).nth(0).click()
                            time.sleep(3)
                            self.page.locator('[data-id="StatusId"]').click()
                            time.sleep(2)
                            self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item") \
                                .get_by_text("Held", exact=True).nth(0).click()
                            time.sleep(2)
                            self.page.locator("#btnSaveAppointmentOutcome").click()
                            time.sleep(2)
                            if self.page.locator(".toast.toast-success").is_visible():
                                message = self.page.locator(".toast-message").inner_text()
                                print(message)
                                logger.info(f"{message}")
                                print(message)
                            time.sleep(6)
                            account_tables = self.page.locator("#tbl_Appoitments")
                            contact_first_tr = account_tables.locator('tbody tr').first
                            out_come = contact_first_tr.locator("td:nth-child(6)").inner_text()
                            logger.info(f"{out_come}")
                            print(f"{out_come}")
                            if out_come == "Held":
                                print(f"Account Appointment Validation Done Successfully and Out come value:{out_come}")
                                logger.info(
                                    f"Account Appointment Validation Done Successfully and Out come value:{out_come}")
                            else:
                                print(f"Account Appointment Validation Failed and Out come value:{out_come}")
                                logger.info(f"Account Appointment Validation Failed and Out come value:{out_come}")

                            self.page.locator(".backarrow").click()
                            time.sleep(2)
                            self.page.locator("#LeadsMenu").click()
                            time.sleep(17)
                            self.page.locator("#searchString").fill(lead_name)
                            self.page.locator("#searchString").press("Enter")
                            time.sleep(17)
                            break
                        else:
                            self.page.locator(".backarrow").click()
                            time.sleep(2)
                else:
                    self.page.locator(".backarrow").click()
                    time.sleep(2)
            else:
                self.page.locator(".backarrow").click()
                time.sleep(2)

    def account_appointment_search(self):
        time.sleep(5)
        self.page.locator("#AccountsMenu").click()
        time.sleep(15)
        searched_info = self.config["account_appointment_search"]
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()

        for i in range(0, tr_count):
            if self.page.locator(".clear-tab-storage").nth(i).is_visible():
                self.page.locator(".clear-tab-storage").nth(i).click()
                time.sleep(5)
                self.page.locator("#accountAppointmentsTab").click()
                time.sleep(6)
                if self.page.locator("#AppointmentsPager").is_visible():
                    time.sleep(2)
                    count_text = self.page.locator("#AppointmentsPager").locator(".px-3").inner_text()
                    value = int(count_text.split()[-2])
                    if value > 0:
                        self.page.locator("#SearchAppointment").fill(searched_info)
                        time.sleep(2)
                        self.page.locator("#SearchAppointment").press("Enter")
                        time.sleep(2)
                        tables = self.page.locator("#tbl_Appoitments")
                        table_first_tr = tables.locator('tbody tr').first
                        check_rows = table_first_tr.locator("td:nth-child(1)").inner_text()
                        logger.info(f"{check_rows}")
                        print(f"{check_rows}")
                        if check_rows == "No data found":
                            value = 0
                            logger.info(f"Account Appointment Search value {searched_info} and count : {value}")
                            print(f"Account Appointment Search value {searched_info} and count : {value}")
                            self.page.locator("#SearchAppointment").fill(" ")
                            time.sleep(2)
                            self.page.locator("#SearchAppointment").press("Enter")
                        else:
                            count_text = self.page.locator("#AppointmentsPager").locator(".px-3").inner_text()
                            value = int(count_text.split()[-2])
                            logger.info(f"Account Appointment Search value {searched_info} and count : {value}")
                            print(f"Account Appointment Search value {searched_info} and count : {value}")
                            self.page.locator("#SearchAppointment").fill(" ")
                            time.sleep(2)
                            self.page.locator("#SearchAppointment").press("Enter")

                        self.page.locator(".backarrow").click()
                        time.sleep(2)
                        break
                    else:
                        self.page.locator(".backarrow").click()
                        time.sleep(2)


    def account_job_project_export_phase3(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()
        for i in range(0, tr_count):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(5)
            self.page.locator("#accountJobsTab").click()
            time.sleep(6)
            self.page.locator(".mr-0.ml-1").nth(0).locator(".btn.btn-secondary").click()
            time.sleep(2)
            self.page.get_by_role("radio", name="Jobs & Projects").click()
            time.sleep(2)
            with self.page.expect_download() as download_info:
                self.page.click("#btnExportJobsAndprojects", no_wait_after=True)
            self.page.wait_for_timeout(6000)
            download = download_info.value
            file_path = os.path.join(os.getcwd(), download.suggested_filename)
            download.save_as(file_path)
            print(f"✅ File downloaded: {file_path}")
            self.validate_job_project_export_downloaded_file(file_path)
            time.sleep(5)
            self.page.locator(".backarrow").click()
            time.sleep(2)
            break

    def account_jobs_generate_statements_phase3(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()
        for i in range(0, tr_count):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(5)
            self.page.locator("#accountJobsTab").click()
            time.sleep(6)
            self.page.get_by_role("link", name="Generate  Statement").click()
            time.sleep(5)
            self.page.locator("//a[text()='Send Email']").click()
            time.sleep(3)
            self.page.locator("#CCEmail").fill("mskrishna.vtiger@gmail.com")
            time.sleep(3)
            self.page.locator("#btnSendCustomerStatementEmail").click()
            time.sleep(3)
            if self.page.locator(".toast.toast-success").is_visible():
                message = self.page.locator(".toast-message").inner_text()
                print(message)
                logger.info(f"{message}")
                print(message)
            self.page.locator(".mdi-arrow-left-thick").click()
            time.sleep(3)
            self.page.locator(".backarrow").click()
            time.sleep(2)
            break

    def account_job_export_jobs(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()
        for i in range(0, tr_count):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(5)
            self.page.locator("#accountJobsTab").click()
            time.sleep(6)
            self.page.locator(".mr-0.ml-1").nth(0).locator(".btn.btn-secondary").click()
            time.sleep(2)
            self.page.get_by_role("radio", name="Jobs Only").click()
            time.sleep(2)
            with self.page.expect_download() as download_info:
                self.page.click("#btnExportJobs", no_wait_after=True)
            self.page.wait_for_timeout(6000)

            download = download_info.value
            file_path = os.path.join(os.getcwd(), download.suggested_filename)
            download.save_as(file_path)
            print(f"✅ File downloaded: {file_path}")
            self.validate_job_export_downloaded_file(file_path)
            time.sleep(5)
            self.page.locator(".backarrow").click()
            time.sleep(2)
            break

    def validate_job_project_export_downloaded_file(self, file_path):
        df = pd.read_excel(file_path)
        assert not df.empty, "❌ Excel file is empty"
        print(f"✅ Excel file has {len(df)} rows")

        # Optional column check
        expected_cols = ["Job ID", "Project ID", "Job Sold Date ", "Total Project Cost", "Total Retail Price",
                         "Total Retail ", "Services", "Project Status", "Paid In Full "]

        missing = [col for col in expected_cols if col not in df.columns]
        assert not missing, f"❌ Missing columns: {missing}"
        print("✅ Excel columns are valid")
        logger.info("✅ Excel columns are valid")
        print("✅ Excel columns are valid")
        logger.info("✅ Excel columns are valid")
        print("✅ Excel columns are valid")
        logger.info("✅ Excel columns are valid")

    def validate_job_export_downloaded_file(self, file_path):
        df = pd.read_excel(file_path)
        assert not df.empty, "❌ Excel file is empty"
        print(f"✅ Excel file has {len(df)} rows")

        # Optional column check
        expected_cols = ["Job ID", "Job Sold Date ", "Total Job Cost", "Total Retail Price", "Total Retail ",
                         "Open Balance", "Services", "Job Status"]

        missing = [col for col in expected_cols if col not in df.columns]
        assert not missing, f"❌ Missing columns: {missing}"
        print("✅ Excel columns are valid")
        logger.info("✅ Excel columns are valid")
        print("✅ Excel columns are valid")
        logger.info("✅ Excel columns are valid")
        print("✅ Excel columns are valid")
        logger.info("✅ Excel columns are valid")

    def account_job_action_mark_cancel(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()
        for i in range(0, tr_count):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(5)
            self.page.locator("#accountJobsTab").click()
            time.sleep(6)
            if self.page.locator("#jobsTab").is_visible():
                time.sleep(2)
                count_text = self.page.locator("#jobsTab").locator(".px-3").inner_text()
                value = int(count_text.split()[-2])
                if value > 0:
                    if self.page.locator("#jobsTab").locator(".mdi-18px").nth(0).is_visible():
                        self.page.locator("#jobsTab").locator(".mdi-18px").nth(0).click()
                        time.sleep(3)
                        self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                            "Mark as Cancel",
                            exact=True).click()
                        time.sleep(3)
                        self.page.wait_for_selector(".CodeMirror")
                        time.sleep(2)
                        self.page.eval_on_selector(".CodeMirror", """
                                                           (el) => {
                                                               el.CodeMirror.setValue("This is the note text set via JS");
                                                           }
                                                """)
                        self.page.locator("#btnSaveCancellation").click()
                        time.sleep(3)
                        if self.page.locator(".toast.toast-success").is_visible():
                            message = self.page.locator(".toast-message").inner_text()
                            print(message)
                            logger.info(f"{message}")
                            print(message)
                        time.sleep(3)
                        self.page.locator(".backarrow").click()
                        time.sleep(2)
                        break
                else:
                    self.page.locator(".backarrow").click()
                    time.sleep(2)

            else:
                self.page.locator(".backarrow").click()
                time.sleep(2)

    def account_job_search(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        searched_info = self.config["account_job_search"]
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()
        for i in range(0, tr_count):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(5)
            self.page.locator("#accountJobsTab").click()
            time.sleep(6)
            if self.page.locator("#jobsTab").is_visible():
                time.sleep(2)
                count_text = self.page.locator("#jobsTab").locator(".px-3").inner_text()
                value = int(count_text.split()[-2])
                if value > 0:
                    self.page.locator("#searchJob").fill(searched_info)
                    time.sleep(2)
                    self.page.locator("#searchJob").press("Enter")
                    time.sleep(2)
                    tables = self.page.locator("#jobsTab").locator(".footable-loaded")
                    table_first_tr = tables.locator('tbody tr').first
                    check_rows = table_first_tr.locator("td:nth-child(1)").inner_text()
                    logger.info(f"{check_rows}")
                    print(f"{check_rows}")
                    if check_rows == "No jobs found":
                        value = 0
                        logger.info(f"Account Jobs Search value {searched_info} and count : {value}")
                        print(f"Account Jobs Search value {searched_info} and count : {value}")
                        self.page.locator("#searchJob").fill(" ")
                        time.sleep(2)
                        self.page.locator("#searchJob").press("Enter")
                    else:
                        count_text = self.page.locator("#jobsTab").locator(".px-3").inner_text()
                        value = int(count_text.split()[-2])
                        logger.info(f"Account Estimates Search value {searched_info} and count : {value}")
                        print(f"Account Estimates Search value {searched_info} and count : {value}")
                        self.page.locator("#searchJob").fill(" ")
                        time.sleep(2)
                        self.page.locator("#searchJob").press("Enter")

                    self.page.locator(".backarrow").click()
                    time.sleep(2)
                    break
                else:
                    self.page.locator(".backarrow").click()
                    time.sleep(2)

    def account_payment_action_edit(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()
        for i in range(0, tr_count):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(5)
            self.page.locator("#accountPaymentTab").click()
            time.sleep(6)
            if self.page.locator("#PaymentPager").is_visible():
                time.sleep(2)
                count_text = self.page.locator("#PaymentPager").locator(".px-3").inner_text()
                value = int(count_text.split()[-2])
                if value > 0:
                    self.page.locator("#paymentsTab").locator(".mdi-18px").nth(0).click()
                    time.sleep(4)
                    self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                        "Edit",
                        exact=True).click()
                    time.sleep(2)
                    self.page.locator('[data-id="PaymentMethodId"]').click()
                    time.sleep(2)
                    self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                        "Check",
                        exact=True).click()
                    time.sleep(2)
                    self.page.locator("#Number").fill("HH123464")
                    time.sleep(2)
                    self.page.locator("#btnUpdatePayment").click()
                    time.sleep(2)
                    if self.page.locator(".toast.toast-success").is_visible():
                        message = self.page.locator(".toast-message").inner_text()
                        print(message)
                        logger.info(f"{message}")
                        print(message)
                    time.sleep(6)
                    tables = self.page.locator("#paymentsTab").locator(".footable-loaded")
                    table_first_tr = tables.locator('tbody tr').first
                    payment_method = table_first_tr.locator("td:nth-child(4)").inner_text()
                    logger.info(f"{payment_method}")
                    print(f"{payment_method}")
                    if payment_method == "Check":
                        logger.info(f"Account Payment Edit action validation done and Payment Method:{payment_method}")
                        print(f"Account Payment Edit action validation done and Payment Method:{payment_method}")
                    else:
                        logger.info(
                            f"Account Payment Edit action validation failed and Payment Method:{payment_method}")
                        print(f"Account Payment Edit action validation failed and Payment Method:{payment_method}")
                    break
                else:
                    self.page.locator(".backarrow").click()
                    time.sleep(2)

    def account_payment_search(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        searched_info = self.config["account_payment_search"]
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()
        for i in range(0, tr_count):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(5)
            self.page.locator("#accountPaymentTab").click()
            time.sleep(6)
            if self.page.locator("#PaymentPager").is_visible():
                time.sleep(2)
                count_text = self.page.locator("#PaymentPager").locator(".px-3").inner_text()
                value = int(count_text.split()[-2])
                if value > 0:
                    self.page.locator("#searchPayment").fill(searched_info)
                    time.sleep(2)
                    self.page.locator("#searchPayment").press("Enter")
                    time.sleep(2)
                    count_text = self.page.locator("#PaymentPager").locator(".px-3").inner_text()
                    new_value = int(count_text.split()[-2])
                    if new_value > 0:
                        logger.info(f"Account Payment Search value {searched_info} and count : {value}")
                        print(f"Account Payment Search value {searched_info} and count : {value}")
                        self.page.locator("#searchPayment").fill(" ")
                        time.sleep(2)
                        self.page.locator("#searchPayment").press("Enter")
                    else:
                        value = 0
                        logger.info(f"Account Payment Search value {searched_info} and count : {value}")
                        print(f"Account Payment Search value {searched_info} and count : {value}")
                        self.page.locator("#searchPayment").fill(" ")
                        time.sleep(2)
                        self.page.locator("#searchPayment").press("Enter")
                    self.page.locator(".backarrow").click()
                    time.sleep(2)
                    break
                else:
                    self.page.locator(".backarrow").click()
                    time.sleep(2)

    def account_activities_search(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        searched_info = self.config["account_activities_search"]
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()
        for i in range(0, tr_count):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(5)
            self.page.locator("#accountActivitiesTab").click()
            time.sleep(6)
            if self.page.locator("#ActivityLogPager").is_visible():
                time.sleep(2)
                count_text = self.page.locator("#ActivityLogPager").locator(".px-3").inner_text()
                value = int(count_text.split()[-2])
                if value > 0:
                    self.page.locator("#SearchActivity").fill(searched_info)
                    time.sleep(2)
                    self.page.locator("#SearchActivity").press("Enter")
                    time.sleep(2)
                    tables = self.page.locator("#activitiesTab").locator(".footable-loaded")
                    table_first_tr = tables.locator('tbody tr').first
                    check_rows = table_first_tr.locator("td:nth-child(1)").inner_text()
                    logger.info(f"{check_rows}")
                    print(f"{check_rows}")
                    if check_rows == "No data found":
                        value = 0
                        logger.info(f"Account Estimates Search value {searched_info} and count : {value}")
                        print(f"Account Estimates Search value {searched_info} and count : {value}")
                        self.page.locator("#SearchActivity").fill(" ")
                        time.sleep(2)
                        self.page.locator("#SearchActivity").press("Enter")
                    else:
                        count_text = self.page.locator("#ActivityLogPager").locator(".px-3").inner_text()
                        value = int(count_text.split()[-2])
                        logger.info(f"Account Estimates Search value {searched_info} and count : {value}")
                        print(f"Account Estimates Search value {searched_info} and count : {value}")
                        self.page.locator("#SearchActivity").fill(" ")
                        time.sleep(2)
                        self.page.locator("#SearchActivity").press("Enter")

                    self.page.locator(".backarrow").click()
                    time.sleep(2)
                    break
                else:
                    self.page.locator(".backarrow").click()
                    time.sleep(2)

    def account_activity_action_edit(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()
        for i in range(0, tr_count):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(5)
            self.page.locator("#accountActivitiesTab").click()
            time.sleep(6)
            if self.page.locator("#ActivityLogPager").is_visible():
                time.sleep(2)
                count_text = self.page.locator("#ActivityLogPager").locator(".px-3").inner_text()
                value = int(count_text.split()[-2])
                if value > 0:
                    self.page.locator(".backarrow").click()
                    time.sleep(2)
                    break
                else:
                    self.page.locator(".backarrow").click()
                    time.sleep(2)

    def account_activity_date_filter(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()
        for i in range(0, tr_count):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(5)
            self.page.locator("#accountActivitiesTab").click()
            time.sleep(6)
            if self.page.locator("#ActivityLogPager").is_visible():
                time.sleep(2)
                count_text = self.page.locator("#ActivityLogPager").locator(".px-3").inner_text()
                value = int(count_text.split()[-2])
                from_date = "01/01/2025"
                to_date = "10/31/2025"
                if value > 0:
                    self.page.locator("#ActivityFromDate").type("01/01/2025")
                    time.sleep(2)
                    self.page.locator("#ActivityToDate").type("10/31/2025")
                    time.sleep(10)
                    self.page.locator("#applyFilter").click()
                    time.sleep(2)
                    tables = self.page.locator("#activitiesTab").locator(".footable-loaded")
                    table_first_tr = tables.locator('tbody tr').first
                    check_rows = table_first_tr.locator("td:nth-child(1)").inner_text()
                    logger.info(f"{check_rows}")
                    print(f"{check_rows}")
                    if check_rows == "No data found":
                        value = 0
                        logger.info(f"Account Activity Search value {from_date} and {to_date} count : {value}")
                        print(f"Account Activity Search value {from_date} and {to_date}  count : {value}")
                        self.page.locator("#ActivityFromDate").fill(" ")
                        time.sleep(2)
                        self.page.locator("#ActivityToDate").press(" ")
                        time.sleep(2)
                        self.page.locator("#applyFilter").click()
                        time.sleep(2)

                    else:
                        count_text = self.page.locator("#activitiesTab").locator(".px-3").inner_text()
                        value = int(count_text.split()[-2])
                        logger.info(f"Account Activity Search value {from_date} and {to_date}  count : {value}")
                        print(f"Account Activity Search value {from_date} and {to_date} count : {value}")
                        self.page.locator("#ActivityFromDate").fill(" ")
                        time.sleep(2)
                        self.page.locator("#ActivityToDate").press(" ")
                        time.sleep(2)
                        self.page.locator("#applyFilter").click()

                    self.page.locator(".backarrow").click()
                    time.sleep(2)
                    break
                else:
                    self.page.locator(".backarrow").click()
                    time.sleep(2)

    def account_activity_search(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        searched_info = self.config["account_acitivity_search"]
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()
        for i in range(0, tr_count):
            self.page.locator(".clear-tab-storage").nth(i).click()
            time.sleep(5)
            self.page.locator("#accountActivitiesTab").click()
            time.sleep(6)
            if self.page.locator("#ActivityLogPager").is_visible():
                time.sleep(2)
                count_text = self.page.locator("#ActivityLogPager").locator(".px-3").inner_text()
                value = int(count_text.split()[-2])
                if value > 0:
                    self.page.locator("#SearchActivity").fill(searched_info)
                    time.sleep(2)
                    self.page.locator("#SearchActivity").press("Enter")
                    time.sleep(2)
                    tables = self.page.locator("#activitiesTab").locator(".footable-loaded")
                    table_first_tr = tables.locator('tbody tr').first
                    check_rows = table_first_tr.locator("td:nth-child(1)").inner_text()
                    logger.info(f"{check_rows}")
                    print(f"{check_rows}")
                    if check_rows == "No data found":
                        value = 0
                        logger.info(f"Account Activity Search value {searched_info} and count : {value}")
                        print(f"Account Activity Search value {searched_info} and count : {value}")
                        self.page.locator("#SearchActivity").fill(" ")
                        time.sleep(2)
                        self.page.locator("#SearchActivity").press("Enter")
                    else:
                        count_text = self.page.locator("#ActivityLogPager").locator(".px-3").inner_text()
                        value = int(count_text.split()[-2])
                        logger.info(f"Account Activity Search value {searched_info} and count : {value}")
                        print(f"Account Activity Search value {searched_info} and count : {value}")
                        self.page.locator("#SearchActivity").fill(" ")
                        time.sleep(2)
                        self.page.locator("#SearchActivity").press("Enter")

                    self.page.locator(".backarrow").click()
                    time.sleep(2)
                    break
                else:
                    self.page.locator(".backarrow").click()
                    time.sleep(2)

    def account_estimate_search(self):
        self.page.locator("#AccountsMenu").click()
        time.sleep(5)
        searched_info = self.config["account_estimate_search"]
        tables = self.page.locator(".footable-loaded")
        tr_count = tables.locator('tbody tr').count()
        for i in range(0, tr_count):
            if self.page.locator(".clear-tab-storage").nth(i).is_visible():
                self.page.locator(".clear-tab-storage").nth(i).click()
                time.sleep(5)
                self.page.locator("#accountEstimatesTab").click()
                time.sleep(6)
                if self.page.locator("#EstimatePager").is_visible():
                    time.sleep(2)
                    count_text = self.page.locator("#EstimatePager").locator(".px-3").inner_text()
                    value = int(count_text.split()[-2])
                    if value > 0:
                        self.page.locator("#searchEstimate").fill(searched_info)
                        time.sleep(2)
                        self.page.locator("#searchEstimate").press("Enter")
                        time.sleep(2)
                        tables = self.page.locator("#estimatesTab").locator(".custom-table")
                        table_first_tr = tables.locator('tbody tr').first
                        check_rows = table_first_tr.locator("td:nth-child(1)").inner_text()
                        logger.info(f"{check_rows}")
                        print(f"{check_rows}")
                        if check_rows == "No data found":
                            value = 0
                            logger.info(f"Account Estimates Search value {searched_info} and count : {value}")
                            print(f"Account Estimates Search value {searched_info} and count : {value}")
                            self.page.locator("#searchEstimate").fill(" ")
                            time.sleep(2)
                            self.page.locator("#searchEstimate").press("Enter")
                        else:
                            count_text = self.page.locator("#EstimatePager").locator(".px-3").inner_text()
                            value = int(count_text.split()[-2])
                            logger.info(f"Account Estimates Search value {searched_info} and count : {value}")
                            print(f"Account Estimates Search value {searched_info} and count : {value}")
                            self.page.locator("#searchEstimate").fill(" ")
                            time.sleep(2)
                            self.page.locator("#searchEstimate").press("Enter")

                        self.page.locator(".backarrow").click()
                        time.sleep(2)
                        break
                    else:
                        self.page.locator(".backarrow").click()
                        time.sleep(2)




















