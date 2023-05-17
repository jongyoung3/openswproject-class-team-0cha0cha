import requests

# 구글지도 api에서 관광명소 이름, 평점, 리뷰 수를 가져오는 함수
def get_attractions(api_key, location, min_rating, min_reviews, max_attractions=2):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=tourist+attractions+in+{location}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    attractions = []
    places = []
    
    for result in data['results']:
        name = result.get('name')
        rating = result.get('rating')
        reviews = result.get('user_ratings_total')

        # 관광명소, 평점, 리뷰가 있는 것만 추가
        if name is not None and rating is not None and reviews is not None:
            if rating >= min_rating and reviews >= min_reviews:
                attractions.append(( name, rating, reviews))
            else:
                places.append((name, rating, reviews))
               

    # 받은 관광명소 내림차순으로 정렬해서 그 중 위의 2개 반환 
    attractions.sort(key=lambda x: (x[1], x[2]), reverse=True)

    if attractions:
        return attractions[:max_attractions]  # Return top attractions
    else:
        return places[:max_attractions]  # Return top places if no attractions found


# API 키
api_key = 'AIzaSyAg-D0M1X87OyIMkyTMmU6rNRJjFTP8ebI'

# chat_gpt api를 통해 받은 장소 데이터
search_location = ['Ginza', 'Shibuya 109', 'Harajuku', 
'Omotesando', 'Tokyo Solamachi', 
'Mega Don Quijote Shibuya', 
'Kiddy Land Harajuku', 'Kitkat Chocolatory', 
'Tsukiji Outer Market', 'Odaiba VenusFort'] 

min_rating = 0  # 최소 평점
min_reviews = 0  # 최소 리뷰 수
max_attractions = 2  # 선택할 수 있는 최대 관광명소의 개수

# 출력
for location in search_location:
    results  = get_attractions(api_key, location, min_rating, min_reviews, max_attractions)

    if results:
        for result  in results:
            name, rating, reviews = result
            print(f"Search_location: <{location}>\nName: {name}\nRating: {rating}\nNumber of Reviews: {reviews}\n")
            print("---------------------------------------\n")
    
