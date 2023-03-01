import requests
from bs4 import BeautifulSoup
from utility_data.rental_listing_data import RentalListing
from utility.parser import ParseDutchPostalCode
import uuid

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

cities_funda = [
    "amsterdam",
    "rotterdam",
    "den-haag",
    "utrecht",
    "eindhoven",
    "tilburg",
    "almere",
    "groningen",
    "breda",
    "nijmegen",
    "enschede",
    "apeldoorn",
    "haarlem",      
    "arnhem",           
    "gemeente-zaanstad",         
    "amersfoort",          
    "gemeente-haarlemmermeer",  
    "den-bosch",
    "zoetermeer",
    "zwolle",
    ]


def GetFundaRentalHtml(city, page):
    if page == 1:
        full_url = f'https://www.funda.nl/huur/{city}/1-dag/'
        return requests.get(full_url, headers=headers)
    full_url = f'https://www.funda.nl/huur/{city}/1-dag/p{page}'
    return requests.get(full_url, headers=headers)

def ConvertFundaRentalSoups(city):
    results = []
    soups = []
    #TODO: Change page not be a constant
    for i in range(1, 5):
        results.append(GetFundaRentalHtml(city, i))
    for i in range(len(results)):
        soups.append(BeautifulSoup(results[i].text, "html.parser"))
    return soups

def GetFundaRentalListingLinks(city):
    funda_soups = ConvertFundaRentalSoups(city)
    links = []
    for soup in funda_soups:

        try:
            search_content = soup.find('div', attrs = {'class': 'search-content-output'})
            search_content_listings = search_content.find_all('li', attrs = {'class': 'search-result'})
        except:
            print("Funda problem fetching listings")
            continue

        for listing in search_content_listings:
            if not listing:
                print("Funda listing was null")
                continue

            img_obj = None
            try:
                img_obj = listing.find('div', attrs = {'class': 'search-result-media'}) \
                    .find('img')
            except:
                print("Rental does not have regular images, trying promo")
                try:
                    img_obj = listing.find('div', attrs = {'class': 'search-result-media-promo'}) \
                    .find('img')
                except:
                    print("Rental has no images at all")
            
            try:
                if img_obj.has_attr('src'):
                    image_href = img_obj['src']
            except:
                print("Problem with the images")
                                                            
            if listing.find('div', attrs = {'class': 'search-promolabel-new'}):
                listing_content = listing.find('div', attrs = {'class': 'search-result-content-promo'})
                listing_href = "https://www.funda.nl" + listing_content.find('a', attrs = {'data-object-url-tracking': 'resultlist'}, href = True)['href']
            
                if image_href is None:
                    links.append((listing_href,"Unavailable"))
                else: 
                    links.append((listing_href,image_href))
                continue
            
            listing_content = listing.find('div', attrs = {'class': 'search-result-content'})
            listing_href = "https://www.funda.nl" + listing_content.find('a', attrs = {'data-object-url-tracking': 'resultlist'}, href = True)['href']
            if image_href is None:
                links.append((listing_href,"Unavailable"))
            else: 
                links.append((listing_href,image_href))
                
    return links

def GetFundaRentalListings(city):
    image_and_listing_links = GetFundaRentalListingLinks(city)

    rental_listings = []
    if image_and_listing_links is None:
        return None

    for link in image_and_listing_links:
        try:
            listing_html = requests.get(link[0], headers=headers)
            listing_soup = BeautifulSoup(listing_html.text, "html.parser")


            if listing_soup is None:
                continue
            if listing_soup.find('div', attrs = {'class': 'search-result-similar'}) is not None:
                continue
            listing_header_details = listing_soup.find('div', attrs = {'class': 'object-header__details'})
            if listing_header_details is None:
                continue

            listing_title = listing_header_details.find('span', attrs={'class': 'object-header__title'}).text.strip()
            listing_subtitle = listing_header_details.find('span', attrs = {'class': 'object-header__subtitle fd-color-dark-3'}).text.strip()

            listing_postal = ParseDutchPostalCode(listing_subtitle)
            listing_price = listing_header_details.find('div', attrs = {'class': 'object-header__pricing fd-text-size-l fd-flex--bp-m fd-align-items-center'}).find('strong').text.strip()    
            listing_price = ''.join(filter(lambda i: i.isdigit(), listing_price))

            listing_living_details = []

            listing_living_details_set = listing_header_details.find_all('span', attrs = {'class': 'kenmerken-highlighted__value fd-text--nowrap'})

            for listing_living_detail in listing_living_details_set:
                listing_living_details.append(listing_living_detail.text.strip())
            
            listing_deposit = listing_soup.find('dd',attrs= {'class': 'object-kenmerken-group-list'}).text.strip()

            if len(listing_living_details) != 0:
                listing_living_details[0] = ''.join(filter(lambda i: i.isdigit(), listing_living_details[0]))
                listing_living_details[0] = listing_living_details[0].replace('²', '')


            city = city.lower() # Ensuring that the cities are one format

            if len(listing_living_details) == 3:
                rental_listings.append(
                    RentalListing(
                        str(uuid.uuid4()),
                        "Rental property",
                        listing_title,
                        "Today",
                        int(listing_price),
                        int(listing_living_details[0]),
                        listing_living_details[2],
                        f"Deposit: {listing_deposit} | Property size: {listing_living_details[2]}",
                        link[0],
                        listing_title + " " + listing_subtitle,
                        listing_postal,
                        city,
                        link[1]
                    )
                )

            if len(listing_living_details) == 2:
                rental_listings.append(
                    RentalListing(
                        str(uuid.uuid4()),
                        "Rental property",
                        listing_title,
                        "Today",
                        int(listing_price),
                        listing_living_details[0],
                        listing_living_details[1],
                        f"Deposit: {listing_deposit} | Property size: Unavailable",
                        link[0],
                        listing_title + " " + listing_subtitle,
                        listing_postal,
                        city,
                        link[1]
                    )
                )

            if len(listing_living_details) == 1:
                rental_listings.append(
                    RentalListing(
                        str(uuid.uuid4()),
                        "Rental property",
                        listing_title,
                        "Today",
                        int(listing_price),
                        listing_living_details[0],
                        "Unavailable",
                        f"Deposit: {listing_deposit} | Property size: Unavailable",
                        link[0],
                        listing_title + " " + listing_subtitle,
                        listing_postal,
                        city,
                        link[1]
                    )
                )
            
            if len(listing_living_details) == 0:
                rental_listings.append(
                    RentalListing(
                        str(uuid.uuid4()),
                        "Rental property",
                        listing_title,
                        "Today",
                        int(listing_price),
                        0,
                        "Unavailable",
                        f"Deposit: {listing_deposit} | Property size: Unavailable",
                        link[0],
                        listing_title + " " + listing_subtitle,
                        listing_postal,
                        city,
                        link[1]
                    )
                )

        except Exception as e:
            print(e)
            print(link)
    return rental_listings

listings = GetFundaRentalListings("amsterdam")
for listing in listings:
    print("------------------------------------------")
    print(listing.listingType)
    print(listing.listingName)
    print(listing.listingDate)
    print(listing.listingPrice)
    print(listing.listingSqm)
    print(listing.listingRooms)
    print(listing.listingExtraInfo)
    print(listing.listingUrl)
    print(listing.listingAdress)
    print(listing.listingPostcode)
    print(listing.imageUrl)