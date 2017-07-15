import requests
from bs4 import BeautifulSoup

root_url = 'https://philadelphia.eat24hours.com'
index_url = root_url + '/university-city/all-cuisines'

def getVendorName(vendor):
    return vendor.contents[3].getText().rstrip()

def getRegion(div):
# Only works with one region at a time
    return div[0].select('span#content_list_results_add')[0].getText()

# def getCategories(vendor):
#     return vendor.contents[7].getText().strip('\n').split(',')

def getDeliveryFee(vendor):
# Returns a list of the info, perhaps can be used later for csv
    return vendor.contents[11].getText().split()

# def getAddress(vendor, div):
#     return vendor.contents[3].getText()


def getVendorInfo():
    response = requests.get(index_url)
    html = BeautifulSoup(response.text, 'html.parser')
    div = html.select('#contents_list')
    region = getRegion(div)

    for vendor in div[0].select('div.content_list_restaurant_left'):
        print getVendorName(vendor)
        print region
        # print getCategories(vendor)
        print getDeliveryFee(vendor)

getVendorInfo()
