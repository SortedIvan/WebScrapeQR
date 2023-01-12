import requests
import json
import uuid
from utility_data.rental_listing_data import RentalListing

body_part_one = "{\"force\":false,\"location\":{\"location\":\"Nederland\",\"distance\":null,\"suggestType\":\"city\",\"suggestId\":null,\"neighborhoodSlug\":null,\"streetSlug\":null,\"districtSlug\":null},\"price\":{\"from\":0,\"till\":100000},\"properties\":{\"rooms\":0,\"livingArea\":0,\"deliveryLevel\":null,\"rentalType\":null,\"outside\":[]},\"page\":"
body_part_two = ",\"sorting\":\"datum-af\",\"resultsPerPage\":21}"

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
    "referer": "https://www.huurstunt.nl/huren/nederland/",      
    "Referrer-Policy": "strict-origin-when-cross-origin"
}


def GetHuurstuntDataJson(page_count):
    final_body = body_part_one + str(page_count) + body_part_two
    serv_headers = headers
    if page_count != 0:
        serv_headers['referer'] = "https://www.huurstunt.nl/huren/nederland/" + "p" + str(page_count + 1)
    page = requests.post("https://www.huurstunt.nl/public/api/search", headers = serv_headers, data = final_body)
    return page.json()

def GetHuurstuntListingInfo():
    all_listing_info = []
    for page in range(10):
        all_listing_info.append(json.loads(json.dumps(GetHuurstuntDataJson(page))))
    return all_listing_info

def GetAllRentalListings(city):
    all_listings = []
    listing_info_raw = GetHuurstuntListingInfo()
    for i in range(len(listing_info_raw)):
        print(listing_info_raw[i])
        all_listings.append(listing_info_raw[0]['data']['rentals'])

    complete_listings = []
    for i in range(len(all_listings)):
        for k in range(len(all_listings[i])):
            if all_listings[i][k]['isNew'] == True:
                listing_type =  all_listings[i][k]['type']
                listing_street =  all_listings[i][k]['street']
                listing_rooms =  all_listings[i][k]['rooms']
                listing_price =  all_listings[i][k]['price']
                listing_url = "https://www.huurstunt.nl" +  all_listings[i][k]['url']
                listing_sqm =  all_listings[i][k]['floorspace']
                listing_full_address =  all_listings[i][k]['city'] + " " +  all_listings[i][k]['street']
                listing_title =  all_listings[i][k]['title']

                complete_listings.append(
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
                        listing_full_address,
                        city
                    )
                )

    return complete_listings
