import requests
from bs4 import BeautifulSoup
import re

def furnished_regex(input_text):
    return re.findall(r'<li class="illustrated-features__item illustrated-features__item--interior">[a-zA-Z]+</li>',input_text)

class ParariusListing():
    def __init__(self, url, houseName, houseLocation, housePrice, houseType, houseMetrics, nrOfRooms, interior):
        self.url = url
        self.houseName = houseName
        self.houseLocation = houseLocation
        self.housePrice = housePrice
        self.houseType = houseType
        self.houseMetrics = houseMetrics
        self.nrOfRooms = nrOfRooms
        self.interior = interior

def RetrieveParariusHTML(city,priceLow, priceHigh, pageNr):
    return requests.get(f"https://www.pararius.com/apartments/{city}/{priceLow}-{priceHigh}/page-{pageNr}")


def GetParariusSoups(city,priceLow,priceHigh):
    results = []
    soups = []
    for i in range(5):
        results.append(RetrieveParariusHTML(city, priceLow, priceHigh, i))
    for i in range(len(results)):
        soups.append(BeautifulSoup(results[i].text, "html.parser"))
    return soups

def GetRawListings(city, priceLow, priceHigh):
    soups = GetParariusSoups(city, priceLow, priceHigh)
    rawlistings = []
    for i in range(len(soups)):
        rawlistings.append(soups[i].find_all("li", attrs = {"class" : "search-list__item search-list__item--listing"}))
    return rawlistings



def GetProcessedListings(city, priceLow, priceHigh):
    rawListsings = GetRawListings(city, priceLow, priceHigh)
    processedListings = []
    for i in range(len(rawListsings)):
        for raw in rawListsings[i]:
            url = "https://www.pararius.com" + raw.find("a", attrs = {"class" : "listing-search-item__link listing-search-item__link--depiction"}, href = True)['href']
            houseName = raw.find("h2", attrs = {"class" : "listing-search-item__title"}).find("a").text.strip().strip('\n')
            houseLocation = raw.find("div", attrs = {"class" : "listing-search-item__sub-title"}).text.strip().strip('\n')
            housePrice = raw.find("div", attrs = {"class" : "listing-search-item__price"}).text.strip().strip('\n')
            houseMetrix = raw.find("li", attrs = {"class":"illustrated-features__item illustrated-features__item--surface-area"}).text.strip().strip('\n')
            nrOfRooms = raw.find("li", attrs = {"class": "illustrated-features__item illustrated-features__item--number-of-rooms"}).text.strip().strip('\n')
            interior = "Unknown"
            if (raw.find("li", attrs = {"class": "illustrated-features__item illustrated-features__item--interior"}) is not None):
                interior = raw.find("li", attrs = {"class": "illustrated-features__item illustrated-features__item--interior"}).text
            processedListings.append(
                ParariusListing(url=url, houseLocation=houseLocation,
                 houseName=houseName, housePrice=housePrice, houseType=1, 
                 houseMetrics=houseMetrix, nrOfRooms=nrOfRooms, interior=interior)
            )
    return processedListings

processedListings = GetProcessedListings("eindhoven", 700, 1100)
for i in range(len(processedListings)):
    print(processedListings[i].url)
    print(processedListings[i].houseName)
    print(processedListings[i].houseLocation)
    print(processedListings[i].housePrice)
    print(processedListings[i].houseMetrics)
    print(processedListings[i].nrOfRooms)
    print(processedListings[i].interior)
    print("----------------------------------------------------------------")





