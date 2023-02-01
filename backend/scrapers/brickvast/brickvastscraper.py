import requests
from bs4 import BeautifulSoup
import re
from utility_data.rental_listing_data import RentalListing
import uuid

brickvast_url = "https://en.brickvastgoed.nl/aanbod"

def GetBrickvastHtml():
    return requests.get(brickvast_url).text

def GetAllSoups():
    main_html = BeautifulSoup(GetBrickvastHtml())
    all_soups = []
    try:
        all_soups = main_html.find_all('a', attrs = {'class': 'item'})
    except:
        return []
    return all_soups

def GetAllBrickvastRentalListings():
    all_soups = GetAllSoups()
    all_listings = []
    for soup in all_soups:
        check_if_new = soup.find('div', attrs = {'class': 'overlay'})
        if not str(check_if_new.find('img')['src']).find("niuew"):
            continue
        
        url = "https://en.brickvastgoed.nl" + soup['href']
        description = soup.find('div', attrs = {'class':'description'})
        address_and_title = description.find('div', attrs = {'class': 'adres'}).find('small').text
        price = description.find('div', attrs = {'class':'price'}).text
        price_number_array = re.findall('\d+', price)
        price_number = int(''.join(price_number_array))
        image = "https://en.brickvastgoed.nl" + str(soup.find('div', attrs = {'class': 'image'}).find('img')['src'])

        print(url)
        print(address_and_title)
        print(price_number)
        print(image)
    
        rental = RentalListing(
            str(uuid.uuid4()),
            "room",
            address_and_title,
            "Today",
            price_number,
            0,
            "Unavailable",
            "None",
            url,
            address_and_title,
            "eindhoven",
            image
        )
        all_listings.append(rental)

    return all_listings
    