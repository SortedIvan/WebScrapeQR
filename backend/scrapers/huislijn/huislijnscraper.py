import requests
from bs4 import BeautifulSoup
from huislijn_url_dict import urls

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
url_base = 'https://www.huislijn.nl'


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
        all_listings = soup.find_all('div', attrs = {'class': 'object-panel'})
        for listing in all_listings:
            for a in listing.find_all('a', href = True):
                links.append(a['href'])
    return links

def GetHuislijnRentalListingSoups(city):
    huislijn_property_links = GetHuislijnRentalListingLinks(city)
    final_listing_soups = []
    
    for i in range(len(huislijn_property_links)):
        final_listing_soups.append(BeautifulSoup(requests.get(url_base + huislijn_property_links[i], headers=headers).text,  "html.parser"))

    return final_listing_soups


def GetHuislijnRentalListings(city):
    huislijn_properties_soups = GetHuislijnRentalListingSoups(city)

    for i in range(len(huislijn_properties_soups)):
        address_and_name = huislijn_properties_soups[i].find('div', attrs = {'class': 'address'})
        name = address_and_name.find('span', attrs = {'class': 'address-line'}).text.split()
        address_and_zip = address_and_name.find('span', attrs = {'class': 'second-line'})
        zip = address_and_zip.find('span', attrs = {'class': 'zip'}).text.split()
        address = address_and_zip.find('span', attrs = {'class': 'place'}).text.split()
        price = huislijn_properties_soups[i].find('div', attrs = {'class':'pricing'}).text.split()

        if type(name) is list:
            name = ' '.join(name)
        if type(address) is list:
            address = ''.join(address)
        if type(price) is list:
            price = ''.join(price)
            if price.__contains__("Ikwilmeerinformatieoverdezehuurwoning"):
                price = price.replace("Ikwilmeerinformatieoverdezehuurwoning", "")
        if (type(zip) is list):
            zip = ''.join(zip)

        print('\n')
        print(name)
        print(address)
        print(zip)
        print(price)
        print('\n')

GetHuislijnRentalListings("amsterdam")