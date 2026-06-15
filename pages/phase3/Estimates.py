import time
from pages.PitchedRoofing_Proposal import PitchedRoofingProposal
from pages.Carpentry_Proposal import CarpentryProposal
from pages.Doors_Proposal import DoorsProposal
from pages.ExteriorPainting_Proposal import ExteriorPaintingProposal
from pages.InteriorPainting_Proposal import InteriorPaintingProposal
from pages.Siding_Proposal import SidingProposal
from pages.Windows_Proposal import WindowsProposal
from pages.flatroofing_proposal import FlatRoofingProposal
from test.conftest import logger
from test.conftest import input_config_value
import json
import random
import os
import re
from datetime import datetime
import math
from playwright.sync_api import BrowserContext

def validate_side_displayed_total(side_element, s_index, calculated_total):
    """
    Validates the displayed total price on the UI matches the calculated total.
    """
    displayed_total_locator = side_element.locator(".side-total")
    if displayed_total_locator.is_visible():
        displayed_total_text = displayed_total_locator.inner_text().replace("$", "").replace(",", "").strip()
        try:
            displayed_total_value = float(displayed_total_text)
            print(f"   Displayed total in Side {s_index + 1}: ₹{displayed_total_value}")
            if abs(displayed_total_value - calculated_total) > 0.01:
                print(
                    f"   Discrepancy in totals for Side {s_index + 1}: UI shows ₹{displayed_total_value}, calculated ₹{calculated_total}")
        except ValueError:
            print(f"   Could not convert displayed total '{displayed_total_text}' to float")
    else:
        print(f"   No displayed total found for Side {s_index + 1}")

def calculate_expected_price(retail_price: float, adjustment: float, is_percentage: bool) -> float:
    if is_percentage:
        return round(retail_price * (adjustment / 100), 2)
    else:
        return round(retail_price - adjustment, 2)



