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
import folium
import webbrowser
import requests
from geopy.distance import geodesic
import matplotlib.pyplot as plt



n=int(input("몇 개의 지점? "))
lat1=[]
lon1=[]
#distance=[]
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


# 맵 생성
map = folium.Map(location=[lat1[0], lon1[0]], zoom_start=13)

for i in range(n-1):
    '''
    
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
    
    '''
    origin=(lat1[i],lon1[i])
    destination=(lat1[i+1],lon1[i+1])
    base_url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'key': API_KEY,
        'origin': origin,
        'destination': destination
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if data['status'] == 'OK':
        routes = data['routes']
        for route in routes:
            # 경로 좌표를 가져옵니다.
            points = route['overview_polyline']['points']
            
            # 좌표를 디코딩하여 경로의 위도와 경도 리스트로 변환합니다.
            decoded_points = decode_polyline(points)
            latitudes = [point[0] for point in decoded_points]
            longitudes = [point[1] for point in decoded_points]
            
            # 경로를 그립니다.
            plt.plot(longitudes, latitudes, color='blue')
            
        # 출발지와 도착지를 표시합니다.
        plt.scatter([origin[1]], [origin[0]], color='green', label='출발지')
        plt.scatter([destination[1]], [destination[0]], color='red', label='도착지')
        
        # 그래프를 표시합니다.
        plt.legend()
        plt.show()
    else:
        print("Directions API request failed.") 