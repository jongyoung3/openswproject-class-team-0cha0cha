import os
import googlemaps

api_key = ''
map_clinet = googlemaps.Client(api_key)

result = []


search_locations = ['Ginza', 'Shibuya 109', 'Harajuku',
                   'Omotesando', 'Tokyo Solamachi',
                   'Mega Don Quijote Shibuya',
                   'Kiddy Land Harajuku', 'Kitkat Chocolatory',
                   'Tsukiji Outer Market', 'Odaiba VenusFort']

for locations in search_locations:
    response = map_clinet.places(query=locations)

    destination = []

    if('rating' in response['results'][0]): # 인덱스 번호에 따라 영업점 나오는 듯. 기준으로만 일단 만듬
        destination.append(0)
        destination.append(response['results'][0]['name'])
        destination.append(response['results'][0]['rating'])
        destination.append(response['results'][0]['user_ratings_total'])
        
    else:
        destination.append(1)
        # destination.append(response['results'][0][])
    result.append(destination)

print(result)
