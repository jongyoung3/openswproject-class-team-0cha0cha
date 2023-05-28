'''import googlemaps
import folium
import webbrowser
import folium
import requests
from geopy.distance import geodesic
n=2
lat=[0.0,0.0]
lon=[0.0,0.0]
distance=[]
site=["",""]
for i in range(n):
    site[i]=input("장소 입력: ")
# API 키

wanted=''
# API 키
API_KEY = 'AIzaSyAg-D0M1X87OyIMkyTMmU6rNRJjFTP8ebI'

# Geocoding API 엔드포인트
url = 'https://maps.googleapis.com/maps/api/geocode/json'

# 요청 파라미터
params = {
    'address': wanted,
    'key': API_KEY,
}

# API 요청 보내기
for i in range(n):
    wanted=site[i]
    response = requests.get(url, params=params)

    # 응답 처리
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            # 첫 번째 결과의 좌표 얻기
            location = data['results'][0]['geometry']['location']
            lat[i] = location['lat']
            lon[i] = location['lng']
        else:
            print('장소를 찾을 수 없습니다.')
    else:
        print('API 요청 실패')

# 맵 생성
map = folium.Map(location=[lat[0], lon[0]], zoom_start=13)

for i in range(n):
    # 좌표 설정 
    latitude = lat[n]
    longitude = lon[n]



    # 맵에 마커 추가
    folium.Marker([latitude, longitude], popup=site[n]).add_to(map)

#지점 저장
point=[]
for i in range(n):
    point.append([lat[i],lon[i]])    
    
#거리 저장
for i in range(n-1):
    distance[i] = geodesic(point[i], point[i+1]).meters
    
folium.PolyLine(locations=[point[i], point[i+1]], color='blue', weight=2.5, opacity=1).add_to(map)
    
# 맵 저장
map.save('map.html')


webbrowser.open('map.html')



#지도를 사진으로 저장

# API 키
API_KEY = 'AIzaSyAg-D0M1X87OyIMkyTMmU6rNRJjFTP8ebI'

# 구글 지도 API 엔드포인트
url = f'https://maps.googleapis.com/maps/api/staticmap?key={API_KEY}'

# 요청 파라미터
params = {
    'center': '서울',
    'zoom': 13,
    'size': '600x400',
    'maptype': 'roadmap',
}

# API 요청 보내기
response = requests.get(url, params=params)

# 응답 처리
if response.status_code == 200:
    # 이미지 파일로 저장
    with open('map.png', 'wb') as file:
        file.write(response.content)
    print('지도 이미지 저장 완료')
else:
    print('지도 이미지 가져오기 실패')
'''
import googlemaps
import gmaps
import folium
import webbrowser
import requests
from geopy.distance import geodesic
from datetime import datetime


n=int(input("몇개의 지점?"))
lat1=[]
lon1=[]
distance=[]
site=[]
for i in range(n):
    temp=input("장소 입력: ")
    site.append(temp)

# API 키
API_KEY = 'AIzaSyAg-D0M1X87OyIMkyTMmU6rNRJjFTP8ebI'

# Geocoding API 엔드포인트
geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'

    
for i in range(n):
    
    wanted=site[i]
    # 요청 파라미터
    
    
    params = {
        'address': wanted,
        'key': API_KEY,
    }

    # API 요청 보내기
    response = requests.get(geocode_url, params=params)

    # 응답 처리
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            # 첫 번째 결과의 좌표 얻기
            location = data['results'][0]['geometry']['location']
            lat1.append(location['lat'])
            lon1.append(location['lng'])
        else:
            print('장소를 찾을 수 없습니다.')
    else:
        print('API 요청 실패')

gmaps.configure(api_key=API_KEY)
fig=gmaps.figure()
for i in range(n-1):
    origin=(lat1[i],lon1[i])
    destination=(lat1[i+1],lon1[i+1])
    layer=gmaps.directions.Directions(origin,destination,mode="driving",avoid="ferries",departure_time=0)
    fig.add_layer(layer)
fig.show()



 

# 맵 생성
map = folium.Map(location=[lat1[0], lon1[0]], zoom_start=13)
'''
for i in range(n-1):
    # Directions API 엔드포인트
    directions_url = 'https://maps.googleapis.com/maps/api/directions/json'
    
    la=lat1[i]
    lo=lon1[i]
    lap=lat1[i+1]
    lop=lon1[i+1]
    
    # 경로 요청 파라미터
    directions_params = {
        'origin': f"{la},{lo}",
        'destination': f"{lap},{lop}",
        'key': API_KEY,
    }
    
    # 경로 API 요청 보내기
    directions_response = requests.get(directions_url, params=directions_params)
    directions_data = directions_response.json()
    routes = directions_data['routes']
    
    #마커 표시
    if i==0:
        folium.Marker([lat1[i], lon1[i]], popup=site[i]).add_to(map)
    folium.Marker([lat1[i+1], lon1[i+1]], popup=site[i]).add_to(map)
    
    # 경로 그리기
    for route in routes:
        steps = route['legs'][0]['steps']
        for step in steps:
            polyline = step['polyline']['points']
            coordinates[] = polyline
            coords = []
            for coord in coordinates:
                lat = coord[0]
                lng = coord[1]
                coords.append([lat, lng])
            folium.PolyLine(locations=coords, color='red', weight=2.5, opacity=1).add_to(map)

# 맵 저장
map.save('map.html')


webbrowser.open('map.html')
'''