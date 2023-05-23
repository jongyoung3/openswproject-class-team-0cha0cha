import os
import googlemaps
import requests

api_key = 'YOUR_API_KEY'
map_clinet = googlemaps.Client(api_key)

result_list = [] #최종 결과물 리스트
result_ex=[] #최종 결과물 리스트 전 단계

# chat-gpt 로 받아올 데이터
search_locations=['Tower of London', 'Westminster Abbey', 
                  'Buckingham Palace', 'Churchill War Rooms', 
                  'The British Museum', 'Canterbury Cathedral', 
                  'Stonehenge', 'Roman Baths', "St. Paul's Cathedral", 
                  'Edinburgh Castle']

min_rating = 0  # 최소 평점
min_reviews = 0  # 최소 리뷰 수


# 지도에 데이터 보낼 때 좌표로 보내는 걸로 코드 바꾸기(원한다면)
for locations in search_locations:
    response = map_clinet.places(query=locations) # 데이터를 api로 보냄
    #print(response['results'])
    destination = [] #
    
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
                
            # 받아온 데이터 상태가 없음일 경우를 제외
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
                
            #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때) 텍스트 검색으로 다시 찾기
            else: 
                url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={locations}&key={api_key}"
                response = requests.get(url)
                data = response.json()
                
                attractions = []

                for result in data['results']:
                    name = result.get('name')
                    rating = result.get('rating')
                    reviews = result.get('user_ratings_total')

                    # 이름, 평점, 리뷰가 있는 것만 추가
                    if name is not None and rating is not None and reviews is not None:
                        if rating >= min_rating:
                            attractions.append((name, rating, reviews))

                #받은 관광명소 내림차순으로 정렬해서 그 중 위의 1개 반환 
                attractions.sort(key=lambda x: x[1], reverse=True)
                
                # 받아온 데이터가 공백리스트가 아닌 경우만 destination 리스트에 추가
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
            
            # 이름, 평점, 리뷰가 있는 것만 추가
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
print(result_list) #최종 결과 출력
