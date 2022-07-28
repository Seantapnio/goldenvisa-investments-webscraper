from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import pandas as pd
import os
import sys
import time

application_path = os.path.dirname(sys.executable)
now = datetime.now()
month_day_year = now.strftime("%m%d%Y")

website = "https://www.goldenvisas.com/investment/portugal"
path = "/Users/seant/chromedriver_win32/chromedriver"

# Mandatory step for Sel.V4
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)
url = "https://www.goldenvisas.com/investment?location=portugal&paged={page}"

location = []
price = []
links = []

for page in range(1, 3):

    driver.get(url.format(page=page))
    containers = driver.find_elements(by="xpath", value='//div[@class="list"]')

    driver.maximize_window()
    time.sleep(1)

    # Headless mode
    # option = Options()
    # option.headless = True

    for container in containers:
        locations = container.find_element(by="xpath", value='./a/h3[@itemprop="name"]/span[@class="location"]').text
        prices = container.find_element(by="xpath", value='./a/h3[@itemprop="name"]/span[@class="price"]').text
        link = container.find_element(by="xpath", value='./a').get_attribute("href")
        location.append(locations)
        price.append(prices)
        links.append(link)

driver.quit()
my_dict = {'location': location, 'price': price, 'links': links}
print(my_dict)
df_headline = pd.DataFrame(my_dict)

file_name = f'goldenvisa-investment-{month_day_year}.csv'
final_path = os.path.join(application_path, file_name)

df_headline.to_csv(final_path)