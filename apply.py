from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver import ActionChains

from bs4 import BeautifulSoup

import spreadsheet

import os # get resume
import time # sleep
from datetime import date

_app_info = { # replace for personal use
    "first_name": "FIRST",
    "last_name": "LAST",
    "email": "EMAIL",
    "phone": "123-456-7890",
    "resume": "resume.txt",
    "linkedin": "https://www.linkedin.com/in/timbim1681",
    "github": "https://www.github.com/timbim1681",
}

def greenhouse(driver):
    # Compile values to append to spreadsheet
    company_name = driver.find_element(By.CLASS_NAME, value='company-name').text 
    position_name = driver.find_element(By.CLASS_NAME, value='app-title').text 
    date_applied = str(date.today())
    values_for_ss = [company_name, position_name, date_applied]

    # Basic info
    driver.find_element(By.ID, value="first_name").send_keys(_app_info['first_name'])
    driver.find_element(By.ID, value="last_name").send_keys(_app_info['last_name'])
    driver.find_element(By.ID, value="email").send_keys(_app_info['email'])
    driver.find_element(By.ID, value='phone').send_keys(_app_info['phone'])

    # Upload Resume (through text)
    driver.find_element(By.CSS_SELECTOR, value="[data-source='paste']").click()
    resume_zone = driver.find_element(By.ID, value='resume_text')
    resume_zone.click()
    with open(_app_info['resume']) as f:
        lines = f.readlines()
        for line in lines:
            resume_zone.send_keys(line)

    # Add LinkedIn
    try:
        driver.find_element(By.XPATH, value='//*[@id="job_application_answers_attributes_0_text_value"]').send_keys(_app_info['linkedin'])
    except NoSuchElementException:
        pass

    # Add Website
    try:
        driver.find_element(By.XPATH, value='//*[@id="job_application_answers_attributes_1_text_value"]').send_keys(_app_info['github'])
    except NoSuchElementException:
        pass

    # Give an LLM my info - take every (mandatory) question and ask ChatGPT "how will the person answer this question?" & give it the options
    # use OpenAI ChatGPT or other free LLM
    
    # Cannot handle other "mandatory" questions at the moment
    # Tried: Select dropdown, ActionChains, etc. ElementNotInteractableException for both
    # TODO: research this approach later

    # Add graduation year
    try:
        driver.find_element(By.XPATH, value="//select/option[text()='2025']").click()
    except NoSuchElementException:
        pass

    # Add university
    try:
        driver.find_element(By.XPATH, value="//select/option[contains(.,'University of California, Irvine')]").click()
    except NoSuchElementException:
        try:
            driver.find_element(By.XPATH, value="//select/option[contains(.,'University of California - Irvine')]").click()
        except NoSuchElementException:
            pass

    # Add degree
    try:
        driver.find_element(By.XPATH, value="//select/option[contains(.,'Bachelor')]").click()
    except NoSuchElementException:
        pass

    # Add major
    try:
        driver.find_element(By.XPATH, value="//select/option[contains(.,'Computer Science and Engineering')]").click()
    except NoSuchElementException:
        try:
            driver.find_element(By.XPATH, value="//select/option[contains(.,'Computer Science & Engineering')]").click()
        except NoSuchElementException:
            try:
                driver.find_element(By.XPATH, value="//select/option[contains(.,'Computer Science')]").click()
            except NoSuchElementException:
                pass

    # Add work authorization
    try:
        driver.find_element(By.XPATH, value="//select/option[contains(.,'any employer')]").click()
    except NoSuchElementException:
        pass

    time.sleep(5) # Buffer time to answer questions that are mandatory

    # driver.find_element(By.ID, value="submit_app").click()
    
    return values_for_ss


def lever(driver):
    driver.find_element(By.CLASS_NAME, value='template-btn-submit').click()

    first_name = _app_info['first_name']
    last_name = _app_info['last_name']
    full_name = first_name + ' ' + last_name
    driver.find_element(By.NAME, value='name').send_keys(full_name)
    driver.find_element(By.NAME, value='email').send_keys(_app_info['email'])
    driver.find_element(By.NAME, value='phone').send_keys(_app_info['phone'])

    driver.find_element(By.NAME, value='urls[LinkedIn]').send_keys(_app_info['linkedin'])
    
    try:
        driver.find_element(By.NAME, value='urls[Github]').send_keys(_app_info['github'])
    except:
        try:
            driver.find_element(By.NAME, value='urls[GitHub]').send_keys(_app_info['github'])
        except:
            pass
    
    try:
        driver.find_element(By.CLASS_NAME, value='application-university').click()
        search = driver.find_element(By.XPATH, value="//*[@type='search']")
        search.send_keys("University of California, Irvine")
        search.send_keys(Keys.RETURN)
    except NoSuchElementException:
        try:
            driver.find_element(By.CLASS_NAME, value='application-university').click()
            search = driver.find_element(By.XPATH, value="//*[@type='search']")
            search.send_keys("University of California - Irvine")
            search.send_keys(Keys.RETURN)
        except NoSuchElementException:
            pass

    driver.find_element(By.NAME, value='resume').send_keys(os.getcwd()+"/tim_oh_resume.pdf")
    
    # driver.find_element(By.CLASS_NAME, value='template-btn-submit').click()

    time.sleep(10)

if __name__ == "__main__":
    # 02/04/2024: around 30 seconds per application to submit

    data_for_ss = []
    # "https://boards.greenhouse.io/andurilindustries/jobs/4159194007?gh_jid=4159194007&gh_src=83e1be777us"
    # "https://jobs.lever.co/leverdemo-8/e56e2e68-f9d1-4c8f-b13d-88b9ca17f88a?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic"
    jobURLs = ["https://boards.greenhouse.io/andurilindustries/jobs/4159194007?gh_jid=4159194007&gh_src=83e1be777us"]

    # one listing for now
    driver = webdriver.Chrome()
    
    for url in jobURLs:
        vals_for_sslist = []
        print('\n')

        if 'greenhouse' in url:
            driver.get(url)
            try:
                vals_for_sslist.append(greenhouse(driver))
                print(f'SUCCESS FOR {url}')
            except: 
                continue

        elif 'lever' in url:
            driver.get(url)
            try:
                lever(driver)
                print(f'SUCCESS FOR: {url}')
            except:
                continue
        
        else:
            continue

        time.sleep(1)

    print(vals_for_sslist)
    spreadsheet.update_spreadsheet(vals_for_sslist)
    driver.close()