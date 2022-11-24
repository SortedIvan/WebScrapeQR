# Possibly rentalist
import requests
from bs4 import BeautifulSoup
import re


class FundaListing():
    def __init__(self, url, houseName, houseLocation, housePrice, propertyFeatures):
        self.url = url
        self.houseName = houseName
        self.houseLocation = houseLocation
        self.housePrice = housePrice
        self.propertyFeatures = propertyFeatures

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
def get_funda_html(city, price_low, price_high, km, page_nr):
    if page_nr == 1:
        full_url = f'https://www.funda.nl/huur/gemeente-{city}/{price_low}-{price_high}/'
        return requests.get(full_url, headers=headers)
    full_url = f'https://www.funda.nl/huur/gemeente-{city}/{price_low}-{price_high}/p{page_nr}/'
    return requests.get(full_url, headers=headers)

def get_funda_soups(city, priceLow, priceHigh, km):
    results = []
    soups = []
    for i in range(1, 10):
        results.append(get_funda_html(city, priceLow, priceHigh,km, i))
    for i in range(len(results)):
        soups.append(BeautifulSoup(results[i].text, "html.parser"))
    return soups

def create_funda_listings(soup):
    funda_listings = []
    property_area = ""
    room_amount = ""
    available_from = ""
    search_content_output = soup.find('div', attrs={'class': 'search-content-output'})
    listings = search_content_output.find_all('li', attrs = {'class': 'search-result'})
    for i in range(len(listings)):
        listing_link = listings[i].find('a', attrs = {'data-object-url-tracking': 'resultlist'}, href = True)['href']
        title_street = listings[i].find('h2', attrs = {'class' : 'search-result__header-title fd-m-none'}).text.strip()
        postcode = listings[i].find('h4', attrs = {'class' : 'search-result__header-subtitle fd-m-none'}).text.strip()
        price = listings[i].find('span', attrs = {'class' : 'search-result-price'}).text.strip()
        further_info = listings[i].find('ul', attrs = {'class': 'search-result-kenmerken'})
        try:
            further_info_subelements = further_info.find_all('li')
            try:
                property_area = further_info_subelements[0].text.strip()
            except IndexError:
                print("")
            try:
                room_amount = further_info_subelements[1].text.strip()
            except IndexError:
                print("")
            try:
                available_from = further_info_subelements[2].text.strip()
            except IndexError:
                print("")
        except:
            further_info = []
        
        property_features = [("property_area: " + property_area), ("room_amount: " + room_amount), ("available_from: " + available_from)]
        funda_listings.append(FundaListing(
            listing_link,
            title_street,
            title_street + " " + postcode,
            price,
            property_features
        ))
    return funda_listings

def GetAllFundaListings(city, priceLow, priceHigh, km):
    soups = get_funda_soups(city, priceLow, priceHigh, km)
    all_listings_pages = []
    all_listings_seperate = [] 
    for i in range(len(soups)):
        all_listings_pages.append(create_funda_listings(soups[i]))
    for x in range(len(soups)):
        for y in range(len(all_listings_pages[x])):
            all_listings_seperate.append(all_listings_pages[x][y])
    return all_listings_seperate


def PrintResults():
    listings = GetAllFundaListings("eindhoven", 200, 1500, 15)
    for i in range(len(listings)):
        print(listings[i].url)
        print(listings[i].houseName)
        print(listings[i].houseLocation)
        print(listings[i].housePrice)
        print(listings[i].propertyFeatures)
        print("------------------------------------------------------------------------")

PrintResults()