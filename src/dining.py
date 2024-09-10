# Abandon all hope, ye who enter here.

import datetime
import json
import urllib.parse
import requests
import time
from bs4 import BeautifulSoup
import pint


ureg = pint.UnitRegistry()


#TODO: handle multiple levels of parentheses
#e.g. Chili (spicy (but not too spicy))
def parse_list(ingredients):
    if ingredients == '':
        return []
    naive_split = ingredients.split(', ')
    ingredient_list = []
    
    # for (i = 0; i < len(naive_split); i++)
    i = 0
    while i < len(naive_split):
        ingredient = ''
        if '(' in naive_split[i]:
            while i < len(naive_split):
                ingredient += naive_split[i]
                if ')' in naive_split[i]:
                    break
                else:
                    ingredient += ', '
                i += 1
        else:
            ingredient = naive_split[i]
        ingredient.strip()
        ingredient_list.append(ingredient)
        i += 1
    return ingredient_list

def category_html_to_dict(html_string, meal, category):
    soup = BeautifulSoup(html_string, 'html.parser')
    items = soup.find_all('a', href='#inline')
    ret = []
    for item in items:
        dish = {}
        dish['category-name'] = category
        dish['meal-name'] = meal
        for attribute in item.attrs.keys():
            if attribute.startswith('data-') and not attribute.endswith('dv'):
                attribute_name = attribute[5:]
                data = item.attrs[attribute]
                if attribute_name == 'calories' or attribute_name == 'calories-from-fat':
                    data = int(data) if data else None
                elif attribute_name == 'clean-diet-str':
                    data = data.split(', ')
                    attribute_name = 'diets'
                elif attribute_name in ['allergens', 'ingredient-list']:
                    data = parse_list(data)
                elif attribute_name in ['cholesterol', 'sodium', 'dietary-fiber', 'protein', 'sat-fat', 'sugars',
                                        'total-carb', 'total-fat', 'trans-fat']:
                    data = ureg.Quantity(data) if data else None
                dish[attribute_name] = data
        ret.append(dish)
    return ret




def location_id_to_name(location_id):
    locations = get_locations()
    for location in locations:
        if location['id'] == location_id:
            return location['name']
    raise KeyError('no locations found with ID %d' % location_id)

def get_menu(location, date ):
    # If there is no menu available (for example, if the location is closed), then UMass Dining will simply return a blank page.
    # Status code is 200 no matter what...
    try:
        query_params = {'tid': location,
                        'date': date.strftime('%m/%d/%Y')}
        request_url = 'https://umassdining.com/foodpro-menu-ajax?' + urllib.parse.urlencode(query_params)
        r = ''
        print(request_url)
        r=requests.get(request_url).json()
    except json.decoder.JSONDecodeError:
        return []
    ret = []
    for meal in r.keys():
        for category in r[meal].keys():
            ret.extend(category_html_to_dict(r[meal][category], meal, category))
    return ret

def get_food_trucks():
    trucks = requests.get('https://www.umassdining.com/umassapi/truck_location').json()
    for key in trucks.keys():
        trucks[key]['id'] = int(key)
    trucks = [trucks[key] for key in trucks.keys()]

    def truck_is_open(truck):
        return truck['long'] != '' and truck['lat'] != ''

    ret = []
    for truck in trucks:
        truck_data = {
            'id': truck['id']
        }
        if truck_is_open(truck):
            truck_data['longitude'] = float(truck['long'])
            truck_data['latitude'] = float(truck['lat'])
            truck_data['is_open'] = True
        else:
            truck_data['is_open'] = False
        ret.append(truck_data)
    return ret
