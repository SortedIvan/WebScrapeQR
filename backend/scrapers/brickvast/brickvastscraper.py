import requests
from bs4 import BeautifulSoup
import re
from utility_data.rental_listing_data import RentalListing
import uuid

BASE_URL = "https://en.brickvastgoed.nl"
PAGES_TO_CHECK = 2



def GetBrickvastHtml():
    all_html = []
    for i in range(PAGES_TO_CHECK):
        try:
            all_html.append(requests.get(f"https://en.brickvastgoed.nl/aanbod/page-{i}/"))
        except:
            return []
    return all_html

def GetListingLinks():
    all_html = GetBrickvastHtml()
    all_links = []
    temp = []
    image_links = []

    for i in range(len(all_html)):
        temp = BeautifulSoup(all_html[i].text, "html.parser").find_all('a', attrs = {'class': 'item'}, href = True)
        for i in range(len(temp)):
            try:
                listing_label = temp[i].find('div', attrs = {'class': 'overlay'}).find('img')['src']
                if not "nieuw" in str(listing_label):
                    continue

                all_links.append(temp[i]['href'])
                try:
                    image_temp = temp[i].find('div', attrs = {'class': 'image'}).find('img')['src']
                    image_links.append(image_temp)
                except Exception as ex:
                    print(ex)
                    print("Image empty")
                    image_links.append("")

            except Exception as ex:
                print(ex)
                continue
        temp = []
    return all_links, image_links

def GetListingSoups():
    links, image_links = GetListingLinks()
    listing_soups = []
    for i in range(len(links)):
        listing_html = requests.get(BASE_URL + links[i])
        links[i] = BASE_URL + links[i]
        listing_soups.append(
            BeautifulSoup(listing_html.text, "html.parser")
        )
    return listing_soups, links, image_links


def GetAllListings():
    soups,links, image_links = GetListingSoups()
    info_segments = []
    final_listings = []
    for i in range(len(soups)):
        try:
            listing_info_block = soups[i].find('table', attrs = {'class':'table_style'})
            rent_price = listing_info_block.find('td', text='Rent per month:').find_next_sibling('td').text
            address = listing_info_block.find('td', text='Address:').find_next_sibling('td').text
            city = listing_info_block.find('td', text='City:').find_next_sibling('td').text
            house_type = listing_info_block.find('td', text='Type of house:').find_next_sibling('td').text
            rooms = listing_info_block.find('td', text='Rooms:').find_next_sibling('td').text
            zip_row = listing_info_block.find("tr", {"class": "odd"}).find_next_sibling("tr")
            # extract the zip code text
            zip_text = zip_row.find_all("td")[1].text.strip()
            # format the zip code to match the desired format in the RentalListing object
            zip_code = zip_text.replace(" ", "")
            living_area = listing_info_block.find('td', text = "Living area:").find_next_sibling('td').text.strip()
            numeric_part = re.sub('[^0-9]', '', living_area)
            living_area_int = int(numeric_part)
            rent = rent_price.replace('&euro;', '').replace(',', '').replace('.','-').strip()
            address = address.strip()
            city = city.strip()
            house_type = house_type.strip()
            rooms = rooms.strip()
            rent_digits = re.sub(r'[^\d,]', '', rent)
            # convert to integer
            rent_int = int(float(rent_digits.replace(',', '.')))
            
            rental = RentalListing(
                str(uuid.uuid4()),
                "eindhoven",
                house_type,
                address + " " + city,
                "Today",
                rent_int,
                living_area_int,
                rooms,
                "None",
                links[i],
                address,
                zip_code,
                "https://en.brickvastgoed.nl" + image_links[i]
            )
            final_listings.append(rental)
        except:
            print("listing is none")
    return final_listings
        
# def print_all_listings():
#     for listing in listings:
#         print("------------------------------------------")
#         print(listing.listingCity)
#         print(listing.listingType)
#         print(listing.listingCity)
#         print(listing.listingName)
#         print(listing.listingDate)
#         print(listing.listingPrice)
#         print(listing.listingSqm)
#         print(listing.listingRooms)
#         print(listing.listingExtraInfo)
#         print(listing.listingUrl)
#         print(listing.listingAdress)
#         print(listing.listingPostcode)
#         print(listing.imageUrl)
