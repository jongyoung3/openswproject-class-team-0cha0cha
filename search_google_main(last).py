import os
import googlemaps
import requests

api_key = 'AIzaSyAg-D0M1X87OyIMkyTMmU6rNRJjFTP8ebI'
map_clinet = googlemaps.Client(api_key)

result = [] #최종 결과물 리스트

def get_response_data(search_locations, min_rating, min_reviews):
    for locations in search_locations:
        response = map_clinet.places(query=locations) # 데이터를 api로 보냄

        destination = []

        if('rating' in response['results'][0]): # 인덱스 번호에 따라 영업점 나오는 듯. 기준으로만 일단 만듬
            # '0'->지역 외의 장소, 평점이 있는 것
            # [0,'name','rating','user_ratings_total']
            destination.append(0)
            destination.append(response['results'][0]['name'])
            destination.append(response['results'][0]['rating'])
            destination.append(response['results'][0]['user_ratings_total'])
            
        else:
            # '1'->지역이름, 여기서 지역이름에 관광명소를 평점높고 리뷰수 많은거 1개 가져오면 됨. 단, 없는건 건너뛰고
            # [1,'locations',('name','rating','user_ratings_total')]
            destination.append(1)

            # 장소 '1'에 해당되는 장소의 좌표값
            location_lat=response['results'][0]['geometry']['location']['lat']
            location_lng=response['results'][0]['geometry']['location']['lng']
            
            radius=2000 # 반경 2,000m
            
            # 장소 세부요청 (전달받은 위치의 반경 2000m에 있는 관광명소 탐색)
            payload={}
            headers = {}
            attractions = []
            res_attr=[]
            
            #장소 세부요청
            url=f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location_lat},{location_lng}&radius={radius}&type=tourist+attractions&keyword=cruise&key={api_key}"
            data=requests.request("GET", url, headers=headers, data=payload)
            res_lo=data.json()
            
            name = res_lo['results'][0]['name']
            rating = res_lo['results'][0]['rating']
            reviews = res_lo['results'][0]['user_ratings_total']

            # 관광명소, 평점, 리뷰가 있는 것만 추가
            if name is not None and rating is not None and reviews is not None:
                if rating >= min_rating and reviews >= min_reviews:
                    if attractions!=(name,rating,reviews): #리스트 내에 있는 관광명소와 중복방지
                        attractions.append((name,rating,reviews))
                        
            #받은 관광명소 내림차순으로 정렬해서 그 중 위의 1개 반환 
            attractions.sort(key=lambda x: (x[1]), reverse=True)
            
            destination.append(locations) # 검색한 지역이름
            destination.extend(attractions)
            
        result.append(destination)

# chat-gpt 로 받아올 데이터
search_locations = ['Ginza', 'Shibuya 109', 'Harajuku',
                   'Omotesando', 'Tokyo Solamachi',
                   'Mega Don Quijote Shibuya',
                   'Kiddy Land Harajuku', 'Kitkat Chocolatory',
                   'Tsukiji Outer Market', 'Odaiba VenusFort']

min_rating = 0  # 최소 평점
min_reviews = 0  # 최소 리뷰 수

get_response_data(search_locations, min_rating, min_reviews)

print(result)
