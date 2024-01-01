from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver import ActionChains

from bs4 import BeautifulSoup

import os # get resume
import time # sleep

_app_info = { # replace for personal use
    "first_name": "FIRST",
    "last_name": "LAST",
    "email": "EMAIL",
    "phone": "123-456-7890",
    "resume": "resume.txt",
    "linkedin": "https://www.linkedin.com/in/timbim1681",
    "github": "https://www.github.com/timbim1681"
}

"""
driver = webdriver.Chrome()
driver.get("https://www.python.org")
print(driver.title)

search_bar = driver.find_element(By.NAME, value="q")
search_bar.clear()
search_bar.send_keys("getting started with python")
search_bar.send_keys(Keys.RETURN)

print(driver.current_url)
driver.close()
"""

def greenhouse(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')

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

    driver.find_element_by_id("submit_app").click()


if __name__ == "__main__":
    jobURLs = ["https://boards.greenhouse.io/andurilindustries/jobs/4159194007?gh_jid=4159194007&gh_src=83e1be777us"]
    # one listing for now
    driver = webdriver.Chrome()
    
    for url in jobURLs:
        print('\n')

        if 'greenhouse' in url:
            driver.get(url)
            try:
                greenhouse(driver)
                print(f'SUCCESS FOR {url}')
            except: 
                continue
        
        else:
            continue

        time.sleep(1)
    
    driver.close()