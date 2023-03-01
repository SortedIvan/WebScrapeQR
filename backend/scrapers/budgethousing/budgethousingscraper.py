from bs4 import BeautifulSoup
from utility_data.rental_listing_data import RentalListing
from utility.parser import ParseStringNumber
import requests
import re
import uuid



url = "https://budgethousing.nl/zoekresultaten/?filter_search_action%5B%5D=huur&adv6_search_tab=huur&term_id=134&term_counter=0&advanced_city=&filter_search_type%5B%5D=&aantal-kamers=&aantal-slaapkamers=&min-oppervlakte=&price_low_134=0&price_max_134=5000&submit=Search+for+properties"

def GetBudgetHousingSoup():
    html = requests.get(url).text
    return BeautifulSoup(html)


def GetBudgetHousingListings():
    soup = GetBudgetHousingSoup()
    individual_listing_soups = soup.find_all('div', attrs = {'class': 'property_listing'})

    rentals = []

    for listing_soup in individual_listing_soups:

        try:
            listing_url = listing_soup.find('a', href = True)['href']
        except:
            continue # Listing does not exist

        try:
            image_url = listing_soup.find('img')['src']
        except:
            image_url = "None"

        try:
            listing_title = listing_soup.find('h4').find('a', href = True)['href']
        except:
            listing_title = "None"

        try:
            listing_address = listing_soup.find('div', attrs = {'class': 'address'}).text.strip()
            postcode = listing_address[:6]
        except:
            listing_address = "None"

        try:
            listing_price = listing_soup.find('div', attrs = {'class':'property-price'}).text.strip()
            price_number_array = re.findall('\d+', listing_price)
            price_number = int(''.join(price_number_array))
        except:
            price_number = 0

        try:
            listing_rooms = listing_soup.find('div', attrs = {'class':'rooms'}).text.strip()
        except:
            listing_rooms = "None"

        try:
            listing_sqm = listing_soup.find('div', attrs = {'class':'size'}).text.strip()
            listing_sqm = re.findall('\d+', listing_sqm)
            listing_sqm = int(''.join(listing_sqm))
        except:
            listing_sqm = 0

        rental = RentalListing(
        str(uuid.uuid4()),
        "Appartment",
        listing_title,
        "Today",
        ParseStringNumber(str(price_number)),
        ParseStringNumber(str(listing_sqm)),
        ParseStringNumber(str(listing_rooms)),
        "None",
        listing_url,
        listing_address,
        "eindhoven",
        postcode,
        image_url
        )
        rentals.append(rental)

    return rentals


listings = GetBudgetHousingListings()
def print_all_listings():
    for listing in listings:
        print("------------------------------------------")
        print(listing.listingType)
        print(listing.listingName)
        print(listing.listingDate)
        print(listing.listingPrice)
        print(listing.listingSqm)
        print(listing.listingRooms)
        print(listing.listingExtraInfo)
        print(listing.listingUrl)
        print(listing.listingAdress)
        print(listing.listingPostcode)
        print(listing.imageUrl)
print_all_listings()