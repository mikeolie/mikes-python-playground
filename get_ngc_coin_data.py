
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = 'https://www.ngccoin.com/redirects/coin-explorer/019189/'
path = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(executable_path=path)

driver.get(url)

html = driver.page_source


soup = BeautifulSoup(html, "html.parser")
grade_table = soup.find(
    'table', {'class': 'ccg-data-table ccg-data-table--grade'})


print(soup)

driver.close()
