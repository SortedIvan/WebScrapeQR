import requests
import json
import uuid

from utility_data.rental_listing_data import RentalListing
from bs4 import BeautifulSoup


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,da;q=0.7",
    "content-type": "application/json",
    "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Google Chrome\";v=\"108\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "utm_source=objectomschrijving; utm_medium=huislijn.nl; PHPSESSID=123fff58b6035a81b31dde98982e6a04; cookieconsent_status=allow; newsletter-modal-progress=3; g_state={\"i_p\":1673031487744,\"i_l\":3}; __cf_bm=7ngBfiGyeIJB_NYV3aT.rmozyhRMIGik3BL1Z8UXDmI-1672431521-0-ASZI7ctuDHMvnZf78sYztv35HNJlebUsiyx7+zdKwTuybWLOVWrjPF9ze2pw50hQdv1NtDPWFYTpIL/Z1kYlLHEIVVIv6leDgfgvBWqPqxwqbuck22xo0Y8VG1z6oUeQiz6BSMeObDfj+ALdCidsPNI=",
    "Referer": "https://www.huurstunt.nl/huren/eindhoven/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

body = "{\"force\":false,\"location\":{\"location\":\"Eindhoven\",\"distance\":null,\"suggestType\":\"city\",\"suggestId\":974,\"neighborhoodSlug\":null,\"streetSlug\":null,\"districtSlug\":null},\"price\":{\"from\":0,\"till\":100000},\"properties\":{\"rooms\":0,\"livingArea\":0,\"deliveryLevel\":null,\"rentalType\":null,\"outside\":[]},\"page\":1,\"sorting\":\"datum-af\",\"resultsPerPage\":21}"


def GetHuurstuntDataJson(city):
    headers['Referer'] = f"https://www.huurstunt.nl/huren/{city}/"
    page = requests.post("https://www.huurstunt.nl/public/api/search", headers = headers, data = body)
    return page.json()

def GetHuurstuntListingInfo(city):
    return json.loads(json.dumps(GetHuurstuntDataJson(city)))

def GetAllRentalListings(city):
    listings = GetHuurstuntListingInfo(city)['data']['rentals']
    all_listings = []
    for i in range(len(listings)):
        if listings[i]['isNew'] == True:
            listing_type = listings[i]['type']
            listing_street = listings[i]['street']
            listing_rooms = listings[i]['rooms']
            listing_price = listings[i]['price']
            listing_url = "https://www.huurstunt.nl" + listings[i]['url']
            listing_sqm = listings[i]['floorspace']
            listing_full_address = listings[i]['city'] + " " + listings[i]['street']
            listing_title = listings[i]['title']

            all_listings.append(
                RentalListing(
                    str(uuid.uuid4()),
                    listing_type,
                    listing_title,
                    "Today",
                    listing_price,
                    listing_sqm,
                    listing_rooms,
                    "None",
                    listing_url,
                    listing_full_address
                )
            )
    return all_listings

all_listings = GetAllRentalListings("eindhoven")

for listing in all_listings:
    print("-----------------------------------")
    print(listing.listingId)
    print(listing.listingSqm)
    print(listing.listingName)
    print(listing.listingUrl)
    print(listing.listingPrice)
    print(listing.listingAdress)
    print(listing.listingRooms)
    print("-----------------------------------")
