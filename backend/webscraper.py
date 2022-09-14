import requests
from bs4 import BeautifulSoup

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
    soups = len(GetParariusSoups(city, priceLow, priceHigh))
    listings = []

    for i in range(soups):
        listings.append(soups[i])

print(GetParariusSoups("Eindhoven", "0", "3000"))