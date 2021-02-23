'''
Lab3 Task3 Mykhailo Kuzmyn
'''
import folium
import json
import requests
from fastapi import FastAPI
from geopy.geocoders import Nominatim
import random


def twitter_api(name, token):
    base_url = "https://api.twitter.com/"

    bearer_token = token

    search_url = '{}1.1/friends/list.json'.format(base_url)

    search_headers = {
        'Authorization': 'Bearer {}'.format(bearer_token)
    }

    search_params = {
        'screen_name': '@' + str(name),
        'count':100
    }

    response = requests.get(search_url, headers = search_headers, params=search_params)
    return response


def get_locations_from_json(json_obj):
    '''
    gets location of 10 friend from json
    returns dict
    '''
    # dct = json.load(json_obj)
    names_locations = {}
    counter = 0

    friends = json_obj
    friends = {friend['name']: friend['location'] for friend in friends}

    for name, loc in friends.items():

        if loc != '':
            names_locations[name] = loc
    # while len(names_locations) < 10:
    #     rand_tupp = random.choice(friends)

    #     if rand_tupp[1] == '':
    #         pass

    #     else:
    #         names_locations[rand_tupp[0]] = rand_tupp[1]

    #     counter += 1
    #     if counter > 1000:
    #         break

    return names_locations


def get_coordinates(names_locations):
    '''
    gets coordinates for locations
    returns dict of names with coordinates
    '''
    names_coordinates = {}
    geolocator = Nominatim(user_agent='my_app')

    for name, loc in names_locations.items():
        coord = geolocator.geocode(loc)

        if coord != None:
            names_coordinates[name] = [coord.latitude + random.randint(-1000, 1000)/1000, coord.longitude + random.randint(-1000, 1000)/1000]

    return names_coordinates


def create_map():
    '''
    creates folium map
    '''
    world_map = folium.Map(location=[37.7765, -122.4172], zoom_start=6)
    return world_map


def add_markers(locations):
    '''
    '''
    fg_markers = folium.FeatureGroup('Markers')

    for name, loc in locations.items():
        fg_markers.add_child(folium.Marker(location=[loc[0], loc[1]], popup=name, icon=folium.Icon(color='lightgray', icon='home')))
    
    return fg_markers


def location_map(username, token):
    '''
    creates location map
    '''
    w_map = create_map()
    friends = twitter_api(username, token).json()['users']
    # friends = 
    names_locations = get_locations_from_json(friends)
    names_coordinates = get_coordinates(names_locations)
    print(names_locations)
    markers = add_markers(names_coordinates)

    w_map.add_child(markers)
    w_map.save('templates/followers_locations.html')
    return w_map
