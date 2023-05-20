import os
import googlemaps
import requests

api_key = 'AIzaSyAg-D0M1X87OyIMkyTMmU6rNRJjFTP8ebI'
map_clinet = googlemaps.Client(api_key)

result_list = [] #최종 결과물 리스트
result_ex=[] #최종 결과물 리스트 전 단계

# chat-gpt 로 받아올 데이터
# 도쿄 애니메이션 여행
# search_locations =['Ghibli Museum(Mitaka, Tokyo, Japan)', 'Akihabara(Chiyoda City, Tokyo, Japan)', 
#                    'Odaiba(Minato City, Tokyo, Japan)', 'Nakano Broadway(Nakano, Tokyo, Japan)', 
#                    'Pokemon Center Tokyo(Chuo City, Tokyo, Japan)', 'J-World Tokyo(Ikebukuro, Tokyo, Japan)', 
#                    'Animate Ikebukuro(Toshima City, Tokyo, Japan)', 'Tokyo Anime Center(Chiyoda City, Tokyo, Japan)', 
#                    'Otome Road(Ikebukuro, Tokyo, Japan)', 'Shinjuku Wald 9(Shinjuku City, Tokyo, Japan)']
# chat-gpt 로 받아올 데이터
# search_locations = ['Ginza', 'Shibuya 109', 'Harajuku',
#                    'Omotesando', 'Tokyo Solamachi',
#                    'Mega Don Quijote Shibuya',
#                    'Kiddy Land Harajuku', 'Kitkat Chocolatory',
#                    'Tsukiji Outer Market', 'Odaiba VenusFort']
# search_locations=['Tower of London', 'Westminster Abbey', 
#                   'Buckingham Palace', 'Churchill War Rooms', 
#                   'The British Museum', 'Canterbury Cathedral', 
#                   'Stonehenge', 'Roman Baths', "St. Paul's Cathedral", 
#                   'Edinburgh Castle']
# data_locations=['Tower of London(London, UK)', 'Westminster Abbey(London, UK)', 
#                   'Buckingham Palace(London, UK)', 'Churchill War Rooms(London, UK)', 
#                   'The British Museum(London, UK)', 'Canterbury Cathedral(Canterbury, UK)', 
#                   'Stonehenge(Amesbury, UK)', 'Roman Baths(Bath, UK)', "St. Paul's Cathedral(London, UK)", 
#                   'Edinburgh Castle(Edinburgh, UK)']
data_locations=[
    #도쿄 애니메이션 여행
    ['Ghibli Museum(Mitaka, Tokyo, Japan)', 'Akihabara(Chiyoda City, Tokyo, Japan)', 
    'Odaiba(Minato City, Tokyo, Japan)', 'Nakano Broadway(Nakano, Tokyo, Japan)', 
    'Pokemon Center Tokyo(Chuo City, Tokyo, Japan)', 'J-World Tokyo(Ikebukuro, Tokyo, Japan)', 
    'Animate Ikebukuro(Toshima City, Tokyo, Japan)', 'Tokyo Anime Center(Chiyoda City, Tokyo, Japan)', 
    'Otome Road(Ikebukuro, Tokyo, Japan)', 'Shinjuku Wald 9(Shinjuku City, Tokyo, Japan)']

    #영국 역사 여행
    ,['Tower of London(London, UK)', 'Westminster Abbey(London, UK)', 
    'Buckingham Palace(London, UK)', 'Churchill War Rooms(London, UK)', 
    'The British Museum(London, UK)', 'Canterbury Cathedral(Canterbury, UK)', 
    'Stonehenge(Amesbury, UK)', 'Roman Baths(Bath, UK)', 
    "St. Paul's Cathedral(London, UK)", 'Edinburgh Castle(Edinburgh, UK)']

    #한국 자연휴식 여행
    ,['Nami Island(Chuncheon, Gangwon-do, South Korea)', 'Seoraksan National Park(Sokcho-si, Gangwon-do, South Korea)',
    'Jeju Island(Jeju Province, South Korea)', 'Jirisan National Park(Gurye-gun, Jeollanam-do, South Korea)', 
    'Bukhansan National Park(Goyang-si, Gyeonggi-do, South Korea)', 'Seorak Waterpia(Sokcho-si, Gangwon-do, South Korea)', 
    'Gyeongju(Gyeongsangbuk-do, South Korea)', 'Hallasan National Park(Jeju Province, South Korea)', 
    'Odaesan National Park(Pyeongchang, Gangwon-do, South Korea)', 'Gapyeong(Gyeonggi-do, South Korea)']

    #제주도 여행
    ,['Seongsan Ilchulbong(Seongsan-eup, Seogwipo, Jeju Island, South Korea)', 
    'Jeju Folk Village(Pyoseon-myeon, Seogwipo, Jeju Island, South Korea)', 
    'Manjanggul Cave(Gujwa-eup, Jeju City, Jeju Island, South Korea)', 
    'Jusangjeolli Cliff(Daepo-dong, Seogwipo, Jeju Island, South Korea)', 
    'Museum of Sex and Health(Aewol-eup, Jeju City, Jeju Island, South Korea)', 
    'Spirited Garden(Gangjeong-dong, Seogwipo, Jeju Island, South Korea)',
    'Hallasan National Park(Jeju-do, South Korea)', 'Jeju Loveland(Daejeong-eup, Seogwipo, Jeju Island, South Korea)', 
    'Beaches of Jeju Island(Jeju-do, South Korea)', 'Jeju Teddy Bear Museum(2829-10, Saekdal-dong, Seogwipo, Jeju Island, South Korea)']

    #미국 자동차 역사 여행
    ,['Ford Piquette Avenue Plant(Detroit, Michigan, USA)', 'The Henry Ford Museum(Dearborn, Michigan, USA)', 
    'Gilmore Car Museum(Hickory Corners, Michigan, USA)', 'Studebaker National Museum(South Bend, Indiana, USA)', 
    "Walt Disney's Barn(Griffith Park, Los Angeles, California, USA)", 'Petersen Automotive Museum(Los Angeles, California, USA)',
    "Bonnie and Clyde's Death Car(Primm, Nevada, USA)", 'Route 66 Museum(Kingman, Arizona, USA)', 
    'National Automobile Museum(Reno, Nevada, USA)', 'The Auburn Cord Duesenberg Automobile Museum(Auburn, Indiana, USA)']

    #남미 오지탐험 여행
    ,['Machu Picchu(Cusco, Peru)', 'Galapagos Islands(Ecuador)', 'Iguazu Falls(Misiones Province, Argentina/Brazil)',
    'Torres del Paine National Park(Magallanes Region, Chile)', 'Cartagena(Bolívar Department, Colombia)', 
    'La Paz(Bolivia)', 'Rio de Janeiro(Rio de Janeiro State, Brazil)', 'Salar de Uyuni(Potosi and Oruro Departments, Bolivia)',
    'Atacama Desert(Antofagasta Region, Chile)', 'Amazon Rainforest(Brazil, Peru, Colombia)']
    ]

