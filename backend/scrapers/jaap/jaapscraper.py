import requests
from bs4 import BeautifulSoup
from utility_data.rental_listing_data import RentalListing
import uuid
import re

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
url_base = 'https://www.jaap.nl/huurhuizen'

def GetJaapHtml(page):
    if page == 1:
        full_url = 'https://www.jaap.nl/huurhuizen'
    else: full_url = f'https://www.jaap.nl/huurhuizen/?p={page}'
    return requests.get(full_url, headers=headers)

def ConvertJaapHtml():
    results = []
    soups = []
    #TODO: Change page not be a constant, for jaap we need the first 20 pages
    # since we are scraping the entirety of the netherlands
    for i in range(1, 20):
        results.append(GetJaapHtml(i))
    for i in range(len(results)):
        soups.append(BeautifulSoup(results[i].text, "html.parser"))
    return soups

def GetJaapSoups():
    jaap_soups = ConvertJaapHtml()
    individual_listings = []

    for i in range(len(jaap_soups)):
        main_content_tab = jaap_soups[i].find('div', attrs = {'class': 'listings_grid'})
        listings = main_content_tab.find_all('app-listing-item')
        for listing in listings:
            individual_listings.append(listing)
    return individual_listings

def GetAllListings():
    listings = []
    listing_soups = GetJaapSoups()

    for i in range(len(listing_soups)):
        price_and_image = listing_soups[i].find('section', attrs = {'class':'image-wrapper'})
        rest_info = listing_soups[i].find('section', attrs = {'class': 'item-content'})
        
        if price_and_image.find('div', attrs = {'class': 'sticker'}).text.strip() != "Nieuw":
            continue
        
        image_obj = price_and_image.find('img')

        if image_obj.has_attr('src'):
            image_url = image_obj['src']

        listing_price = price_and_image.find('span', attrs = {'class': 'price'}).text.strip()

        street_title = rest_info.find('div', attrs = {'class': 'straat'}).text.strip()
        street_address = rest_info.find('div', attrs = {'class': 'gemeente'}).text.strip()

        print(street_address)
        
print(GetJaapHtml(1).text)