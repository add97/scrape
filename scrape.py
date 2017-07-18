import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from selenium import webdriver
# from selenium.webdriver.common.keys import keys

import csv
import requests
from bs4 import BeautifulSoup

root_url = 'https://philadelphia.eat24hours.com'
index_url = root_url + '/university-city/all-cuisines'
scrapeList = []

def getVendorName(vendor):
    return [vendor.contents[3].getText().strip()]

def getRegion(div):
    return div[0].select('span#content_list_results_add')[0].getText().split()

# def getCategories(vendor):
#     return vendor.contents[7].getText().strip('\n').split(',')

# def getAddress(vendor, div):
#     return vendor.contents[3].getText()

def getDeliveryFee(vendor):
    return vendor.contents[11].getText().split()

def getRating(vendor):
    ratingStr = vendor.contents[5].findAll()[0]['class'][2]
    rating = ratingStr.split('-')[1]
    return [rating]

def getVendorInfo():
    response = requests.get(index_url)
    html = BeautifulSoup(response.text, 'html.parser')
    div = html.select('#contents_list')

    for vendor in div[0].select('div.content_list_restaurant_left'):
        name = getVendorName(vendor)
        region = getRegion(div)
        fees = getDeliveryFee(vendor)
        rating = getRating(vendor)
        data = name + region + fees + rating

        scrapeList.append(data)

def output2csv():
    fields = [ 'Vendor', 'City', 'Neighborhood', 'Delivery Min', 'Delivery Fee', 'Rating' ]
    with open('eat24_scrape.csv', 'wb') as csvfile:
        wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        wr.writerow(fields)
        for data in scrapeList[1::]:
            data[1] = data[1].rstrip(',')
            data[2] = data[2].rstrip(',')
            row = [data[0], data[1], data[2]]
            if data[5].find('$') == -1:
                data[5] = ''
            if data[8].find('$') == -1:
                data[8] = ''
            if data[len(data)-1].find('0') == -1:
                data[len(data)-1] == ''
            wr.writerow([data[0], data[1], data[2], data[5], data[8], data[len(data)-1]])

getVendorInfo()
output2csv()

########################

dir = os.path.dirname('C:\Users\addu\scrape')
chrome_driver_path = dir + "\chromedriver.exe"

driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.maximize_window()

driver.get('https://philadelphia.eat24hours.com/')
neighborhoodLinks = driver.find_elements_by_xpath("//table[@class='column_list']/a[@href]")
print neighborhoodLinks
for neighborhood in neighborhoodLinks:
    print neighborhood.get_attribute('href')
