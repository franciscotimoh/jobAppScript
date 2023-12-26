from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

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

    

    time.sleep(3)


if __name__ == "__main__":
    jobURLs = ["https://boards.greenhouse.io/elementbiosciences/jobs/5033562004?gh_src=86bf34104us&source=LinkedIn"]
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