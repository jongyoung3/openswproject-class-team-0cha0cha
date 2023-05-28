import os
import googlemaps
import requests
from pprint import pprint #줄맞춤 출력을 위해 임포트 한 것이므로 나중에 지워야함

########################################-----------수정 사항---------#########################################################
# result_list에 사진 값도 추가하긴 했는데 값이 길어서 이건 어떻게 할 건지 정하기(url로 대체함 안되면 content로 변경)
# 폐업상태 제외하기
# ㄴ완료
#############################################################################################################################

api_key = 'YOUR_API_KEY'
map_clinet = googlemaps.Client(api_key)

result_list = [] #최종 결과물 리스트
result_ex=[] #최종 결과물 리스트 전 단계

# chat-gpt 로 받아올 데이터
    #도쿄 애니메이션 여행
search_locations=['Ghibli Museum(Mitaka, Tokyo, Japan)', 'Akihabara(Chiyoda City, Tokyo, Japan)', 'Odaiba(Minato City, Tokyo, Japan)', 
                  'Nakano Broadway(Nakano, Tokyo, Japan)', 'Pokemon Center Tokyo(Chuo City, Tokyo, Japan)', 'J-World Tokyo(Ikebukuro, Tokyo, Japan)', 
                  'Animate Ikebukuro(Toshima City, Tokyo, Japan)', 'Tokyo Anime Center(Chiyoda City, Tokyo, Japan)', 'Otome Road(Ikebukuro, Tokyo, Japan)', 
                  'Shinjuku Wald 9(Shinjuku City, Tokyo, Japan)']
#search_locations=['Pokemon Center Tokyo(Chuo City, Tokyo, Japan)']


min_rating = 0  # 최소 평점
min_reviews = 0  # 최소 리뷰 수


