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
    # 2 | setWindowSize | 683x720 | 
    self.driver.set_window_size(683, 720)
    # 3 | click | css=.action-card:nth-child(2) > a:nth-child(1) > .img-responsive | 
    # self.driver.find_element(By.CSS_SELECTOR, ".action-card:nth-child(2) > a:nth-child(1) > .img-responsive").click()
    element = driver.find_element(By.XPATH, '//img[@src="/dist/assets/images/SearchAvailability.png"]').click()
    # 4 | click | id=test_sponsor | 
    self.driver.find_element(By.ID, "test_sponsor").click()
    # 5 | select | id=test_sponsor | label=National Board of Medical Examiners
    dropdown = self.driver.find_element(By.ID, "test_sponsor")
    dropdown.find_element(By.XPATH, "//option[. = 'National Board of Medical Examiners']").click()
    # 6 | click | id=testProgram | 
    self.driver.find_element(By.ID, "testProgram").click()
    # 7 | select | id=testProgram | label=STEP1
    dropdown = self.driver.find_element(By.ID, "testProgram")
    dropdown.find_element(By.XPATH, f"//option[. = '{exam_name}']").click()

    if exam_name == 'STEP1':
        test_name = 'Step 1 - United States Medical Licensing Examination'
    elif exam_name == 'STEP2':
        test_name = 'Step 2 - United States Medical Licensing Examination'
    elif exam_name == 'STEP3':
        test_name = 'Step 3 - United States Medical Licensing Examination'

    # 8 | click | id=testSelector | 
    self.driver.find_element(By.ID, "testSelector").click()
    # 9 | select | id=testSelector | label=Step 1 - United States Medical Licensing Examination
    dropdown = self.driver.find_element(By.ID, "testSelector")
    dropdown.find_element(By.XPATH, f"//option[. = '{test_name}']").click()
    # 10 | click | id=nextBtn | 
    self.driver.find_element(By.ID, "nextBtn").click()
    # 11 | type | id=searchLocation | Karachi, Pakistan
    i = 0
    active_links = False
    for city in addresses:
        dates_in_city = []
        self.driver.find_element(By.ID, "searchLocation").send_keys(city)
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
            WebDriverWait(self.driver, 10).until(
                available_dates = self.driver.find_elements_by_css_selector('strong[_ngcontent-c12=""]')
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
                available_dates = self.driver.find_elements_by_css_selector('strong[_ngcontent-c12=""]')
            )
            dates = [element.text for element in available_dates]
            dates_in_city.append(dates)
            active_links = True
            print('.')
            
        except TimeoutException:
            print('.')

        dates_found.update[(city, dates_in_city)]

    if active_links:
        return dates_found
    else:
        return False