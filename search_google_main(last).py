import os
import googlemaps
import requests

# result_list에 사진 값도 추가하긴 했는데 값이 길어서 이건 어떻게 할 건지 정하기
# 폐업상태 제외하기

api_key = 'YOUR_API_KEY'
map_clinet = googlemaps.Client(api_key)

result_list = [] #최종 결과물 리스트
result_ex=[] #최종 결과물 리스트 전 단계

# chat-gpt 로 받아올 데이터
# search_locations=['Tower of London', 'Westminster Abbey', 
#                   'Buckingham Palace', 'Churchill War Rooms', 
#                   'The British Museum', 'Canterbury Cathedral', 
#                   'Stonehenge', 'Roman Baths', "St. Paul's Cathedral", 
#                   'Edinburgh Castle']
#도쿄 애니메이션 여행
#search_locations=['Ghibli Museum(Mitaka, Tokyo, Japan)', 'Akihabara(Chiyoda City, Tokyo, Japan)', 'Odaiba(Minato City, Tokyo, Japan)', 'Nakano Broadway(Nakano, Tokyo, Japan)', 'Pokemon Center Tokyo(Chuo City, Tokyo, Japan)', 'J-World Tokyo(Ikebukuro, Tokyo, Japan)', 'Animate Ikebukuro(Toshima City, Tokyo, Japan)', 'Tokyo Anime Center(Chiyoda City, Tokyo, Japan)', 'Otome Road(Ikebukuro, Tokyo, Japan)', 'Shinjuku Wald 9(Shinjuku City, Tokyo, Japan)']
search_locations=['Ghibli Museum(Mitaka, Tokyo, Japan)']
#도쿄 애니메이션 여행
#search_locations=['J-World Tokyo(Ikebukuro, Tokyo, Japan)', 'Tokyo Anime Center(Chiyoda City, Tokyo, Japan)', 'Otome Road(Ikebukuro, Tokyo, Japan)']

min_rating = 0  # 최소 평점
min_reviews = 0  # 최소 리뷰 수


