import re
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--nogpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

ua = UserAgent(verify_ssl=False)
user_agent = ua.random
chrome_options.add_argument(f'user-agent={user_agent}')
print(user_agent)
path = '/usr/local/bin/chromedriver'

driver = webdriver.Chrome(service=Service(path), options=chrome_options)
url = 'https://www.pcgs.com/cert/43927099'

driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
data_table = soup.find('table', {'class': 'table table-condensed'})
coin_data = {}
soup_rows = data_table.find_all('tr')
for soup_row in soup_rows:
    row_data = soup_row.find_all('td')
    row_label = re.sub('\W+', '', row_data[0].find(text=True))
    row_value = re.sub('\W+', '', row_data[1].find(text=True))
    if row_label == 'Population' or row_label == 'PCGS' or row_label == 'PCGSPriceGuide':
        row_value = soup_row.find('a').text
    coin_data[row_label] = row_value

img_container = soup.find(
    'div', {'class': 'col-xs-12 col-md-5 margin-top-min text-center'})
img = img_container.find('img')['src']
coin_data['images'] = [img]
header_xpath = '/html/body/main/div[1]/div[3]/div[2]/h1'

print(coin_data)
driver.close()
