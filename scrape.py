import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import requests
import time
from bs4 import BeautifulSoup

# For Philadelphia neighborhoods only; change root_url to expand area
root_url = 'https://philadelphia.eat24hours.com'

# Retrieve the links to the neighborhoods in Philadelphia
def getLinks(driver):
    source = driver.page_source
    html = BeautifulSoup(source, 'html.parser')
    neighborhoodList = html.select('.column_list')[2]
    neighborhoods = []
    for a in neighborhoodList.findAll('a', href=True):
        neighborhoods.append(a['href'])
    return neighborhoods

# Go to neighborhood's page that lists all restaurants
def navigate(link, driver):
    index_url = link + '/all-cuisines'
    driver.get(index_url)

# Scroll down the page to load the vendors
def scrollDown(driver):
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight

# Get the address of the vendor
def getAddressPhone(driver):
    source = driver.page_source
    html = BeautifulSoup(source, 'html.parser')
    address = html.find('span', {'itemprop': 'streetAddress'}).contents[0]
    phoneNum = html.find('span', {'itemprop': 'telephone'}).contents[0]
    return [address, phoneNum]

# Get the delivery minimum and delivery fee for that vendor
def getDeliveryFee(vendor):
    info = vendor.select('.content_list_rest_info')[0].getText().split()
    deliveryMin = info[2]
    deliveryFee = info[5]

    if '$' not in deliveryMin:
        deliveryMin = ''
    if '$' not in deliveryFee:
        deliveryFee = ''

    info = [deliveryMin, deliveryFee]
    return info

def output2csv(driver, wr):
    source = driver.page_source
    html = BeautifulSoup(source, 'html.parser')
    vendors = html.find_all('div', class_= 'content_list_restaurant')
    for vendor in vendors:
        if vendor.find('a', class_= 'rest_menu').get('title'):
            vendorId = vendor['id'].split('_')[1]
            name = vendor.find('a', class_= 'rest_menu').get('title')
            latlng = vendor.get('latlng').split(':')[1].strip('()').split(',')
            city = html.find('span', {'id': 'content_list_results_add'}).contents[0].split(',')[0]
            fees = getDeliveryFee(vendor)
            rating = vendor.find('div', class_='crating').get('class')[3].split('-')[1]
            if vendor.find('span', class_='rating_count').contents:
                reviews = vendor.find('span', class_='rating_count').contents[0].split()[0]
            else:
                reviews = '0'
            navigate(vendor.find('a', class_= 'rest_menu').get('href'), driver)
            addressPhone = getAddressPhone(driver)
            address = addressPhone[0]
            phone = addressPhone[1]

            data = [vendorId, name, phone, address, city, latlng[0], latlng[1], fees[0], fees[1], rating, reviews]
            wr.writerow(data)
            print data
            driver.execute_script("window.history.go(-1)")

def main():
    driver = webdriver.PhantomJS(executable_path=r'C:\Users\addu\node_modules\phantomjs-prebuilt\lib\phantom\bin\phantomjs')
    driver.implicitly_wait(15)
    driver.get(root_url)

    links = getLinks(driver)
    with open('eat24_scrape.csv', 'wb') as csvfile:
        fields = [ 'ID', 'Name', 'Phone Number', 'Address', 'City', 'Latitude', 'Longitude', 'Delivery Min', 'Delivery Fee', 'Rating', 'Reviews' ]
        wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        wr.writerow(fields)
        for link in links:
            if link != 'https://philadelphia.eat24hours.com/girard -state':
                navigate(link, driver)
                scrollDown(driver)
                output2csv(driver, wr)

###############################

main()
