from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def find_header_tag_index(tags, item_grade):
    output = [idx for idx, tag in enumerate(tags) if tag.parents.contents[0] == item_grade]
    return output[0]

def find_grade_to_search(grade, supp_code):
    if supp_code != '':
        if supp_code == '07' or '08':
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

barcode = "01851463006311146064"
barcode_len = len(barcode)
coin_num = barcode[0:5]
coin_grade = barcode[6:7]
coin_sup_cond = ''
coin_invoice_num = ''
coin_line_item_num = ''

if barcode_len == 20:
    coin_sup_cond = barcode[8:9]
    coin_invoice_num = barcode[10:16]
    coin_line_item_num = barcode[17:19]
if barcode_len == 18:
    coin_invoice_num = barcode[8:14]
    coin_line_item_num = barcode[15:17]
if barcode_len == 16:
    coin_invoice_num = barcode[8:13]
    coin_line_item_num = barcode[14:15]


print(coin_num)
url = 'https://www.ngccoin.com/redirects/coin-explorer/{coin_num}/'
driver.get(url)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

coin_data = {}
data_list = soup.find('ul', {'class': 'ce-coin__specs-list'})
# first element is the product desc
# third element is the product mintage
list_elements = data_list.find_all('li')

# for the ngc data table, get the price grade you're looking for using the barcode
# get the header index by finding the grade you're looking for using the value
# get ngc census value at header index
grade_scroller_table = soup.find(
    'div', {'id': 'gradeScroller'})
grade_to_search = find_grade_to_search(coin_grade, coin_sup_cond)
headers = grade_scroller_table.find_all('th')
header_index = find_header_tag_index(headers, grade_to_search)

print(list_elements)
driver.close()
