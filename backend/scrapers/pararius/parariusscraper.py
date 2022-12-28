from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

def GetHtmlUrl(city, page):
    session = HTMLSession()
    if page == 1:
        r = session.get(f'https://www.pararius.com/apartments/{city}/')     
        r.html.render()
        return r.html.url
    r = session.get(f'https://www.pararius.com/apartments/{city}/page-{page}')
    r.html.render()
    return r.html.url


def GetParariusRentalHtml(city, page): 
    html_url = GetHtmlUrl(city, page)
    return requests.get(html_url, headers=headers)

def ConvertParariusRentalHtml(city):
    results = []
    soups = []
    #TODO: Change page not be a constant
    for i in range(1, 5):
        results.append(GetParariusRentalHtml(city, i))
    for i in range(len(results)):
        soups.append(BeautifulSoup(results[i].text, "html.parser"))
    return soups

def GetParariusRentalLinks(city):
    pararius_soups = ConvertParariusRentalHtml(city)
    links = []
    for soup in pararius_soups:
        print(soup)

        # search_elements_mixed = soup.find_all('li', attrs = {'class': 'search-list__item search-list__item--listing'})
        # for search_element in search_elements_mixed:
        #     if not search_element.find('div', attrs = {'class': 'listing-search-item__label'}).text.strip() == "New":
        #         links.append(search_element.find('h2', attrs = {'class': 'listing-search-item__title'})['href'])
    return links

links = GetParariusRentalLinks("eindhoven")
print(links)

