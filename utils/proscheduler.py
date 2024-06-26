# Generated by Selenium IDE
import calendar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

class Proscheduler():
  def start(self):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def halt(self):
    self.driver.quit()
  
  def get_dates(self, exam_name, addresses, month_year):

    dates_found = {}
    month, year = month_year.split(' ')
    last_date = calendar.monthrange(int(year), int(month))[1]
    # Test name: proscheduler2
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("https://proscheduler.prometric.com/")

    # wait for button and click it
    avail_btn = WebDriverWait(self.driver, 10).until(
       EC.element_to_be_clickable((By.XPATH, '//img[@src="/dist/assets/images/SearchAvailability.png"]'))
    )
    avail_btn.click()
    # 4 | click | id=test_sponsor | 
    test_sponser_btn = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'test_sponsor'))
    )
    test_sponser_btn.click()
    # 5 | select | id=test_sponsor | label=National Board of Medical Examiners
    dropdown = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "test_sponsor"))
    )
    select = Select(dropdown)
    select.select_by_visible_text("National Board of Medical Examiners")
    # 6 | click | id=testProgram | 
    test_program_btn = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "testProgram"))
    )
    test_program_btn.click()
    # 7 | select | id=testProgram | label=STEP1
    dropdown = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "testProgram"))
    )
    select = Select(dropdown)
    select.select_by_visible_text(exam_name)

    if exam_name == 'STEP1':
        test_name = 'Step 1 - United States Medical Licensing Examination'
    elif exam_name == 'STEP2':
        test_name = 'Step 2 - United States Medical Licensing Examination'
    elif exam_name == 'STEP3':
        test_name = 'Step 3 - United States Medical Licensing Examination'

    # 8 | click | id=testSelector | 
    test_selector_btn = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "testSelector"))
    )
    test_selector_btn.click()
    # 9 | select | id=testSelector | label=Step 1 - United States Medical Licensing Examination
    dropdown = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "testSelector"))
    )
    select = Select(dropdown)
    select.select_by_visible_text(test_name)
    # scroll down
    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    self.driver.find_element(By.XPATH, f"//*[text()='{test_name}']").click()
    # 10 | click | id=nextBtn | 
    next_btn = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "nextBtn"))
    )
    next_btn.click()
    # 11 | type | id=searchLocation | Karachi, Pakistan
    i = 0
    active_links = False
    for city in addresses:
        dates_in_city = []
        # Enter City in field
        location_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "searchLocation"))
        )
        location_field.send_keys(city)
        # 12 | type | id=undefined | 06/01/2024
        self.driver.find_element(By.ID, "undefined").send_keys(f"{month}/01/{year}")
        # 13 | type | css=.end-date #undefined | 06/15/2024
        self.driver.find_element(By.CSS_SELECTOR, ".end-date #undefined").send_keys(f"{month}/15/{year}")
        # 14 | click | id=nextBtn | 
        # click next button only on first try
        # click search button on consequent tries
        if i == 0:
            self.driver.find_element(By.ID, "nextBtn").click()
            i += 1
        else:
            self.driver.find_element(By.CSS_SELECTOR, "#searchBtn > span").click()
        # --------------------------------------------------
        # check for dates here and append them to a list
        try:
            available_dates = WebDriverWait(self.driver, 10).until(
                EC.visibilty_of_element_located((By.XPATH, '//strong[@_ngcontent-c12=""]'))
            )
            dates = [element.text for element in available_dates]
            dates_in_city.append(dates)
            active_links = True
            print('.')
        except TimeoutException:
            print('.')
        
        # 15 | click | id=startDate | 
        self.driver.find_element(By.ID, "startDate").click()
        # 16 | type | id=startDate | 06/15/2024
        self.driver.find_element(By.ID, "startDate").send_keys(f"{month}/15/{year}")
        # 17 | click | id=endDate | 
        self.driver.find_element(By.ID, "endDate").click()
        # 18 | type | id=endDate | 06/29/2024
        self.driver.find_element(By.ID, "endDate").send_keys(f"{month}/{last_date}/{year}")
        # 19 | click | css=#searchBtn > span | 
        self.driver.find_element(By.CSS_SELECTOR, "#searchBtn > span").click()
        # ----------------------------------------------------------------
        # check for dates here and append them to a list
        try:
            WebDriverWait(self.driver, 10).until(
                available_dates = EC.visibilty_of_element_located((By.XPATH, '//strong[@_ngcontent-c12=""]'))
            )
            dates = [element.text for element in available_dates]
            dates_in_city.append(dates)
            active_links = True
            print('.')
            
        except TimeoutException:
            print('.')

        dates_found.update[(city, dates_in_city)]

    if len(dates_found) > 0:
        return dates_found
    else:
        return False