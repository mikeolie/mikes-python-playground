from bs4 import BeautifulSoup
import re
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def find_header_tag_index(tags, item_grade):
    output = [idx for idx, tag in enumerate(
        tags) if tag.text == item_grade]
    return output[0]


def find_grade_to_search(grade, sup_code):
    if sup_code != '':
        if sup_code == '07' or sup_code == '08':
            return f'{grade}+'
    return grade


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--nogpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_experimental_option(
    "excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

ua = UserAgent(verify_ssl=False)
user_agent = ua.random
chrome_options.add_argument(f'user-agent={user_agent}')
path = '/usr/local/bin/chromedriver'

driver = webdriver.Chrome(service=Service(path), options=chrome_options)

barcode = '01206166011916066001'
barcode_len = len(barcode)
coin_num = barcode[:6]
coin_grade = barcode[6:8]
coin_sup_cond = ''
coin_invoice_num = ''
coin_line_item_num = ''

if barcode_len == 20:
    coin_sup_cond = barcode[8:10]
    coin_invoice_num = barcode[10:17]
    coin_line_item_num = barcode[-3:]
if barcode_len == 18:
    coin_invoice_num = barcode[8:14]
    coin_line_item_num = barcode[-3:]
if barcode_len == 16:
    coin_invoice_num = barcode[8:14]
    coin_line_item_num = barcode[-2:]

url = f'https://www.ngccoin.com/redirects/coin-explorer/{coin_num}/'
driver.get(url)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

coin_data = {}
data_list = soup.find('ul', {'class': 'ce-coin__specs-list'})
# first element is the product desc
# third element is the product mintage
list_elements = data_list.find_all('li')
for list_element in list_elements:
    raw_list_string = list_element.text
    data = re.sub(r'\n', "", raw_list_string).split(":")
    key = data[0]
    value = data[1]
    coin_data[key] = value


# for the ngc data table, get the price grade you're looking for using the barcode
# get the header index by finding the grade you're looking for using the value
# get ngc census value at header index
grade_scroller_table = soup.find(
    'div', {'id': 'gradeScroller'})
grade_to_search = find_grade_to_search(coin_grade, coin_sup_cond)
headers = grade_scroller_table.find_all('th')
ngc_grade_index = find_header_tag_index(headers, grade_to_search)


table_body = grade_scroller_table.select_one(
    '#gradeScroller > div > table > tbody')
ngc_census_row = table_body.find_all('tr')[2]
ngc_census_pop = ngc_census_row.find_all('td')[ngc_grade_index].text
coin_data['pop'] = ngc_census_pop


coin_image_url = f'https://www.ngccoin.com/certlookup/{coin_invoice_num}-{coin_line_item_num}/{coin_grade}'
driver.get(coin_image_url)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
images = []
image_containers = soup.find_all('div', {'class': 'certlookup-images-item'})
for image_container in image_containers:
    image_link = image_container.select_one("a")['href']
    images.append(image_link)

coin_data['images'] = images
print(coin_data)
driver.close()
