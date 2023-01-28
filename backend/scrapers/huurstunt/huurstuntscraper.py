import requests
import json
import uuid
from bs4 import BeautifulSoup
from utility_data.rental_listing_data import RentalListing

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

def GetHuurstuntRentalHtml(city, page):
    if page == 1:
        return requests.get(
            "https://www.huurstunt.nl/huren/" + city + "/",
            headers = headers
        )
    return requests.get(
        f"https://www.huurstunt.nl/huren/{city}/p{page}",
        headers = headers
    )

def GetHuurstuntRentalSoups(city):
    all_listing_soups = []

    # for the first 5 pages
    for i in range(0, 5):
        all_listing_soups.append(
            BeautifulSoup(GetHuurstuntRentalHtml(city, i).text, "html.parser")
        )

    return all_listing_soups

def GetImageAndListingLinks(city):
    all_listing_soups = GetHuurstuntRentalSoups(city)
    image_links = []
    listing_links = []

    for i in range(len(all_listing_soups)):
        individual_listings = all_listing_soups[i].find_all('div', attrs = {'class': 'rental-card-wide col-lg-12 col-md-12'})

        for listing in individual_listings:
            # in case the element is actually new
            if listing.find('span', attrs = {'class': 'property-type property--green'}):
                try:
                    listing_url = listing.find('a', href = True)['href']
                except:
                    print("Image_url does not exist")
                
                try:
                    image_url_obj = listing.find('img')
                    
                    if image_url_obj.has_attr('src'):
                        image_url = image_url_obj['src']
                    else: listing_url = "Empty"
                except:
                    print("Image url does not exist")
                image_links.append(image_url)
                listing_links.append(listing_url)
    return listing_links, image_links

def GetIndividualListingSoups(city):
    all_links = GetImageAndListingLinks(city)
    listing_links = all_links[0]
    individual_listings = []

    for i in range(len(listing_links)):
        individual_listings.append(
            BeautifulSoup
                (
                requests.get(listing_links[i]).text, "html.parser"
                )
            )
    
    return all_links, individual_listings

def GetAllHuurstuntRentals(city):
    links_and_soups = GetIndividualListingSoups(city)
    image_links = links_and_soups[0]
    listings = links_and_soups[1]
    
    for listing in listings:
        try:
            main_container = listing.find('div', attrs = {'class': 'container'})
        except:
            print("Main container does not exist. Skipping listing")

        