from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import os # get resume
import time # sleep

_app_info = { # replace for personal use
    "first_name": "FIRST",
    "last_name": "LAST",
    "email": "EMAIL",
    "phone": "123-456-7890",
    "resume": "resume.pdf",
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

    # Upload Resume (through click hopefully!)
    resume_attach = driver.find_element(By.XPATH, value='//*[@id="resume_fieldset"]/div/div[3]/button[1]')
    resume_attach.click()
    time.sleep(3)

    # TODO: instead of uploading resume through file, upload through text - have a textfile of my resume


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