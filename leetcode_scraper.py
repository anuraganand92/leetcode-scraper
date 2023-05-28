from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set the path to the ChromeDriver executable
webdriver_path = 'C:/Users/Anurag/Downloads/chromedriver_win32/chromedriver.exe'

# Create ChromeOptions instance and set desired options
options = Options()
options.add_argument("--ignore-certificate-errors")

# Create an instance of Chrome WebDriver
driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

# Open LeetCode website
driver.get("https://leetcode.com/problemset/all/")

# Find all the question links
links = driver.find_elements(By.CLASS_NAME, "title-cell__grippy")

# Extract the URLs and save them in a text file
with open("leetcode_links.txt", "w") as file:
    for link in links:
        url = link.get_attribute("href")
        file.write(url + "\n")

# Close the browser
driver.quit()
