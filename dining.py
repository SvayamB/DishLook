# Abandon all hope, ye who enter here.

import datetime
import json
import urllib.parse
import requests
import time
from bs4 import BeautifulSoup
import pint
from difflib import SequenceMatcher
import datetime


ureg = pint.UnitRegistry()

def isSubstring(s1, s2):
    s1=s1.lower()
    s2=s2.lower()
    M = len(s1)
    N = len(s2)

    # A loop to slide pat[] one by one
    for i in range(N - M + 1):

        # For current index i,
        # check for pattern match
        for j in range(M):
            if (s2[i + j] != s1[j]):
                break

        if j + 1 == M:
            return i

    return -1


def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()



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



def get_locations():
    locations = requests.get('https://www.umassdining.com/uapp/get_infov2').json()
    ret = []
    for location in locations:
        if location['opening_hours'] == 'Closed' or location['closing_hours'] == 'Closed':
            opening_hours = None
            closing_hours = None
        else:
            # TODO: this is horrific replace it
            opening_hours = datetime.datetime(2000, 1, 1).strptime(location['opening_hours'], '%I:%M %p').time()
            closing_hours = datetime.datetime(2000, 1, 1).strptime(location['closing_hours'], '%I:%M %p').time()
        ret.append({
            'name': location['location_title'],
            'id': location['location_id'],
            'opening_hours': opening_hours,
            'closing_hours': closing_hours,
        })
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
        while r == '':
            try:
                r = requests.get(request_url).json()
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue
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

def getDay(Foodname,days,diningHalls):
    indexes=diningHalls#1 wussy,2 frank,3 hamp, 4 berk
    found=0
    count=0
    date = datetime.date.today()
    while (found==0 and count<days):
        for dinHall in indexes:
            menu=get_menu(dinHall,date)
            for items in menu:
                if (similar(Foodname,items['dish-name'])>=0.8 or items['dish-name'].__contains__(Foodname)):
                    found=items
                if found!=0:
                    return (items['dish-name']+" At "+location_id_to_name(dinHall)+" on "+ date.strftime("%m/%d/%Y")+" during "+ found['meal-name'])
        date=date + datetime.timedelta(days = 1)
        count=count+1
    return "There will not be any " + Foodname + " in the next 15 days"

if __name__ == '__main__':
    print(getDay("smth random",15,[1,2,3,4]))