import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from selenium import webdriver
import csv
import requests
import time
from bs4 import BeautifulSoup

# For Philadelphia neighborhoods only; change root_url to expand area
root_url = 'https://philadelphia.eat24hours.com'

# Retrieve the links to the neighborhoods in Philadelphia
def getLinks():
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

# Get the name of the vendor
def getVendorName(vendor):
    name = [vendor.select('.rest_menu')[0].getText().strip()]
    return name

# Get the city and neighborhood of the vendors
def getRegion(div):
    region = div[0].select('span#content_list_results_add')[0].getText().split()
    city = region[0].rstrip(',')
    neighborhood = region[1].rstrip(',')
    region = [city, neighborhood]
    return region

# Get the delivery minimum and delivery fee for that vendor
def getDeliveryFee(vendor):
    info = vendor.contents[11].getText().split()
    print info
    deliveryMin = info[2]
    deliveryFee = info[5]

    if '$' not in deliveryMin:
        deliveryMin = ''
    if info[3] == 'Free':
        deliveryFee = ''

    info = [deliveryMin, deliveryFee]
    return info

# Get the rating (a multiple of 10)
def getRating(vendor):
    rating = [vendor.select('.rating_stars')[0].findAll()[0]['class'][3].split('-')[1]]
    return rating

# Get the number of reviews for a vendor
def getReviewCount(vendor):
    reviews = [vendor.contents[5].getText().strip().split()[0]]
    return reviews

def getVendorInfo():
    source = driver.page_source
    html = BeautifulSoup(source, 'html.parser')
    div = html.select('#contents_list')

    for vendor in div[0].select('div.content_list_restaurant_left'):
        if getVendorName(vendor) != ['']:
            name = getVendorName(vendor)
            region = getRegion(div)
            fees = getDeliveryFee(vendor)
            rating = getRating(vendor)
            reviews = getReviewCount(vendor)

            data = name + region + fees + rating + reviews
            return data

def output2csv(dataList):
    fields = [ 'Name', 'City', 'Neighborhood', 'Delivery Min', 'Delivery Fee', 'Rating', 'Reviews' ]
    with open('eat24_scrape.csv', 'wb') as csvfile:
        wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        wr.writerow(fields)
        for data in dataList:
            print data

            wr.writerow([data[0], data[1], data[2], data[5], data[8], data[len(data)-1]])

###############################

dir = os.path.dirname('C:\Users\addu\scrape')
chrome_driver_path = dir + "\chromedriver.exe"

# driver = webdriver.Chrome()
driver = webdriver.PhantomJS(executable_path=r'C:\Users\addu\node_modules\phantomjs-prebuilt\lib\phantom\bin\phantomjs')
driver.implicitly_wait(30)
driver.get(root_url)

links = getLinks()
for link in links:
    if link != 'https://philadelphia.eat24hours.com/girard -state':
        navigate(link, driver)
        scrollDown(driver)
        getVendorInfo()
        #output2csv()
