#!/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.support.ui import WebDriverWait
import sys

import time

from fake_useragent import UserAgent

import boto3

if(len(sys.argv) < 2):
    print("No argument given")
    print("Usage: ./ksl_scraper.py <search keyword>")
    quit()
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--nogpu")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1280,1280")
chrome_options.add_argument("--no-sandbox")

chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

ua = UserAgent()
userAgent = ua.random

# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.implicitly_wait(7)

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})

# driver.get("https://classifieds.ksl.com")
# print(driver.title)
# search_box = driver.find_element("xpath", "//input[@aria-label='Search classifieds']")

# search_box.send_keys("gpu")
# search_box.send_keys(Keys.ENTER)
print('sleeping for 3 seconds')

time.sleep(3)
#breakpoint()
print('Getting classifieds page for \'{}\''.format(sys.argv[1]))

driver.get("https://classifieds.ksl.com/search/keyword/{}".format(sys.argv[1]))

# lnks=driver.find_elements("tag name", 'a')



#breakpoint()
#time.sleep(3)

print('Geting links')

lnks = driver.find_elements("xpath", "//div[@class='item-info-title-link']/a")
#breakpoint()
#time.sleep(3)
#driver.implicitly_wait(10)

# print(driver.page_source.encode("utf-8"))
print('Number of links = ' + str(len(lnks)))
#breakpoint()
print('KSL Listings:')
# s3 = boto3.resource("s3")

client = boto3.client('sqs')


# bucket_name = "bennion-selenium"

file_name = "selenium-log-" + time.strftime("%Y-%m%d-%H%M%S") + ".txt"
links_string = ""
for lnk in lnks:
   with open(file_name, "a") as file:
    file.write(lnk.text + "\n")
   print(lnk.text)
   links_string += lnk.text + "\n"
# s3.Bucket(bucket_name).upload_file(file_name, file_name)
message = client.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/321965405476/s3_writer_sqs',
        MessageBody=("This was sent on: " + time.strftime("%Y-%m%d-%H%M%S") + links_string)
        )

#breakpoint()
driver.quit()

# print(driver.find_element("xpath", "//div[@class='item-info-title-link']/a").text)