# 지도에 데이터 보낼 때 좌표로 보내는 걸로 코드 바꾸기(원한다면)
for locations in search_locations:
    response = map_clinet.places(query=locations) # 데이터를 api로 보냄
    #print(response)
    destination = [] 
    
    if(response['status'] !='ZERO_RESULTS'): #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때)를 걸러줌
        if('rating' in response['results'][0]): # 인덱스 번호에 따라 영업점 나오는 듯. 기준으로만 일단 만듬
            #if(response['results'][0]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
                # '0'->지역 외의 장소, 평점이 있는 것
                # [0,'name','rating','user_ratings_total']
                
                #사진 요청
                photo_reference=response['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                response_photo = requests.get(photo_url)
                res_photo=response_photo.content
                #print(res_photo)
                
                
                destination.append(0)
                destination.append(response['results'][0]['name'])
                destination.append(response['results'][0]['rating'])
                destination.append(response['results'][0]['user_ratings_total'])
                destination.append(res_photo)
                    
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
            url=f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location_lat},{location_lng}&radius={radius}&type=tourist+attractions&key={api_key}"
            data=requests.request("GET", url, headers=headers, data=payload)
            res_lo=data.json()
                
            # 받아온 데이터 상태가 없음일 경우를 제외
            if(res_lo['status']!='ZERO_RESULTS'):
                max_reviewer = -1
                max_index = -1
                for i in range(len(res_lo)):
                    # 리뷰 수가 높은 순으로 정렬 필요
                    #print(i)
                    if 'rating' in res_lo['results'][i]:
                        name = res_lo['results'][i]['name']
                        rating = res_lo['results'][i]['rating']
                        reviews = res_lo['results'][i]['user_ratings_total']
                        if reviews >= max_reviewer:
                            max_reviewer = reviews
                            max_index = i
                            
                name = res_lo['results'][max_index]['name']
                rating = res_lo['results'][max_index]['rating']
                reviews = res_lo['results'][max_index]['user_ratings_total']
                
                # 관광명소, 평점, 리뷰가 있는 것만 추가
                if name is not None and rating is not None and reviews is not None:
                    if rating >= min_rating and reviews >= min_reviews:
                        if attractions!=(name,rating,reviews): #리스트 내에 있는 관광명소와 중복방지
                            attractions.append((name,rating,reviews))
                                    
                #받은 관광명소 내림차순으로 정렬해서 그 중 위의 1개 반환 
                #attractions.sort(key=lambda x: (x[1]), reverse=True)
                #사진 요청
                photo_reference=res_lo['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                response_photo = requests.get(photo_url)
                res_photo=response_photo.content
                attractions.append(res_photo)
                        
                destination.append(locations) # 검색한 지역이름
                destination.extend(attractions)
                
            #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때) 텍스트 검색으로 다시 찾기
            else: 
                url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={locations}&key={api_key}"
                response = requests.get(url)
                data = response.json()
                
                attractions = []
                
                max_reviewer = -1
                max_index = -1
                for i in range(len(res_lo)):
                    # 리뷰 수가 높은 순으로 정렬 필요
                    #print(i)
                    if 'rating' in data['results'][i]:
                        name = data['results'][i]['name']
                        rating = data['results'][i]['rating']
                        reviews = data['results'][i]['user_ratings_total']
                        if reviews >= max_reviewer:
                            max_reviewer = reviews
                            max_index = i
                            
                name = data['results'][max_index]['name']
                rating = data['results'][max_index]['rating']
                reviews = data['results'][max_index]['user_ratings_total']

                # for result in data['results']:
                #     name = result.get('name')
                #     rating = result.get('rating')
                #     reviews = result.get('user_ratings_total')

                    # 이름, 평점, 리뷰가 있는 것만 추가
                if name is not None and rating is not None and reviews is not None:
                    if rating >= min_rating:
                        attractions.append((name, rating, reviews))

                #받은 관광명소 내림차순으로 정렬해서 그 중 위의 1개 반환 
                #attractions.sort(key=lambda x: x[1], reverse=True)
                #사진 요청
                photo_reference=res_lo['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                response_photo = requests.get(photo_url)
                res_photo=response_photo.content
                attractions.append(res_photo)
                
                # 받아온 데이터가 공백리스트가 아닌 경우만 destination 리스트에 추가
                if(attractions!=[]):
                    destination.append(locations) # 검색한 지역이름
                    destination.extend(attractions)
                
    else: #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때) 텍스트 검색으로 다시 찾기
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={locations}&key={api_key}"
        response = requests.get(url)
        data = response.json()

        attractions = []
        if(data['status'] !='ZERO_RESULTS'): # 이것도 공백 리스트 경우를 제외
            max_reviewer = -1
            max_index = -1
            for i in range(len(res_lo)):
                # 리뷰 수가 높은 순으로 정렬 필요
                #print(i)
                if 'rating' in data['results'][i]:
                    name = data['results'][i]['name']
                    rating = data['results'][i]['rating']
                    reviews = data['results'][i]['user_ratings_total']
                    if reviews >= max_reviewer:
                        max_reviewer = reviews
                        max_index = i
                            
            name = data['results'][max_index]['name']
            rating = data['results'][max_index]['rating']
            reviews = data['results'][max_index]['user_ratings_total']
            
            # for result in data['results']:
            #     name = result.get('name')
            #     rating = result.get('rating')
            #     reviews = result.get('user_ratings_total')
                
                # 이름, 평점, 리뷰가 있는 것만 추가
            if name is not None and rating is not None and reviews is not None:
                if rating >= min_rating:
                    attractions.append((name, rating, reviews))

            #받은 관광명소 내림차순으로 정렬해서 그 중 위의 1개 반환 
            #attractions.sort(key=lambda x: x[1], reverse=True)
            
            #사진 요청
            photo_reference=data['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
            response_photo = requests.get(photo_url)
            res_photo=response_photo.content
            attractions.append(res_photo)
            
            destination.append(locations) # 검색한 지역이름
            destination.extend(attractions)
        else: # 그래도 공백 리스트인 경우
            locations_blank_text=locations.split("(")
            
            response_blank = map_clinet.places(query=locations_blank_text[0]) # 데이터를 api로 보냄
            
           
            if(response_blank['status'] !='ZERO_RESULTS'): #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때)를 걸러줌
                if('rating' in response_blank['results'][0]): # 인덱스 번호에 따라 영업점 나오는 듯. 기준으로만 일단 만듬
                    # '0'->지역 외의 장소, 평점이 있는 것
                    # [0,'name','rating','user_ratings_total']
                    destination.append(0)
                    
                    #사진 요청
                    photo_reference=response_blank['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                    response_photo = requests.get(photo_url)
                    res_photo=response_photo.content
                    
            
                    destination.append(response_blank['results'][0]['name'])
                    destination.append(response_blank['results'][0]['rating'])
                    destination.append(response_blank['results'][0]['user_ratings_total'])
                    attractions.append(res_photo)
                    
                            
                else:
                    # '1'->지역이름, 여기서 지역이름에 관광명소를 평점높고 리뷰수 많은거 1개 가져오면 됨. 단, 없는건 건너뛰고
                    # [1,'locations',('name','rating','user_ratings_total')]
                    destination.append(1)

                    # 장소 '1'에 해당되는 장소의 좌표값
                    location_lat=response_blank['results'][0]['geometry']['location']['lat']
                    location_lng=response_blank['results'][0]['geometry']['location']['lng']
                        
                    radius=2000 # 반경 2,000m
                        
                    # 장소 세부요청 (전달받은 위치의 반경 2000m에 있는 관광명소 탐색)
                    payload={}
                    headers = {}
                    attractions = []
                        
                    #장소 세부요청
                    url=f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location_lat},{location_lng}&radius={radius}&type=tourist+attractions&key={api_key}"
                    data=requests.request("GET", url, headers=headers, data=payload)
                    res_lo=data.json()
                        
                    # 받아온 데이터 상태가 없음일 경우를 제외
                    if(res_lo['status']!='ZERO_RESULTS'):
                        max_reviewer = -1
                        max_index = -1
                        for i in range(len(res_lo)):
                            # 리뷰 수가 높은 순으로 정렬 필요
                            #print(i)
                            if 'rating' in res_lo['results'][i]:
                                name = res_lo['results'][i]['name']
                                rating = res_lo['results'][i]['rating']
                                reviews = res_lo['results'][i]['user_ratings_total']
                                if reviews >= max_reviewer:
                                    max_reviewer = reviews
                                    max_index = i
                            
                        name = res_lo['results'][max_index]['name']
                        rating = res_lo['results'][max_index]['rating']
                        reviews = res_lo['results'][max_index]['user_ratings_total']
                        
                        # for i in range(len(res_lo)):
                        #     if 'rating' in res_lo['results'][i]:
                        #         name = res_lo['results'][0]['name']
                        #         rating = res_lo['results'][0]['rating']
                        #         reviews = res_lo['results'][0]['user_ratings_total']

                        # 관광명소, 평점, 리뷰가 있는 것만 추가
                        if name is not None and rating is not None and reviews is not None:
                            if rating >= min_rating and reviews >= min_reviews:
                                if attractions!=(name,rating,reviews): #리스트 내에 있는 관광명소와 중복방지
                                    attractions.append((name,rating,reviews))
                                            
                        #받은 관광명소 내림차순으로 정렬해서 그 중 위의 1개 반환 
                        #attractions.sort(key=lambda x: (x[1]), reverse=True)
                        #사진 요청
                        photo_reference=res_lo['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                        response_photo = requests.get(photo_url)
                        res_photo=response_photo.content
                        attractions.append(res_photo)
                        
                                
                        destination.append(locations) # 검색한 지역이름
                        destination.extend(attractions)
                        
                    #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때) 텍스트 검색으로 다시 찾기
                    else: 
                        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={locations_blank_text[0]}&key={api_key}"
                        response = requests.get(url)
                        data = response.json()
                        
                        attractions = []
                        max_reviewer = -1
                        max_index = -1
                        for i in range(len(res_lo)):
                            # 리뷰 수가 높은 순으로 정렬 필요
                            #print(i)
                            if 'rating' in data['results'][i]:
                                name = data['results'][i]['name']
                                rating = data['results'][i]['rating']
                                reviews = data['results'][i]['user_ratings_total']
                                if reviews >= max_reviewer:
                                    max_reviewer = reviews
                                    max_index = i
                            
                        name = data['results'][max_index]['name']
                        rating = data['results'][max_index]['rating']
                        reviews = data['results'][max_index]['user_ratings_total']

                        # for result in data['results']:
                        #     name = result.get('name')
                        #     rating = result.get('rating')
                        #     reviews = result.get('user_ratings_total')

                        # 이름, 평점, 리뷰가 있는 것만 추가
                        if name is not None and rating is not None and reviews is not None:
                            if rating >= min_rating:
                                attractions.append((name, rating, reviews))

                        #받은 관광명소 내림차순으로 정렬해서 그 중 위의 1개 반환 
                        #attractions.sort(key=lambda x: x[1], reverse=True)
                        
                        #사진 요청
                        photo_reference=data['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                        response_photo = requests.get(photo_url)
                        res_photo=response_photo.content
                        attractions.append(res_photo)
                        
                        # 받아온 데이터가 공백리스트가 아닌 경우만 destination 리스트에 추가
                        if(attractions!=[]):
                            destination.append(locations) # 검색한 지역이름
                            destination.extend(attractions)
            
            
                
    #print(destination)
        
    if(destination!=[]): # destination 안에 0 혹은 1만 있는 경우가 아니면
        result_ex.append(destination)    

result_list.extend(result_ex)
print(result_list) #최종 결과 출력
