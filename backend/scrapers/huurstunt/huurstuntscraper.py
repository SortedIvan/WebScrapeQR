import requests
import json
import uuid
from bs4 import BeautifulSoup
from utility_data.rental_listing_data import RentalListing
from requests_html import HTMLSession

base_url = "https://www.huurstunt.nl"
url = "https://www.huurstunt.nl/public/api/search"

payload_json = {
  "force": False,
  "location": {
    "location": "Nederland",
    "distance": None,
    "suggestType": "country",
    "suggestId": None,
    "neighborhoodSlug": None,
    "streetSlug": None,
    "districtSlug": None
  },
  "price": {
    "from": 0,
    "till": 100000
  },
  "properties": {
    "rooms": 0,
    "livingArea": 0,
    "deliveryLevel": None,
    "rentalType": None,
    "outside": []
  },
  "page": 1,
  "sorting": "datum-af",
  "resultsPerPage": 21
}


headers = {
  "accept-encoding": "gzip, deflate",
  'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,da;q=0.7',
  'Origin': 'https://www.huurstunt.nl',
  'Referer': 'https://www.huurstunt.nl/huren/eindhoven/',
  'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
  'Content-Type': 'application/json',
  'Cookie': 'PHPSESSID=d9c5ad595b1e00dc88ea8224a6ceb308'
}


def GetAllListingJsons():
    all_jsons = []
    for i in range(1,30): # We check the first 50 pages
        payload_json['page'] = i
        payload = json.dumps(payload_json)
        response = requests.request('POST', url, headers=headers, data=payload).json()
        all_jsons.append(response)
    return all_jsons


def GetAllListings():
    all_jsons = GetAllListingJsons()
    all_listings = []
    for i in range(len(all_jsons)):
        for listing in all_jsons[i]['data']['rentals']:
            if listing['isNew'] != True:
                continue
            if listing['isBlurred']:
                continue
            if listing['status'] == 5:
                continue
            if listing['city'] == "Zaandam" or listing['city'] == 'Westzaan' or listing['city'] == 'Heemskerk' or listing['city'] == 'Wormerveer' or listing['city'] == 'Assendelft':
                listing['city'] = "gemeente-zaanstad"

            if listing['city'] == "Den Haag":
                listing['city'] = 'den-haag'

            if listing['city'] == 'Nootdorp':
                listing['city'] = 'zoetermeer'

            if listing['city'] == 'Vlijmen':
                listing['city'] = 'den-bosch'

            if listing['city'] == 'Den Bosch':
                listing['city'] = 'den-bosch'

            try:
                listing['city'] = listing['city'].lower() # All cities should be one format
            except:
                print("listing city does not exist")

            rental = RentalListing(
                str(uuid.uuid4()),
                listing['type'],
                listing['title'],
                "Today",
                listing['price'],
                listing['floorspace'],
                listing['rooms'],
                "None",
                base_url + listing['url'],
                listing['city'] + " " + listing['street'],
                listing['city'],
                listing['image']['src']
            )
            all_listings.append(rental)
    return all_listings