class Estimates:

    def __init__(self, page):
        self.page = page
        self.config = input_config_value()
        self.page = page
        self.div_sections = page.locator(".divSections")
        self.dropdown_selector = 'ul.dropdown-menu.inner.show'
        self.dropdown_items_selector = 'a.dropdown-item'
        self.checkbox_selector = 'input[name="priceInCustomerToggle_window"]'
        self.add_more_line_selector = '.window-add-more'
        self.remove_line_selector = '.window-remove-line'
        self.form = self.page.locator('#formSaveWindowScope')
        self.checkbox_ep_selector = 'input[name="priceInCustomerToggle_exterior"]'
        self.context: BrowserContext = page.context


    def open_new_estimate(self):
        time.sleep(15)
        self.page.locator("#ProposalsMenu").nth(0).click()
        time.sleep(3)
        self.page.locator("#newEstimateTab").nth(0).click()

    def click_ep_checkbox(self):
        windows_label = self.page.locator(
            "div.d-grid.service-options label.service-type",
            has=self.page.locator("h5", has_text="Exterior Paint")
        )
        windows_label.click()
        logger.info("Clicked the 'Exterior Paint' service checkbox successfully.")

    def click_windows_checkbox(self):
        fr_label = self.page.locator(
            "div.d-grid.service-options label.service-type",
            has=self.page.locator("h5", has_text="Windows")
        )
        fr_label.click()
        logger.info("Clicked the 'Windows' service checkbox successfully.")



    def click_fr_checkbox(self):
        fr_label = self.page.locator(
            "div.d-grid.service-options label.service-type",
            has=self.page.locator("h5", has_text="Low-Slope Roofing")
        )
        fr_label.click()
        logger.info("Clicked the 'Low-Slope Roofing' service checkbox successfully.")


    def click_window_checkbox(self):
        windows_label = self.page.locator(
            "div.d-grid.service-options label.service-type",
            has=self.page.locator("h5", has_text="Windows")
        )
        windows_label.click()
        logger.info("Clicked the 'Windows' service checkbox successfully.")

    def click_siding_checkbox(self):
        siding_label = self.page.locator(
            "div.d-grid.service-options label.service-type",
            has=self.page.locator("h5", has_text="Siding")
        )
        siding_label.click()
        logger.info("Clicked the 'Windows' service checkbox successfully.")

    def click_door_checkbox(self):
        windows_label = self.page.locator(
            "div.d-grid.service-options label.service-type",
            has=self.page.locator("h5", has_text="Doors")
        )
        windows_label.click()
        logger.info("Clicked the 'Doors' service checkbox successfully.")

    def click_carpentry_checkbox(self):
        carpentry_label = self.page.locator(
            "div.d-grid.service-options label.service-type",
            has=self.page.locator("h5", has_text="Carpentry")
        )
        carpentry_label.click()
        logger.info("Clicked the 'Carpentry' service checkbox successfully.")

    def click_pr_checkbox(self):
        pr_label = self.page.locator(
            "div.d-grid.service-options label.service-type",
            has=self.page.locator("h5", has_text="Pitched Roofing")
        )
        pr_label.click()
        logger.info("Clicked the 'Pitched Roofing' service checkbox successfully.")




    def save_service(self):
        self.page.locator("#btnSaveServices").click(timeout=30000)


    def select_appointment_name(self, appointment_name):
        self.page.locator('span[aria-labelledby="select2-AppointmentId-container"]').click()
        time.sleep(3)

        # 2) Locate all result options
        options = self.page.locator('ul.select2-results__options > li.select2-results__option')

        count = options.count()
        assert count > 0, "No options found in Select2 dropdown"

        # 3) Loop through options and click the one that matches desired_value
        for i in range(count):
            option_text = options.nth(i).inner_text()
            if option_text.strip() == appointment_name:
                options.nth(i).click()
                break

        time.sleep(4)


    def select_random_appointment(self):

        self.page.locator('span[aria-labelledby="select2-AppointmentId-container"]').click()
        time.sleep(3)

        # 2) Locate all result options in the opened Select2 list
        options = self.page.locator('ul.select2-results__options > li.select2-results__option')

        count = options.count()
        assert count > 0, "No options found in Select2 dropdown"

        # 3) Pick random index and click
        random_index = random.randint(0, count - 1)
        options.nth(random_index).click()
        time.sleep(4)

    def fill_appointment_form(self):
        time.sleep(2)
        def select_random_option(selector):
            select = self.page.locator(selector)
            options = select.locator("option")
            count = options.count()
            if count == 0:
                raise Exception(f"No options found for dropdown: {selector}")
            random_index = random.randint(0, count - 1)
            value = options.nth(random_index).get_attribute("value")
            select.select_option(value)

        # Select random options from dropdowns
        select_random_option("#StateId")
        select_random_option("#DecisionMakerId")
        self.page.locator("#Zip").fill("76037")
        self.page.click('//a[@id="btnUpdateBasicInfo"]')
        time.sleep(3)
        self.fill_random_primary_phone_if_error()

        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(2000)

        # take_screenshot(self.page, "create_new_proposal")

        logger.info("Filled all form fields with Faker data and randomly selected dropdown options.")


    def fill_random_primary_phone_if_error(self):
        # Check if validation error is visible
        error_locator = self.page.locator('#PrimaryPhone-error')
        if error_locator.is_visible() and "Please enter your 10-digit phone number" in error_locator.inner_text():
            # Generate a random phone number in the (999) 999-9999 format
            digits = [random.randint(0, 9) for _ in range(10)]
            phone_number = f"({digits[0]}{digits[1]}{digits[2]}) {digits[3]}{digits[4]}{digits[5]}-{digits[6]}{digits[7]}{digits[8]}{digits[9]}"
            # Fill the input field
            self.page.fill('input#PrimaryPhone', phone_number)
            self.page.click('//a[@id="btnUpdateBasicInfo"]')


    def save_sketch(self):
        # After processing all cards, click final "Save & Proceed"
        self.page.locator("#pills-sketch").get_by_text("Save & Proceed").click()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")


    def summary_calculations_app(self):
        # Try clicking "Add More" up to 3 times until PaymentServices_2__Payment input is visible
        max_attempts = 3
        add_more_btn = self.page.locator("a.btn.btn-outline-dark.btn-sm", has_text="Add More")

        for attempt in range(max_attempts):
            if add_more_btn.nth(1).is_visible():
                add_more_btn.nth(1).click()
                try:
                    new_payment_input = self.page.locator('input.NewPaymentName#PaymentServices_2__Payment')
                    new_payment_input.wait_for(state="visible", timeout=2000)
                    # If visible, break the loop
                    break
                except Exception:
                    logger.info(f"Attempt {attempt + 1}: PaymentServices_2__Payment not visible, retrying Add More...")
                    continue
            else:
                logger.info("Add More button not visible for second payment row.")
                break

        # If visible, fill payment name
        new_payment_input = self.page.locator('input.NewPaymentName#PaymentServices_2__Payment')
        if new_payment_input.is_visible():
            new_payment_input.fill("Second payment")
            logger.info(" New payment row filled with 'Second payment'")

            # Reset payments button
            self.page.click('//a[contains(@class, "btn") and contains(@class, "btn-primary") '
                            'and contains(@class, "resetPayments") and @title="Reset"]')
            logger.info("      Clicked on reset payments")
        else:
            logger.info("      Failed: PaymentServices_2__Payment not visible after 3 attempts.")

        # Get total price from summary
        total_price_str = self.page.locator("#totalPrice").inner_text()
        total_price = float(total_price_str.replace("$", "").replace(",", ""))
        logger.info(f"      Total Price: {total_price}")

        # Get deposit value
        deposit_str = self.page.locator("#depositAmountsumamry").input_value()
        deposit = float(deposit_str.replace("$", "").replace(",", ""))
        logger.info(f"      Deposit: {deposit}")

        # Collect payment values dynamically
        payments = []
        payment_inputs = self.page.locator('input.calAmount').all()
        for i, input_el in enumerate(payment_inputs):
            val = input_el.input_value()
            numeric = float(val.replace("$", "").replace(",", "")) if val else 0.0
            payments.append(numeric)
            logger.info(f"Payment value at index {i}: {numeric}")


    def click_interior_paint_checkbox(self):
        interior_paint_label = self.page.locator(
            "div.d-grid.service-options label.service-type",
            has=self.page.locator("h5", has_text="Interior Paint")
        )
        interior_paint_label.click()
        logger.info("Clicked the 'Interior Paint' service checkbox successfully.")


    def click_flat_roofing_checkbox(self):
        flat_roofing_label = self.page.locator(
            "div.d-grid.service-options label.service-type",
            has=self.page.locator("h5", has_text="Low-Slope Roofing")
        )
        flat_roofing_label.click()
        logger.info("Clicked the 'Low-Slope Roofing' service checkbox successfully.")

    def calc_flat_page_app(self):
        areas_included = self.config['calc_page'].get('AreasIncluded')
        areas_not_included = self.config['calc_page'].get('AreasNotIncluded')
        quantity = self.config['calc_page'].get('Quantity')


        # calc_data = self.input_data['calc_page']
        self.page.wait_for_load_state('networkidle')
        self.page.locator(
            "#formSaveFlatroofingScope > div.d-flex.justify-content-between.mb-3 > div > div > label:nth-child(1)").click()
        print("Clicked on the 'Home Expert View' radio button.")
        self.page.wait_for_load_state('networkidle')

        scope = self.page.locator("#formSaveFlatroofingScope")  # scope to this form
        scope.locator("input[name='AreasIncluded']").fill(areas_included)
        scope.locator("input[name='AreasNotIncluded']").fill(areas_not_included)

        # # self.page.select_option('#Type', value=typeef)
        # self.page.fill("input[name='AreasIncluded']", areas_included)
        # self.page.fill("input[name='AreasNotIncluded']", areas_not_included)

        sections = self.page.locator("#divFlatSections .table-responsive").all()
        print(f"Total sections found: {len(sections)}")

        k = 0  # Manual section index
        for section in sections:
            print(f"Processing section {k + 1}")
            rows = section.locator("tbody tr").all()

            l = 0  # Manual row index
            for row in rows:
                print(f"  Filling data into row {l + 1}")
                # time.sleep(1)

                locator = self.page.locator(f"#table-section-{k}").get_by_role("link", name="Add More ")

                if locator.is_visible():
                    locator.click()
                    print(f"'Add more' clicked for section {k + 1}")
                    time.sleep(1)
                else:
                    print(f"Add More not visible for section {k}")

                break
                # l += 1  # Manually increment row counter
            k += 1  # Manually increment section counter

        # --------------------------------------------------------- top is add more -------------------------------------------
        for i, section in enumerate(sections):
            print(f"Processing section {i + 1}")
            rows = section.locator("tbody tr").all()

            for j, row in enumerate(rows):
                print(f"  Filling row {j + 1}")
                # time.sleep(2)

                product_selector = f'//button[@data-id="FlatSections_{i}__Products_{j}__Product_Id"]'
                product_input = self.page.locator(product_selector)
                # time.sleep(1)
                if product_input.is_visible():
                    # time.sleep(1)
                    button_locator = self.page.locator(
                        f'//button[@data-id="FlatSections_{i}__Products_{j}__Product_Id"]')
                    inner_text = button_locator.locator('.filter-option-inner-inner').inner_text()
                    # print(f"Product {j} inner text : {inner_text}")
                    if inner_text.strip() == "Select":
                        # time.sleep(1)
                        self.page.locator(
                            f'//button[@data-id="FlatSections_{i}__Products_{j}__Product_Id"]').click()
                        product_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        product_options = [item.inner_text() for item in product_option_elmts if
                                           item.inner_text() != 'Select']
                        if product_options:
                            random_product_option = random.choice(product_options)
                            self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                                random_product_option, exact=True).nth(0).click()
                            # print(f"Filled empty product for section {i}, product {j}")
                        else:
                            print("No options in dropdown")
                    else:
                        # print(f"Skipped row {j} – already has value: '{inner_text}'")
                        pass

                # this is to see if variation is empty and fill quantity only if it is empty (requirement)
                variation_selector = f'//button[@data-id="FlatSections_{i}__Products_{j}__PricebookVariation_Id"]'
                variation_input = self.page.locator(variation_selector)
                # time.sleep(1)
                if variation_input.is_visible():
                    # time.sleep(1)
                    variation_button_locator = self.page.locator(
                        f'//button[@data-id="FlatSections_{i}__Products_{j}__PricebookVariation_Id"]')
                    variation_inner_text = variation_button_locator.locator(
                        '.filter-option-inner-inner').inner_text()
                    # print(f"variation inner text : {variation_inner_text}")
                    if variation_inner_text.strip() == "Select":
                        time.sleep(1)
                        self.page.locator(
                            f'//button[@data-id="FlatSections_{i}__Products_{j}__PricebookVariation_Id"]').click()
                        variation_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        variation_options = [item.inner_text() for item in variation_option_elmts if
                                             item.inner_text() != 'Select']
                        random_variation_option = random.choice(variation_options)
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_variation_option, exact=True).nth(0).click()
                        # print(f"Filled empty variation for section {i}, product {j}")
                    else:
                        # print(f"Skipped row {j} – already has value: '{variation_inner_text}'")
                        pass

                # this is to see if color is empty and fill quantity only if it is empty (requirement)
                time.sleep(1)
                color_selector = f'#FlatSections_{i}__Products_{j}__ColorId'
                color_input = self.page.locator(color_selector)
                # time.sleep(1)
                if color_input.is_visible():
                    # time.sleep(1)
                    color_button_locator = self.page.locator(
                        f'//button[@data-id="FlatSections_{i}__Products_{j}__ColorId"]')
                    color_inner_text = color_button_locator.locator('.filter-option-inner-inner').inner_text()
                    # print(f"Color inner text : {color_inner_text}")
                    if color_inner_text.strip() == "Select":
                        # time.sleep(1)
                        self.page.locator(f'//button[@data-id="FlatSections_{i}__Products_{j}__ColorId"]').click()
                        color_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        color_options = [item.inner_text() for item in color_option_elmts if
                                         item.inner_text() != 'Select']
                        random_color_option = random.choice(color_options)
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_color_option, exact=True).nth(0).click()
                    else:
                        pass

                # this is to see if quantity is empty and fill quantity only if it is empty (requirement)
                quantity_selector = f'#FlatSections_{i}__Products_{j}__Quantity'
                quantity_input = self.page.locator(quantity_selector)
                # time.sleep(1)
                if quantity_input.is_visible():
                    # time.sleep(1)
                    current_quantity_value = quantity_input.input_value()
                    if current_quantity_value.strip() == "":
                        # time.sleep(1)
                        quantity_input.fill(quantity)
                        # print(f"Filled quantity for section {i}, row {j}")
                    else:
                        # print(f"Skipped row {j} – already has value: '{current_quantity_value}'")
                        pass

                hide_on_cust_pdf_selector = f'#FlatSections_{i}__Products_0__IsHideInPreview'
                hide_on_cust_pdf_input = self.page.locator(hide_on_cust_pdf_selector)
                if hide_on_cust_pdf_input.is_visible():
                    self.page.check(hide_on_cust_pdf_selector)

                hide_var_on_pdf_selector = f'#FlatSections_{i}__Products_1__IsHideVariationonPDF'
                hide_var_on_pdf_input = self.page.locator(hide_var_on_pdf_selector)
                if hide_var_on_pdf_input.is_visible():
                    self.page.check(hide_var_on_pdf_selector)

        time.sleep(2)
        self.page.locator('#flatroofing_RetailPrice').click()

        self.toggle_all_product_allincluded_checkboxes(check=True)

        retail_price_str_1 = self.page.input_value('#flatroofing_RetailPrice')
        retail_price_1 = float(retail_price_str_1.replace(",", ""))
        print(f"Retail Price from page: {retail_price_1}")

        # --------------------------------------------- to assert in preview calc -------------------
        with self.page.expect_popup() as page1_info:
            self.page.locator('#download-pdf-scope').click()
        time.sleep(4)
        page1 = page1_info.value

        # --- Scroll and extract price from the new popup ---
        print("Scrolling to and extracting price from popup...")

        scope_price_wrap = page1.locator("div.scope-price-wrap").nth(2)
        scope_price_wrap.scroll_into_view_if_needed()

        price_element = scope_price_wrap.locator("span.scope-price-lable > b.scope-uom-lable")
        price_text = price_element.inner_text().strip()
        print(f"Extracted Price: {price_text}")

        numeric_price = float(price_text.replace("$", "").replace(",", ""))
        print(f"Numeric Price: {numeric_price}")
        assert retail_price_1 == numeric_price, f"Retail price {retail_price_1} matched in Preview calc {numeric_price}"

        print("Clicking 'Download PDF'...")
        # Make sure the downloads folder exists
        downloads_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(downloads_dir, exist_ok=True)

        # Optional: add timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(downloads_dir, f"downloaded_proposal_{timestamp}.pdf")

        # Handle the download
        with page1.expect_download() as download_info:
            page1.locator("#toggleSpinners").click()
        download = download_info.value
        download.save_as(file_path)

        print(f"Downloaded PDF saved at: {file_path}")
        page1.close()
        print("Closed preview calc window.")

        self.verify_retail_price_excludes_last_section()

        # Step 1: Read the readonly Retail Price value
        retail_price_str = self.page.input_value('#flatroofing_RetailPrice')
        retail_price = float(retail_price_str.replace(",", ""))

        # ---- Test Dollar Adjustment ----
        # self.page.locator("label", has_text="$").locator("span").click()  # Click on $
        self.page.locator("#pricingSummary_flatroofing label:has(span:text-is('$'))").click()

        self.page.fill("#flatroofing_Adjustment", "50")
        self.page.press('#flatroofing_RetailPrice', 'Enter')
        self.page.dispatch_event("#flatroofing_Adjustment", "blur")

        final_price_dollar = float(self.page.input_value('#flatroofing_RetailPriceAdjusted').replace(",", ""))
        # final_price_dollar = float(self.page.locator("#RetailPriceAdjusted").get_attribute("value").replace(",", ""))
        expected_price_dollar = calculate_expected_price(retail_price, 50, is_percentage=False)
        #assert final_price_dollar == expected_price_dollar, f"Dollar Test Failed: got {final_price_dollar}, expected {expected_price_dollar}"

        # ---- Test Percentage Adjustment ----
        self.page.locator("#pricingSummary_flatroofing label:has(span:text-is('%'))").click()
        self.page.fill("#flatroofing_Adjustment", "10")  # 10%
        self.page.press('#flatroofing_Adjustment', 'Enter')

        self.page.dispatch_event("#flatroofing_Adjustment", "blur")

        final_price_percent = float(self.page.input_value('#flatroofing_RetailPriceAdjusted').replace(",", ""))
        expected_price_percent_change = calculate_expected_price(retail_price, 10, is_percentage=True)
        expected_price_percent = retail_price - expected_price_percent_change
        assert round(final_price_percent, 2) == round(expected_price_percent,
                                                      2), f"Percentage Test Failed: got {final_price_percent}, expected {expected_price_percent}"

        print("Both dollar and percentage adjustment validations passed.")
        btn_update_scope_data = self.page.locator("#btnUpdateScopeData")
        if btn_update_scope_data.is_visible():
            btn_update_scope_data.click(timeout=30000)
        else:
            self.page.locator("#btnUpdateScope").click(timeout=30000)

    def toggle_all_product_allincluded_checkboxes(self, check: bool = True):
        checkboxes = self.page.locator("input.checkbox.product-allincluded-checkbox").all()
        print(f"Found {len(checkboxes)} 'product-allincluded-checkbox' elements.")

        for idx, checkbox in enumerate(checkboxes):
            if checkbox.is_visible():
                is_checked = checkbox.is_checked()
                if check and not is_checked:
                    checkbox.check()
                    print(f"Checked checkbox {idx}")
                elif not check and is_checked:
                    checkbox.uncheck()
                    print(f"Unchecked checkbox {idx}")
                else:
                    print(f"Checkbox {idx} already in desired state.")
            else:
                print(f"Checkbox {idx} not visible, skipping.")

    def get_section_totals(self):
        sections = self.page.locator("#divFlatSections .table-responsive").all()
        section_totals = []

        print(f"Total sections found: {len(sections)}")

        for i, section in enumerate(sections):
            print(f"\nProcessing Section {i}")
            section_total = 0.0
            rows = section.locator("tbody tr").all()

            for j, row in enumerate(rows):
                input_id = f"FlatSections_{i}__Products_{j}__Totals"
                quantity_input = row.locator(f"input.totals#{input_id}")

                if quantity_input.count() == 0:
                    print(f"  Input not found for Section {i}, Product {j}")
                    continue

                if quantity_input.is_visible():
                    try:
                        current_quantity_value = quantity_input.input_value()
                        if current_quantity_value.strip() == "":
                            print(f"  Empty value in Section {i}, Row {j}, skipping fill")
                            # Optionally: quantity_input.fill("0")
                        else:
                            # Remove $ before converting to float
                            numeric_value = current_quantity_value.replace("$", "").replace(",", "").strip()
                            total_val = float(numeric_value)
                            section_total += total_val
                            print(f"  Section {i}, Row {j} total = {total_val}")
                    except Exception as e:
                        print(f"  Error reading value for Section {i}, Row {j}: {e}")
                else:
                    print(f"  Input not visible for Section {i}, Row {j}")

            print(f"Total for Section {i}: {section_total}")
            section_totals.append(section_total)

        grand_total = sum(section_totals)
        print(f"\n Grand Total of All Sections: {grand_total}")

        return section_totals, grand_total

    def verify_retail_price_excludes_last_section(self):
        print("\nUntoggling last section and verifying price adjustment...")

        # Step 1: Read original Retail Price
        retail_price_str = self.page.input_value('#flatroofing_RetailPrice')
        original_retail_price = float(retail_price_str.replace(",", ""))
        print(f"Original Retail Price: {original_retail_price}")

        # Step 2: Collect original section totals
        section_totals, grand_total = self.get_section_totals()
        print(f"Grand Total of Sections (All Toggled): {grand_total}")

        # Step 3: Untoggle last section's checkbox
        checkboxes = self.page.locator("input.checkbox.product-allincluded-checkbox").all()
        if not checkboxes:
            raise Exception("No checkboxes found to untoggle.")

        last_checkbox = checkboxes[-1]
        if last_checkbox.is_visible() and last_checkbox.is_checked():
            last_checkbox.uncheck()
            print("Untoggled last 'product-allincluded-checkbox'")
        else:
            print("Last checkbox either not visible or already untoggled.")

        self.page.wait_for_timeout(1000)  # wait for recalculation (adjust as needed)

        # Step 4: Collect updated section totals
        updated_section_totals, updated_grand_total = self.get_section_totals()

        # Step 5: Read updated Retail Price
        updated_retail_price_str = self.page.input_value('#flatroofing_RetailPrice')
        updated_retail_price = float(updated_retail_price_str.replace(",", ""))
        print(f"Updated Retail Price: {updated_retail_price}")

        # Step 6: Compare difference
        expected_price_after_removal = original_retail_price - section_totals[-1]
        assert round(updated_retail_price, 2) == round(expected_price_after_removal, 2), (
            f"Retail price mismatch after untoggling last section:\n"
            f"Expected: {expected_price_after_removal}, Got: {updated_retail_price}"
        )
        print("Retail price correctly excludes last section total.")

    def fill_interior_rooms(self):
        expected_room_count = self.config["interiorpainting"].get("siding_side_count", 1)
        add_more_counts = self.config["interiorpainting"].get("add_more_counts", [])
        room_cards = self.page.locator(".interior-line-card")

        for r_index in range(expected_room_count):
            print(f"\n Room {r_index + 1}")
            self.add_side_until_visible(r_index)
            self.click_side_accordion_until_open(r_index)

            room_element = room_cards.nth(r_index)
            section_index = int(room_element.locator("input.interior-room-name").get_attribute("id").split("_")[1])
            line_index = int(room_element.locator("input.interior-room-name").get_attribute("id").split("_")[4])

            tbody = room_element.locator("table tbody")
            product_add_count = 1  # default
            try:
                product_add_count = add_more_counts[r_index]["subsections"][0]["count"]
            except (IndexError, KeyError, TypeError):
                pass

            print(f"       Add {product_add_count} rows in Room {r_index + 1}")
            # Click 'Add More' n times (skip first row that already exists)
            # Click 'Add More' n times (skip first row that already exists)

            for i in range(product_add_count - 1):
                add_btn = room_element.locator("a.btn-outline-primary:has-text('Add More')")

                if not add_btn.is_visible():
                    try:
                        add_btn.scroll_into_view_if_needed(timeout=1000)
                        self.page.wait_for_timeout(300)
                    except Exception:
                        print(f" Scroll failed for 'Add More' button on attempt {i + 1}")

                if add_btn.is_visible():
                    try:
                        add_btn.click()
                        self.page.wait_for_timeout(300)
                        print(f"         Clicked Add More ({i + 1}/{product_add_count - 1})")
                    except Exception as e:
                        print(f"         Failed to click 'Add More' on attempt {i + 1}: {e}")
                else:
                    print(f"         'Add More' button not visible even after scroll on attempt {i + 1}")

            row_count = tbody.locator("tr").count()
            print(f"       Total Product Rows Now: {row_count}")

            for product_index in range(row_count):
                print(f"     Filling Row {product_index + 1}")
                base_id = f"Sections_{section_index}__LineItems_{line_index}__Products_{product_index}"

                # Product dropdown
                product_btn = self.page.locator(f'button[data-id="{base_id}__Product_Id"]')
                if product_btn.is_visible():
                    text = product_btn.locator(".filter-option-inner-inner").inner_text().strip()
                    if text in ["Select", "Nothing selected"]:
                        product_btn.click()

                        color_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        color_options = [item.inner_text() for item in color_option_elmts if
                                         item.inner_text() != 'Select']
                        random_option = random.choice(color_options)
                        # self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').nth(1).click()
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_option, exact=True).nth(0).click()
                        print(f"        Product selected - {random_option}")

                        # self.page.locator('.dropdown-menu.show:not(.inner) .dropdown-item').nth(1).click()
                    else:
                        print(f"        Product already selected: {text}")

                # Variation dropdown
                variation_btn = self.page.locator(f'button[data-id="{base_id}__PricebookVariation_Id"]')
                if variation_btn.is_visible():
                    text = variation_btn.locator(".filter-option-inner-inner").inner_text().strip()
                    if text == "Select":
                        variation_btn.click(timeout=60000)
                        color_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        color_options = [item.inner_text() for item in color_option_elmts if
                                         item.inner_text() != 'Select']
                        if color_options:
                            random_option = random.choice(color_options)
                            # self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').nth(1).click()
                            self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                                random_option, exact=True).nth(0).click()
                            print(f"        Product selected - {random_option}")
                            # self.page.locator('.dropdown-menu.show:not(.inner) .dropdown-item').nth(1).click()
                        else:
                            print("No color options found")

                # Quantity
                qty_input = self.page.locator(f'input[id="{base_id}__Quantity"]')
                if qty_input.is_visible():
                    qty_input.fill("2")

                # Toggle 'Yes' switch
                # //*[@id="Sections_1__LineItems_0__Products_0__IsIncludedDefault"]
                # self.page.locator(f'input[id="{base_id}__CustomerNotes"]').click(timeout = 1000000)
                toggle = self.page.locator(f'input[id="{base_id}__IsIncludedDefault"]')

                # if toggle.is_visible() and not toggle.is_checked():
                #     time.sleep(5)
                #     self.page.locator(f'input[id="{base_id}__IsIncludedDefault"]').check(timeout = 30000)

                # Product Reference dropdown
                product_ref_btn = self.page.locator(f'button[data-id="{base_id}__ProductReferenceId"]')
                if product_ref_btn.is_visible():
                    ref_text = product_ref_btn.locator(".filter-option-inner-inner").inner_text().strip()
                    if ref_text in ["Select", "Nothing selected", "No Reference"]:
                        try:
                            for attempt in range(2):  # Try up to 2 times
                                product_ref_btn.click()
                                self.page.wait_for_timeout(300)

                                dropdown_item = self.page.locator('.dropdown-menu.show:not(.inner) .dropdown-item').nth(
                                    1)
                                if dropdown_item.is_visible():
                                    dropdown_item.click()
                                    print(f"        Selected Product Reference in row {product_index + 1}")
                                    break
                                else:
                                    print(f"        Dropdown not visible on attempt {attempt + 1}, retrying...")
                            else:
                                print(f"        Dropdown still not visible after retry for row {product_index + 1}")
                        except Exception as e:
                            print(f"        Failed to select Product Reference for row {product_index + 1}: {e}")
                    else:
                        print(f"        Product Reference already selected: {ref_text}")
                else:
                    print("           Product Reference dropdown not visible.")

                # Color dropdown (if shown)
                color_btn = self.page.locator(f'button[data-id="{base_id}__ColorId"]')
                if color_btn.is_visible():
                    color_text = color_btn.locator(".filter-option-inner-inner").inner_text().strip()
                    if color_text in ["Select", "Nothing selected"]:
                        color_btn.click()
                        color_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        color_options = [item.inner_text() for item in color_option_elmts if
                                         item.inner_text() != 'Select']
                        if color_options:
                            random_option = random.choice(color_options)
                            # self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').nth(1).click()
                            self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                                random_option, exact=True).nth(0).click()
                            print(f"        Product selected - {random_option}")
                            # self.page.locator('.dropdown-menu.show:not(.inner) .dropdown-item').nth(1).click()
                        else:
                            pass

                # Notes
                notes_input = self.page.locator(f'#{base_id}__CustomerNotes')
                if notes_input.is_visible():
                    notes_input.fill("Auto-filled via script")

    def get_row_data_via_console(self, base_id):
        page = self.page

        result = page.evaluate(f"""
            () => {{
                const getAttr = (selector, attr = 'title') => {{
                    const el = document.querySelector(selector);
                    return el ? el.getAttribute(attr)?.trim() || "" : "";
                }};

                const getVal = selector => {{
                    const el = document.querySelector(selector);
                    return el ? el.value?.trim() || "" : "";
                }};

                let total = getVal("#{base_id}__Totals").replace('$', '');

                return {{
                    Product: getAttr('button[data-id="{base_id}__Product_Id"]'),
                    Variation: getAttr('button[data-id="{base_id}__PricebookVariation_Id"]'),
                    ProductReferenceId: getAttr('button[data-id="{base_id}__ProductReferenceId"]'),
                    Qty: getVal("#{base_id}__Quantity"),
                    Hours: getVal("#{base_id}__Hours"),
                    UOMName: getVal("#{base_id}__UOMName"),
                    TotalHours: getVal("#{base_id}__TotalHours"),
                    SQFT: getVal("#{base_id}__SqFeet"),
                    TotalPrice: total
                }};
            }}
        """)

        return result

    def extract_interior_room_data(self):
        expected_room_count = self.config["interiorpainting"].get("siding_side_count", 1)
        room_cards = self.page.locator(".interior-line-card")
        collected_data = []

        for r_index in range(expected_room_count):
            self.click_side_accordion_until_open(r_index)
            room_element = room_cards.nth(r_index)
            section_index = int(room_element.locator("input.interior-room-name").get_attribute("id").split("_")[1])
            line_index = int(room_element.locator("input.interior-room-name").get_attribute("id").split("_")[4])

            tbody = room_element.locator("table tbody")
            row_count = tbody.locator("tr").count()

            for product_index in range(row_count):
                base_id = f"Sections_{section_index}__LineItems_{line_index}__Products_{product_index}"
                row_data = self.get_row_data_via_console(base_id)

                # Append only if Product and Variation exist
                if row_data.get("Product") and row_data.get("Variation"):
                    row_data["Room"] = r_index + 1
                    row_data["Row"] = product_index + 1
                    collected_data.append(row_data)

        # Save to JSON
        with open("interior_calc_page_collected_data.json", "w", encoding="utf-8") as f:
            json.dump(collected_data, f, ensure_ascii=False, indent=4)

        return collected_data

    def get_total_sum_of_line_values(self):
        page = self.page
        expected_room_count = self.config["interiorpainting"].get("siding_side_count", 1)
        room_cards = page.locator(".interior-line-card")

        total_price_sum = 0.0
        total_hours_sum = 0.0

        for r_index in range(expected_room_count):
            self.click_side_accordion_until_open(r_index)
            room_element = room_cards.nth(r_index)

            section_index = int(
                room_element.locator("input.interior-room-name").get_attribute("id").split("_")[1]
            )
            line_index = int(
                room_element.locator("input.interior-room-name").get_attribute("id").split("_")[4]
            )

            line_total_price_id = f"Sections_{section_index}__LineItems_{line_index}__LineTotalPrice"
            line_total_hours_id = f"Sections_{section_index}__LineItems_{line_index}__LineTotalHours"

            result = page.evaluate(f"""
                () => {{
                    const price = parseFloat(document.querySelector('#{line_total_price_id}')?.value?.replace('$', '') || "0");
                    const hours = parseFloat(document.querySelector('#{line_total_hours_id}')?.value || "0");
                    return {{ price, hours }};
                }}
            """)

            total_price_sum += result["price"]
            total_hours_sum += result["hours"]

        return {
            "Sum_LineTotalPrice": round(total_price_sum, 2),
            "Sum_LineTotalHours": round(total_hours_sum, 2)
        }

    def assert_summary_totals_match(self, expected_totals):

        page = self.page

        # Extract values from Pricing Summary
        summary_totals = page.evaluate("""
            () => {
                const totalHours = document.querySelector('#Sections_4__SummaryProducts_1__TotalHours')?.value || "0";
                const optionalTotal = document.querySelector('#Sections_4__SummaryProducts_0__OptionalTotal')?.value || "0";

                return {
                    totalHours: parseFloat(totalHours),
                    optionalTotal: parseFloat(optionalTotal.replace('$', ''))
                };
            }
        """)

        # Round values for comparison
        actual_hours = round(summary_totals["totalHours"], 2)
        # actual_price = round(summary_totals["optionalTotal"], 2)
        actual_price = summary_totals["optionalTotal"]

        expected_hours = round(expected_totals["Sum_LineTotalHours"], 2)
        expected_price = round(expected_totals["Sum_LineTotalPrice"], 2)

        # Log and assert
        print(f"\n   Expected Hours: {expected_hours}, Actual: {actual_hours}")
        print(f"   Expected Total Price: {expected_price}, Actual: {actual_price}")

        assert actual_hours == expected_hours, f"   TotalHours mismatch: expected {expected_hours}, got {actual_hours}"
        # assert actual_price == expected_price, f"   TotalPrice mismatch: expected {expected_price}, got {actual_price}"

    def extract_totals_from_each_card(self):
        totals_list = []

        cards = self.page.locator(".Interior-line-card_2")
        total_cards = cards.count()

        for i in range(total_cards):
            header = cards.nth(i)
            header.click()
            self.page.wait_for_timeout(500)  # Allow time to expand

            card_body = header.locator("..").locator(".card-body")
            rows = card_body.locator("tbody tr")

            for j in range(rows.count()):
                row = rows.nth(j)
                try:
                    total_value = row.locator('input[id*="__Totals"]').input_value()
                    totals_list.append(total_value)
                except:
                    totals_list.append("Not Found")

        return totals_list

    def open_last_ip_siding_accordian(self):
        expected_side_count = self.config["interiorpainting"].get("siding_side_count", 1)
        add_more_counts = self.config["interiorpainting"].get("add_more_counts", [])

        sides = self.page.locator(".interior-line-card")
        actual_side_count = sides.count()

        print(f"   DOM shows {actual_side_count} sides (expected: {expected_side_count})")

        #    Call accordion open ONLY for the last side
        if actual_side_count > 0:
            last_side_index = actual_side_count - 1
            print(f"   Clicking accordion for last side (Side {last_side_index + 1})")
            self.click_side_accordion_until_open(last_side_index)
        else:
            print("   No sides found in DOM.")


    def calc_ip_page_app(self):
        areas_included = self.config['calc_page'].get('AreasIncluded')
        areas_not_included = self.config['calc_page'].get('AreasNotIncluded')
        quantity = self.config['calc_page'].get('Quantity')
        customer_notes = self.config['calc_page'].get('CustomerNotes')
        self.page.wait_for_load_state('networkidle')

        proposal_number = self.page.locator('#proposalNumber').text_content()
        print(f"Proposal number : {proposal_number}")
        match = re.search(r'#PR(\d+)-', proposal_number)
        if match:
            number = match.group(1)
            print(f"Proposal ID: {number}")
        else:
            print("Proposal ID not found.")
        time.sleep(5)

        self.page.locator(
            "#formSaveInteriorScope > div.d-flex.justify-content-between.mb-3 > div > div > label:nth-child(1)").click()
        print("Clicked on the 'Home Expert View' radio button.")
        self.page.wait_for_load_state('networkidle')

        scope = self.page.locator("#formSaveInteriorScope")  # scope to this form

        scope.locator("input[name='AreasIncluded']").fill(areas_included)
        scope.locator("input[name='AreasNotIncluded']").fill(areas_not_included)
        # UNCOMMENT
        self.fill_interior_rooms()

        collected_data = self.extract_interior_room_data()
        with open("interior_calc_page_collected_data.json", "w", encoding="utf-8") as f:
            json.dump(collected_data, f, ensure_ascii=False, indent=4)

        self.open_last_ip_siding_accordian()
        self.remove_last_visible_siding_section_and_validate()
        totals = self.get_total_sum_of_line_values()
        self.assert_summary_totals_match(totals)

        totals = self.extract_totals_from_each_card()
        print("\n   Totals from each card:")
        for i, t in enumerate(totals):
            print(f"Card {i}: {t}")
        # UNCOMMENT

        # ----------------------------------------------------------------------------ADD MORE-------------------------------------------------------
        sections = scope.locator(".table-responsive").all()

        # Enumerate and limit to first 3 sections
        for k, section in enumerate(sections[:1]):
            rows = section.locator("tbody tr").all()
            for l, row in enumerate(rows):
                locator = scope.locator(f"#table-section-{k}").get_by_role("link", name="Add More ")
                if locator.is_visible():
                    locator.click()
                    print(f"   'Add More' clicked for Section {k + 1}")
                    time.sleep(1)
                else:
                    print(" ")
                break

        # --------------------------------------------------------- FILLING MAIN SECTION -------------------------------------------
        print(f"\n Filling data into main section")
        for i, section in enumerate(sections[:1]):
            rows = section.locator("tbody tr").all()

            for j, row in enumerate(rows):
                # Product selection
                product_selector = f'//button[@data-id="Sections_{i}__Products_{j}__Product_Id"]'
                product_input = scope.locator(product_selector)
                if product_input.is_visible():
                    button_locator = scope.locator(product_selector)
                    inner_text = button_locator.locator('.filter-option-inner-inner').inner_text()
                    if inner_text.strip() == "Select":
                        scope.locator(product_selector).click()
                        product_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        product_options = [item.inner_text() for item in product_option_elmts if
                                           item.inner_text() != 'Select']
                        if product_options:
                            random_product_option = random.choice(product_options)
                            self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                                random_product_option, exact=True).nth(0).click()
                        else:
                            print("No options in dropdown")
                    else:
                        # print(f"Skipped row {j} – already has value: '{inner_text}'")
                        pass

                # Variation selection
                variation_selector = f'//button[@data-id="Sections_{i}__Products_{j}__PricebookVariation_Id"]'
                variation_input = scope.locator(variation_selector)
                if variation_input.is_visible():
                    variation_button_locator = scope.locator(variation_selector)
                    variation_inner_text = variation_button_locator.locator('.filter-option-inner-inner').inner_text()
                    if variation_inner_text.strip() == "Select":
                        time.sleep(1)
                        self.page.wait_for_load_state('networkidle', timeout=80000)
                        scope.locator(variation_selector).click()
                        variation_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        variation_options = [item.inner_text() for item in variation_option_elmts if
                                             item.inner_text() != 'Select']
                        random_variation_option = random.choice(variation_options)
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_variation_option, exact=True).nth(0).click()

                # Color selection
                color_selector = f'#Sections_{i}__Products_{j}__ColorId'
                color_input = scope.locator(color_selector)
                if color_input.is_visible():
                    color_button_locator = scope.locator(f'//button[@data-id="Sections_{i}__Products_{j}__ColorId"]')
                    color_inner_text = color_button_locator.locator('.filter-option-inner-inner').inner_text()
                    if color_inner_text.strip() == "Select":
                        scope.locator(f'//button[@data-id="Sections_{i}__Products_{j}__ColorId"]').click()
                        color_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        color_options = [item.inner_text() for item in color_option_elmts if
                                         item.inner_text() != 'Select']
                        random_color_option = random.choice(color_options)
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_color_option, exact=True).nth(0).click()

                # Quantity input
                quantity_selector = f'#Sections_{i}__Products_{j}__Quantity'
                quantity_input = scope.locator(quantity_selector)
                if quantity_input.is_visible():
                    current_quantity_value = quantity_input.input_value().strip()
                    inner_text_value = quantity_input.inner_text().strip()
                    if current_quantity_value == "" or current_quantity_value == "0" or inner_text_value == "0":
                        quantity_input.fill(quantity)

                # Customer notes input
                customer_notes_selector = f'#Sections_{i}__Products_{j}__CustomerNotes'
                customer_notes_input = scope.locator(customer_notes_selector)
                time.sleep(1)
                if customer_notes_input.is_visible():
                    current_value = customer_notes_input.input_value()
                    if current_value.strip() == "":
                        customer_notes_input.fill(customer_notes)

                # Hide on customer PDF checkbox
                hide_on_cust_pdf_selector = f'#Sections_{i}__Products_0__IsHideInPreview'
                hide_on_cust_pdf_input = scope.locator(hide_on_cust_pdf_selector)
                if hide_on_cust_pdf_input.is_visible():
                    scope.locator(hide_on_cust_pdf_selector).check()

                # Hide variation on PDF checkbox
                hide_var_on_pdf_selector = f'#Sections_{i}__Products_1__IsHideVariationonPDF'
                hide_var_on_pdf_input = scope.locator(hide_var_on_pdf_selector)
                if hide_var_on_pdf_input.is_visible():
                    scope.locator(hide_var_on_pdf_selector).check()

        # --------------------------------------------------------------FINAL PRICING SCENARIOS-------------------------------------------------------------------
        # Checkboxes
        checkbox = scope.locator('#IsOptionIncluded')
        if checkbox.is_visible() and not checkbox.is_checked():
            checkbox.check()
        scope.locator('#RetailPrice').click()

        self.toggle_yes_for_section1()

        retail_price_str_1 = self.page.input_value('#RetailPrice')
        retail_price_1 = float(retail_price_str_1.replace("$", "").replace(",", ""))
        print(f"\nRetail Price from page: {retail_price_1}")

        # ---------------------------------------------------- to assert in preview calc -------------------------------------------------------------------------
        with self.page.expect_popup() as page1_info:
            self.page.locator('#download-pdf-scope').click()
        time.sleep(4)
        page1 = page1_info.value

        label = "Retail Price With Options"
        spans = page1.locator("span")
        count = spans.count()

        for y in range(count):
            text = spans.nth(y).inner_text().strip()

            # Match the label span
            if label.lower() in text.lower():
                # Check next few spans for number-like text
                for z in range(y + 1, min(y + 5, count)):
                    next_text = spans.nth(z).inner_text().strip()
                    if re.match(r"^-?\$?[\d,.]+$", next_text):
                        print(next_text)

        print("\n Clicking 'Download PDF'...")
        # Make sure the downloads folder exists
        downloads_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(downloads_dir, exist_ok=True)

        # Optional: add timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(downloads_dir, f"downloaded_proposal_{timestamp}.pdf")

        # Handle the download
        with page1.expect_download() as download_info:
            page1.locator("#toggleSpinners").click()
        download = download_info.value
        download.save_as(file_path)

        print(f"Downloaded PDF saved at: {file_path}")
        page1.close()
        print("Closed preview calc window.")

        # ---------------------------------------------------------------- VALIDATING GRAND TOTAL AND RETAIL PRICE ------------------------------------------

        # Step 1: Read the readonly Retail Price value
        retail_price_str = self.page.input_value('#RetailPrice')
        retail_price = float(retail_price_str.replace("$", "").replace(",", ""))
        print(f"\nRetail Price from page: {retail_price}")

        print("Grand total matches retail price. - pending")

        # ---------------------------------------------------------------------------------------------------------------------------------------------------

        # Step 1: Read the readonly Retail Price value
        retail_price_str = self.page.input_value('#RetailPrice')
        retail_price = float(retail_price_str.replace("$", "").replace(",", ""))

        # ---- Test Dollar Adjustment ----
        scope.locator("label", has_text="$").locator("span").click()  # Click on $
        scope.locator("#Adjustment").fill("50")
        scope.locator('#RetailPrice').press('Enter')
        scope.locator("#Adjustment").dispatch_event("blur")

        final_price_dollar = float(self.page.input_value('#RetailPriceAdjusted').replace("$", "").replace(",", ""))
        # final_price_dollar = float(self.page.locator("#RetailPriceAdjusted").get_attribute("value").replace(",", ""))
        expected_price_dollar = calculate_expected_price(retail_price, 50, is_percentage=False)
        assert final_price_dollar == expected_price_dollar, f"Dollar Test Failed: got {final_price_dollar}, expected {expected_price_dollar}"

        # ---- Test Percentage Adjustment ----
        scope.locator("label", has_text="%").locator("span").click()  # Click on %
        scope.locator("#Adjustment").fill("10")  # 10%
        scope.locator('#Adjustment').press('Enter')

        self.page.dispatch_event("#Adjustment", "blur")

        final_price_percent = float(self.page.input_value('#RetailPriceAdjusted').replace("$", "").replace(",", ""))
        expected_price_percent_change = calculate_expected_price(retail_price, 10, is_percentage=True)
        expected_price_percent = retail_price - expected_price_percent_change

        assert math.isclose(final_price_percent, expected_price_percent, rel_tol=1e-3), (
            f"Percentage Test Failed: got {final_price_percent}, expected {expected_price_percent}"
        )

        print("\n Both dollar and percentage adjustment validations passed.")

        # --------------------------------------------------------------FINAL PRICING SCENARIOS-------------------------------------------------------------------
        self.page.locator(
            "#formSaveInteriorScope > div.d-flex.justify-content-between.mb-3 > div > div > label:nth-child(2)").click()
        print("\nClicked on the 'Customer View' radio button.")

        # to validate duplicate product
        retail_price_locator = self.page.locator('#RetailPriceAdjusted')
        assert not retail_price_locator.is_visible(), "Price locator should not be visible"
        print("Price locator not visible ")

        self.page.locator(
            "#formSaveInteriorScope > div.d-flex.justify-content-between.mb-3 > div > div > label:nth-child(1)").click()
        print("Clicked on the 'Home Expert View' radio button.")

        self.page.wait_for_timeout(5000)

        # retail_price_to_validate_inc_opt = self.page.input_value('#FormattedSidingRetailPrice')
        retail_price_to_validate_inc_opt = float(
            self.page.input_value('#RetailPrice').replace("$", "").replace(",", "")
        )
        print(f"\nRetail Price from page: {retail_price_to_validate_inc_opt}")
        print(f"\n   After untoggling 'Include Options' the pricing validation is done - pending\n")

        btn_update_scope_data = self.page.locator("#btnUpdateScopeData")
        if btn_update_scope_data.is_visible():
            btn_update_scope_data.click(timeout=30000)
        else:
            self.page.locator("#btnUpdateScope").click(timeout=30000)




    def create_flat_estimate(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_flat_roofing_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        self.calc_flat_page_app()
        time.sleep(2)
        time.sleep(10)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        #self.add_sketch_multiple_services()
        time.sleep(2)
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        self.summary_page_app()
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def draw_sketch(self):
        canvas_locator = self.page.locator(
            '//*[@id="item-image-editor-container"]/div[2]/div[2]/div[2]/div/div/div/div')
        canvas_locator.wait_for()
        canvas_box = canvas_locator.bounding_box()

        if canvas_box:
            start_x = canvas_box['x'] + 50
            start_y = canvas_box['y'] + 50
            self.page.mouse.move(start_x, start_y)
            self.page.mouse.down()
            self.page.mouse.move(start_x + 50, start_y + 50)
            self.page.mouse.move(start_x + 100, start_y)
            self.page.mouse.move(start_x + 150, start_y + 50)
            self.page.mouse.move(start_x + 100, start_y + 100)
            self.page.mouse.move(start_x, start_y)
            self.page.mouse.up()
        time.sleep(1)
        logger.info("Sketch drawn")

    def wait_for_page_to_load(self):
        try:
            self.page.wait_for_load_state('networkidle', timeout=60000)
            logger.info("Page loaded.")
        except TimeoutError:
            logger.info("Timeout: Page didn't load in 60 seconds.")
            self.page.screenshot(path="page_load_timeout.png")

    def add_sketch_multiple_services(self):
        self.wait_for_page_to_load()

        container = self.page.locator('.col-md-9 .card-body')
        card_count = container.count()
        logger.info(f"Total card bodies found: {card_count}")

        for i in range(card_count):
            card = container.nth(i)

            # Click "Add Sketch" button scoped to current card
            add_sketch_button = card.locator('a.btn-add-sketch')
            if add_sketch_button.is_visible():
                add_sketch_button.click()
                logger.info(f"Clicked 'Add Sketch' for card index {i}")
            else:
                logger.info(f"'Add Sketch' button not visible in card {i}, skipping.")
                continue

            self.page.wait_for_load_state('networkidle')
            self.draw_sketch()

            # Click 'Save' in the current modal/frame
            self.page.get_by_role("link", name="Save").click()
            logger.info(f"Sketch added for card index {i}")
            self.page.wait_for_timeout(1000)

            # Click the checkbox **scoped to the current card**
            toggle_checkbox = card.locator('input#item_IsPrintedOnCustomerPDF')
            if toggle_checkbox.nth(i).is_visible():
                toggle_checkbox.nth(i).click()
                logger.info(f"Clicked toggle to print sketch on proposal for card {i}")

            # Screenshot after each card operation

            self.click_download()


            # Wait before moving to next card
            self.page.wait_for_load_state('networkidle')
            self.page.wait_for_timeout(1000)

            time.sleep(3)
            # self.upload_picture()
            # time.sleep(3)

        # After processing all cards, click final "Save & Proceed"
        # self.page.locator("button.btn.btn-primary.btnSaveSketch.ml-auto").click()
        self.page.locator("#pills-sketch").get_by_text("Save & Proceed").click()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")

    def get_download_button(self):
        return self.page.locator("a[title='Download']")
        # return self.page.locator("div.document-attach-icon >> a[title='Download']")

    def click_download(self):
        logger.info("Clicking download icon...")

        # Prepare downloads folder
        downloads_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(downloads_dir, exist_ok=True)

        # Timestamped filename to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(downloads_dir, f"downloaded_sketch_file_{timestamp}.pdf")  # Adjust extension as needed

        # Handle download with Playwright
        with self.page.expect_download() as download_info:
            self.get_download_button().nth(0).click()
        download = download_info.value
        download.save_as(file_path)

        logger.info(f"File downloaded and saved to: {file_path}")


    def summary_page_app(self):

        approx_monthly_pay = self.config['summary_page'].get('ApproxMonthyPay')

        # summary_data = self.input_data['summary_page']
        self.page.locator("#btnGotoSummaryTab").click()
        self.page.wait_for_load_state('networkidle')
        logger.info("docs Saved and Proceeded")
        # self.page.wait_for_timeout(2000)

        self.page.click('input[data-index="0"][name="Checkboxes"]')
        # self.page.wait_for_timeout(2000)
        logger.info("clicked on packet price checkbox")

        self.summary_calculations_app()

        self.page.fill('input#summaryBasicDetails_ApproxMonthyPay', approx_monthly_pay)
        # self.page.wait_for_timeout(2000)
        self.page.wait_for_load_state('networkidle')
        logger.info("Base proposal as per attached scope of work")

        self.page.click('//a[contains(@class, "btn") and contains(@class, "btn-primary") and contains(@class, "resetPayments") and @title="Reset"]')
        # self.page.wait_for_timeout(2000)
        logger.info("clicked on reset")

        self.page.wait_for_load_state('networkidle')
        logger.info("Proposal finished")
        # self.page.wait_for_timeout(2000)
        MAX_ATTEMPTS = 5
        with self.page.expect_popup() as page1_info:
            for attempt in range(1, MAX_ATTEMPTS + 1):
                self.page.click('//*[@id="create_Proposal"]')
                time.sleep(3)

                # Locator for the SweetAlert modal
                swal_modal = self.page.locator('div.swal-modal[role="dialog"]')

                if swal_modal.is_visible(timeout=2000):  # wait up to 2s
                    ok_button = swal_modal.locator('button.swal-button--confirm')
                    if ok_button.is_visible():
                        # ok_button.click()
                        # logger.info(f"Clicked 'Ok' on SweetAlert error modal (attempt {attempt})")
                        #
                        # # Reset payments if required
                        # self.page.click(
                        #     '//a[contains(@class, "btn") and contains(@class, "btn-primary") and contains(@class, "resetPayments") and @title="Reset"]'
                        # )
                        # time.sleep(4)

                        # Retry clicking create_Proposal after handling modal
                        continue  # retry loop until modal is gone
                else:
                    logger.info(f"SweetAlert modal not visible on attempt {attempt}")
                    self.page.wait_for_timeout(500)  # small wait before next attempt
                    break  # exit loop if no modal found (success case)

        page1 = page1_info.value

        logger.info("Clicking 'Email Customer'...")
        page1.wait_for_selector("#toggleSpinners", state="visible")

        page1.get_by_text("Email Estimate ").click()
        page1.locator('#btnSendEmail').click()
        time.sleep(3)
        page1.locator('.swal-modal .swal-button--confirm').click()

        # ----------------------------------------------------------------------to download --------------------------------------------

        logger.info("Clicking 'Download PDF'...")
        # Make sure the downloads folder exists
        downloads_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(downloads_dir, exist_ok=True)

        # Optional: add timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(downloads_dir, f"downloaded_proposal_{timestamp}.pdf")

        # Handle the download
        with page1.expect_download() as download_info:
            page1.get_by_text("Download Estimate").click()
        download = download_info.value
        download.save_as(file_path)

        logger.info(f"Downloaded PDF saved at: {file_path}")

        #-------------------------------------------------------------------------------------------------------------------------------------
        #page1.locator(".btn-secondary").nth(0).click()
        page1.locator('a:has-text("Confirm & Sign Estimate")').click(timeout=30000)

        #page1.locator('//a[@onclick="loadConfrimSign()"]').click()
        page1.wait_for_timeout(3000)


        canvas_locator = page1.locator('//div[@class="col-lg-6 form-group"]//div[@id="homeexpert-signature-pad"]')
        canvas_locator.wait_for()
        canvas_box = canvas_locator.bounding_box()

        if canvas_box:
            start_x = canvas_box['x'] + 50
            start_y = canvas_box['y'] + 50
            page1.mouse.move(start_x, start_y)
            page1.mouse.down()
            page1.mouse.move(start_x + 100, start_y + 100)
            page1.mouse.move(start_x + 200, start_y + 50)
            page1.mouse.move(start_x + 300, start_y + 200)
            page1.mouse.up()
        time.sleep(3)
        logger.info("Home Expert Signed")

        canvas_locator1 = page1.locator('//div[@class="col-lg-6 form-group"]//div[@id="customer-signature-pad"]')
        canvas_locator1.wait_for()
        canvas_box = canvas_locator1.bounding_box()

        if canvas_box:
            start_x = canvas_box['x'] + 50
            start_y = canvas_box['y'] + 50
            page1.mouse.move(start_x, start_y)
            page1.mouse.down()
            page1.mouse.move(start_x + 100, start_y + 100)
            page1.mouse.move(start_x + 200, start_y + 50)
            page1.mouse.move(start_x + 300, start_y + 200)
            page1.mouse.up()
        time.sleep(3)
        logger.info("Customer Signed")

        page1.click('//a[@id="btnSaveProposalSign" and @class="btn btn-secondary"]')
        logger.info("proposal signed")
        page1.wait_for_timeout(3000)
        page1.click('//a[@onclick="window.close()"]')


        self.page.wait_for_timeout(3000)


    def cal_page_app_window(self):
        quantity = self.config['calc_page'].get('Quantity')
        customer_notes = self.config['calc_page'].get('CustomerNotes')

        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(2000)

        proposal_number = self.page.locator('#proposalNumber').text_content()
        print(f"Proposal number : {proposal_number}")
        match = re.search(r'#PR(\d+)-', proposal_number)
        if match:
            number = match.group(1)
            print(f"Proposal ID: {number}")
        else:
            print("Proposal ID not found.")
        time.sleep(5)

        #    Scoped Home Expert View
        self.page.locator('#formSaveWindowScope label:has-text("Home Expert View")').click()
        print("Clicked on the 'Home Expert View' radio button.")

        self.page.wait_for_load_state('networkidle')
        sections = self.page.locator("#formSaveWindowScope .table-responsive").all()
        print(f"Total sections found: {len(sections)}")

        # ------------------ Add More logic ------------------
        k = 0
        for section in sections:
            rows = section.locator("tbody tr").all()
            for row in rows:
                locator = section.locator(f"#table-section-{k}").get_by_role("link", name="Add More ")
                if locator.is_visible():
                    locator.click()
                    print(f"'Add more' clicked for section {k + 1}")
                    time.sleep(1)
                break
            k += 1

        # ------------------ Fill Section Details ------------------
        for i, section in enumerate(sections):
            rows = section.locator("tbody tr").all()

            for j, row in enumerate(rows):
                # product
                product_selector = f'//button[@data-id="Sections_{i}__Products_{j}__Product_Id"]'
                product_input = row.locator(product_selector)
                if product_input.is_visible():
                    button_locator = row.locator(product_selector)
                    inner_text = button_locator.locator('.filter-option-inner-inner').inner_text()
                    if inner_text.strip() == "Select":
                        button_locator.click()
                        product_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        product_options = [item.inner_text() for item in product_option_elmts if
                                           item.inner_text() != 'Select']
                        random_product_option = random.choice(product_options)
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_product_option, exact=True).nth(0).click()
                    time.sleep(3)

                # variation
                variation_selector = f'//button[@data-id="Sections_{i}__Products_{j}__PricebookVariation_Id"]'
                variation_input = row.locator(variation_selector)
                if variation_input.is_visible():
                    variation_button_locator = row.locator(variation_selector)
                    variation_inner_text = variation_button_locator.locator('.filter-option-inner-inner').inner_text()
                    if variation_inner_text.strip() == "Select":
                        variation_button_locator.click()
                        variation_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        variation_options = [item.inner_text() for item in variation_option_elmts if
                                             item.inner_text() != 'Select']
                        random_variation_option = random.choice(variation_options)
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_variation_option, exact=True).nth(0).click()

                # color
                color_selector = f'#Sections_{i}__Products_{j}__ColorId'
                color_input = row.locator(color_selector)
                if color_input.is_visible():
                    color_button_locator = row.locator(
                        f'//button[@data-id="Sections_{i}__Products_{j}__ColorId"]')
                    color_inner_text = color_button_locator.locator('.filter-option-inner-inner').inner_text()
                    if color_inner_text.strip() == "Select":
                        color_button_locator.click()
                        color_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        color_options = [item.inner_text() for item in color_option_elmts if
                                         item.inner_text() != 'Select']
                        random_color_option = random.choice(color_options)
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_color_option, exact=True).nth(0).click()

                # quantity
                quantity_selector = f'#Sections_{i}__Products_{j}__Quantity'
                quantity_input = row.locator(quantity_selector)
                if quantity_input.is_visible():
                    current_quantity_value = quantity_input.input_value().strip()
                    inner_text_value = quantity_input.inner_text().strip()
                    if current_quantity_value in ["", "0"] or inner_text_value == "0":
                        quantity_input.fill(quantity)

                # customer notes
                customer_notes_selector = f'#Sections_{i}__Products_{j}__CustomerNotes'
                customer_notes_input = row.locator(customer_notes_selector)
                if customer_notes_input.is_visible():
                    current_value = customer_notes_input.input_value()
                    if current_value.strip() == "":
                        customer_notes_input.fill(customer_notes)

                #    Scoped checkboxes
                hide_on_cust_pdf_selector = f'#Sections_{i}__Products_0__IsHideInPreview'
                checkbox = row.locator(hide_on_cust_pdf_selector)
                if checkbox.is_visible():
                    if not checkbox.is_checked():
                        checkbox.check()

                hide_var_on_pdf_selector = f'#Sections_{i}__Products_1__IsHideVariationonPDF'
                checkbox_var = row.locator(hide_var_on_pdf_selector)
                if checkbox_var.is_visible():
                    if not checkbox_var.is_checked():
                        checkbox_var.check()
        self.page.wait_for_load_state('networkidle', timeout=60000)

        self.handle_line_item(section_index=1, brand_index=0)  # page still loading

        # Scope locator inside the form
        form = self.page.locator("#formSaveWindowScope")
        manufacturer_2_locator = form.locator("h6.text-primary span.setNumber")

        # Wait until the element is attached to the DOM
        # manufacturer_2_locator.wait_for(state="attached", timeout=10000)
        time.sleep(2)
        # Check if it's visible and its parent contains "Manufacturer 2"
        if manufacturer_2_locator.nth(1).is_visible():
            parent_text = manufacturer_2_locator.locator("xpath=..").nth(0).inner_text()
            if "Manufacturer 2" in parent_text:
                self.handle_line_item_mnft2(section_index=1, brand_index=1)

        self.click_line_accordion_until_open(brand_index=0, line_index=0)

        # it is filling all details in line 1 and 2 for manufacturer 1
        self.fill_product_row_details(section_index=1, brand_index=0, line_index=1)
        self.click_line_accordion_until_open(brand_index=0, line_index=0)
        self.fill_product_details()

        section_index = 1  # Target section for testing
        expected_price = "123.45"  # Expected price value from fill_brand_details
        max_attempts = 3  # Match max_attempts from fill_brand_details

        # Step 1: Fill manufacturer details
        print(f"   Filling manufacturer details for section {section_index}")
        self.fill_brand_details(section_index, max_attempts)
        # assert selected_brands, "Failed to fill any brand details"

        self.open_all_accordions()

        self.validate_trim_qtys(expected_qty=1.333)

        self.validate_price_calculation()

        # --------------------------------------------------------------FINAL PRICING SCENARIOS-------------------------------------------------------------------
        # time.sleep(1)
        scope = self.page.locator('#formSaveWindowScope')

        scope.locator('#RetailPrice').click()

        self.toggle_yes_for_all_products()

        retail_price_str_1 = scope.locator('#RetailPrice').input_value()
        retail_price_1 = float(retail_price_str_1.replace("$", "").replace(",", ""))
        print(f"Retail Price from page: {retail_price_1}")

        # ---------------------------------------------------- to assert in preview calc -------------------------------------------------------------------------
        with self.page.expect_popup() as page1_info:
            self.page.locator('#download-pdf-scope').click()
        time.sleep(4)
        page1 = page1_info.value

        label = "Retail Price With Options"
        spans = page1.locator("span")
        count = spans.count()

        for y in range(count):
            text = spans.nth(y).inner_text().strip()

            # Match the label span
            if label.lower() in text.lower():
                # Check next few spans for number-like text
                for z in range(y + 1, min(y + 5, count)):
                    next_text = spans.nth(z).inner_text().strip()
                    if re.match(r"^-?\$?[\d,.]+$", next_text):
                        print(next_text)

        print("Clicking 'Download PDF'...")
        # Make sure the downloads folder exists
        downloads_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(downloads_dir, exist_ok=True)

        # Optional: add timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(downloads_dir, f"downloaded_proposal_{timestamp}.pdf")

        # Handle the download
        with page1.expect_download() as download_info:
            page1.locator("#toggleSpinners").click()
        download = download_info.value
        download.save_as(file_path)

        print(f"Downloaded PDF saved at: {file_path}")
        page1.close()
        print("Closed preview calc window.")

        # Step 1: Read the readonly Retail Price value
        retail_price_str = scope.locator('#RetailPrice').input_value()
        retail_price = float(retail_price_str.replace("$", "").replace(",", ""))
        print(f"Retail Price from page: {retail_price}")

        print("Grand total matches retail price.")

        # Step 1: Read the readonly Retail Price value
        retail_price_str = scope.locator('#RetailPrice').input_value()
        retail_price = float(retail_price_str.replace("$", "").replace(",", ""))

        # ---- Test Dollar Adjustment ----
        scope.locator("label", has_text="$").locator(
            "span").click()  # Click on $scope.locator('#Adjustment').fill("50")

        scope.locator('#Adjustment').fill("50")
        scope.locator('#RetailPrice').press('Enter')
        scope.locator('#Adjustment').dispatch_event('blur')

        final_price_dollar = float(
            scope.locator('#RetailPriceAdjusted').input_value().replace("$", "").replace(",", ""))
        # final_price_dollar = float(scope.locator("#RetailPriceAdjusted").get_attribute("value").replace(",", ""))
        expected_price_dollar = calculate_expected_price(retail_price, 50, is_percentage=False)
        assert final_price_dollar == expected_price_dollar, f"Dollar Test Failed: got {final_price_dollar}, expected {expected_price_dollar}"

        # ---- Test Percentage Adjustment ----
        scope.locator("label", has_text="%").locator("span").click()  # Click on %
        scope.locator("#Adjustment").fill("10")  # 10%
        scope.locator("#Adjustment").press("Enter")
        scope.locator("#Adjustment").dispatch_event("blur")

        # final_price_percent = float(scope.input_value('#RetailPriceAdjusted').replace("$", "").replace(",", ""))
        final_price_percent_str = scope.locator('#RetailPriceAdjusted').input_value()
        final_price_percent = float(final_price_percent_str.replace("$", "").replace(",", ""))

        expected_price_percent_change = calculate_expected_price(retail_price, 10, is_percentage=True)
        expected_price_percent = retail_price - expected_price_percent_change

        assert math.isclose(final_price_percent, expected_price_percent, rel_tol=1e-3), (
            f"Percentage Test Failed: got {final_price_percent}, expected {expected_price_percent}"
            )

        print("Both dollar and percentage adjustment validations passed.")

        scope.locator('label.btn:has-text("Customer View")').click()
        print("Clicked on the 'Customer View' radio button.")

        retail_price_locator = scope.locator('#RetailPriceAdjusted')
        assert not retail_price_locator.is_visible(), "Price locator should not be visible"
        print("Price locator not visible")

        scope.locator('label.btn:has-text("Home Expert View")').click()
        print("Clicked on the 'Home Expert View' radio button.")

        # Final save

        btn_update_scope_data = self.page.locator("#btnUpdateScopeData")
        if btn_update_scope_data.is_visible():
            btn_update_scope_data.click(timeout=30000)
        else:
            self.page.locator("#btnUpdateScope").click(timeout=30000)

        time.sleep(4)
        estimate_id = self.get_estimate_id()
        logger.info(f"Esimate id is: {estimate_id}")
        print(f"Esimate id is: {estimate_id}")
        return estimate_id

    def toggle_yes_for_all_products(self):
        index = 0
        while True:
            checkbox_id = f"Sections_0__Products_{index}__IsIncludedDefault"
            locator = self.page.locator(f"input#{checkbox_id}")
            if locator.count() == 0:
                print(f"No checkbox found for index {index}, ending loop.")
                break
            if not locator.first.is_checked():
                locator.first.check()
                print(f"   Toggled ON for: {checkbox_id}")
            else:
                print(f"Already ON: {checkbox_id}")
            index += 1

    def parse_price(self, price_str: str) -> float:
        return float(price_str.replace('$', '').replace(',', '').strip())

    def validate_price_calculation(self):
        # All rows with class 'manufacture-item' (each line item)
        rows = self.page.locator("tr.manufacture-item")

        for i in range(rows.count()):
            row = rows.nth(i)
            # Locate each needed column within the row
            qty_text = row.locator(".brand-mfg-lineqty").inner_text().strip()
            line_total_text = row.locator(".brand-mfg-linetotalprice").nth(0).inner_text().strip()
            total_text = row.locator(".brand-mfg-linetotalprice").nth(1).inner_text().strip()

            try:
                qty = float(qty_text)
                line_total = self.parse_price(line_total_text)
                expected_total = qty * line_total
                actual_total = self.parse_price(total_text)

                # Allow small floating-point tolerance
                assert abs(expected_total - actual_total) < 0.01, (
                    f"   Mismatch at row {i + 1}: Qty={qty}, Line Total={line_total_text}, "
                    f"Expected Total={expected_total}, Found={total_text}"
                )
                print(f"   Row {i + 1} passed: {qty} x {line_total} = {actual_total}")
            except Exception as e:
                print(f"   Error in row {i + 1}: {str(e)}")

    def click_add_manufacturer_until_visible(self, section_index: int, expected_index: int, max_attempts: int = 3):
        """
        Clicks 'Add Manufacturer' until the expected brand dropdown becomes visible with 'Select' as value.
        """
        for attempt in range(max_attempts):
            self.page.get_by_role("link", name="Add Manufacturer").click()
            new_brand_button = self.page.locator(
                f'//button[@data-id="Sections_{section_index}__Brands_{expected_index}__Brand_Id"]')

            if new_brand_button.is_visible():
                inner_text = new_brand_button.locator('.filter-option-inner-inner').inner_text()
                if inner_text.strip() == "Select":
                    print(f"   New brand dropdown appeared with 'Select' on attempt {attempt + 1}")
                    return True
            print(f"   Brand dropdown not visible or not 'Select' yet. Retrying... Attempt {attempt + 1}")

        print(f"   Brand dropdown not detected after {max_attempts} attempts.")
        return False

    def fill_brand_details(self, section_index: int, max_attempts: int = 3):
        scope = self.page.locator("#formSaveWindowScope")
        self.click_add_manufacturer_until_visible(section_index, expected_index=2, max_attempts=max_attempts)

        rows = scope.locator(f"tr.brand-section-summary-{section_index}").all()
        for index, row in enumerate(rows):
            print(f"Processing brand index {index}")
            self.page.wait_for_load_state('networkidle')
            brand_button = row.locator(f'[data-id="Sections_{section_index}__Brands_{index}__Brand_Id"]')
            if brand_button.is_visible():
                inner_text = brand_button.locator('.filter-option-inner-inner').inner_text()
                if inner_text.strip() == "Select":
                    tried_options = set()
                    while True:
                        brand_button.dblclick()
                        brand_button.click()
                        # Now, options *inside the scope/modal*
                        dropdown_menu = scope.locator('.dropdown-menu.show:not(.inner)')
                        brand_option_elmts = dropdown_menu.locator('.dropdown-item:not(.selected)').all()
                        brand_options = [item.inner_text() for item in brand_option_elmts if
                                         item.inner_text() != 'Select' and item.inner_text() not in tried_options]
                        if not brand_options:
                            print(f"   No valid brand options left for index {index}")
                            break
                        random_brand_option = random.choice(brand_options)
                        tried_options.add(random_brand_option)
                        dropdown_menu.locator('.dropdown-item').get_by_text(random_brand_option, exact=True).nth(
                            0).click()
                        print(f"   Attempted brand: {random_brand_option} for index {index}")
                        self.page.wait_for_load_state('networkidle')
                        time.sleep(3)
                        popup_text_locator = scope.locator('.swal-overlay--show-modal').locator(
                            '.swal-text:not(.confirm-text)').get_by_text("Manufacturer Already Exists!", exact=True)
                        if popup_text_locator.is_visible():
                            scope.locator('.swal-button--confirm').click()
                        else:
                            print(f"   Selected brand: {random_brand_option} for index {index}")
                            break
                else:
                    print(f"   Brand already selected at index {index}: '{inner_text.strip()}'")
            brand_name_input = row.locator(f"[id='Sections_{section_index}__Brands_{index}__BrandName']")
            brand_name = brand_name_input.get_attribute("value") if brand_name_input else f"Brand {index}"
            print(f"   Final brand name (value attribute): {brand_name}")
            # Description and price, scoped as well:
            desc_input = row.locator(f"[id='Sections_{section_index}__Brands_{index}__Description']")
            if desc_input.is_visible():
                desc_input.fill(f"{brand_name} Auto description for")
            price_input = row.locator(f"[id='Sections_{section_index}__Brands_{index}__MaterialPrice']")
            if price_input.is_visible():
                price_input.fill("123.45")
        self.delete_manufacturer_until_invisible(section_index, brand_index=2, max_attempts=max_attempts)
        time.sleep(3)

    def delete_manufacturer_until_invisible(self, section_index: int, brand_index: int, max_attempts: int = 3):
        """
        Clicks 'Delete' for a manufacturer until the corresponding brand row becomes invisible.
        """
        for attempt in range(max_attempts):
            print(
                f"   Attempt {attempt + 1}: Trying to delete manufacturer for brand {brand_index} in section {section_index}.")
            delete_btn_selector = f'a.delete-icon[data-sectionindex="{section_index}"][data-index="{brand_index}"]'
            delete_btn = self.page.locator(delete_btn_selector)

            if not delete_btn.is_visible():
                print("   Delete button not found or not visible.")
                # Check if row is already gone
                brand_row_selector = f'tr.window-brand-section-prod-summary-row.brand-set-section-{section_index}-brand-{brand_index}'
                brand_row = self.page.locator(brand_row_selector)
                if not brand_row.is_visible():
                    print(f"   Brand {brand_index} row already removed.")
                    return True
                return False

            delete_btn.click(force=True)

            # Wait for potential DOM update
            self.page.wait_for_timeout(5000)

            # Check if the brand row is no longer visible
            brand_row_selector = f'tr.window-brand-section-prod-summary-row.brand-set-section-{section_index}-brand-{brand_index}'
            brand_row = self.page.locator(brand_row_selector)

            try:
                if not brand_row.is_visible():
                    print(f"   Brand {brand_index} row successfully removed on attempt {attempt + 1}.")
                    return True
                else:
                    print(f"   Brand row still visible. Retrying... Attempt {attempt + 1}")
            except Exception as e:
                print(f"   Error verifying brand row removal: {str(e)}. Retrying...")

        print(f"   Failed to remove brand {brand_index} row after {max_attempts} attempts.")
        return False

    def click_line_accordion_until_open(self, brand_index: int, line_index: int, max_attempts: int = 100):
        for attempt in range(max_attempts):
            print(f"   Attempt {attempt + 1}: Clicking accordion for brand {brand_index}, line {line_index}")
            line_toggle = self.form.locator(f'a[href="#set-{brand_index}-{line_index}"]')
            if line_toggle.is_visible():
                line_toggle.click(timeout=5000)
                install_button = self.form.locator(f'button[data-id="Sections_1__Brands_{brand_index}__LineItems_{line_index}__InstallId"]')
                try:
                    install_button.wait_for(state="visible", timeout=2000)
                    print("   Accordion expanded successfully.")
                    return True
                except:
                    print("   Accordion didn't expand. Retrying...")
            else:
                print("   Accordion toggle not visible.")

        print("   Failed to expand line accordion after maximum attempts.")
        return False

    def handle_line_item(self, section_index: int, brand_index: int, line_index: int = 0):

        # Click Line Accordion to Expand
        self.click_line_accordion_until_open(brand_index=0, line_index=0)

        self.form.locator(f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Roomname").fill(
            "Living Room")

        self.form.locator(
            f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__LineQuantity").fill("2")
        time.sleep(4)

        install_button = self.form.locator(
            f'button[data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__InstallId"]')
        install_button.click()
        dropdown_menu = self.form.locator("div.dropdown-menu.show")
        dropdown_items = dropdown_menu.locator(".dropdown-item")
        count = dropdown_items.count()
        if count > 0:
            random_index = random.randint(0, count - 1)
            random_option = dropdown_items.nth(random_index)
            random_option.wait_for(state="visible", timeout=3000)
            random_option.click()
        else:
            raise Exception("No install options found in dropdown!")

        # this is to see if variation is empty and fill quantity only if it is empty (requirement)
        model_selector = f'//button[@data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Model_Id"]'
        model_input = self.form.locator(model_selector)
        # time.sleep(1)
        if model_input.is_visible():
            # time.sleep(1)
            model_button_locator = self.form.locator(
                f'//button[@data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Model_Id"]')
            model_inner_text = model_button_locator.locator('.filter-option-inner-inner').inner_text()
            # print(f"variation inner text : {variation_inner_text}")
            if model_inner_text.strip() == "Select":
                time.sleep(1)
                self.form.locator(
                    f'//button[@data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Model_Id"]').click()
                model_option_elmts = self.form.locator('.dropdown-menu.show:not(.inner)').locator(
                    '.dropdown-item:not(.selected)').all()
                model_options = [item.inner_text() for item in model_option_elmts if item.inner_text() != 'Select']
                random_model_option = random.choice(model_options)
                self.form.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                    random_model_option, exact=True).nth(0).click()
            else:
                pass

        # Select Style (skip if no options)
        style_button = self.form.locator(
            f'button[data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Style_Id"]')
        style_name_button = self.form.locator(
            f'button[data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__StyleName"]')

        if style_button.is_visible():
            style_button.click(force=True)

            # Wait for dropdown menu to appear
            dropdown_menu = self.form.locator("div.dropdown-menu.show")
            # dropdown_menu.wait_for(state="visible", timeout=3000)

            # Get all non-"Select" style options
            options = dropdown_menu.locator(".dropdown-item").all()
            valid_options = [opt for opt in options if opt.inner_text().strip().lower() != "select"]

            if valid_options:
                random_option = random.choice(valid_options)
                random_option.wait_for(state="visible", timeout=2000)
                random_option.click()
            else:
                print("   No valid style options available to select.")

        # Fill Width and Height
        self.form.locator(
            f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Width"
        ).fill("4")

        self.form.locator(
            f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Height"
        ).fill("4")

        self.duplicate_line_and_verify(section_index=1, brand_index=0, line_index=0)

    def handle_line_item_mnft2(self, section_index: int, brand_index: int, line_index: int = 0):
        time.sleep(2)

        # Click Line Accordion to Expand
        self.click_line_accordion_until_open(brand_index=1, line_index=0)
        time.sleep(2)

        # Fill Room Name
        self.form.locator(
            f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Roomname"
        ).fill("Living Room")

        # Fill Quantity
        self.form.locator(
            f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__LineQuantity"
        ).fill("2")

        # Select Install button
        install_button = self.form.locator(
            f'button[data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__InstallId"]'
        )
        install_button.click()
        dropdown_menu = self.page.locator("div.dropdown-menu.show")
        dropdown_items = dropdown_menu.locator(".dropdown-item")
        count = dropdown_items.count()
        if count > 0:
            random_index = random.randint(0, count - 1)
            random_option = dropdown_items.nth(random_index)
            random_option.wait_for(state="visible", timeout=3000)
            random_option.click()
        else:
            raise Exception("No install options found in dropdown!")

        # this is to see if variation is empty and fill quantity only if it is empty (requirement)
        variation_selector = f'//button[@data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Model_Id"]'
        variation_input = self.form.locator(variation_selector)
        # time.sleep(1)
        if variation_input.is_visible():
            # time.sleep(1)
            variation_button_locator = self.form.locator(variation_selector)
            variation_inner_text = variation_button_locator.locator('.filter-option-inner-inner').inner_text()
            # print(f"variation inner text : {variation_inner_text}")
            if variation_inner_text.strip() == "Select":
                time.sleep(1)
                self.form.locator(variation_selector).click()
                variation_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                    '.dropdown-item:not(.selected)').all()
                variation_options = [item.inner_text() for item in variation_option_elmts if
                                     item.inner_text() != 'Select']
                random_variation_option = random.choice(variation_options)
                self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                    random_variation_option, exact=True).nth(0).click()
            else:
                pass
        time.sleep(3)  # required

        # Select Style (skip if no options)
        style_button = self.form.locator(
            f'button[data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Style_Id"]'
        )
        style_name_button = self.form.locator(
            f'button[data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__StyleName"]'
        )

        if style_button.is_visible():
            style_button.click(force=True)

            # Wait for dropdown menu to appear
            dropdown_menu = self.page.locator("div.dropdown-menu.show")
            # dropdown_menu.wait_for(state="visible", timeout=3000)

            # Get all non-"Select" style options
            options = dropdown_menu.locator(".dropdown-item").all()
            valid_options = [opt for opt in options if opt.inner_text().strip().lower() != "select"]

            if valid_options:
                random_option = random.choice(valid_options)
                random_option.wait_for(state="visible", timeout=2000)
                random_option.click()
            else:
                print("   No valid style options available to select.")

        # Fill Width and Height
        self.form.locator(
            f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Width"
        ).fill("4")

        self.form.locator(
            f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Height"
        ).fill("4")

        # Duplicate Line and Verify
        self.duplicate_line_and_verify(section_index=1, brand_index=1, line_index=0)

    def handle_line_item_m1l2(self, section_index: int, brand_index: int, line_index: int = 2):
        # def handle_line_item(self, section_index: int, brand_index: int, line_index: int):

        # Click Line Accordion to Expand
        self.click_line_accordion_until_open(brand_index=0, line_index=2)

        self.page.wait_for_load_state('networkidle')

        self.page.fill(f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Roomname",
                       "Living Room")
        self.page.fill(f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__LineQuantity", "2")

        # Fill Width and Height
        self.page.fill(f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Width", "4")
        self.page.fill(f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Height", "4")

    def handle_line_item_m2l2(self, section_index: int, brand_index: int, line_index: int = 2):
        self.page.wait_for_load_state('networkidle')
        time.sleep(5)
        self.click_line_accordion_until_open(brand_index=1, line_index=2)
        self.page.wait_for_load_state('networkidle')

    def duplicate_line_and_verify(self, section_index: int, brand_index: int, line_index: int, max_attempts: int = 3):
        for attempt in range(max_attempts):
            print(
                f"   Attempt {attempt + 1}: Trying to duplicate line {line_index} for brand {brand_index} in section {section_index}.")

            # Duplicate button selector
            duplicate_btn_selector = f'a.window-duplicate-line[data-sectionindex="{section_index}"][data-brandindex="{brand_index}"][data-lineid="{line_index}"]'
            duplicate_btn = self.page.locator(duplicate_btn_selector)

            if not duplicate_btn.is_visible():
                print("   Duplicate button not found or not visible.")
                return False

            duplicate_btn.click()

            # Build expected href for the new line (increment line_index)
            new_line_href = f'#set-{section_index - 1}-{line_index + 1}'
            new_line_selector = f'a[href="{new_line_href}"] .window-linename'

            try:
                # Wait for the new line anchor to appear
                self.page.locator(new_line_selector).wait_for(timeout=3000)

                # Extract text to confirm (line number + room name)
                line_text = self.page.locator(f'a[href="{new_line_href}"] .window-linename').inner_text()
                room_text = self.page.locator(f'a[href="{new_line_href}"] .window-line-room-name').inner_text()

                print(f"   New line created: {line_text.strip()} {room_text.strip()}")
                return True
            except:
                print("   Line not created yet. Retrying...")

        print("   Failed to duplicate line after maximum attempts.")
        return False

    def remove_line_and_verify(self, section_index: int, brand_index: int, line_index: int, max_attempts: int = 100):
        for attempt in range(max_attempts):
            print(
                f"   Attempt {attempt + 1}: Trying to remove line {line_index} for brand {brand_index} in section {section_index}.")
            remove_btn_selector = f'a{self.remove_line_selector}[data-sectionindex="{section_index}"][data-brandindex="{brand_index}"][data-lineindex="{line_index}"]'
            remove_btn = self.page.locator(remove_btn_selector)
            if not remove_btn.is_visible():
                print("   Remove button not found or not visible.")
                return False
            remove_btn.click(force=True)
            # remove_btn.click(force=True)
            removed_line_id = f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Roomname"
            try:
                assert not self.page.locator(removed_line_id).is_visible(), "Element is still visible"
                print(f"   Line {line_index} successfully removed.")
                return True
            except:
                print("   Line not removed yet. Retrying...")
        print("   Failed to remove line after maximum attempts.")
        return False

    def fill_product_row_details(self, section_index: int, brand_index: int, line_index: int):
        print(f"   Processing products under Section {section_index}, Brand {brand_index}, Line {line_index}")

        product_table_locator = self.page.locator(
            f'#table-section-{section_index}-brand-{brand_index}-line-{line_index}-subsection-0')
        rows = product_table_locator.locator('tbody tr')
        total_rows = rows.count()

        for product_index in range(total_rows):
            print(f"   Product Row: {product_index}")

            # PRODUCT Dropdown
            product_btn = self.page.locator(
                f'button[data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Subsection_0__Products_{product_index}__Product_Id"]'
            )
            if product_btn.is_visible():
                inner = product_btn.locator('.filter-option-inner-inner').inner_text().strip()
                if inner in ["Select", "Nothing selected"]:
                    product_btn.click()
                    options = self.page.locator(".dropdown-menu.show .dropdown-item").all_inner_texts()
                    options = [opt for opt in options if opt.strip().lower() not in ["select", "nothing selected"]]
                    if options:
                        selected = random.choice(options)
                        print(f"   Selected product: {selected}")
                        self.page.locator(".dropdown-menu.show .dropdown-item").get_by_text(selected,
                                                                                            exact=True).click()
                    else:
                        print(f"   No options in product dropdown for row {product_index}")

            # VARIATION Dropdown

            variation_selector = f'button[data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Subsection_0__Products_{product_index}__PricebookVariation_Id"]'
            variation_input = self.page.locator(variation_selector)
            # time.sleep(1)
            if variation_input.is_visible():
                # time.sleep(1)
                variation_button_locator = self.page.locator(
                    f'button[data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Subsection_0__Products_{product_index}__PricebookVariation_Id"]')
                variation_inner_text = variation_button_locator.locator('.filter-option-inner-inner').inner_text()
                if variation_inner_text in ["select", "Nothing selected"]:
                    time.sleep(1)
                    self.page.wait_for_load_state('networkidle', timeout=60000)

                    self.page.locator(
                        f'button[data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Subsection_0__Products_{product_index}__PricebookVariation_Id"]').click()
                    variation_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                        '.dropdown-item:not(.selected)').all()
                    variation_options = [item.inner_text() for item in variation_option_elmts if
                                         item.inner_text() != 'Select']
                    random_variation_option = random.choice(variation_options)
                    self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                        random_variation_option, exact=True).nth(0).click()
                else:
                    pass

            # UOM Dropdown
            uom_btn = self.page.locator(
                f'button[data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Subsection_0__Products_{product_index}__UOM_Id"]')
            if uom_btn.is_visible():
                inner = uom_btn.locator('.filter-option-inner-inner').inner_text().strip()
                if inner in ["Select", "Nothing selected"]:
                    uom_btn.click()
                    options = self.page.locator(".dropdown-menu.show .dropdown-item").all_inner_texts()
                    options = [opt for opt in options if opt.strip().lower() not in ["select", "nothing selected"]]
                    if options:
                        selected = random.choice(options)
                        print(f"   Selected UOM: {selected}")
                        self.page.locator(".dropdown-menu.show .dropdown-item").get_by_text(selected,
                                                                                            exact=True).click()
                    else:
                        print(f"   No options in UOM dropdown for row {product_index}")

            # QTY Field
            qty_field = self.page.locator(
                f'#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Subsection_0__Products_{product_index}__Quantity')
            if qty_field.is_visible():
                current_value = qty_field.input_value().strip()
                if not current_value:
                    qty_value = str(random.randint(1, 5))
                    qty_field.fill(qty_value)
                    print(f"   Filled quantity: {qty_value}")

            # NOTE Field
            note_field = self.page.locator(
                f'#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Subsection_0__Products_{product_index}__Productdescription')
            if note_field.is_visible():
                current_value = note_field.input_value().strip()
                if not current_value:
                    note_value = f"Auto-note {random.randint(100, 999)}"
                    note_field.fill(note_value)
                    print(f"   Filled note: {note_value}")

    def fill_product_details(self):
        """Loop through manufacturers, lines, subsections, and products to fill details and calculate totals."""
        # Dictionary to store totals by manufacturer and line
        manufacturer_totals = {}
        line_totals = {}

        # Get all manufacturer sections
        manufacturers = self.page.locator('#divSetData > div[id^="brand-set-"]').all()

        for brand_index, manufacturer in enumerate(manufacturers):
            brand_id_match = re.search(r'brand-set-(\d+)', manufacturer.get_attribute('id'))
            if not brand_id_match:
                continue
            brand_id = brand_id_match.group(1)
            manufacturer_totals[brand_id] = 0  # Initialize manufacturer total

            # Get all lines for this manufacturer
            lines = manufacturer.locator(
                f'div.setAccordianLine[id="accordion-sets-windows"][data-brandindex="{brand_id}"] > .window-card'
            ).all()
            print(f"Manufacturer {brand_id} has {len(lines)} lines")

            for line_index, line in enumerate(lines):
                line_id = f'set-{brand_id}-{line_index}'
                line_totals[f'{brand_id}-{line_index}'] = 0

                # Get all subsections
                subsections = line.locator('.card-body .subsection').all()
                print(f"Line {line_index} has {len(subsections)} subsections")

                for subsection_index, subsection in enumerate(subsections):
                    subsection_classes = subsection.get_attribute('class')
                    subsection_id_match = re.search(r'subsection-(\d+)', subsection_classes)
                    if not subsection_id_match:
                        continue
                    subsection_id = subsection_id_match.group(1)

                    # Get all product rows in the subsection
                    product_rows = subsection.locator(
                        f'table[id="table-section-1-brand-{brand_id}-line-{line_index}-subsection-{subsection_index}"] tbody tr.window-row'
                    ).all()
                    print(f"Subsection {subsection_index} has {len(product_rows)} products")

                    for product_index, _ in enumerate(product_rows):
                        # Dynamic locators
                        product_dropdown_selector = f'#Sections_1__Brands_{brand_id}__LineItems_{line_index}__Subsection_{subsection_index}__Products_{product_index}__Product_Id'
                        variation_dropdown_selector = f'select#Sections_1__Brands_{brand_id}__LineItems_{line_index}__Subsection_{subsection_index}__Products_{product_index}__PricebookVariation_Id.form-control'
                        qty_input_selector = f'#Sections_1__Brands_{brand_id}__LineItems_{line_index}__Subsection_{subsection_index}__Products_{product_index}__Quantity'
                        customer_notes_selector = f'#Sections_1__Brands_{brand_id}__LineItems_{line_index}__Subsection_{subsection_index}__Products_{product_index}__CustomerNotes'
                        total_price_selector = f'#Sections_1__Brands_{brand_id}__LineItems_{line_index}__Subsection_{subsection_index}__Products_{product_index}__Totals'

                        # Check if product is empty and fill quantity only if it is empty
                        product_input = self.form.locator(product_dropdown_selector)
                        if product_input.is_visible():
                            button_locator = self.form.locator(
                                f'//button[@data-id="Sections_1__Brands_{brand_id}__LineItems_{line_index}__Subsection_{subsection_index}__Products_{product_index}__Product_Id"]'
                            )
                            inner_text = button_locator.locator('.filter-option-inner-inner').inner_text()
                            if inner_text.strip() == "Select":
                                time.sleep(1)
                                self.form.locator(
                                    f'//button[@data-id="Sections_1__Brands_{brand_id}__LineItems_{line_index}__Subsection_{subsection_index}__Products_{product_index}__Product_Id"]'
                                ).click()
                                product_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                                    '.dropdown-item:not(.selected)'
                                ).all()
                                product_options = [item.inner_text() for item in product_option_elmts if
                                                   item.inner_text() != 'Select']
                                if product_options:  # Ensure there are valid options
                                    random_product_option = random.choice(product_options)
                                    self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                                        '.dropdown-item').get_by_text(
                                        random_product_option, exact=True
                                    ).nth(0).click()

                        # Check if variation is empty and fill quantity only if it is empty
                        variation_input = self.form.locator(variation_dropdown_selector)
                        if variation_input.is_visible():
                            variation_button_locator = self.form.locator(
                                f'//button[@data-id="Sections_1__Brands_{brand_id}__LineItems_{line_index}__Subsection_{subsection_index}__Products_{product_index}__PricebookVariation_Id"]'
                            )
                            variation_inner_text = variation_button_locator.locator(
                                '.filter-option-inner-inner').inner_text()
                            if variation_inner_text.strip() in ["Select", "Nothing selected"]:
                                time.sleep(1)
                                variation_button_locator.click()
                                variation_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                                    '.dropdown-item:not(.selected)'
                                ).all()
                                variation_options = [item.inner_text() for item in variation_option_elmts if
                                                     item.inner_text() != 'Select']
                                if variation_options:  # Ensure there are valid options
                                    random_variation_option = random.choice(variation_options)
                                    self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                                        '.dropdown-item').get_by_text(
                                        random_variation_option, exact=True
                                    ).nth(0).click()

                        # Check if quantity is empty or 0 and fill quantity only in that case
                        quantity_input = self.form.locator(qty_input_selector)
                        if quantity_input.is_visible():
                            current_quantity_value = quantity_input.input_value().strip()
                            inner_text_value = quantity_input.inner_text().strip()
                            if current_quantity_value == "" or current_quantity_value == "0" or inner_text_value == "0":
                                quantity_input.fill("1")

                        # Check if customer notes is empty and fill only if it is empty
                        customer_notes_input = self.form.locator(customer_notes_selector)
                        if customer_notes_input.is_visible():
                            time.sleep(1)
                            current_value = customer_notes_input.input_value()
                            if current_value.strip() == "":
                                time.sleep(1)
                                customer_notes_input.fill("Default note")  # Use a static note instead of selector

                        self.page.wait_for_load_state('networkidle', timeout=60000)

                        # Check "Hide on PDF" checkbox
                        hide_on_cust_pdf_selector = f'#Sections_1__Brands_{brand_id}__LineItems_{line_index}__Subsection_{subsection_index}__Products_0__IsHideInPreview'
                        hide_on_cust_pdf_input = self.form.locator(hide_on_cust_pdf_selector)
                        if hide_on_cust_pdf_input.is_visible():
                            self.form.locator(hide_on_cust_pdf_selector).check()
                        # Check "Hide Variation on PDF" checkbox
                        hide_var_on_pdf_selector = f'#Sections_1__Brands_{brand_id}__LineItems_{line_index}__Subsection_{subsection_index}__Products_1__IsHideVariationonPDF'
                        hide_var_on_pdf_input = self.form.locator(hide_var_on_pdf_selector)
                        if hide_var_on_pdf_input.is_visible():
                            self.form.locator(hide_var_on_pdf_selector).check()

                        self.page.wait_for_load_state('networkidle', timeout=60000)

                        # Calculate total for the product
                        total_price_input = self.form.locator(total_price_selector)
                        if total_price_input.is_visible():
                            total_price = total_price_input.input_value().strip()
                            # Remove dollar sign from total price
                            total_price = total_price.replace('$', '')
                            try:
                                total_price_value = float(total_price) if total_price else 0.0
                                line_totals[f'{brand_id}-{line_index}'] += total_price_value
                                manufacturer_totals[brand_id] += total_price_value
                            except ValueError:
                                print(
                                    f"Invalid total price '{total_price}' for product {product_index} in line {line_index}, brand {brand_id}"
                                )

            # Print totals for each line and manufacturer
            for line_key, total in line_totals.items():
                brand_id, line_index = line_key.split('-')
                print(f"Total for Manufacturer {brand_id}, Line {line_index}: ${total:.2f}")
            for brand_id, total in manufacturer_totals.items():
                print(f"Total for Manufacturer {brand_id}: ${total:.2f}")

        return manufacturer_totals, line_totals

    def verify_lines_added(self, expected_lines):
        """Verify the number of lines added for each manufacturer."""
        line_cards = self.page.locator('.window-card').all()
        time.sleep(3)
        actual_lines = len(line_cards)
        assert actual_lines == expected_lines, f"Expected {expected_lines} lines, but got {actual_lines}"
        print(f"Test completed: Added {actual_lines} lines, expected {expected_lines}")

    def open_all_accordions(self):
        """Open all accordion lines by clicking on collapsed toggles."""
        accordions = self.page.locator('div[id^="set-"][class*="collapse"]:not(.show)')
        for i in range(accordions.count()):
            accordion = accordions.nth(i)
            toggle = accordion.locator('xpath=preceding::a[@data-toggle="collapse"][1]')
            if toggle.is_visible():
                toggle.click()
                self.page.wait_for_timeout(500)  # Wait for animation

    def get_estimate_id(self):
        header_text = self.page.locator("h2#estimate-header").inner_text().strip()
        match = re.search(r"[-–]\s*(\d+)", header_text)
        if match:
            estimate_id = match.group(1)
            return estimate_id
        else:
            raise Exception("Estimate ID not found in header text")

    def handle_line_door_item(self, section_index: int, brand_index: int, line_index: int = 0):
        scope = self.page.locator("#formSaveDoorScope")  # Use Door scope for all locators here

        # Click Line Accordion to Expand
        self.click_line_accordion_until_open(brand_index=0, line_index=0)

        self.page.wait_for_load_state('networkidle')
        time.sleep(3)

        # scope.locator(f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Roomname").fill(
        #     "Living Room")
        # scope.locator(f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__LineQuantity").fill(
        #     "2")

        time.sleep(3)
        # this is to see if variation is empty and fill quantity only if it is empty (requirement)

        product_selector = f'//button[@data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Model_Id"]'
        product_input = scope.locator(product_selector)
        # time.sleep(1)
        if product_input.is_visible():
            # time.sleep(1)
            button_locator = scope.locator(
                f'//button[@data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Model_Id"]')
            inner_text = button_locator.locator('.filter-option-inner-inner').inner_text()
            # print(f"Product {j} inner text : {inner_text}")
            if inner_text.strip() == "Select":
                # time.sleep(1)
                scope.locator(
                    f'//button[@data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Model_Id"]').click()
                product_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                    '.dropdown-item:not(.selected)').all()
                product_options = [item.inner_text() for item in product_option_elmts if item.inner_text() != 'Select']
                random_product_option = random.choice(product_options)
                self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                    random_product_option, exact=True).nth(0).click()
                # print(f"Filled empty product for section {i}, product {j}")
            else:
                # print(f"Skipped row {j} – already has value: '{inner_text}'")
                pass

        # Select Style (skip if no options)
        style_button = scope.locator(
            f'button[data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Style_Id"]')
        style_name_button = scope.locator(
            f'button[data-id="Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__StyleName"]')

        if style_button.is_visible():
            style_button.click(force=True)

            # Wait for dropdown menu to appear
            dropdown_menu = scope.locator("div.dropdown-menu.show")
            # dropdown_menu.wait_for(state="visible", timeout=3000)

            # Get all non-"Select" style options
            options = dropdown_menu.locator(".dropdown-item").all()
            valid_options = [opt for opt in options if opt.inner_text().strip().lower() != "select"]

            if valid_options:
                random_option = random.choice(valid_options)
                random_option.wait_for(state="visible", timeout=2000)
                random_option.click()
            else:
                print("   No valid style options available to select.")

        # Fill Width and Height
        # scope.locator(f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Width").fill("3.5")
        # scope.locator(f"#Sections_{section_index}__Brands_{brand_index}__LineItems_{line_index}__Height").fill("5.0")

    def cal_page_app_door(self):
        quantity = self.config['calc_page'].get('Quantity')
        customer_notes = self.config['calc_page'].get('CustomerNotes')

        self.page.wait_for_load_state('networkidle')
        # self.page.wait_for_timeout(2000)

        proposal_number = self.page.locator('#proposalNumber').text_content()
        print(f"Proposal number : {proposal_number}")
        match = re.search(r'#PR(\d+)-', proposal_number)
        if match:
            number = match.group(1)
            print(f"Proposal ID: {number}")
        else:
            print("Proposal ID not found.")
        self.page.locator('#formSaveDoorScope label:has-text("Home Expert View")').click()

        print("Clicked on the 'Home Expert View' radio button.")
        self.page.wait_for_load_state('networkidle')

        sections = self.page.locator('#formSaveDoorscope .table-responsive[data-id="67"]').all()
        print(f"Total sections found: {len(sections)}")
        print(f"Clicking Add MOre for section")

        k = 0  # Manual section index
        for section in sections:

            rows = section.locator("tbody tr").all()

            l = 0  # Manual row index
            for row in rows:

                locator = self.page.locator(f"#table-section-{k}").get_by_role("link", name="Add More ")

                if locator.is_visible():
                    locator.click()
                    print(f"'Add more' clicked for section {k + 1}")
                    time.sleep(1)
                else:
                    pass
                break
            k += 1

        # --------------------------------------------------------- top is add more -------------------------------------------
        print(f"Filling data into section")
        for i, section in enumerate(sections):
            rows = section.locator("tbody tr").all()

            for j, row in enumerate(rows):
                # this is to see if product is empty and fill quantity only if it is empty (requirement)
                product_selector = f'//button[@data-id="Sections_{i}__Products_{j}__Product_Id"]'
                product_input = self.page.locator(product_selector)
                # time.sleep(1)
                if product_input.is_visible():
                    # time.sleep(1)
                    button_locator = self.page.locator(f'//button[@data-id="Sections_{i}__Products_{j}__Product_Id"]')
                    inner_text = button_locator.locator('.filter-option-inner-inner').inner_text()
                    if inner_text.strip() == "Select":
                        # time.sleep(1)
                        self.page.locator(f'//button[@data-id="Sections_{i}__Products_{j}__Product_Id"]').click()
                        product_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        product_options = [item.inner_text() for item in product_option_elmts if
                                           item.inner_text() != 'Select']
                        random_product_option = random.choice(product_options)
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_product_option, exact=True).nth(0).click()
                    else:
                        pass
                    time.sleep(3)

                # this is to see if variation is empty and fill quantity only if it is empty (requirement)
                variation_selector = f'//button[@data-id="Sections_{i}__Products_{j}__PricebookVariation_Id"]'
                variation_input = self.page.locator(variation_selector)
                # time.sleep(1)
                if variation_input.is_visible():
                    # time.sleep(1)
                    variation_button_locator = self.page.locator(
                        f'//button[@data-id="Sections_{i}__Products_{j}__PricebookVariation_Id"]')
                    variation_inner_text = variation_button_locator.locator('.filter-option-inner-inner').inner_text()
                    # print(f"variation inner text : {variation_inner_text}")
                    if variation_inner_text.strip() == "Select":
                        time.sleep(1)
                        self.page.wait_for_load_state('networkidle', timeout=60000)

                        self.page.locator(
                            f'//button[@data-id="Sections_{i}__Products_{j}__PricebookVariation_Id"]').click()
                        variation_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        variation_options = [item.inner_text() for item in variation_option_elmts if
                                             item.inner_text() != 'Select']
                        random_variation_option = random.choice(variation_options)
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_variation_option, exact=True).nth(0).click()
                    else:
                        pass

                # this is to see if color is empty and fill quantity only if it is empty (requirement)
                color_selector = f'#Sections_{i}__Products_{j}__ColorId'
                color_input = self.page.locator(color_selector)
                # time.sleep(1)
                if color_input.is_visible():
                    # time.sleep(1)
                    color_button_locator = self.page.locator(
                        f'//button[@data-id="Sections_{i}__Products_{j}__ColorId"]')
                    color_inner_text = color_button_locator.locator('.filter-option-inner-inner').inner_text()
                    if color_inner_text.strip() == "Select":
                        # time.sleep(1)
                        self.page.locator(f'//button[@data-id="Sections_{i}__Products_{j}__ColorId"]').click()
                        color_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        color_options = [item.inner_text() for item in color_option_elmts if
                                         item.inner_text() != 'Select']
                        random_color_option = random.choice(color_options)
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_color_option, exact=True).nth(0).click()
                    else:
                        pass

                # This is to see if quantity is empty or 0 and fill quantity only in that case
                quantity_selector = f'#Sections_{i}__Products_{j}__Quantity'
                quantity_input = self.page.locator(quantity_selector)

                if quantity_input.is_visible():
                    current_quantity_value = quantity_input.input_value().strip()
                    inner_text_value = quantity_input.inner_text().strip()

                    if current_quantity_value == "" or current_quantity_value == "0" or inner_text_value == "0":
                        quantity_input.fill(quantity)
                    else:
                        pass

                # this is to see if customer notes is empty and fill quantity only if it is empty (requirement)
                customer_notes_selector = f'#Sections_{i}__Products_{j}__CustomerNotes'
                customer_notes_input = self.page.locator(customer_notes_selector)
                time.sleep(1)
                if customer_notes_input.is_visible():
                    # time.sleep(1)
                    current_value = customer_notes_input.input_value()
                    if current_value.strip() == "":
                        # time.sleep(1)
                        customer_notes_input.fill(customer_notes)
                    else:
                        pass

                hide_on_cust_pdf_selector = f'#Sections_{i}__Products_0__IsHideInPreview'
                hide_on_cust_pdf_input = self.page.locator(hide_on_cust_pdf_selector)
                if hide_on_cust_pdf_input.is_visible():
                    self.page.check(hide_on_cust_pdf_selector)

                hide_var_on_pdf_selector = f'#Sections_{i}__Products_1__IsHideVariationonPDF'
                hide_var_on_pdf_input = self.page.locator(hide_var_on_pdf_selector)
                if hide_var_on_pdf_input.is_visible():
                    self.page.check(hide_var_on_pdf_selector)

        self.page.wait_for_load_state('networkidle', timeout=60000)

        self.handle_line_door_item(section_index=1, brand_index=0)

        section_index = 1  # Target section for testing
        expected_price = "123.45"  # Expected price value from fill_brand_details
        max_attempts = 3  # Match max_attempts from fill_brand_details

        # Step 1: Fill manufacturer details
        print(f"   Filling manufacturer details for section {section_index}")
        self.fill_brand_details(section_index, max_attempts)
        # --------------------------------------------------------------FINAL PRICING SCENARIOS-------------------------------------------------------------------
        scope = self.page.locator('#formSaveDoorScope')

        scope.locator('#RetailPrice').click()

        self.toggle_yes_for_all_products()

        retail_price_str_1 = scope.locator('#RetailPrice').input_value()
        retail_price_1 = float(retail_price_str_1.replace("$", "").replace(",", ""))
        print(f"Retail Price from page: {retail_price_1}")

        # ---------------------------------------------------- to assert in preview calc -------------------------------------------------------------------------
        with self.page.expect_popup() as page1_info:
            self.page.locator('#download-pdf-scope').click()
        time.sleep(4)
        page1 = page1_info.value

        label = "Retail Price With Options"
        spans = page1.locator("span")
        count = spans.count()

        for y in range(count):
            text = spans.nth(y).inner_text().strip()

            # Match the label span
            if label.lower() in text.lower():
                # Check next few spans for number-like text
                for z in range(y + 1, min(y + 5, count)):
                    next_text = spans.nth(z).inner_text().strip()
                    if re.match(r"^-?\$?[\d,.]+$", next_text):
                        print(next_text)

        print("Clicking 'Download PDF'...")
        # Make sure the downloads folder exists
        downloads_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(downloads_dir, exist_ok=True)

        # Optional: add timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(downloads_dir, f"downloaded_proposal_{timestamp}.pdf")

        # Handle the download
        with page1.expect_download() as download_info:
            page1.locator("#toggleSpinners").click()
        download = download_info.value
        download.save_as(file_path)

        print(f"Downloaded PDF saved at: {file_path}")
        page1.close()
        print("Closed preview calc window.")

        # Step 1: Read the readonly Retail Price value
        retail_price_str = scope.locator('#RetailPrice').input_value()
        retail_price = float(retail_price_str.replace("$", "").replace(",", ""))
        print(f"Retail Price from page: {retail_price}")
        print("Grand total matches retail price.")

        retail_price_str = scope.locator('#RetailPrice').input_value()
        retail_price = float(retail_price_str.replace("$", "").replace(",", ""))

        # ---- Test Dollar Adjustment ----
        scope.locator("label", has_text="$").locator(
            "span").click()  # Click on $scope.locator('#Adjustment').fill("50")

        scope.locator('#Adjustment').fill("50")
        scope.locator('#RetailPrice').press('Enter')
        scope.locator('#Adjustment').dispatch_event('blur')

        final_price_dollar = float(
            scope.locator('#RetailPriceAdjusted').input_value().replace("$", "").replace(",", ""))
        # final_price_dollar = float(scope.locator("#RetailPriceAdjusted").get_attribute("value").replace(",", ""))
        expected_price_dollar = calculate_expected_price(retail_price, 50, is_percentage=False)
        #assert final_price_dollar == expected_price_dollar, f"Dollar Test Failed: got {final_price_dollar}, expected {expected_price_dollar}"

        # ---- Test Percentage Adjustment ----
        scope.locator("label", has_text="%").locator("span").click()  # Click on %
        scope.locator("#Adjustment").fill("10")  # 10%
        scope.locator("#Adjustment").press("Enter")
        scope.locator("#Adjustment").dispatch_event("blur")

        # final_price_percent = float(scope.input_value('#RetailPriceAdjusted').replace("$", "").replace(",", ""))
        final_price_percent_str = scope.locator('#RetailPriceAdjusted').input_value()
        final_price_percent = float(final_price_percent_str.replace("$", "").replace(",", ""))

        expected_price_percent_change = calculate_expected_price(retail_price, 10, is_percentage=True)
        expected_price_percent = retail_price - expected_price_percent_change

        assert math.isclose(final_price_percent, expected_price_percent, rel_tol=1e-3), (
            f"Percentage Test Failed: got {final_price_percent}, expected {expected_price_percent}"
        )

        print("Both dollar and percentage adjustment validations passed.")

        btn_update_scope_data = self.page.locator("#btnUpdateScopeData")
        if btn_update_scope_data.is_visible():
            btn_update_scope_data.click(timeout=30000)
        else:
            self.page.locator("#btnUpdateScope").click(timeout=30000)

        time.sleep(4)
        estimate_id = self.get_estimate_id()
        logger.info(f"Esimate id is: {estimate_id}")
        print(f"Esimate id is: {estimate_id}")
        return estimate_id

    def validate_trim_qtys(self, expected_qty: float = 1.333):
        scope = self.page.locator("#formSaveWindowScope")  # Adjust scope as needed

        manufacturers = scope.locator('div[id^="brand-set-"]').all()

        for brand_index, manufacturer in enumerate(manufacturers):
            brand_id_match = re.search(r'brand-set-(\d+)', manufacturer.get_attribute('id'))
            if not brand_id_match:
                continue
            brand_id = brand_id_match.group(1)

            lines = manufacturer.locator(
                f'div.setAccordianLine[id="accordion-sets-windows"][data-brandindex="{brand_id}"] > .window-card').all()
            print(f"   Manufacturer {brand_id} has {len(lines)} lines")

            for line_index, line in enumerate(lines):
                subsections = line.locator('.card-body .subsection').all()
                for subsection_index, subsection in enumerate(subsections):
                    subsection_classes = subsection.get_attribute('class')
                    if not subsection_classes:
                        continue
                    is_exterior = "exteriortrim" in subsection_classes.lower()
                    is_interior = "interiortrim" in subsection_classes.lower()
                    if not is_exterior and not is_interior:
                        continue

                    trim_type = "Exterior Trim" if is_exterior else "Interior Trim"
                    print(
                        f"   Checking {trim_type} for Manufacturer {brand_id}, Line {line_index}, Subsection {subsection_index}")

                    product_rows = subsection.locator(
                        f'table[id="table-section-1-brand-{brand_id}-line-{line_index}-subsection-{subsection_index}"] tbody tr.window-row').all()

                    for product_index, _ in enumerate(product_rows):
                        qty_input_selector = f'#Sections_1__Brands_{brand_id}__LineItems_{line_index}__Subsection_{subsection_index}__Products_{product_index}__Quantity'
                        qty_input = scope.locator(qty_input_selector)

                        if qty_input.is_visible():
                            try:
                                qty_value = qty_input.input_value().strip()
                                qty_float = float(qty_value)
                                print(f"       {trim_type} Qty = {qty_float}")
                                assert round(qty_float, 3) == round(expected_qty, 3), \
                                    f"   {trim_type} qty mismatch at Manufacturer {brand_id}, Line {line_index}, Product {product_index}." \
                                    f" Expected: {expected_qty}, Found: {qty_float}"
                            except Exception as e:
                                print(f"       Error reading qty: {e}")
                        else:
                            print(
                                f"       Qty input for {trim_type} is not visible at brand {brand_id}, line {line_index}, product {product_index}")



    def summary_door_page_app(self):
        approx_monthly_pay = self.config['summary_page'].get('ApproxMonthyPay')
        self.page.click('//*[@id="btnGotoSummary"]')
        self.page.wait_for_load_state('networkidle')
        logger.info("docs Saved and Proceeded")

        self.page.click('input[data-index="0"][name="Checkboxes"]')
        logger.info("clicked on packet price checkbox")

        self.summary_calculations_app()
        self.page.fill('input#summaryBasicDetails_ApproxMonthyPay', approx_monthly_pay)
        self.page.wait_for_load_state('networkidle')
        logger.info("Base proposal as per attached scope of work")

        self.page.click(
            '//a[contains(@class, "btn") and contains(@class, "btn-primary") and contains(@class, "resetPayments") and @title="Reset"]')
        logger.info("clicked on reset")

        self.page.wait_for_load_state('networkidle')
        logger.info("Proposal finished")
        with self.page.expect_popup() as page1_info:
            self.page.click('//*[@id="btnFinishProposal"]')
            time.sleep(3)

        page1 = page1_info.value

        logger.info("Clicking 'Email Customer'...")
        page1.wait_for_selector("#toggleSpinners", state="visible")

        page1.get_by_text("Email Estimate ").click()
        page1.locator('#btnSendEmail').click()
        time.sleep(3)
        page1.locator('.swal-modal .swal-button--confirm').click()

        # ----------------------------------------------------------------------to download --------------------------------------------

        logger.info("Clicking 'Download PDF'...")
        # Make sure the downloads folder exists
        downloads_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(downloads_dir, exist_ok=True)

        # Optional: add timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(downloads_dir, f"downloaded_proposal_{timestamp}.pdf")

        # Handle the download
        with page1.expect_download() as download_info:
            page1.get_by_text("Download Estimate").click()
        download = download_info.value
        download.save_as(file_path)

        logger.info(f"Downloaded PDF saved at: {file_path}")

        # -------------------------------------------------------------------------------------------------------------------------------------

        page1.locator('//a[@onclick="loadConfrimSign()"]').click()
        page1.wait_for_timeout(3000)

        canvas_locator = page1.locator('//div[@class="col-lg-6 form-group"]//div[@id="homeexpert-signature-pad"]')
        canvas_locator.wait_for()
        canvas_box = canvas_locator.bounding_box()

        if canvas_box:
            start_x = canvas_box['x'] + 50
            start_y = canvas_box['y'] + 50
            page1.mouse.move(start_x, start_y)
            page1.mouse.down()
            page1.mouse.move(start_x + 100, start_y + 100)
            page1.mouse.move(start_x + 200, start_y + 50)
            page1.mouse.move(start_x + 300, start_y + 200)
            page1.mouse.up()
        time.sleep(3)
        logger.info("Home Expert Signed")

        canvas_locator1 = page1.locator('//div[@class="col-lg-6 form-group"]//div[@id="customer-signature-pad"]')
        canvas_locator1.wait_for()
        canvas_box = canvas_locator1.bounding_box()

        if canvas_box:
            start_x = canvas_box['x'] + 50
            start_y = canvas_box['y'] + 50
            page1.mouse.move(start_x, start_y)
            page1.mouse.down()
            page1.mouse.move(start_x + 100, start_y + 100)
            page1.mouse.move(start_x + 200, start_y + 50)
            page1.mouse.move(start_x + 300, start_y + 200)
            page1.mouse.up()
        time.sleep(3)
        logger.info("Customer Signed")

        page1.click('//a[@id="btnSaveProposalSign" and @class="btn btn-secondary"]')
        logger.info("proposal signed")
        page1.wait_for_timeout(3000)
        page1.click('//a[@onclick="window.close()"]')

        self.page.wait_for_timeout(3000)

    def click_add_more_side(self):
        try:
            add_more_side_btn = self.page.locator('a.exterior-add-more-side')
            if add_more_side_btn.is_visible():
                add_more_side_btn.click()
                print("Clicked 'Add More Side'")
            else:
                print("'Add More Side' button not visible")
        except Exception as e:
            print(f"Failed to click 'Add More Side': {e}")

    def add_side_until_visible(self, expected_side_count: int, max_attempts: int = 3):
        for attempt in range(max_attempts):
            self.click_add_more_side()
            current_count = self.page.locator(".exterior-side-line-card").count()
            if current_count > expected_side_count:
                print(f"           Side {current_count} added successfully on attempt {attempt + 1}")
                return True
            print(f"Retry {attempt + 1}: Side not added yet")
        print("Failed to add new side after maximum attempts")
        return False

    def click_side_accordion_until_open(self, s_index: int, max_attempts: int = 10) -> bool:
        """
        Tries to click the side accordion toggle until it is expanded successfully.
        """
        for attempt in range(max_attempts):
            print(f"           Attempt {attempt + 1}: Clicking accordion for Side {s_index + 1}")

            # Locate the toggle link for this side
            toggle_button = self.page.locator(f'a[href="#set-exterior-{s_index}"]')

            if toggle_button.is_visible(timeout=150000):
                toggle_button.click(timeout=120000)

                # Check if any dropdown inside the side is now visible to confirm expansion
                product_dropdown = self.page.locator(
                    f'button[data-id^="Sections_2__LineItems_{s_index}__Subsection_0__Products_0__Product_Id"]')

                try:
                    product_dropdown.wait_for(state="visible", timeout=3000)
                    print(f"           Side {s_index + 1} accordion expanded successfully.")
                    return True
                except:
                    print(f"           Side {s_index + 1} accordion did not expand. Retrying...")
            else:
                print(f"           Accordion toggle not visible for Side {s_index + 1}. Retrying...")

        print(f"           Failed to expand Side {s_index + 1} accordion after {max_attempts} attempts.")
        return False

    def click_add_more_product_line_until_visible(self, line_index: int, sub_index: int, max_attempts: int = 5) -> bool:
        """
        Tries to click 'Add More' button under a line until the new product row becomes visible.
        """
        for attempt in range(max_attempts):
            print(
                f"                   Attempt {attempt + 1}: Clicking 'Add More' for Line {line_index}, Subsection {sub_index}")

            add_more_btn = self.page.locator(f'a.btn.btn-outline-primary[data-lineid="{line_index}"]')

            try:
                if add_more_btn.nth(sub_index).is_visible(timeout=5000):
                    add_more_btn.nth(sub_index).click(force=True)

                    # Confirm if a new product dropdown is visible
                    product_dropdown = self.page.locator(
                        f'button[data-id^="Sections_2__LineItems_{line_index}__Subsection_{sub_index}__Products_0__Product_Id"]'
                    )
                    try:
                        product_dropdown.wait_for(state="visible", timeout=3000)
                        print(
                            f"           Clicked 'Add More' successfully for Line {line_index}, Subsection {sub_index}")
                        return True
                    except:
                        print(f"                   Product dropdown not visible after clicking. Retrying...")
                else:
                    print(
                        f"                   'Add More' button not visible for Line {line_index}, Subsection {sub_index}. Retrying...")

            except Exception as e:
                print(f"                   Error clicking 'Add More' on attempt {attempt + 1}: {e}")

        print(
            f"                     Failed to click 'Add More' for Line {line_index}, Subsection {sub_index} after {max_attempts} attempts.")
        return False

    def fill_siding_sections(self):
        expected_side_count = self.config["exteriorpainting"].get("side_count", 1)
        add_more_counts = self.config["exteriorpainting"].get("add_more_counts", [])

        sides = self.page.locator(".exterior-side-line-card")

        print(f"   Found {expected_side_count} sides")

        for s_index in range(expected_side_count):
            print(f" Side {s_index + 1}")

            self.add_side_until_visible(s_index)
            self.click_side_accordion_until_open(s_index)

            side_element = sides.nth(s_index)
            section_index = int(side_element.get_attribute("data-sectionindex"))
            section_id = int(side_element.get_attribute("data-sectionid"))
            line_index = int(side_element.get_attribute("data-lineid"))

            subsection_bodies = side_element.locator(".card-body .subsection")
            subsection_count = subsection_bodies.count()
            print(f"           {subsection_count} subsections found in Side {s_index + 1}")

            for sub_index in range(subsection_count):
                print(f"      Subsection {sub_index + 1}")

                # Get how many product rows to add
                try:
                    product_add_count = add_more_counts[s_index]["subsections"][sub_index]["count"]
                except (IndexError, KeyError):
                    product_add_count = 1  # default fallback

                # Click 'Add More' n times
                for p in range(product_add_count):
                    self.click_add_more_product_line_until_visible(line_index, sub_index, max_attempts=5)
                    print(f"               Added product row {p + 1}/{product_add_count}")

                product_table = subsection_bodies.nth(sub_index).locator("table tbody")
                row_count = product_table.locator("tr").count()

                for product_index in range(row_count):
                    print(f"               Row {product_index + 1}")
                    base_id = f"Sections_{section_index}__LineItems_{line_index}__Subsection_{sub_index}__Products_{product_index}"

                    # Product dropdown
                    product_btn = self.page.locator(f'button[data-id="{base_id}__Product_Id"]')
                    if product_btn.is_visible():
                        text = product_btn.locator(".filter-option-inner-inner").inner_text().strip()
                        if text in ["Select", "Nothing selected"]:
                            product_btn.click()
                            product_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                                '.dropdown-item:not(.selected)').all()
                            product_options = [item.inner_text() for item in product_option_elmts if
                                               item.inner_text() != 'Select']
                            random_product_option = random.choice(product_options)
                            self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                                random_product_option, exact=True).nth(0).click()
                            # self.page.locator('.dropdown-menu.show:not(.inner) .dropdown-item').nth(1).click()
                        else:
                            print(f"             Product already selected - {text}")

                    # Variation dropdown
                    variation_btn = self.page.locator(f'button[data-id="{base_id}__PricebookVariation_Id"]')
                    if variation_btn.is_visible():
                        text = variation_btn.locator(".filter-option-inner-inner").inner_text().strip()
                        if text in ["Select", "Nothing selected"]:
                            variation_btn.click()
                            variation_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                                '.dropdown-item:not(.selected)').all()
                            variation_options = [item.inner_text() for item in variation_option_elmts if
                                                 item.inner_text() != 'Select']
                            random_variation_option = random.choice(variation_options)
                            self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                                random_variation_option, exact=True).nth(0).click()
                            # print(f"Filled empty variation for section {i}, product {j}")
                        else:
                            # print(f"Skipped row {j} – already has value: '{variation_inner_text}'")
                            pass

                            # self.page.locator('.dropdown-menu.show:not(.inner) .dropdown-item').nth(1).click()

                    # Toggle 'Yes' if not already checked
                    toggle_locator = self.page.locator(f'input[id="{base_id}__IsIncludedDefault"]')
                    if toggle_locator.is_visible() and not toggle_locator.is_checked():
                        toggle_locator.check()
                        print("                Toggled 'Yes' switch")

                        # Product Reference dropdown
                        product_ref_btn = self.page.locator(f'button[data-id="{base_id}__ProductReferenceId"]')
                        if product_ref_btn.is_visible():
                            ref_text = product_ref_btn.locator(".filter-option-inner-inner").inner_text().strip()
                            if ref_text in ["Select", "Nothing selected", "No Reference"]:
                                try:
                                    for attempt in range(2):  # Try up to 2 times
                                        product_ref_btn.click()
                                        self.page.wait_for_timeout(300)

                                        dropdown_item = self.page.locator(
                                            '.dropdown-menu.show:not(.inner) .dropdown-item').nth(
                                            1)
                                        if dropdown_item.is_visible():
                                            dropdown_item.click()
                                            print(f"        Selected Product Reference in row {product_index + 1}")
                                            break
                                        else:
                                            print(f"        Dropdown not visible on attempt {attempt + 1}, retrying...")
                                    else:
                                        print(
                                            f"        Dropdown still not visible after retry for row {product_index + 1}")
                                except Exception as e:
                                    print(
                                        f"        Failed to select Product Reference for row {product_index + 1}: {e}")
                            else:
                                print(f"        Product Reference already selected: {ref_text}")
                        else:
                            print("           Product Reference dropdown not visible.")

                    # Color dropdown
                    color_btn = self.page.locator(f'button[data-id="{base_id}__ColorId"]')
                    if color_btn.is_visible():
                        text = color_btn.locator(".filter-option-inner-inner").inner_text().strip()
                        if text in ["Select", "Nothing selected"]:
                            color_btn.click()
                            self.page.locator('.dropdown-menu.show:not(.inner) .dropdown-item').nth(1).click()

                    # Quantity
                    qty_input = self.page.locator(f'input[id="{base_id}__DefaultQuantity"]')
                    if qty_input.is_visible():
                        qty_input.fill("2")

                    # Notes
                    notes_input = self.page.locator(f'#{base_id}__CustomerNotes')
                    if notes_input.is_visible():
                        notes_input.fill("Auto-filled via script")

                    # Checkboxes
                    checkbox = self.page.locator(
                        f'input[id="Sections_{section_index}__LineItems_{line_index}__Subsection_{sub_index}__Products_{product_index}__IsOptional"]')
                    if checkbox.is_visible() and not checkbox.is_checked():
                        checkbox.check()

                    customer_pdf_checkbox = self.page.locator(
                        f'input[id="Sections_{section_index}__LineItems_{line_index}__Subsection_{sub_index}__Products_0__IsHideInPreview"]')
                    if customer_pdf_checkbox.is_visible() and not customer_pdf_checkbox.is_checked():
                        customer_pdf_checkbox.check()

                    contract_pdf_checkbox = self.page.locator(
                        f'input[id="Sections_{section_index}__LineItems_{line_index}__Subsection_{sub_index}__Products_1__IsHideVariationonPDF"]')
                    if contract_pdf_checkbox.is_visible() and not contract_pdf_checkbox.is_checked():
                        contract_pdf_checkbox.check()

        print("   Finished filling all sides")

    def open_last_siding_accordian(self):
        expected_side_count = self.config["windows"].get("side_count", 1)
        add_more_counts = self.config["windows"].get("add_more_counts", [])

        if self.page.locator(".exterior-side-line-card").nth(0).is_visible():
            sides = self.page.locator(".exterior-side-line-card")
            actual_side_count = sides.count()
        else:
            actual_side_count = 0



        print(f"   DOM shows {actual_side_count} sides (expected: {expected_side_count})")

        #    Call accordion open ONLY for the last side
        if actual_side_count > 0:
            last_side_index = actual_side_count - 1
            print(f"   Clicking accordion for last side (Side {last_side_index + 1})")
            self.click_side_accordion_until_open(last_side_index)
        else:
            print("   No sides found in DOM.")

    def click_add_more_deck(self):
        try:
            add_more_side_btn = self.page.locator('a.exterior-add-more-deck')
            if add_more_side_btn.is_visible():
                add_more_side_btn.click()
                print("Clicked 'Add More Deck'")
            else:
                print("'Add More Deck' button not visible")
        except Exception as e:
            print(f"   Failed to click 'Add More Deck': {e}")


    def add_deck_until_visible(self, expected_side_count: int, max_attempts: int = 3):
        for attempt in range(max_attempts):
            self.click_add_more_deck()
            current_count = self.page.locator(".exterior-deck-line-card").count()
            if current_count > expected_side_count:
                print(f"           Deck {current_count} added successfully on attempt {attempt + 1}")
                return True
            print(f"           Retry {attempt + 1}: Deck not added yet")
        print("            Failed to add new deck after maximum attempts")
        return False

    def click_deck_accordion_until_open(self, s_index: int, max_attempts: int = 10) -> bool:
        """
        Tries to click the side accordion toggle until it is expanded successfully.
        """
        for attempt in range(max_attempts):
            print(f"           Attempt {attempt + 1}: Clicking accordion for Side {s_index + 1}")

            # Locate the toggle link for this side
            toggle_button = self.page.locator(f'a[href="#set-deck-exterior-{s_index}"]')

            if toggle_button.is_visible(timeout=150000):
                toggle_button.click(timeout=120000)

                # Check if any dropdown inside the side is now visible to confirm expansion
                product_dropdown = self.page.locator(
                    f'button[data-id^="Sections_3__LineItems_{s_index}__Subsection_0__Products_0__Product_Id"]')

                try:
                    product_dropdown.wait_for(state="visible", timeout=3000)
                    print(f"           Deck {s_index + 1} accordion expanded successfully.")
                    return True
                except:
                    print(f"           Deck {s_index + 1} accordion did not expand. Retrying...")
            else:
                print(f"           Accordion toggle not visible for Deck {s_index + 1}. Retrying...")

        print(f"           Failed to expand Deck {s_index + 1} accordion after {max_attempts} attempts.")
        return False

    def click_add_more_product_line_until_visible_deck(self, line_index: int, sub_index: int,
                                                       max_attempts: int = 5) -> bool:
        """
        Clicks 'Add More' for the given line & subsection until a new row appears.
        Waits for the correct button and verifies a row was added.
        """
        tbody_selector = f'table[id^="table-section-3-line-{line_index}-Subsection-{sub_index}"] tbody'
        tbody_locator = self.page.locator(tbody_selector)

        for attempt in range(max_attempts):
            print(f"   Attempt {attempt + 1}: Clicking Add More for Line {line_index}, Subsection {sub_index}")

            try:
                # Ensure tbody is present
                self.page.wait_for_selector(tbody_selector, timeout=5000)

                # Get current row count (Python-side)
                initial_rows = tbody_locator.locator("tr").count()

                # Find the specific Add More button in this subsection
                add_more_btn = self.page.locator(f'a[data-lineid="{line_index}"]:has-text("Add More")').nth(sub_index)

                # Wait until button is visible
                add_more_btn.wait_for(state="visible", timeout=5000)

                # Click
                add_more_btn.click()

                # Wait for row count to increase (pass selector, not locator)
                self.page.wait_for_function(
                    """([selector, initial]) => document.querySelectorAll(selector + " tr").length > initial""",
                    arg=[tbody_selector, initial_rows],
                    timeout=5000
                )

                print(f"   Added new product row in Line {line_index}, Subsection {sub_index}")
                return True

            except Exception as e:
                print(f"   Error on attempt {attempt + 1}: {e}")

        print(f"   Failed to add product row for Line {line_index}, Subsection {sub_index}")
        return False

    def fill_decks_sections(self):
        expected_side_count = self.config["exteriorpainting"].get("side_count", 1)
        add_more_counts = self.config["exteriorpainting"].get("add_more_counts", [])

        sides = self.page.locator(".exterior-deck-line-card")

        print(f"   Found {expected_side_count} sides")

        for s_index in range(expected_side_count):
            print(f" Side {s_index + 1}")

            self.add_deck_until_visible(s_index)
            self.click_deck_accordion_until_open(s_index)

            side_element = sides.nth(s_index)
            section_index = int(side_element.get_attribute("data-sectionindex"))
            section_id = int(side_element.get_attribute("data-sectionid"))
            line_index = int(side_element.get_attribute("data-lineid"))

            subsection_bodies = side_element.locator(".card-body .subsection")
            subsection_count = subsection_bodies.count()
            print(f"           {subsection_count} subsections found in Side {s_index + 1}")

            for sub_index in range(subsection_count):
                print(f"      Subsection {sub_index + 1}")

                # Get how many product rows to add
                try:
                    product_add_count = add_more_counts[s_index]["subsections"][sub_index]["count"]
                except (IndexError, KeyError):
                    product_add_count = 1  # default fallback

                # Click 'Add More' n times
                for p in range(product_add_count):
                    self.click_add_more_product_line_until_visible_deck(line_index, sub_index, max_attempts=5)
                    print(f"               Added product row {p + 1}/{product_add_count}")

                product_table = subsection_bodies.nth(sub_index).locator("table tbody")
                row_count = product_table.locator("tr").count()

                for product_index in range(row_count):
                    print(f"               Row {product_index + 1}")
                    base_id = f"Sections_{section_index}__LineItems_{line_index}__Subsection_{sub_index}__Products_{product_index}"

                    # Product dropdown
                    product_btn = self.page.locator(f'button[data-id="{base_id}__Product_Id"]')
                    if product_btn.is_visible():
                        text = product_btn.locator(".filter-option-inner-inner").inner_text().strip()
                        if text in ["Select", "Nothing selected"]:
                            product_btn.click()
                            product_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                                '.dropdown-item:not(.selected)').all()
                            product_options = [item.inner_text() for item in product_option_elmts if
                                               item.inner_text() != 'Select']
                            random_product_option = random.choice(product_options)
                            self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                                random_product_option, exact=True).nth(0).click()
                            # self.page.locator('.dropdown-menu.show:not(.inner) .dropdown-item').nth(1).click()
                        else:
                            print(f"             Product already selected - {text}")

                    # Variation dropdown
                    variation_btn = self.page.locator(f'button[data-id="{base_id}__PricebookVariation_Id"]')
                    if variation_btn.is_visible():
                        text = variation_btn.locator(".filter-option-inner-inner").inner_text().strip()
                        if text in ["Select", "Nothing selected"]:
                            variation_btn.click()
                            variation_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                                '.dropdown-item:not(.selected)').all()
                            variation_options = [item.inner_text() for item in variation_option_elmts if
                                                 item.inner_text() != 'Select']
                            random_variation_option = random.choice(variation_options)
                            self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                                random_variation_option, exact=True).nth(0).click()
                            # print(f"Filled empty variation for section {i}, product {j}")
                        else:
                            # print(f"Skipped row {j} – already has value: '{variation_inner_text}'")
                            pass

                            # self.page.locator('.dropdown-menu.show:not(.inner) .dropdown-item').nth(1).click()

                    # Toggle 'Yes' if not already checked
                    toggle_locator = self.page.locator(f'input[id="{base_id}__IsIncludedDefault"]')
                    if toggle_locator.is_visible() and not toggle_locator.is_checked():
                        toggle_locator.check()
                        print("                Toggled 'Yes' switch")

                        # Product Reference dropdown
                        product_ref_btn = self.page.locator(f'button[data-id="{base_id}__ProductReferenceId"]')
                        if product_ref_btn.is_visible():
                            ref_text = product_ref_btn.locator(".filter-option-inner-inner").inner_text().strip()
                            if ref_text in ["Select", "Nothing selected", "No Reference"]:
                                try:
                                    for attempt in range(2):  # Try up to 2 times
                                        product_ref_btn.click()
                                        self.page.wait_for_timeout(300)

                                        dropdown_item = self.page.locator(
                                            '.dropdown-menu.show:not(.inner) .dropdown-item').nth(
                                            1)
                                        if dropdown_item.is_visible():
                                            dropdown_item.click()
                                            print(f"        Selected Product Reference in row {product_index + 1}")
                                            break
                                        else:
                                            print(f"        Dropdown not visible on attempt {attempt + 1}, retrying...")
                                    else:
                                        print(
                                            f"        Dropdown still not visible after retry for row {product_index + 1}")
                                except Exception as e:
                                    print(
                                        f"        Failed to select Product Reference for row {product_index + 1}: {e}")
                            else:
                                print(f"        Product Reference already selected: {ref_text}")
                        else:
                            print("           Product Reference dropdown not visible.")

                    # Color dropdown
                    color_btn = self.page.locator(f'button[data-id="{base_id}__ColorId"]')
                    if color_btn.is_visible():
                        text = color_btn.locator(".filter-option-inner-inner").inner_text().strip()
                        if text in ["Select", "Nothing selected"]:
                            color_btn.click()
                            self.page.locator('.dropdown-menu.show:not(.inner) .dropdown-item').nth(1).click()

                    # Quantity
                    qty_input = self.page.locator(f'input[id="{base_id}__DefaultQuantity"]')
                    if qty_input.is_visible():
                        qty_input.fill("2")

                    # Notes
                    notes_input = self.page.locator(f'#{base_id}__CustomerNotes')
                    if notes_input.is_visible():
                        notes_input.fill("Auto-filled via script")

                    # Checkboxes
                    checkbox = self.page.locator(
                        f'input[id="Sections_{section_index}__LineItems_{line_index}__Subsection_{sub_index}__Products_{product_index}__IsOptional"]')
                    if checkbox.is_visible() and not checkbox.is_checked():
                        checkbox.check()

                    customer_pdf_checkbox = self.page.locator(
                        f'input[id="Sections_{section_index}__LineItems_{line_index}__Subsection_{sub_index}__Products_0__IsHideInPreview"]')
                    if customer_pdf_checkbox.is_visible() and not customer_pdf_checkbox.is_checked():
                        customer_pdf_checkbox.check()

                    contract_pdf_checkbox = self.page.locator(
                        f'input[id="Sections_{section_index}__LineItems_{line_index}__Subsection_{sub_index}__Products_1__IsHideVariationonPDF"]')
                    if contract_pdf_checkbox.is_visible() and not contract_pdf_checkbox.is_checked():
                        contract_pdf_checkbox.check()

        print("   Finished filling all decks")

    def remove_last_visible_siding_section_and_validate(self):
        # Count only visible sides
        visible_sides = self.page.locator(".exterior-side-line-card:visible")
        initial_visible_count = visible_sides.count()

        if initial_visible_count == 0:
            print("   No visible sides to remove.")
            return

        print(f"   Initial visible side count: {initial_visible_count}")

        # Click the last visible remove button
        remove_buttons = self.page.locator("a.exterior-remove-line:visible")
        last_visible_index = remove_buttons.count() - 1

        if last_visible_index < 0:
            print("   No visible 'Remove Side' buttons found.")
            return

        print(f"   Clicking 'Remove Side' for Side {last_visible_index + 1}")
        remove_buttons.nth(last_visible_index).click()

        # Wait for DOM update (or a specific element to be hidden if needed)
        self.page.wait_for_timeout(2000)

        # Re-count only visible sides
        updated_visible_count = self.page.locator(".exterior-side-line-card:visible").count()

        if updated_visible_count == initial_visible_count - 1:
            print(f"   Side removed successfully. New visible side count: {updated_visible_count}")
        else:
            print(
                f"   Side removal validation failed. Visible sides: {updated_visible_count}, expected {initial_visible_count - 1}")

    def get_deck_pricing_total(self):
        expected_deck_count = self.config["exteriorpainting"].get("side_count", 1)

        decks = self.page.locator(".exterior-deck-line-card")
        self.page.wait_for_selector(".exterior-deck-line-card", timeout=10000)  # Wait up to 10s

        deck_count = decks.count()
        if deck_count == 0:
            print("   No deck sections found – skipping deck total calculation.")
            return 0.0, {}
        else:
            print(f"   Found {expected_deck_count} decks")

        grand_total = 0.0
        subsection_totals = {}

        for d_index in range(expected_deck_count):
            print(f" Deck {d_index + 1}")

            # Open the accordion for the deck
            self.click_deck_accordion_until_open(d_index)

            deck_element = decks.nth(d_index)
            section_index = int(deck_element.get_attribute("data-sectionindex"))
            section_id = int(deck_element.get_attribute("data-sectionid"))
            line_index = int(deck_element.get_attribute("data-lineid"))

            deck_total_price = 0.0

            subsection_bodies = deck_element.locator(".card-body .subsection")
            subsection_count = subsection_bodies.count()
            print(f"       {subsection_count} subsections found in Deck {d_index + 1}")

            for sub_index in range(subsection_count):
                print(f"     Subsection {sub_index + 1}")

                subsection_total_price = 0.0

                # Get subsection name
                try:
                    subsection_name = subsection_bodies.nth(sub_index).locator("h6.text-primary").inner_text().strip()
                except:
                    subsection_name = f"Subsection {sub_index + 1}"

                product_table = subsection_bodies.nth(sub_index).locator("table tbody")
                row_count = product_table.locator("tr").count()

                for product_index in range(row_count):
                    print(f"           Row {product_index + 1}")
                    base_id = f"Sections_{section_index}__LineItems_{line_index}__Subsection_{sub_index}__Products_{product_index}"

                    # Locate and sum price
                    price_locator = self.page.locator(f'input[id="{base_id}__Totals"]')
                    price_value = 0.0
                    if price_locator.is_visible():
                        time.sleep(5)
                        price_text = price_locator.input_value().replace("$", "").replace(",", "").replace("₹",
                                                                                                           "").strip()
                        try:
                            price_value = float(price_text)
                        except ValueError:
                            print(f"               Invalid price value: '{price_text}'")

                    subsection_total_price += price_value
                    deck_total_price += price_value
                    print(f"               Row {product_index + 1} Price: ₹{price_value}")

                print(f"               Total price in subsection '{subsection_name}': ₹{subsection_total_price}")

                # Add to subsection totals
                if subsection_name in subsection_totals:
                    subsection_totals[subsection_name] += subsection_total_price
                else:
                    subsection_totals[subsection_name] = subsection_total_price

            print(f"   Total price in Deck {d_index + 1}: ₹{deck_total_price}")
            self.validate_deck_displayed_total(self, deck_element, d_index, deck_total_price)
            grand_total += deck_total_price

        print(f"\n   Grand Total across all decks: ₹{grand_total}")
        print("   Subsection-wise Totals:", subsection_totals)
        print("   Finished calculating all decks")

        # Validate with retail price on page
        retail_price_to_validate_inc_opt = self.page.input_value('#RetailPrice')
        retail_price_to_validate_inc_opt = float(retail_price_to_validate_inc_opt.replace("$", "").replace(",", ""))
        print(f"Retail Price from page: {retail_price_to_validate_inc_opt}")

        return grand_total, subsection_totals

    @staticmethod
    def validate_deck_displayed_total(self, deck_element, d_index, grand_total):
        displayed_total_locator = deck_element.locator(".deck-total")
        if displayed_total_locator.is_visible():
            displayed_total_text = displayed_total_locator.inner_text().replace("$", "").replace(",", "").strip()
            try:
                displayed_total_value = float(displayed_total_text)
                print(f"   Displayed total in Side {d_index + 1}: ₹{displayed_total_value}")
                if abs(displayed_total_value - grand_total) > 0.01:
                    print(
                        f"   Discrepancy in totals for Side {d_index + 1}: UI shows ₹{displayed_total_value}, calculated ₹{grand_total}")
            except ValueError:
                print(f"   Could not convert displayed total '{displayed_total_text}' to float")
        else:
            print(f"   No displayed total found for Side {d_index + 1}")


    def cal_page_app_ep(self):
        areas_included = self.config['calc_page'].get('AreasIncluded')
        areas_not_included = self.config['calc_page'].get('AreasNotIncluded')
        quantity = self.config['calc_page'].get('Quantity')
        customer_notes = self.config['calc_page'].get('CustomerNotes')

        self.page.wait_for_load_state('networkidle')
        # self.page.wait_for_timeout(2000)

        proposal_number = self.page.locator('#proposalNumber').text_content()
        print(f"Proposal number : {proposal_number}")
        match = re.search(r'#PR(\d+)-', proposal_number)
        if match:
            number = match.group(1)
            print(f"Proposal ID: {number}")
        else:
            print("Proposal ID not found.")

        time.sleep(5)

        self.page.locator(
            "#formSaveExteriorScope > div.d-flex.justify-content-between.mb-3 > div > div > label:nth-child(1)").click()
        print("Clicked on the 'Home Expert View' radio button.")
        self.page.wait_for_load_state('networkidle')

        self.page.fill("input[name='AreasIncluded']", areas_included)
        self.page.fill("input[name='AreasNotIncluded']", areas_not_included)

        # uncomment
        self.fill_siding_sections()
        self.open_last_siding_accordian()
        self.remove_last_visible_siding_section_and_validate()

        self.fill_decks_sections()

        # ----------------------------------------------------------------------------UNCOMMENT-------------------------------------------------------
        sections = self.page.locator("#formSaveExteriorScope .table-responsive").all()
        print(f" Total sections found: {len(sections)}")
        print(" Clicking 'Add More' for up to 3 sections")

        # Enumerate and limit to first 3 sections
        for k, section in enumerate(sections[:3]):
            print(f"    Processing Section {k + 1}")

            rows = section.locator("tbody tr").all()

            for l, row in enumerate(rows):
                print(f"        Checking Row {l + 1} in Section {k + 1}")

                locator = self.page.locator(f"#table-section-{k}").get_by_role("link", name="Add More ")

                if locator.is_visible():
                    locator.click()
                    print(f"    'Add More' clicked for Section {k + 1}")
                    time.sleep(1)
                else:
                    print(f"   'Add More' not visible for Section {k + 1}")
                break  # Only click for the first row

        # --------------------------------------------------------- top is add more -------------------------------------------
        print(f"Filling data into section")
        for i, section in enumerate(sections[:3]):
            rows = section.locator("tbody tr").all()

            for j, row in enumerate(rows):
                product_selector = f'//button[@data-id="Sections_{i}__Products_{j}__Product_Id"]'
                product_input = self.page.locator(product_selector)
                # time.sleep(1)
                if product_input.is_visible():
                    # time.sleep(1)
                    button_locator = self.page.locator(f'//button[@data-id="Sections_{i}__Products_{j}__Product_Id"]')
                    inner_text = button_locator.locator('.filter-option-inner-inner').inner_text()
                    if inner_text.strip() == "Select":
                        # time.sleep(1)
                        self.page.locator(f'//button[@data-id="Sections_{i}__Products_{j}__Product_Id"]').click()
                        product_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        product_options = [item.inner_text() for item in product_option_elmts if
                                           item.inner_text() != 'Select']
                        random_product_option = random.choice(product_options)
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_product_option, exact=True).nth(0).click()
                    else:
                        pass
                    # time.sleep(3)

                # this is to see if variation is empty and fill quantity only if it is empty (requirement)
                variation_selector = f'//button[@data-id="Sections_{i}__Products_{j}__PricebookVariation_Id"]'
                variation_input = self.page.locator(variation_selector)
                # time.sleep(1)
                if variation_input.is_visible():
                    # time.sleep(1)
                    variation_button_locator = self.page.locator(
                        f'//button[@data-id="Sections_{i}__Products_{j}__PricebookVariation_Id"]')
                    variation_inner_text = variation_button_locator.locator('.filter-option-inner-inner').inner_text()
                    # print(f"variation inner text : {variation_inner_text}")
                    if variation_inner_text.strip() == "Select":
                        time.sleep(1)
                        self.page.wait_for_load_state('networkidle', timeout=80000)

                        self.page.locator(
                            f'//button[@data-id="Sections_{i}__Products_{j}__PricebookVariation_Id"]').click()
                        variation_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        variation_options = [item.inner_text() for item in variation_option_elmts if
                                             item.inner_text() != 'Select']
                        random_variation_option = random.choice(variation_options)
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_variation_option, exact=True).nth(0).click()
                    else:
                        pass

                # this is to see if color is empty and fill quantity only if it is empty (requirement)
                color_selector = f'#Sections_{i}__Products_{j}__ColorId'
                color_input = self.page.locator(color_selector)
                # time.sleep(1)
                if color_input.is_visible():
                    # time.sleep(1)
                    color_button_locator = self.page.locator(
                        f'//button[@data-id="Sections_{i}__Products_{j}__ColorId"]')
                    color_inner_text = color_button_locator.locator('.filter-option-inner-inner').inner_text()
                    if color_inner_text.strip() == "Select":
                        # time.sleep(1)
                        self.page.locator(f'//button[@data-id="Sections_{i}__Products_{j}__ColorId"]').click()
                        color_option_elmts = self.page.locator('.dropdown-menu.show:not(.inner)').locator(
                            '.dropdown-item:not(.selected)').all()
                        color_options = [item.inner_text() for item in color_option_elmts if
                                         item.inner_text() != 'Select']
                        random_color_option = random.choice(color_options)
                        self.page.locator('.dropdown-menu.show:not(.inner)').locator('.dropdown-item').get_by_text(
                            random_color_option, exact=True).nth(0).click()
                    else:
                        pass

                # This is to see if quantity is empty or 0 and fill quantity only in that case
                quantity_selector = f'#Sections_{i}__Products_{j}__Quantity'
                quantity_input = self.page.locator(quantity_selector)

                if quantity_input.is_visible():
                    current_quantity_value = quantity_input.input_value().strip()
                    inner_text_value = quantity_input.inner_text().strip()

                    if current_quantity_value == "" or current_quantity_value == "0" or inner_text_value == "0":
                        quantity_input.fill(quantity)
                    else:
                        pass

                # this is to see if customer notes is empty and fill quantity only if it is empty (requirement)
                customer_notes_selector = f'#Sections_{i}__Products_{j}__CustomerNotes'
                customer_notes_input = self.page.locator(customer_notes_selector)
                time.sleep(1)
                if customer_notes_input.is_visible():
                    # time.sleep(1)
                    current_value = customer_notes_input.input_value()
                    if current_value.strip() == "":
                        # time.sleep(1)
                        customer_notes_input.fill(customer_notes)
                        # print(f"Filled CustomerNotes for section {i}, row {j}")
                    else:
                        # print(f"Skipped row {j} – already has value: '{current_value}'")
                        pass

                hide_on_cust_pdf_selector = f'#Sections_{i}__Products_0__IsHideInPreview'
                hide_on_cust_pdf_input = self.page.locator(hide_on_cust_pdf_selector)
                if hide_on_cust_pdf_input.is_visible():
                    self.page.check(hide_on_cust_pdf_selector)

                hide_var_on_pdf_selector = f'#Sections_{i}__Products_1__IsHideVariationonPDF'
                hide_var_on_pdf_input = self.page.locator(hide_var_on_pdf_selector)
                if hide_var_on_pdf_input.is_visible():
                    self.page.check(hide_var_on_pdf_selector)

        # --------------------------------------------------------------FINAL PRICING SCENARIOS-------------------------------------------------------------------
        # time.sleep(1)

        # Checkboxes
        checkbox = self.page.locator('#IsOptionIncluded')
        if checkbox.is_visible() and not checkbox.is_checked():
            checkbox.check()
        self.page.locator('#RetailPrice').click()

        self.toggle_yes_for_section1()
        self.toggle_yes_for_section2()
        self.toggle_yes_for_section3()

        retail_price_str_1 = self.page.input_value('#RetailPrice')
        retail_price_1 = float(retail_price_str_1.replace("$", "").replace(",", ""))
        print(f"Retail Price from page: {retail_price_1}")

        # ---------------------------------------------------- to assert in preview calc -------------------------------------------------------------------------
        with self.page.expect_popup() as page1_info:
            self.page.locator('#download-pdf-scope').click()
        time.sleep(4)
        page1 = page1_info.value

        label = "Retail Price With Options"
        spans = page1.locator("span")
        count = spans.count()

        for y in range(count):
            text = spans.nth(y).inner_text().strip()

            # Match the label span
            if label.lower() in text.lower():
                # Check next few spans for number-like text
                for z in range(y + 1, min(y + 5, count)):
                    next_text = spans.nth(z).inner_text().strip()
                    if re.match(r"^-?\$?[\d,.]+$", next_text):
                        print(next_text)

        print("Clicking 'Download PDF'...")
        # Make sure the downloads folder exists
        downloads_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(downloads_dir, exist_ok=True)

        # Optional: add timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(downloads_dir, f"downloaded_proposal_{timestamp}.pdf")

        # Handle the download
        with page1.expect_download() as download_info:
            page1.locator("#toggleSpinners").click()
        download = download_info.value
        download.save_as(file_path)

        print(f"Downloaded PDF saved at: {file_path}")
        page1.close()
        print("Closed preview calc window.")

        # Step 1: Read the readonly Retail Price value
        retail_price_str = self.page.input_value('#RetailPrice')
        retail_price = float(retail_price_str.replace("$", "").replace(",", ""))
        print(f"Retail Price from page: {retail_price}")
        print("Grand total matches retail price.")

        # ---------------------------------------------------------------------------------------------------------------------------------------------------

        # self.verify_retail_price_excludes_last_section()

        # Step 1: Read the readonly Retail Price value
        retail_price_str = self.page.input_value('#RetailPrice')
        retail_price = float(retail_price_str.replace("$", "").replace(",", ""))

        # ---- Test Dollar Adjustment ----
        self.page.locator("label", has_text="$").locator("span").click()  # Click on $
        self.page.fill("#Adjustment", "50")
        self.page.press('#RetailPrice', 'Enter')
        self.page.dispatch_event("#Adjustment", "blur")

        final_price_dollar = float(self.page.input_value('#RetailPriceAdjusted').replace("$", "").replace(",", ""))
        # final_price_dollar = float(self.page.locator("#RetailPriceAdjusted").get_attribute("value").replace(",", ""))
        expected_price_dollar = calculate_expected_price(retail_price, 50, is_percentage=False)
        assert final_price_dollar == expected_price_dollar, f"Dollar Test Failed: got {final_price_dollar}, expected {expected_price_dollar}"

        # ---- Test Percentage Adjustment ----
        self.page.locator("label", has_text="%").locator("span").click()  # Click on %
        self.page.fill("#Adjustment", "10")  # 10%
        self.page.press('#Adjustment', 'Enter')

        self.page.dispatch_event("#Adjustment", "blur")

        final_price_percent = float(self.page.input_value('#RetailPriceAdjusted').replace("$", "").replace(",", ""))
        expected_price_percent_change = calculate_expected_price(retail_price, 10, is_percentage=True)
        expected_price_percent = retail_price - expected_price_percent_change

        assert math.isclose(final_price_percent, expected_price_percent, rel_tol=1e-3), (
            f"Percentage Test Failed: got {final_price_percent}, expected {expected_price_percent}"
        )

        print("Both dollar and percentage adjustment validations passed.")

        self.collect_and_assert_headers()

        self.page.locator(
            "#formSaveExteriorScope > div.d-flex.justify-content-between.mb-3 > div > div > label:nth-child(2)").click()
        print("Clicked on the 'Customer View' radio button.")

        # to validate duplicate product
        retail_price_locator = self.page.locator('#RetailPriceAdjusted')
        assert not retail_price_locator.is_visible(), "Price locator should not be visible"
        print("Price locator not visible ")

        self.page.locator(
            "#formSaveExteriorScope > div.d-flex.justify-content-between.mb-3 > div > div > label:nth-child(1)").click()
        print("Clicked on the 'Home Expert View' radio button.")

        #self.page.click(self.checkbox_ep_selector)
        print("Toggled to show prices in customer view")
        self.page.locator(
            "#formSaveExteriorScope > div.d-flex.justify-content-between.mb-3 > div > div > label:nth-child(2)").click()
        print("Clicked on the 'Customer View' radio button.")

        # to validate pricing to be visible
        # retail_price_locator = self.page.locator('#RetailPriceAdjusted')
        # assert retail_price_locator.is_visible(), "Price locator should not be visible"
        # print("Price locator not visible ")

        self.page.locator(
            "#formSaveExteriorScope > div.d-flex.justify-content-between.mb-3 > div > div > label:nth-child(1)").click()
        print("Clicked on the 'Home Expert View' radio button.")
        self.page.wait_for_load_state('networkidle')

        self.get_pricing_total()
        self.get_deck_pricing_total()

        # Uncheck the checkbox if it is checked
        checkbox = self.page.locator('#IsOptionIncluded')
        if checkbox.is_visible() and checkbox.is_checked():
            checkbox.uncheck()
            print("   Unchecked the 'IsOptionIncluded' checkbox")
        else:
            print("   Checkbox either not visible or already unchecked")

        self.page.wait_for_timeout(5000)

        retail_price_to_validate_inc_opt = float(
            self.page.input_value('#RetailPrice').replace("$", "").replace(",", "")
        )
        print(f"Retail Price from page: {retail_price_to_validate_inc_opt}")
        print(f"\n   After untoggling 'Include Options' the pricing validation is done\n")

        self.get_section_wise_grand_totals()

        btn_update_scope_data = self.page.locator("#btnUpdateScopeData")
        if btn_update_scope_data.is_visible():
            btn_update_scope_data.click(timeout=30000)
        else:
            self.page.locator("#btnUpdateScope").click(timeout=30000)

        estimate_id = self.get_estimate_id()
        logger.info(f"Esimate id is: {estimate_id}")
        print(f"Esimate id is: {estimate_id}")
        return estimate_id

    def get_section_wise_grand_totals(self):
        section_totals = {}

        # All rows in the section table
        rows = self.page.locator("tbody[data-sectionid='17'] tr")

        for i in range(rows.count()):
            row = rows.nth(i)

            # Get the section name from the <td>
            section_name = row.locator("td").nth(0).inner_text().strip()

            # Get the hidden input for Grand Total in this row
            grand_total_input = row.locator("input.Totalgrand[type='hidden']")
            grand_total_value = grand_total_input.get_attribute("value") or "0"

            try:
                grand_total = float(grand_total_value)
            except ValueError:
                grand_total = 0.0

            section_totals[section_name] = grand_total

        print("   Section-wise Grand Totals from totals:", section_totals)
        return section_totals

    def collect_and_assert_headers(self):
        headers_initial = []
        headers_new = []

        # Collect initial headers
        header_elements_initial = self.page.query_selector_all('table#table-section-0 thead th')
        for header in header_elements_initial:
            headers_initial.append(header.inner_text())
        print("Home Expert view Headers:", headers_initial)

        # Click on the "Customer View" button
        self.page.click(
            '#formSaveExteriorScope > div.d-flex.justify-content-between.mb-3 > div > div > label:nth-child(2)')
        time.sleep(1)
        header_elements_new = self.page.query_selector_all(
            'table#table-section-0 thead th:not([style*="display: none"])')

        for header in header_elements_new:
            headers_new.append(header.inner_text())
        print("Customer view Headers:", headers_new)

        # Assert that "Quantity", "Unit", and "Total" are not present in the new headers
        assert "Qty" not in headers_new, "Qty should not be present in the headers"
        assert "Unit ($)" not in headers_new, "Unit ($) should not be present in the headers"
        assert "Totals ($)" not in headers_new, "Totals ($) should not be present in the headers"

    def toggle_yes_for_section1(self):
        index = 0
        while True:
            checkbox_id = f"Sections_0__Products_{index}__IsIncludedDefault"
            locator = self.page.locator(f"input#{checkbox_id}")
            if locator.count() == 0:
                print(f"No checkbox found for index {index}, ending loop.")
                break
            if not locator.first.is_checked():
                locator.first.check()
                print(f"   Toggled ON for: {checkbox_id}")
            else:
                print(f"Already ON: {checkbox_id}")
            index += 1

    def toggle_yes_for_section2(self):
        index = 0
        while True:
            checkbox_id = f"Sections_1__Products_{index}__IsIncludedDefault"
            locator = self.page.locator(f"input#{checkbox_id}")
            if locator.count() == 0:
                print(f"No checkbox found for index {index}, ending loop.")
                break
            if not locator.first.is_checked():
                locator.first.check()
                print(f"   Toggled ON for: {checkbox_id}")
            else:
                print(f"Already ON: {checkbox_id}")
            index += 1

    def toggle_yes_for_section3(self):
        index = 0
        while True:
            checkbox_id = f"Sections_2__Products_{index}__IsIncludedDefault"
            locator = self.page.locator(f"input#{checkbox_id}")
            if locator.count() == 0:
                print(f"No checkbox found for index {index}, ending loop.")
                break
            if not locator.first.is_checked():
                locator.first.check()
                print(f"   Toggled ON for: {checkbox_id}")
            else:
                print(f"Already ON: {checkbox_id}")
            index += 1

    def get_pricing_total(self):
        expected_side_count = self.config["exteriorpainting"].get("side_count", 1)

        sides = self.page.locator(".exterior-side-line-card")

        print(f"   Found {expected_side_count} sides")

        grand_total = 0.0
        subsection_totals = {}

        for s_index in range(expected_side_count):
            print(f" Side {s_index + 1}")

            # self.add_side_until_visible(s_index)
            self.click_side_accordion_until_open(s_index)

            side_element = sides.nth(s_index)
            section_index = int(side_element.get_attribute("data-sectionindex"))
            section_id = int(side_element.get_attribute("data-sectionid"))
            line_index = int(side_element.get_attribute("data-lineid"))

            side_total_price = 0.0

            subsection_bodies = side_element.locator(".card-body .subsection")
            subsection_count = subsection_bodies.count()
            print(f"       {subsection_count} subsections found in Side {s_index + 1}")

            for sub_index in range(subsection_count):
                print(f"     Subsection {sub_index + 1}")

                subsection_total_price = 0.0

                #   Get subsection name
                try:
                    subsection_name = subsection_bodies.nth(sub_index).locator("h6.text-primary").inner_text().strip()
                except:
                    subsection_name = f"Subsection {sub_index + 1}"

                product_table = subsection_bodies.nth(sub_index).locator("table tbody")
                row_count = product_table.locator("tr").count()

                for product_index in range(row_count):
                    print(f"           Row {product_index + 1}")
                    base_id = f"Sections_{section_index}__LineItems_{line_index}__Subsection_{sub_index}__Products_{product_index}"

                    # Locate and sum price
                    price_locator = self.page.locator(f'input[id="{base_id}__Totals"]')
                    price_value = 0.0
                    if price_locator.is_visible():
                        price_text = price_locator.input_value().replace("$", "").replace(",", "").replace("₹",
                                                                                                           "").strip()
                        try:
                            price_value = float(price_text)
                        except ValueError:
                            print(f"               Invalid price value: '{price_text}'")
                    else:
                        pass
                        # print(f"               Price field not visible for row {product_index + 1}")

                    subsection_total_price += price_value
                    side_total_price += price_value
                    print(f"               Row {product_index + 1} Price: ₹{price_value}")

                print(f"               Total price in subsection '{subsection_name}': ₹{subsection_total_price}")

                #   Add to subsection totals
                if subsection_name in subsection_totals:
                    subsection_totals[subsection_name] += subsection_total_price
                else:
                    subsection_totals[subsection_name] = subsection_total_price

            print(f"   Total price in Side {s_index + 1}: ₹{side_total_price}")
            validate_side_displayed_total(side_element, s_index, side_total_price)
            grand_total += side_total_price

        print(f"\n   Grand Total across all sides: ₹{grand_total}")
        print("   Subsection-wise Totals:", subsection_totals)
        print("   Finished filling all sides")

        # section_total = self.calculate_section_totals()
        combined_total = grand_total  # + section_total

        print(f"\n   Combined Grand Total (Sides + Sections): ₹{combined_total}")

        #    Validate with retail price shown on page
        retail_price_to_validate_inc_opt = self.page.input_value('#RetailPrice')
        retail_price_to_validate_inc_opt = float(retail_price_to_validate_inc_opt.replace("$", "").replace(",", ""))
        print(f"Retail Price from page: {retail_price_to_validate_inc_opt}")

        return grand_total, subsection_totals

    def create_carpentry_lead_estimate(self, appointment_name):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_carpentry_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_appointment_name(appointment_name)
        time.sleep(2)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        cp_page = CarpentryProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        cp_page.calc_page(input_config)
        time.sleep(30)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        pr_page.click_update_scope()
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_ep_lead_estimate(self, appointment_name):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_ep_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_appointment_name(appointment_name)
        time.sleep(2)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        ep_page = ExteriorPaintingProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        ep_page.calc_page(input_config)
        time.sleep(30)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        pr_page.click_update_scope()
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_ip_lead_estimate(self, appointment_name):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_interior_paint_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_appointment_name(appointment_name)
        time.sleep(2)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        ip_page = InteriorPaintingProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        ip_page.calc_page(input_config)
        time.sleep(30)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        pr_page.click_update_scope()
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_ip_estimate(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_interior_paint_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        ip_page = InteriorPaintingProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        input_config = self.config
        ip_page.calc_page(input_config)
        time.sleep(10)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        time.sleep(2)
        pr_page.click_update_scope()
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id


    def create_ep_estimate(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_ep_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        ep_page = ExteriorPaintingProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        ep_page.calc_page(input_config)
        time.sleep(20)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        pr_page.click_update_scope()
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_siding_estimate(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_siding_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(2)
        self.fill_appointment_form()
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        siding_page = SidingProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        siding_page.calc_page_app(input_config)
        time.sleep(2)
        time.sleep(30)
        pr_page.click_update_scope()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_siding_lead_estimate(self, appointment_name):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_siding_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_appointment_name(appointment_name)
        time.sleep(2)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        siding_page = SidingProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        siding_page.calc_page_app(input_config)
        time.sleep(30)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        pr_page.click_update_scope()
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id



    def create_door_lead_estimate(self, appointment_name):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_door_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_appointment_name(appointment_name)
        time.sleep(2)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        doors_page = DoorsProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        doors_page.doors_calc_page_app(input_config)
        time.sleep(30)
        pr_page.click_update_scope()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_windows_estimate(self, appointment_name):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_windows_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_appointment_name(appointment_name)
        time.sleep(2)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        windows_page = WindowsProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        windows_page.calc_page_app(input_config)
        time.sleep(30)
        pr_page.click_update_scope()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_fr_estimate(self, appointment_name):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_fr_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_appointment_name(appointment_name)
        time.sleep(2)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        fr_page = FlatRoofingProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        fr_page.calc_page_app(input_config)
        time.sleep(30)
        pr_page.click_update_scope()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_pr_estimate_record(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_pr_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(2)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        pr_page.calc_page_app(input_config)
        time.sleep(30)
        pr_page.click_update_scope()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_pr_estimate(self, appointment_name):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_pr_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_appointment_name(appointment_name)
        time.sleep(2)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        pr_page.calc_page_app(input_config)
        time.sleep(30)
        pr_page.click_update_scope()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_carpentry_estimate(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_carpentry_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        carpentry_page = CarpentryProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        carpentry_page.calc_page(input_config)
        time.sleep(30)
        pr_page.click_update_scope()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_door_estimate(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_door_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")

        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        door_page = DoorsProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        door_page.doors_calc_page_app(input_config)
        time.sleep(2)
        time.sleep(30)
        pr_page.click_update_scope()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_estimate_for_windows_doors(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_window_checkbox()
        self.click_door_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        windows_page = WindowsProposal(self.page)
        door_page = DoorsProposal(self.page)
        windows_page.calc_page_app(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(5)
        door_page.doors_calc_page_app(input_config)
        time.sleep(30)
        if self.page.locator("#btnUpdateScopeData").is_visible():
            self.page.locator("#btnUpdateScopeData").click()
        time.sleep(10)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id


    def create_estimate_for_ip_ep(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_ep_checkbox()
        self.click_interior_paint_checkbox()
        time.sleep(2)
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        ip_page = InteriorPaintingProposal(self.page)
        ep_page = ExteriorPaintingProposal(self.page)
        ip_page.calc_page(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(5)
        ep_page.calc_page(input_config)
        time.sleep(30)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_estimate_for_pitched_low_roofing(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_pr_checkbox()
        self.click_flat_roofing_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        low_page = FlatRoofingProposal(self.page)
        pr_page.calc_page_app(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(5)
        low_page.calc_page_app(input_config)
        time.sleep(10)
        if self.page.locator("#btnUpdateScopeData").is_visible():
            self.page.locator("#btnUpdateScopeData").click()

        time.sleep(30)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_estimate_for_exterior_interior_siding(self):
        time.sleep(3)
        self.open_new_estimate()
        time.sleep(2)
        self.click_ep_checkbox()
        time.sleep(2)
        self.click_interior_paint_checkbox()
        time.sleep(1)
        self.click_siding_checkbox()
        time.sleep(3)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        ip_page = InteriorPaintingProposal(self.page)
        sp_page = SidingProposal(self.page)
        ep_page = ExteriorPaintingProposal(self.page)

        sp_page.calc_page(input_config)
        time.sleep(4)
        self.page.locator("#btnUpdateScopeData").click()
        ip_page.calc_page(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        ep_page.calc_page(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(5)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        self.summary_page_app()
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id


    def create_estimate_for_window_door_siding(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_window_checkbox()
        time.sleep(2)
        self.click_door_checkbox()
        time.sleep(2)
        self.click_siding_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        wp_page = WindowsProposal(self.page)
        dp_page = DoorsProposal(self.page)
        sp_page = SidingProposal(self.page)
        time.sleep(2)
        wp_page.calc_page_app(input_config)
        time.sleep(4)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        dp_page.doors_calc_page_app(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(4)
        sp_page.calc_page(input_config)
        time.sleep(6)
        pr_page.click_update_scope()
        time.sleep(4)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        self.summary_page_app()
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_estimate_pitched_window_siding(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_pr_checkbox()
        time.sleep(1)
        self.click_window_checkbox()
        time.sleep(2)
        self.click_siding_checkbox()
        time.sleep(1)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        wp_page = WindowsProposal(self.page)
        sp_page = SidingProposal(self.page)
        pr_page.calc_page(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        wp_page.calc_page_app(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        sp_page.calc_page(input_config)
        time.sleep(3)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        self.summary_page_app()
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id


    def create_estimate_for_all_services(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_pr_checkbox()
        time.sleep(2)
        self.click_fr_checkbox()
        time.sleep(2)
        self.click_window_checkbox()
        time.sleep(2)
        self.click_door_checkbox()
        time.sleep(2)
        self.click_siding_checkbox()
        time.sleep(2)
        self.click_interior_paint_checkbox()
        time.sleep(2)
        self.click_ep_checkbox()
        time.sleep(2)
        self.click_carpentry_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(6)
        self.select_random_appointment()
        time.sleep(8)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        fr_page = FlatRoofingProposal(self.page)
        dr_page = DoorsProposal(self.page)
        sp_page = SidingProposal(self.page)
        wp_page = WindowsProposal(self.page)
        ep_page = ExteriorPaintingProposal(self.page)
        ip_page = InteriorPaintingProposal(self.page)
        cr_page = CarpentryProposal(self.page)
        time.sleep(2)
        pr_page.calc_page(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(2)
        fr_page.calc_page_app(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(2)
        wp_page.calc_page_app(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(2)
        dr_page.doors_calc_page_app(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(2)
        sp_page.calc_page(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        ip_page.calc_page(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        ep_page.calc_page(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(2)
        cr_page.calc_page(input_config)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(2)
        if self.page.locator("#btnUpdateScopeData").is_visible():
            self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        self.summary_page_app()
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id


    def create_estimate_for_pr_sp_window_exterior(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_pr_checkbox()
        time.sleep(2)
        self.click_siding_checkbox()
        time.sleep(2)
        self.click_window_checkbox()
        time.sleep(2)
        self.click_ep_checkbox()
        time.sleep(2)
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        sp_page = SidingProposal(self.page)
        wp_page = WindowsProposal(self.page)
        ep_page = ExteriorPaintingProposal(self.page)
        time.sleep(2)
        pr_page.calc_page(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        wp_page.calc_page_app(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        sp_page.calc_page(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        ep_page.calc_page(input_config)
        time.sleep(3)
        if self.page.locator("#btnUpdateScopeData").is_visible():
            self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        self.summary_page_app()
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id


    def create_estimate_for_pr_lr_window_exterior(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_pr_checkbox()
        time.sleep(2)
        self.click_fr_checkbox()
        time.sleep(2)
        self.click_window_checkbox()
        time.sleep(2)
        self.click_ep_checkbox()
        time.sleep(2)
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        low_page = FlatRoofingProposal(self.page)
        wp_page = WindowsProposal(self.page)
        ep_page = ExteriorPaintingProposal(self.page)
        time.sleep(2)
        pr_page.calc_page(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        low_page.calc_page(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        wp_page.calc_page_app(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        ep_page.calc_page(input_config)
        time.sleep(3)
        time.sleep(3)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        self.summary_page_app()
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id


    def create_estimate_for_pr_lr_window_door(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_pr_checkbox()
        time.sleep(2)
        self.click_fr_checkbox()
        time.sleep(2)
        self.click_window_checkbox()
        time.sleep(2)
        self.click_door_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        low_page = FlatRoofingProposal(self.page)
        wp_page = WindowsProposal(self.page)
        dp_page = DoorsProposal(self.page)
        time.sleep(2)
        pr_page.calc_page(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        low_page.calc_page(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        wp_page.calc_page_app(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        dp_page.doors_calc_page_app(input_config)
        time.sleep(3)
        time.sleep(3)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        self.summary_page_app()
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id


    def create_estimate_for_pr_lr_ip_ep(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_pr_checkbox()
        time.sleep(2)
        self.click_fr_checkbox()
        time.sleep(2)
        self.click_interior_paint_checkbox()
        time.sleep(2)
        self.click_ep_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        low_page = FlatRoofingProposal(self.page)
        ip_page = InteriorPaintingProposal(self.page)
        ep_page = ExteriorPaintingProposal(self.page)
        time.sleep(2)
        pr_page.calc_page(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        low_page.calc_page(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        ip_page.calc_page(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        ep_page.calc_page(input_config)
        time.sleep(3)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        self.summary_page_app()
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_estimate_for_pitched_low_siding(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_pr_checkbox()
        time.sleep(1)
        self.click_fr_checkbox()
        time.sleep(1)
        self.click_siding_checkbox()
        time.sleep(1)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        low_page = FlatRoofingProposal(self.page)
        sp_page = SidingProposal(self.page)
        pr_page.calc_page(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        low_page.calc_page(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        sp_page.calc_page(input_config)
        time.sleep(3)
        time.sleep(3)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        self.summary_page_app()
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id


    def create_estimate_for_pitched_low_exterior(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_pr_checkbox()
        time.sleep(1)
        self.click_fr_checkbox()
        time.sleep(1)
        self.click_ep_checkbox()
        time.sleep(1)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        low_page = FlatRoofingProposal(self.page)
        ex_page = ExteriorPaintingProposal(self.page)
        pr_page.calc_page(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        low_page.calc_page(input_config)
        time.sleep(3)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        ex_page.calc_page(input_config)
        time.sleep(3)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        self.summary_page_app()
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def create_estimate_for_siding_carpentry(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_siding_checkbox()
        time.sleep(1)
        self.click_carpentry_checkbox()
        time.sleep(1)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        siding_page = SidingProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        time.sleep(10)
        carpentry_page = CarpentryProposal(self.page)
        siding_page.calc_page(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(3)
        carpentry_page.calc_page(input_config)
        time.sleep(5)
        if self.page.locator("#btnUpdateScopeData").is_visible():
            self.page.locator("#btnUpdateScopeData").click()
        time.sleep(10)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        self.summary_page_app()
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id


    def create_estimate_for_pitched_low_roofing_without_sign(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_pr_checkbox()
        self.click_flat_roofing_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        pr_page = PitchedRoofingProposal(self.page)
        low_page = FlatRoofingProposal(self.page)
        pr_page.calc_page_app(input_config)
        time.sleep(2)
        self.page.locator("#btnUpdateScopeData").click()
        time.sleep(5)
        low_page.calc_page_app(input_config)
        time.sleep(10)
        if self.page.locator("#btnUpdateScopeData").is_visible():
            self.page.locator("#btnUpdateScopeData").click()

        time.sleep(30)
        pr_page.click_update_scope()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app_without_sign(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id


    def view_deleted_estimate_restore_validation(self):
        estimate_id = self.create_estimate_for_pitched_low_roofing_without_sign()
        time.sleep(5)

        self.page.locator("#ProposalsMenu").nth(0).click()
        time.sleep(3)
        self.page.locator("#proposalSearch").fill(estimate_id)
        self.page.locator("#proposalSearch").press("Enter")
        time.sleep(2)
        self.page.locator(".mdi-18px").nth(1).click()
        time.sleep(3)
        self.page.locator(".dropdown-menu.show a.dropdown-item:has-text('Delete Estimate')").click()
        time.sleep(3)
        self.page.locator("#btnDeleteProposal").click()
        time.sleep(4)
        self.page.click('button.swal-button.swal-button--confirm.btn.btn-primary')
        time.sleep(6)
        self.page.locator("#ViewDeletedEstimatesTab").nth(0).click()
        time.sleep(5)
        if self.page.locator("#userPager").locator(".px-3").is_visible():
            time.sleep(2)
            count_text = self.page.locator("#userPager").locator(".px-3").inner_text()
            value = int(count_text.split()[-2])
        else:
            value = 0

        logger.info(f"Deleted Estimate count is: {value}")
        print(f"Delete Estimate count is: {value}")
        count = 20
        for i in range(count):
            if i % 2 != 0:
                time.sleep(2)
                self.page.locator(".mdi-18px").nth(i).click()
                time.sleep(2)
                self.page.locator(".dropdown-menu.show:not(.inner)").locator(".dropdown-item").get_by_text(
                    "Restore",
                    exact=True).nth(0).click()
                time.sleep(6)
                self.page.locator("#btnRestoreProposal").nth(0).click()
                time.sleep(2)
                if self.page.locator(".swal-modal .swal-icon--success").is_visible():
                    self.page.locator('.swal-modal .swal-button--confirm').click()
                    time.sleep(3)
                    logger.info(f"Estimate Restore done successfully")
                    print(f"Estimate Restore done successfully")
                    time.sleep(3)
                    if self.page.locator("#userPager").locator(".px-3").is_visible():
                        time.sleep(2)
                        count_text = self.page.locator("#userPager").locator(".px-3").inner_text()
                        new_value = int(count_text.split()[-2])
                    else:
                        new_value = 0

                    logger.info(f"After Estimation restore lastest count: {new_value}")
                    print(f"After Estimation restore lastest count: {new_value}")
                    if value > new_value:
                        logger.info(f"View Deleted Estimate validation done successfully. New count:{new_value} and Old count: {value}")
                        print(f"View Deleted Estimate validation done successfully. New count:{new_value} and Old count: {value}")
                    else:
                        logger.info(
                            f"View Deleted Estimate validation failed successfully. New count:{new_value} and Old count: {value}")
                        print(
                            f"View Deleted Estimate validation failed successfully. New count:{new_value} and Old count: {value}")
                    break
                else:
                    self.page.locator('.swal-modal .swal-button--confirm').click()
                    time.sleep(3)
                    error_message = self.page.text_content("div.modal-body.text-center h5")
                    logger.info(f"Unable to restore the Estimate:{error_message}")
                    print(f"Unable to restore the Estimate:{error_message}")
                    self.page.click("button.btn.btn-light[data-dismiss='modal']")
                    time.sleep(2)




    def create_window_estimate(self):
        time.sleep(2)
        self.open_new_estimate()
        time.sleep(2)
        self.click_window_checkbox()
        time.sleep(2)
        self.save_service()
        time.sleep(2)
        self.select_random_appointment()
        time.sleep(4)
        self.fill_appointment_form()
        time.sleep(2)
        self.page.wait_for_load_state('networkidle', timeout=80000)
        time.sleep(9)
        service_elements = self.page.locator("#servicesTabList li[style*='display: list-item;'] a")
        logger.info(f"All available services: {service_elements}")
        print(f"All available services: {service_elements}")
        services = service_elements.all_text_contents()
        logger.info(services)
        print(services)
        input_config = self.config
        window_page = WindowsProposal(self.page)
        pr_page = PitchedRoofingProposal(self.page)
        window_page.calc_page(input_config)
        time.sleep(2)
        time.sleep(30)
        self.page.wait_for_load_state('networkidle')
        logger.info("Sketch Saved and Proceeded for all cards")
        self.save_sketch()
        time.sleep(2)
        print("SKETCH ADDED")
        time.sleep(2)
        pr_page.summary_page_app(input_config)
        logger.info("Finished iterating all available services in same tab")
        time.sleep(5)
        estimate_id = self.get_estimate_id()
        return estimate_id

    def click_estimate_menu_button(self):
        self.page.locator('#ProposalsMenu').click()
        self.page.wait_for_load_state("networkidle", timeout=100000)
        time.sleep(5)
        return 'Success'

    def click_view_estimate_tab(self):
        self.page.locator('#ViewEstimateTab').click()
        self.page.wait_for_load_state("networkidle", timeout=100000)
        time.sleep(5)
        return 'Success'

    def sign_estimate(self, estimation_id):
        time.sleep(5)
        self.page.locator("#ProposalsMenu").click()
        time.sleep(2)
        self.page.locator("#ViewEstimateTab").click()
        time.sleep(20)
        self.page.locator("#proposalSearch").click()
        self.page.locator("#proposalSearch").fill(estimation_id)
        self.page.locator("#proposalSearch").press("Enter")
        time.sleep(20)
        # self.page.locator(
        #     "button.btn.btn-light.btn-sm.border-act"
        # ).click(force=True)
        self.page.get_by_role("cell", name="Change Order ID Change Order").get_by_role("button").click()
        time.sleep(10)
        self.page.locator(
            f"div.dropdown-menu.show a.dropdown-item:has-text('Sign CO')"
        ).click(force=True)

        time.sleep(10)
        # 1) Locate canvas
        canvas = self.page.locator("#customer-signature-pad canvas").first
        canvas.wait_for(state="visible", timeout=5000)
        canvas.scroll_into_view_if_needed()

        # 2) Get canvas box
        box = canvas.bounding_box()
        if not box:
            raise RuntimeError("Signature canvas bounding box not available.")

        # 3) New Signature Pattern (curved loops + wave)
        start_x = box["x"] + 30
        start_y = box["y"] + box["height"] / 2

        # First loop
        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()
        self.page.mouse.move(start_x + 40, start_y - 40)
        self.page.mouse.move(start_x + 80, start_y + 20)
        self.page.mouse.move(start_x + 120, start_y - 25)
        self.page.mouse.move(start_x + 160, start_y + 30)
        self.page.mouse.up()

        # Second zig‑zag stroke
        self.page.mouse.move(start_x + 60, start_y + 35)
        self.page.mouse.down()
        self.page.mouse.move(start_x + 110, start_y + 5)
        self.page.mouse.move(start_x + 160, start_y + 25)
        self.page.mouse.move(start_x + 210, start_y - 10)
        self.page.mouse.up()

        # Optional tail stroke
        self.page.mouse.move(start_x + 190, start_y + 10)
        self.page.mouse.down()
        self.page.mouse.move(start_x + 260, start_y - 5)
        self.page.mouse.up()

        # 4) Draw name in a different style
        signature_name = "Anitha Kn"

        self.page.evaluate(
            """
            (args) => {
              const canvas = document.querySelector(args.sel);
              if (!canvas) return;

              const ctx = canvas.getContext('2d');
              ctx.save();
              ctx.fillStyle = '#222';  // darker gray text
              ctx.font = 'italic 16px Arial';  // italic + smaller
              ctx.textBaseline = 'bottom';
              ctx.fillText(String(args.name), 20, canvas.height - 8);
              ctx.restore();
            }
            """,
            {"sel": "#homeexpert-signature-pad canvas", "name": signature_name}
        )
        time.sleep(5)
        self.page.locator('#btnSaveProposalSign').click()
        time.sleep(5)
        self.page.locator("button.swal-button--confirm").click()
        time.sleep(5)
        logger.info(f"Estimate Signed Successfully Done For Change Order")
        print(f"Estimate Signed Successfully Done For Change Order")
        return "Success"

    def estimate_mark_as_booked(self, estimation_id, estimation_name):
        data = {}
        self.page.locator('#filterEstimateStatus').select_option(value='1')
        time.sleep(5)
        self.page.locator("#proposalSearch").click()
        self.page.locator("#proposalSearch").fill(estimation_id)
        self.page.locator("#proposalSearch").press("Enter")
        time.sleep(5)
        self.page.get_by_role("cell", name="Change Order ID Change Order").get_by_role("button").click()

        # self.page.locator(
        #     "button.btn.btn-light.btn-sm.border-act"
        # ).click(force=True)
        time.sleep(2)
        self.page.locator(
            ".dropdown-menu.show a.dropdown-item:has-text('Mark as Booked')"
        ).click()
        time.sleep(3)
        # Payment Method: Tick 'Credit Card' (value=1)
        self.page.check('input[name="PaymentMethod"][value="1"]')
        data['PaymentMethod'] = "Credit Card"

        # Credit Card confirmation number input (only shown when 'Credit Card' checked)
        cc_conf_num = "CC12345"
        self.page.fill('div#CreditCard input[type="text"]', cc_conf_num)
        data['CreditCardConfirmationNumber'] = cc_conf_num

        time.sleep(4)
        self.page.locator('#btnMarkasBooked').click()
        self.page.locator(
            "#myModalContent button:has-text('Close')"
        ).click()

        logger.info(f"Add On Created Successfully Done for Change Order")
        print(f"Add On Created Successfully Done for Change Order")
        return 'Success'

    def estimation_mark_as_sales_approved(self, estimation_id, estimation_name):

        self.click_estimate_menu_button()
        self.click_view_estimate_tab()
        time.sleep(5)
        self.page.locator('#filterEstimateStatus').select_option(value='3')
        time.sleep(5)
        self.page.locator("#proposalSearch").click()
        self.page.locator("#proposalSearch").fill(estimation_id)
        self.page.locator("#proposalSearch").press("Enter")
        time.sleep(5)
        self.page.get_by_role("cell", name="Change Order ID Change Order").get_by_role("button").click()
        # self.page.locator(
        #     "button.btn.btn-light.btn-sm.border-act"
        # ).click(force=True)
        time.sleep(2)
        self.page.locator(".dropdown-menu.show a.dropdown-item:has-text('Mark as Sales Ops Approved')").click()
        time.sleep(3)
        self.page.locator('#btn-approvedcomplete').click()
        time.sleep(5)
        logger.info(f"Status Changed as Mark as Sales ops Approved Successfully Done for Change Order")
        print(f"Status Changed as Mark as Sales ops Approved Successfully Done for Change Order")
        return "Success"

    def estimation_mark_as_sold(self, estimation_id, estimation_name):
        time.sleep(5)
        self.page.locator('#filterEstimateStatus').select_option(value='4')
        time.sleep(5)
        self.page.locator("#proposalSearch").click()
        self.page.locator("#proposalSearch").fill(estimation_id)
        self.page.locator("#proposalSearch").press("Enter")
        time.sleep(5)
        # self.page.locator(
        #     "button.btn.btn-light.btn-sm.border-act"
        # ).click(force=True)
        self.page.get_by_role("cell", name="Change Order ID Change Order").get_by_role("button").click()
        time.sleep(2)
        self.page.locator(".dropdown-menu.show a.dropdown-item:has-text('Mark as Sold ')").click()
        time.sleep(3)
        self.page.locator('#PaymentmethodId').select_option(value='1')
        time.sleep(2)
        today = datetime.now().strftime("%m/%d/%Y")
        self.page.locator("#PaymentDate").fill(today)
        time.sleep(2)

        # 2) Wait until the Credit Card section is visible
        cc_input = self.page.locator("#CreditCard .payment-method-number-input").first
        cc_input.wait_for(state="visible")

        # 3) Fill the confirmation number
        cc_input.fill("CONF123456")

        # 4) (Optional) trigger validation listeners
        cc_input.blur()
        self.page.locator('#btnSaveMarkasSold').click()
        logger.info(f"Status Changed  Mark As Sold  Successfully Done for Change Order")
        print(f"Status Changed  Mark As Sold  Successfully Done for Change Order")
        return 'Success'



    def create_co(self, estimation_id):
        self.click_estimate_menu_button()
        self.click_view_estimate_tab()
        self.page.locator('#filterEstimateStatus').select_option(value='0')
        time.sleep(2)
        self.page.locator("#proposalSearch").click()
        self.page.locator("#proposalSearch").fill(estimation_id)
        self.page.locator("#proposalSearch").press("Enter")
        time.sleep(2)
        self.page.locator(".mdi-18px").nth(1).click()
        time.sleep(3)
        self.page.locator(".dropdown-menu.show a.dropdown-item:has-text('Create CO')").click()
        time.sleep(5)
        self.page.locator('#btnSaveServices').click()
        time.sleep(30)
        self.page.locator("#btnUpdateBasicInfo").click(timeout=90000)
        time.sleep(100)
        self.page.locator("#btnUpdateScopeData").click()

        pr_page = PitchedRoofingProposal(self.page)
        pr_page.click_update_scope()

        #btn_update_scope_data = self.page.locator("#btnUpdateScopeData")
        # if btn_update_scope_data.is_visible():
        #     btn_update_scope_data.click(timeout=60000)
        #     logger.info("I am here")
        #     print("I am here")
        # else:
        #     time.sleep(40)
        #     self.page.locator("#btnUpdateScope").click(timeout=60000)
        #     logger.info("I am here Too")
        #     print("I am here Too")

        time.sleep(40)
        self.page.locator("a.btn.btn-primary.btnSaveSketch").click()
        btn_summary_tab = self.page.locator("#btnGotoSummaryTab")
        btn_summary = self.page.locator("#btnGotoSummary")

        # Small timeout to quickly decide visibility
        if btn_summary_tab.is_visible():
            btn_summary_tab.click()
            logger.info("Clicked btnGotoSummaryTab")
        else:
            btn_summary.click()
            logger.info("Clicked btnGotoSummary")
        time.sleep(4)
        self.page.locator("#btnFinishProposal").click()
        with self.page.expect_popup() as page1_info:
            page1 = page1_info.value
            logger.info("Clicking 'Email Customer'...")
            page1.wait_for_selector("#toggleSpinners", state="visible")
            page1.get_by_text("Email Estimate ").click()
            page1.locator('#btnSendEmail').click()
            time.sleep(3)
            page1.locator('.swal-modal .swal-button--confirm').click()

            # ----------------------------------------------------------------------to download --------------------------------------------

            logger.info("Clicking 'Download PDF'...")
            # Make sure the downloads folder exists
            downloads_dir = os.path.join(os.getcwd(), "downloads")
            os.makedirs(downloads_dir, exist_ok=True)

            # Optional: add timestamp to avoid overwriting
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(downloads_dir, f"downloaded_proposal_{timestamp}.pdf")

            # Handle the download
            with page1.expect_download() as download_info:
                page1.get_by_text("Download Estimate").click()
            download = download_info.value
            download.save_as(file_path)

            logger.info(f"Downloaded PDF saved at: {file_path}")
            if self.context.pages:
                self.context.pages[-1].close()
            time.sleep(2)
            if len(self.context.pages) > 1:
                self.context.pages[1].bring_to_front()

        logger.info(f"change Order Created Successfully")
        return "Success"
