import requests
from bs4 import BeautifulSoup
import json

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


def GetHuurstuntDataJson():
    page = requests.post("https://www.huurstunt.nl/public/api/search", headers = headers, data = body)
    return page.json()

def GetHuurstuntProductInfo():
    return json.loads(json.dumps(GetHuurstuntDataJson()))

def GetAllListingsUrls():
    listings = GetHuurstuntProductInfo()['data']['rentals']
    for i in range(len(listings)):
        if listings[i]['isNew'] == True:
            listing_type = listings[i]['type']
            listing_street = listings[i]['street']
            listing_rooms = listings[i]['rooms']
            listing_price = listings[i]['price']
            listing_url = "https://www.huurstunt.nl" + listings[i]['url']

            print(listing_type)
            print(listing_street)
            print(listing_rooms)
            print(listing_price)
            print(listing_url)
            
print(GetAllListingsUrls())