# 지도에 데이터 보낼 때 좌표로 보내는 걸로 코드 바꾸기(원한다면)
for locations in search_locations:
    response = map_clinet.places(query=locations) # 데이터를 api로 보냄
    #print(response)
    destination = [] 
    
    if(response['status'] !='ZERO_RESULTS'): #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때)를 걸러줌
        if('rating' in response['results'][0]): # 인덱스 번호에 따라 영업점 나오는 듯. 기준으로만 일단 만듬
            if(response['results'][0]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
                # '0'->지역 외의 장소, 평점이 있는 것
                # [0,'name','rating','user_ratings_total']
                
                if('photos' in response['results'][0]): # 'photos'가 아예없는 경우 제외
                    #사진 요청
                    photo_reference=response['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                    response_photo = requests.get(photo_url)
                    #res_photo=response_photo.content
                    res_photo=response_photo.url
                    
                    destination.append(0)
                    destination.append(response['results'][0]['name'])
                    destination.append(response['results'][0]['rating'])
                    destination.append(response['results'][0]['user_ratings_total'])
                    destination.append(res_photo)                                       
                else:
                    destination.append(0)
                    destination.append(response['results'][0]['name'])
                    destination.append(response['results'][0]['rating'])
                    destination.append(response['results'][0]['user_ratings_total'])
                    destination.append('No Image')
                #print(res_photo)
                
                
                    
        else:
            # '1'->지역이름, 여기서 지역이름에 관광명소를 평점높고 리뷰수 많은거 1개 가져오면 됨. 단, 없는건 건너뛰고
            # [1,'locations',('name','rating','user_ratings_total')]

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
                        if(res_lo['results'][i]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
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
                if('photos' in res_lo['results'][max_index]):  # 'photos'가 아예없는 경우 제외
                    #사진 요청
                    photo_reference=res_lo['results'][max_index]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                    response_photo = requests.get(photo_url)
                    res_photo=response_photo.url
                    attractions.append(res_photo)
                    
                    destination.append(1)      
                    destination.append(locations) # 검색한 지역이름
                    destination.extend(attractions)
                else:
                    destination.append(1)      
                    destination.append(locations) # 검색한 지역이름
                    destination.extend(attractions)
                    destination.extend('No Image')
                
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
                    if(res_lo['results'][i]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
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
                if('photos' in res_lo['results'][max_index]):  # 'photos'가 아예없는 경우 제외
                    photo_reference=res_lo['results'][max_index]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                    response_photo = requests.get(photo_url)
                    res_photo=response_photo.url
                    attractions.append(res_photo)
                else:
                    attractions.append('No Image')

                
                # 받아온 데이터가 공백리스트가 아닌 경우만 destination 리스트에 추가
                if(attractions!=[]):
                    destination.append(1)
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
                if(data['results'][i]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
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
            if('photos' in data['results'][max_index]):  # 'photos'가 아예없는 경우 제외
                #사진 요청
                photo_reference=data['results'][max_index]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                response_photo = requests.get(photo_url)
                res_photo=response_photo.url
                attractions.append(res_photo)
                
                destination.append(1)
                destination.append(locations) # 검색한 지역이름
                destination.extend(attractions)
            else:
                destination.append(1)
                destination.append(locations) # 검색한 지역이름
                destination.extend(attractions)
                destination.extend('No Image')
                
        else: # 그래도 공백 리스트인 경우
            locations_blank_text=locations.split("(")
            
            response_blank = map_clinet.places(query=locations_blank_text[0]) # 데이터를 api로 보냄
            
           
            if(response_blank['status'] !='ZERO_RESULTS'): #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때)를 걸러줌
                if('rating' in response_blank['results'][0]): # 인덱스 번호에 따라 영업점 나오는 듯. 기준으로만 일단 만듬
                    if(response_blank['results'][0]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
                        # '0'->지역 외의 장소, 평점이 있는 것
                        # [0,'name','rating','user_ratings_total']
                        destination.append(0)
                        if('photos' in response_blank['results'][0]):  # 'photos'가 아예없는 경우 제외
                            #사진 요청
                            photo_reference=response_blank['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                            response_photo = requests.get(photo_url)
                            res_photo=response_photo.url
                            
                    
                            destination.append(response_blank['results'][0]['name'])
                            destination.append(response_blank['results'][0]['rating'])
                            destination.append(response_blank['results'][0]['user_ratings_total'])
                            attractions.append(res_photo)
                        else:
                            destination.append(response_blank['results'][0]['name'])
                            destination.append(response_blank['results'][0]['rating'])
                            destination.append(response_blank['results'][0]['user_ratings_total'])
                            attractions.append('No Image')
                    
                            
                else:
                    # '1'->지역이름, 여기서 지역이름에 관광명소를 평점높고 리뷰수 많은거 1개 가져오면 됨. 단, 없는건 건너뛰고
                    # [1,'locations',('name','rating','user_ratings_total')]

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
                            if(res_lo['results'][i]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
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
                        if('photos' in res_lo['results'][max_index]):  # 'photos'가 아예없는 경우 제외
                            #사진 요청
                            photo_reference=res_lo['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                            response_photo = requests.get(photo_url)
                            res_photo=response_photo.url
                            attractions.append(res_photo)
                            
                            destination.append(1)
                            destination.append(locations) # 검색한 지역이름
                            destination.extend(attractions)
                        else:
                            destination.append(1)
                            destination.append(locations) # 검색한 지역이름
                            destination.extend(attractions)
                            destination.extend('No Image')
                        
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
                            if(data['results'][i]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
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
                        if('photos' in data['results'][max_index]): # 'photos'가 아예없는 경우 제외
                            #사진 요청
                            photo_reference=data['results'][max_index]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                            response_photo = requests.get(photo_url)
                            res_photo=response_photo.url
                            attractions.append(res_photo)
                        else:
                            attractions.append('No Image')
                        
                        # 받아온 데이터가 공백리스트가 아닌 경우만 destination 리스트에 추가
                        if(attractions!=[]):
                            destination.append(1)
                            destination.append(locations) # 검색한 지역이름
                            destination.extend(attractions)
            
            
                
    #print(destination)
        
    if(destination!=[]): # destination 안에 비어있는 경우 제외
        result_ex.append(destination)    

result_list.extend(result_ex)

# [0 ,'검색한 장소=검색한 결과의 장소','평점','리뷰 수','사진링크']
# [1 ,'검색한 장소','검색한 결과의 장소','평점','리뷰 수','사진링크']
pprint(result_list) #최종 결과 출력


# 사진 코드(이건 content인데 지금은url로 대체함 안되면 다시 content로 변경)
# b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xe1\x00*Exif\x00\x00II*\x00\x08\x00\x00\x00\x01\x001\x01\x02\x00\x07\x00\x00\x00\x1a\x00\x00\x00\x00\x00\x00\x00Google\x00\x00\xff\xdb\x00\x84\x00\x03\x02\x02\n\x08\x08\n\x08\n\n\n\n\n\x08\x0b\n\n\n\n\x08\n\x08\n\x0b\n\n\n\n\x08\n\x08\n\x08\x08\x08\x08\n\x08\n\n\n\x08\x08\n\n\n\n\n\x08\x08\n\n\n\x08\n\x0b\r\x0b\n\r\x0b\n\n\x08\x01\x03\x04\x04\x06\x05\x06\n\x06\x06\n\x10\x0e\x0b\x0e\x10\x0f\x10\x0f\x10\x0f\x0f\x0f\x10\x10\x0f\x10\x0f\x0f\x0f\x0f\x10\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x10\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x10\x0f\x0f\x0f\x0f\x0f\r\r\x0f\x0f\r\x0f\x0f\x0f\r\xff\xc0\x00\x11\x08\x01,\x01\x90\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1d\x00\x00\x01\x04\x03\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x04\x05\x07\x08\x00\x02\x03\x01\t\xff\xc4\x00H\x10\x00\x03\x00\x01\x02\x04\x04\x03\x06\x03\x06\x04\x05\x02\x05\x05\x01\x02\x03\x11\x04\x12\x00\x05\x13!\x06\x07"1\x14AQ\x08#2aq\xf0\x81\x91\xa13B\xb1\xc1\xd1\xe1\x15$CR\x16br\x92\xf1%\x82\tS\xa2\xb2\xc245c\x83\x93\xff\xc4\x00\x1c\x01\x00\x01\x05\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x01\x02\x04\x05\x06\x07\x08\xff\xc4\x00<\x11\x00\x01\x03\x02\x03\x05\x07\x03\x03\x03\x03\x03\x05\x00\x00\x00\x01\x00\x02\x11\x03!\x04\x121\x05AQaq\x13"\x81\x91\xa1\xc1\xf02\xb1\xd1\x06\xe1\xf1\x14#B\x07Rb\x15r\x82$3\xa2\xb2\xc2\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xfa!\xe1\x1f\x11u\xb4\xa9R\xa5p\x08\xc3`\x13\xb0c {\x0c\xe3\xdb\xb6?N:r\x1f\x14OT\xbb\xa6r\x06\x0f\x7f\xcf#\xb1\xfc\'\x05H8\'\x07\xb1\xe2\xa3x\xe3\xedG\x99\xcfM\xa7GE\x0e\xa7)\x84\x0f\x82\x0bd\xe0*3n\xea\x10HQ\xdc\x80F\x03J\x1eEss\xe8\xd4\xbdA\x8d\xf7\x14\xcb\x0f\xc5@_ho\xc0@#\xe5\xb7s0%\x9d\x9c\xe6\xdd<K\x1e\xe8m\xd5\x18S\xd5\x10\xf0\x86\xe9\xc3\x8d-\xf4\xe1\xbbU\xa8\xcf\x1a\r\x92\xa0\xe4\x8d\xf8\xeb\nc\x84\x1a\xaed\x8b\x9d\xcc\xab\x81\x92X\x80\x00\xfc\xc9\xed\xec3\xef\xd8w\xf6\xe2;\xf1O\x9f:m9Q2,I \x85%Go|1S\x9e\xe7\xdf\x04{\x00NG\x00\xc5bh\xe1\x99\x9e\xb3\xa0|\xd0\x0b\x9f\x04 \t0\x11N\x8b\x99\x03\xcfv\x8cz4\x9bN\x08\xed\xf7\x9b\xd7#\xdcgy\xf7\x1f/\xccfSKqJ|3\xe6\xec\xe3\xcf)\xac\xbd:KY\xcb\x7f]v\xaaKQ^\x8e\x9dE\xd0<\xe8\xe8\xf3Y4\xc3\x06\xea\xba{nQ[m\xcb9\xdaUC\xa3\xab\xa9\xf6e \x8f\xcf\xb8\xf9\x8f\x98\xf7\x1cf\xe0\xab\xd3\xc4\x87\xbe\x99\x91\x9a\xdd A\x1c\x8a90\x00;\x87\xb9(\x97\xab\xc6\xddN\x1be\xa9\xe1Z?\x17\x0ba8][\x8d:\x1c{\xbb\x8fV\x9cF\xe1"\xbdip\x83T\x9c8\xf58Ki\xf0\xec\xe6\xa0R8\xaf~\x1d4\xdc&\x96\x97\x87M$08U\x1e\x14\xda\xd9\xb2\xec\xa3\x84\x9a\x8d&O\x0b\xb8\xf7\x8a\xa1\xc4]Yu0\xe1\t\xbeZ.\x16$\xb1\xc7N3\x84\\JL\xa6\x1a\xb3\x8c\xe38\xce \x8a\xb3\x8c\xe38\xf0\x9e\x12K\xde\x1a\xbcE\xcd\xbaS\xc8\xf7=\x87\xfa\xf1\xcfW\xe2\xc9#\xec\xdc\x0b\x1c\xf6\\\x1fo|\x9c\xe3<F\x9e$\xf19\xb5\xc8\xf6@{~\x83\xfdNx\xd3\xc2`\xdfU\xf7\x16\xd5c\xe3q\xec\xa4\xc2\x1a{\xc6\xd6\xdc\x8f\xbc67\xb9\xa3\x1fV=\xb3\x9e\xc7\xfd\xc7\xef\xb6\t@\xe2\x1f\xd1\xf3\xc6\x99R\x84n=\x8fs\xfdx\x96\xb4W\xdc\x81\xbe\xa3\x85\x8e\xa0\xean\x0e:\x1d<\x13l\xecCj\x02\xc1\xa8\xba\xef\xc6q\x9cg\x19\x8beg\x19\xc6q\x9c$\x96q\x9cg\x19\xc2Ig\x19\xc6q\x9c$\x96q\x9cg\x19\xc2Ig\x19\xc6q\x9c$\x96q\x9cg\x19\xc2Ig\x19\xc6q\x9c$\x96q\x9cg\x19\xc2Ig\x19\xc6q\x9c$\x96q\x9cg\x1aR\xb8\xe1&&\x17\xc6\xdf*9\xc3\xf3-F\x9eL\x1a\x8a\xc8CAL\x8b7g\xc3$\xea\xc5\x1c\x80\xe8F\x1aE]P\xab&Y\x84\xb5\xf6}\xf0_3\xbf4\xda\x8b\xb6Zv\x04\x8a\xb8D\t\xe94\x0b\x80\xe7\xa9\xd3\xa2\x9c\x15\x93(m\x8d\x82\x1c\x1a]\xe0\xef\x11V6\xea\xccb\x9bs\xb4\xef\xeeT\xa9\xde\xae\x98\x19\x18$m\x03\x1e\xe1\xc3\x00\xcbk>\xcf>~\xbe\x96\x96\xd7\x19\xe6\xd7R\x8e\xc4\x99\xeez~\x1c:\x8d\xdb&\xca\xa5C\xb9DV\xd8\xbbp\x0c\xf3\x06Jq3\x13\xb9R\x06u_Mi.\x04|m\xe2\x01\xa6\x9e{\x16!\xb03\xdf\x01I-\x8c\x8c\xe0\xe3\xb0 \x91\x9d\xb98\x04K\xcb\x9f4\xbf\xfaD\xf5\x1a\x9c\xa5]Y\x8aT2\x15PJg\xef&\xbe\x93\xb0\xb0\xc0pw\x02\x1d\x83\x0e"o\xb4\x17\x8d7\xe9f\xd1$\xb9d\xdb\x81Bv\x00\xfd\xd9\x95Y\xf6\x95 n\x1e\x92\xc17\x12X\xe3_\x15\x8d\xec\xa89\xcc#4X\x1ei\x9c%\rx\x93\xc5\xf6\xd4R\xd7,\xdftQ\x15\x0b\xaa\xa3\xb3\x85\x01\xca7\xe2\x12L\x9c\x9a\x11\x95u\xc30\x1c;xK\xc3\xf3\xd78~\xe6\x10\xc4\x9d\xdcmu\x08\x8fJ2`z\xe7\x8e\x82\xa8*eB\xc4\x1c\xcfr\n\xdd\xaa\xf1J\x03-\roV\xb6EY\xca\xcc\xd4g~\'\xb1\x15\xb7*\xca\x8c\x01\n\xe5Y\xd5\x85Y\x80s*xO\xc7\xba\xdd\xef\xf0\xd2E]\xc8\xf4\x15\xda\x8e\x11p\xa0\xac\x00\x9d\x8a\xee9I\'V\x94`HN\xa1Yq\xc4`i\x9e\xd3>$f\x99\x9dL\xeb{\xee<8)A\xdc\x8au\x9a]<\xe8\xf6\xa2\x80(\xb2B\x8eA\x0f\x8a\xb8\x03\xef\t\x1f\x86\x98\x0cI\n6\x9ca{\xca\xfc\x9b\x97\xd3E\xf7\x9a|\xed\n\xad\xd2\xc1\xd8\xe8wapX\xfa\x94M\xb1\xb4)\x9e\xd6\x98\xdf\x80^\x00\xd0x\xab_\n\xb2jt\xba<m\x8f\xa7K\xaa\xc1\xd8\xcc\x9bA\x16\x8c\x88\xae\xc5\x1b\xe5\'\xa3\x1c\xb2\xab\x9cl3\x7f/\xf3\xabI\xaaa=JWFk\x02\xca\xba\xb53MFz"\x83M\xa8\xc0\xd3W\xd2\x15\xe4\xd1\xbb\xaa\\).\xb9\x1b\xba-\x9fL0\xbb5\x8d\x80\xea$L\x89\xe5\xafHLtS\x9f\x86\xb9\xfa\xea&(\xb9\x1f&S\xf8\x91\xc7\xe2F\xfc\xc7\xd7\xd9\x81\x0c2\x08$\x92u\xe2\x10\xf0&\xab\xe1m\x0fX3\xb8:vQ\xdc\x16\x9b\x95\x85\xe6\xc3\xb3M\xc3e[\x18Q\xd6]\xcc\xb3@\x93\x82G\x8d\xfau\x0b\xdb\xde\xd4k\xe5)\xa1tW\xe3px\xf1!\x9e\x16&\x9f\x1c\'8\x04\xc4.*8\xed8q\xbfK\x851^\x02\xe7)1\x92V$x\xe9\xc7\xbcg\x00\x95t\x004Y\xc6q\x9cg\x0c\x9dg\x19\xc6q\x9c$\x96q\x9cg\tuZ\x920\x14d\xfe\xff\x00~\xe3\x87\x02T\x1c\xe0\xd1%)\'\x80_\x18\xf8\xcf\x03\xa56\x00\x9fv\xc88\xf9\x11\xd8\x92\x0f\xf0\xcf\xe9\xef\xc1\x17?\xd5m\x89\x0cpX`\xe3\xfa\xe3\xf68\x869\xda\x8c\xf6\xfc\xff\x00g\x8d\xbd\x9b\x85mGf~\xed8.{j\xe3\x1dM\xb9\x19\xe3\xc7\xa2\xd2\xb7\xdar\x181\x1e\xd8\xf6?\xcf\x1f\xe1\xf2\xe3\x8c\xe2\xc4\xe4\xfe\xbf\xb1\xc2\x14~\x0b\xfc\x11\xa77\xb2\xa1\x1e\x85\x1e\xacv\xc8\x1f&\xfa\xe7\xdb\x1f\xaf\x1dec\xd8\xb0\xbf\x80\\}\x11\xdb<3\x89\xb2p\xf2\xd7\x91\n\xd1\xa8\xe3r\xcf\xb0\xcf\xb1c\xf5\x1f<\x0e\xf8\xfa\x91\xc4\xb1\xc2}\x16\x85f\xa1T`\x0f\x97\n8\xe11x\x93\x88\xa8_\xbbp^\x89\x81\xc2\x8c5 \xcd\xfb\xca\xce3\x8c\xe38\xa4\xb4\x16q\x9cg\x19\xc2Ig\x19\xc6q\x9c$\x96q\x9cg\x19\xc2Ig\x19\xc6q\x9c$\x96q\x9cg\x19\xc2Ig\x19\xc6q\xe1\xe1$\xbc\'\x8fW\x8dx\xd9xI/x\xce3\x8dY\xf1\xfcxI-\xb8\xce96\xa0p\x91\xf5\x99\x1d\xb8\x90i(f\xa0\tV\xa3R\x14g\x887\xed\x01\xe7(\xd0".\t\x17V\n\xe8A\xda\xf8\xdc\xb9P7w\x00\x00;n\x14\xed\xdcd;y\xd5\xe6\x8ah4\xcfF\xb2L\x85bK\x14\xdc\xaa\x06\x0b\xac\xc9\xde\xfb\x19\x94\xb0U\xfc9\x19RW?-\xfc\xcd\xfbH\xd7]\xb2`\xb6\t\nI`\xc4\xb0\n=\'\x03h\xce\x02\x85\xdd\xec\x06X\x93\x9a\xf8\xaa\xa6\x8br\xb3\xea#\xc9S\xabP\xba\xc1B\x9e&\xd3,\xd9\x84\xc9]\x9bJ\x854eoN\xda)fl\xbe\xd2{\x9d\x8b\xdc\x90\x08\x1e\x84_\xe0\xbf\x10\xdbID$\x96\xdc\x85\x96~\xa7\xc2\x96"j\xa8\xc7x,w\x03\xf7lJ\x9c\xa8\xcfp\xc3\xa2\xd5\xf4\x88\x8d\x95\x95\x81V\x0cYX\x07\xda\xccKn\xec0\x00\xea!l\xe51\xff\x00\x98\x92s\x85b\r\xf6\x06\x99vF\xda\x15KW\xd8\x8e\xaa(fp\xc5\x81%\x9bs\x0e\xcc\xbe\x90)\\wM\xf9\xf1M7V_\xce\x7f4\xee\xc2e\xe8\xeb\xa8\xb2-\x8c\x89\x99\xcc+\xe8\x95\x14M\x86\xc2\xb6\x93\x01 \xa5\x80Q\xf8}D\xef\xcb\xfc\xc3\xea\xe9 J\xbb\xb2M\xf7\x1c\x15\xd9_\xbd\x93\xb6\x03\x16B\xa1\x83\x03P\x83\r\xbc\x82?\x043_\x1el\x94&\xf4\n\xd0\x0c\x14n\x98G|\xa6\xccVS\xc1!\xd3xq@P\x8c\x12\x0b\x03\xc1\xe7!\xe5\xfa\x8ah\xb7\x06D3\xae\x19\x9fm\x13\x1b\\\x02\x15\x9fz\x12^L\x12l\x81\xdc-\x03\x97f#\'\x16\x04\x078\xc5\xfc\xf5\xf3\xf9\xbdX\x12\x96xbZo\x8bSefJR\x87\'\xb5\x96I\n\x1c y-\x96"\xaf%\x07s\x1ad\x82\x14\x93\xc4\xab\xe1\xbf-ymu\x15\x85om@\x9a\x1a\xb9\x86\xa7W6\xb1\x9c\xe6W`\x16\t\xf7\xac\xb5\xa5\x11\x9c\x06UUU3]\xc6\x10\xd1L\x07`5\x13\x13\x91\x0eSN\xb4Z\n\x95!R\xaf:j+0\x8a\xc4.P\xb2+8\x12\xfe\xd3\x85\x92\xf1Qka\xa8\xd3\xc2L\xefx\xdd\x99\xf6\xe41fx\n\x16g\x07\xf1$\xfd\xc6\xd9\xcf\xd3\xd3\xb3N\xbb\xdb\x19Z\x0cq\xb2N\x05\x1a\x7f\xe1\xa9\xea55\xacuZ\x89$\xa5\xea\x82>\xa1\x81p\xca\x8c\x15\x99\x9d33\x80\xcb\x9a\xca\xc4a\x83n8\x93<\xba\xd3\xebt\xdbE\x1fO\xcc\xb4\xe97\xc4\xddD\xc9[a\xb5S\xa6\xe5}=iZ18w\x9a\xf7\xa398\x1cC~\x13\xe61W\xd4\x83P\xcb\xa8S\xea\xe9j2\x99i05\x0f3\xb4\x05\x9e\xed\xf5\x13\xcb\x0c\x95\x03\xb9.\xf0\xcf:N\x9dZ\x17K$\x89\xdd\xd0\xac\x9b\x15\x1b\x0b%:NB\xb0\xc0\xf4\xb0C\xb7,7gq\x93\xf1l\xc3\xbc<hF\xed$\x9d\'O\x04=,\x9e\xf5\xbe!1\xd4\x04\xd3\x9bt\xa65f\xfc\xbe\xb8\r\xa4\xf5S\xe1)\xa5\xc3\xe5\x14\xcf\xac\xaa\xa0\xbc\xadM3,\xde :\xd6\xf4\xf8\'\xc6I\xaa\xd3F\xc1\xd4\x9b"1\xdb\xed\x96P{|\xbb\xe7+\xdf\xb8=\xb2;\xf1D<{\xcd\xe1\xa8\xf8k#\xa55Zhj\xa6\xd5\x9b)3\xeaT\xdaH\xd6\x07\xb22\xfd\xe1FS\x90\xa2\x9b\x08\xec\xc6>Py\xb2#-\x1e\x9a\x93\xd8\x1f\xa12\x89\x91\xd3d\xeezc\xd8!$m\xc7\xe1\x07\x03\x18\xc8\xbbO\x1a\xcau\xcb5\x0e\x8f\x03\x16\xfc%\x16W\xa6/\xc2\xf9\xb6x\x0f\x87\x88\xd7\xaa\xd3\xc8!zx\xc7\xd5\xcb\x03\xea=\x8e0\xa7\xb7\xb6pNp8"\xe5\xbc\xc06q\xfd\xd6+\xfcW\xb3c\xf4=\xbfQ\xc6\xe5F\xa8\x82\x9dUx\xd8\x0e<C\xc6\xdcUWF\x8b8\xce3\x8c\xe1\x94\x96q\x9cg\x19\xc2Ig\x19\xc6q\x9c$\x96q\xa8N6\xe38I!\xaf\x1a\xf3\x15Y\x95#$\xff\x00!\xf3\x19\xfe]\x86x\x88u\xb5\xcfs\xc4\xa3\xe6\').\xaa\xe0\x9c.C\x0f\x960H?\x97\xd0\x9f\xcc~\x84F\x1c\xb5\x02\xab\xb0\x18b@\xc6~\x9f\xcf\xdf\xb6}\xb2\x0f\x1dV\xce{)\xd2\x07RW\x15\xb4\xd8\xfa\x95\x886\x1e\xc8\x7f\x97\xf8}\xe87\x01\xdb\xdb\xb6=\xfe\x98\xf7\xcf\x127\x84<\x14\xf1\xda\xe4\x8e\xf8%G\xcb\xe9\xdf\x1e\xff\x00\xe5\xc2\x8eU\xcef\xbbQf\x14\x1f\xe7\xfa\xfb~\xf3\xc1|\x9b |\xbf.*\xe3\xb1\xd5\\2\xc4\x03\xf6V\xf6v\xcf\xa2\x0ei\x92\x16\xfcg\x1aE\xf2\x01\xc63\xfb\x1f!\xf2\xe3bx\xe7\xd7T\xbd\xe38I\x0eh\x8d\xec\xca{\x91\xd8\x8fub\x8c?\x83\x82\xbf\xa8\xe1\x1f\x8b<D\xbaM5u\x0e@X\xa39\'\xf2\x1fL\x8c\x9f\xa2\x82\x0b\x1e\xc3\xb9\xe1%+^a\xe3-4\xac4\xf4\xbc\xd2\xac7,\xd9\xd49Rv\x86\x08{\x90[\xd2\x0e0X\x85\xf7 p\xf0\x0f\x1f5<]\xe7^\xa3Yh\xf3\r\xfd*\t\xdd\x8b)\x8fb\x89e+\xb9IuP\x02\x91\xd9\t`\xb3\x99\x0fB\x04\xf7\xe5\xbf\xda\x9a\xac\xbd\x0bz\xd9\xa2\xa1*\xb8m\xb7]\xe9vrd\xa6\x


# search_locations=['Tower of London', 'Westminster Abbey', 
#                   'Buckingham Palace', 'Churchill War Rooms', 
#                   'The British Museum', 'Canterbury Cathedral', 
#                   'Stonehenge', 'Roman Baths', "St. Paul's Cathedral", 
#                   'Edinburgh Castle']

#도쿄 애니메이션 여행
#search_locations=['J-World Tokyo(Ikebukuro, Tokyo, Japan)', 'Tokyo Anime Center(Chiyoda City, Tokyo, Japan)', 'Otome Road(Ikebukuro, Tokyo, Japan)']
