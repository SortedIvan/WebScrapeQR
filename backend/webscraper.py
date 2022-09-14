import requests
from bs4 import BeautifulSoup


class ParariusListing():
    def __init__(self, url, houseName, houseLocation, housePrice):
        self.url = url
        self.houseName = houseName
        self.houseLocation = houseLocation
        self.housePrice = housePrice

def RetrieveParariusHTML(city,priceLow, priceHigh, pageNr):
    return requests.get(f"https://www.pararius.com/apartments/{city}/{priceLow}-{priceHigh}/page-{pageNr}")


def GetParariusSoups(city,priceLow,priceHigh):
    results = []
    soups = []

    for i in range(10):
        results.append(RetrieveParariusHTML(city, priceLow, priceHigh, i))
    
    for i in range(len(results)):
        soups.append(BeautifulSoup(results[i].text, "html.parser"))
    return soups

def ScrapeParariusInformation(city, priceLow, priceHigh):
    soups = GetParariusSoups(city, priceLow, priceHigh)
    rawlistings = []
    completelistings = []

    for i in range(len(soups)):
        rawlistings.append(soups[i].find_all("li", attrs = {"class" : "search-list__item search-list__item--listing"}))
    
    return rawlistings

def GetOneParariusSoup(city, priceLow, priceHigh):
    result = RetrieveParariusHTML(city,priceLow, priceHigh, 1)
    soup = BeautifulSoup(result.text, "html.parser")
    listWithResults = soup.find("ul", attrs = {"class" : "search-list"})
    return listWithResults


print(ScrapeParariusInformation("eindhoven", 100, 1000))