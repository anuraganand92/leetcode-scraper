#IMPORTS
import os
import time
import re
import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# set up selenium
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# login to leetcode
driver.get("https://leetcode.com/accounts/login/")
driver.find_element(By.ID,"id_login").send_keys("username")
driver.find_element(By.ID,"id_password").send_keys("password")
driver.find_element(By.ID,"signin_btn").click()

# wait for login to complete
time.sleep(5)

# get list of all questions
driver.get("https://leetcode.com/problemset/all/")
time.sleep(5)
soup = BeautifulSoup(driver.page_source, "html.parser")
questions = soup.find_all("a", class_="reactable-pagination-page")

# create directory for questions
if not os.path.exists("questions"):
    os.makedirs("questions")

# scrape each question
for question in questions:
    # get question name and url
    name = question.text
    url = "https://leetcode.com" + question["href"]
    print(name)

    # get question page
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # get question description
    description = soup.find("div", class_="question-description")
    if description is not None:
        description = description.text

    # get question code
    code = soup.find("div", class_="question-content")
    if code is not None:
        code = code.text

    # get question tags
    tags = soup.find("div", class_="question-tags")
    if tags is not None:
        tags = tags.text

    # write question to file
    with open("questions/" + name + ".txt", "w") as f:
        f.write(name + "\n\n")
        if description is not None:
            f.write(description + "\n\n")
        if code is not None:
            f.write(code + "\n\n")
        if tags is not None:
            f.write(tags + "\n\n") 

# close selenium
driver.close()

# search for questions
if len(sys.argv) > 1:
    for root, dirs, files in os.walk("questions"):
        for file in files:
            with open(os.path.join(root, file), "r") as f:
                if re.search(sys.argv[1], f.read(), re.IGNORECASE):
                    print(file)
