from bs4 import BeautifulSoup
from utility_data.rental_listing_data import RentalListing
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
            listing_address = listing_soup.find('div', attrs = {'class': 'address'}).text
            if not listing_address.find("Eindhoven"):
                continue
        except:
            listing_address = "None"

        try:
            listing_price = listing_soup.find('div', attrs = {'class':'property-price'}).text
            price_number_array = re.findall('\d+', listing_price)
            price_number = int(''.join(price_number_array))
        except:
            price_number = 0

        try:
            listing_rooms = listing_soup.find('div', attrs = {'class':'rooms'}).text
        except:
            listing_rooms = "None"

        try:
            listing_sqm = listing_soup.find('div', attrs = {'class':'size'}).text
        except:
            listing_sqm = 0

        rental = RentalListing(
        str(uuid.uuid4()),
        "rental",
        listing_title,
        "Today",
        price_number,
        listing_sqm,
        listing_rooms,
        "None",
        listing_url,
        listing_address,
        "eindhoven",
        image_url
        )
        rentals.append(rental)

    return rentals
