import requests
from bs4 import BeautifulSoup

jaap_listing_urls = []


class JaapListing():
    def __init__(self, url, houseName, houseLocation, housePrice, propertyFeatures):
        self.url = url
        self.houseName = houseName
        self.houseLocation = houseLocation
        self.housePrice = housePrice
        self.propertyFeatures = propertyFeatures

def get_jaap_urls():
    with open('jaap_nl_areas.txt') as my_file:
        for line in my_file:
            jaap_listing_urls.append(line[:-2])
        return jaap_listing_urls
 

def match_string_to_url(name, urls):
    for i in range(len(urls)):
        if urls[i].find(name) != -1:
            return urls[i]
    return ""


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
def get_jaap_html(city, price_low, price_high, km, page_nr):
    jaap_listing_urls = get_jaap_urls()
    url = match_string_to_url(city, jaap_listing_urls)
    full_url = f'https://www.jaap.nl/huurhuizen/{url}/+{km}km/{price_low}-{price_high}/p{page_nr}'
    print(full_url)
    return requests.get(full_url, headers=headers)


def get_jaap_soups(city, priceLow, priceHigh, km):
    results = []
    soups = []
    for i in range(10):
        results.append(get_jaap_html(city, priceLow, priceHigh,km,i))
    for i in range(len(results)):
        soups.append(BeautifulSoup(results[i].text, "html.parser"))
    return soups


def get_raw_jaap_listings(city, priceLow, priceHigh, km):
    soups = get_jaap_soups(city, priceLow, priceHigh, km)
    rawlistings = []
    for i in range(len(soups)):
        list_of_results = soups[i].find('div', attrs={'class': 'property-list'})
        actual_listings = list_of_results.find_all('div', attrs= {'class' : 'property'})
        rawlistings.append(actual_listings)
    return rawlistings

def TestSoup():
    jaap_listings = []
    result = BeautifulSoup(get_jaap_html("eindhoven", 100, 1000, 10, 1).text, "html.parser")
    newResult = result.find('div', attrs={'class': 'property-list'})
    listings = newResult.find_all('div', attrs= {'class' : 'property'})
    all_features = []
    for i in range(len(listings)):
        if listings[i].find('a', attrs = {'class': 'property-inner'}) is not None:
            url = listings[i].find('a', attrs = {'class' : 'property-inner'}, href = True)['href']
        if listings[i].find('div', attrs = {'class': 'property-info'}) is not None:
            property_info_list = listings[i].find('div', attrs = {'class': 'property-info'})
            property_name = property_info_list.find('h2', attrs = {'class' : 'property-address-street'}).text
            property_location = property_info_list.find('div', attrs = {'class' : 'property-address-zipcity'}).text
            property_price = property_info_list.find('div', attrs = {'class' : 'property-price'}).text
            if (property_info_list.find_all('div', attrs = {'class': 'property-feature'}) != None):
                property_features = property_info_list.find_all('div', attrs = {'class': 'property-feature'})
                for i in range(len(property_features)):
                    all_features.append(property_features[i].text)
                propertyFeatures = all_features
        jaap_listings.append(
            JaapListing(
                url,
                property_name,
                property_location,
                property_price,
                propertyFeatures
            )
        )
    return jaap_listings


jaap_listings = TestSoup()
for i in range(len(jaap_listings)):
    print("-----------------------------------------------------------------------------------------------------")
    print(jaap_listings[i].url)
    print(jaap_listings[i].houseName)
    print(jaap_listings[i].houseLocation)
    print(jaap_listings[i].housePrice)
    print(jaap_listings[i].propertyFeatures)
