import requests
from bs4 import BeautifulSoup
from huislijn_url_dict import urls

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

def GetHuislijnHtml(city, page):
    if page == 1:
        full_url = 'https://www.huislijn.nl/huurwoning/nederland' + urls[city]
        return requests.get(full_url, headers=headers)
    full_url = 'https://www.huislijn.nl/huurwoning/nederland' + urls[city] + f'?page={page}'
    return requests.get(full_url, headers=headers)

def ConvertHuislijnHtml(city):
    results = []
    soups = []
    #TODO: Change page not be a constant
    for i in range(1, 5):
        results.append(GetHuislijnHtml(city, i))
    for i in range(len(results)):
        soups.append(BeautifulSoup(results[i].text, "html.parser"))
    return soups

def GetHuislijnRentalListingLinks(city):
    huislijn_soups = ConvertHuislijnHtml(city)
    links = []
    for soup in huislijn_soups:
        objects_row = soup.find('div', attrs = {'class': 'objects-row'})
        objects_element = objects_row.find('div', attrs = {'class': 'wrapper-objects'})
        all_objects = objects_element.find_all('div', attrs = {'class': 'hl-search-object-display object'})
        for object in all_objects:
            link = object.find('div', attrs = {'class': 'object-panel'}, href = True)['href']
            links.append(link)    
    return links


print(GetHuislijnRentalListingLinks("amsterdam"))