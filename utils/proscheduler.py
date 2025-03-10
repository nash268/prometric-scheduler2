from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Proscheduler():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def halt(self):
        self.driver.quit()

    def get_dates(
        self, 
        exam_name: str, 
        country_code: str, 
        appointment_selection_value: str, 
        address: str, 
        center_xpath: str,
        month_year: str,
        date_range: list[int]
    ):
        self.driver.get("https://securereg3.prometric.com/Welcome.aspx")

        # Select exam_name in dropdown menu
        programs_menu = self.driver.find_element(By.ID, "masterPage_cphPageBody_ddlPrograms")
        Select(programs_menu).select_by_value(exam_name)

        # Select country
        country_menu = self.driver.find_element(By.ID, "masterPage_cphPageBody_ddlCountry")
        Select(country_menu).select_by_value(country_code)

        # Click next button
        self.driver.find_element(By.ID, "masterPage_cphPageBody_btnNext").click()

        # Wait for page to load and click the initial link
        initial_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "masterPage_cphPageBody_lnkSeatAvail2"))
        )
        initial_link.click()

        # Appointment selection
        appointment_selection = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "masterPage_cphPageBody_ddlExam"))
        )
        Select(appointment_selection).select_by_value(appointment_selection_value)
        self.driver.find_element(By.ID, "masterPage_cphPageBody_btnNext").click()

        # Wait for page to load and enter city
        search_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "txtSearch"))
        )
        search_input.send_keys(address)

        # Click search button
        search_button = self.driver.find_element(By.ID, "btnSearch")
        search_button.click()

        # Selecting center
        availability_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, center_xpath))
        )
        availability_link.click()

        # Select month and year
        dropdown_month = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "masterPage_cphPageBody_monthYearlist"))
        )
        Select(dropdown_month).select_by_value(month_year)

        # Click submit button
        submit_button = self.driver.find_element(By.ID, "masterPage_cphPageBody_btnGoCal")
        submit_button.click()

        try:
            # Check for active links' availability
            active_links = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "calActiveLink"))
            )

            start_date, end_date = date_range

            # Extract dates from active links and filter based on date range
            available_dates_in_range = [
                int(link.text) for link in active_links if start_date <= int(link.text) <= end_date
            ]

            return available_dates_in_range if available_dates_in_range else False

        except TimeoutException:
            return False