min_rating = 0  # 최소 평점
min_reviews = 0  # 최소 리뷰 수

for search_locations in data_locations:

    for locations in search_locations:
        response = map_clinet.places(query=locations) # 데이터를 api로 보냄
        #print(response['results'])
        destination = []
        if(response['results']!=[]): #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때)를 걸러줌
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
                    
                #장소 세부요청
                url=f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location_lat},{location_lng}&radius={radius}&type=tourist+attractions&keyword=tourist+atrractions&key={api_key}"
                data=requests.request("GET", url, headers=headers, data=payload)
                res_lo=data.json()
                    
                #print(res_lo)
                if(res_lo['status']!='ZERO_RESULTS'):
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
                else: #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때) 텍스트 검색으로 다시 찾기
                    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={locations}&key={api_key}"
                    response = requests.get(url)
                    data = response.json()
                    
                    attractions = []

                    for result in data['results']:
                        name = result.get('name')
                        rating = result.get('rating')
                        reviews = result.get('user_ratings_total')

                        if name is not None and rating is not None and reviews is not None:
                            if rating >= min_rating:
                                attractions.append((name, rating, reviews))

                    #받은 관광명소 내림차순으로 정렬해서 그 중 위의 1개 반환 
                    attractions.sort(key=lambda x: x[1], reverse=True)
                    
                    if(attractions!=[]):
                        destination.append(locations) # 검색한 지역이름
                        destination.extend(attractions)
                
        else: #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때) 텍스트 검색으로 다시 찾기
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={locations}&key={api_key}"
            response = requests.get(url)
            data = response.json()

            attractions = []

            for result in data['results']:
                name = result.get('name')
                rating = result.get('rating')
                reviews = result.get('user_ratings_total')

                if name is not None and rating is not None and reviews is not None:
                    if rating >= min_rating:
                        attractions.append((name, rating, reviews))

            #받은 관광명소 내림차순으로 정렬해서 그 중 위의 1개 반환 
            attractions.sort(key=lambda x: x[1], reverse=True)
            
            destination.append(locations) # 검색한 지역이름
            destination.extend(attractions)
                
        #print(destination)
        
        if(destination!=[0] and destination!=[1]): # destination 안에 0 혹은 1만 있는 경우가 아니면
            result_ex.append(destination)

result_list.extend(result_ex)
print(result_list)
