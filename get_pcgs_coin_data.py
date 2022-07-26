from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = 'https://www.pcgs.com/cert/43927099'
path = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(executable_path=path)

driver.get(url)

html = driver.page_source


soup = BeautifulSoup(html, "html.parser")

print(soup)

driver.close()
