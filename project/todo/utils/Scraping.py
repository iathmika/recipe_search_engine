## Author: Radhikesh Jain
## Purpose: Scraping recipes from https:/www.allrecipes.com

from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import json
from recipe_scrapers import scrape_me

response = requests.get('https://www.allrecipes.com/recipes-a-z-6735880')
soup = BeautifulSoup(response.text, "html.parser")
recipe_types = soup.find_all('a',class_ = 'link-list__link type--dog-bold type--dog-link')
recipe_types_urls = []
for recipe_type in recipe_types:
    recipe_types_urls.append(recipe_type['href'])

def get_response(recipe_type):
    response = requests.get(recipe_type)
    soup = BeautifulSoup(response.text, "html.parser")
    recipes = soup.find_all('a',class_ = 'comp mntl-card-list-items mntl-document-card mntl-card card card--no-image')
    return recipes

recipe_urls = []
start_time = time.time()
with ThreadPoolExecutor(max_workers=100) as p:
    recipe_anchors = p.map(get_response, recipe_types_urls)

for anchors in recipe_anchors:
    for anchor in anchors:
        recipe_urls.append(anchor['href'])
#print(f"{(time.time() - start_time):.2f} seconds")

actual_recipes = []
for recipe in recipe_urls:
    if('/recipe/' in recipe):
        actual_recipes.append(recipe)

counter = 1
def get_data(recipe):
    scraper = scrape_me(recipe)
    try:
        if(scraper.title() is None or scraper.ingredients() is None or scraper.instructions() is None):
            return
    except:
        return
    recipe_data = {"id": 1, "title": scraper.title(), "ingredients": scraper.ingredients(), "directions": scraper.instructions(), "link": recipe, "source": scraper.host(), "NER": None}
    return recipe_data

with ThreadPoolExecutor(max_workers=100) as p:
    data = p.map(get_data, actual_recipes[4772:4780])

scraped_recipies = {"data": []}
for r in data:
    scraped_recipies["data"].append(r)

scraped_recipies_json = json.dumps(scraped_recipies)

with open('scraped_recipies.json','w') as f:
    f.write(scraped_recipies_json)








