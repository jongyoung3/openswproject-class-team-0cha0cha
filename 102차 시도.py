import googlemaps
import folium
import webbrowser
import requests
from geopy.distance import geodesic
from datetime import datetime
from googlemaps import convert



#n=int(input("지점 개수: "))
lat=[]
lon=[]
site=['Tokyo(Kanto Region, Japan)', 'Kyoto(Kansai Region, Japan)', 'Osaka(Kansai Region, Japan)', 'Hiroshima(Chugoku Region, Japan)', 'Nara(Kansai Region, Japan)']
n=len(site)
# API 키
API_KEY = 'AIzaSyB8I74JlUYDKbZyDCQs2vAtelO9FrGKNGA'

gmaps = googlemaps.Client(key=API_KEY)

# Geocoding API 엔드포인트
geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'

    
for i in range(n):
    
    wanted=site[i]
    
    # 요청 파라미터
    params = {
        'address': wanted,
        'key': API_KEY,
    }

    # geocode API 요청 보내기
    response = requests.get(geocode_url, params=params)

    # 응답 처리, 좌표 구하기
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            # 첫 번째 결과의 좌표 얻기
            location = data['results'][0]['geometry']['location']
            lat.append(location['lat'])
            lon.append(location['lng'])
        else:
            print('장소를 찾을 수 없습니다.')
    else:
        print('API 요청 실패')

loong=0
origin=[(0.0),(0.0)]
destination=[(0.0),(0.0)]
# 지점 저장
point = []
for i in range(n):
    point.append([lat[i], lon[i]])
    print(site[i])
    print(point[i])


# 시작점, 도착점
for i in range(n - 1): 
    for j in range(n - 1):
        distance = geodesic(point[i], point[j]).meters
        if(distance > loong):
            loong=distance
            origin=point[i]
            destination=point[j]
            a=i
            b=j
    if (i==n-2):
        del(point[a])
        del(point[b-1])
   

# 지도 생성
map = folium.Map(location=origin, zoom_start=5)

for i in range(n-1):
    
    
    #마커 찍기
    if i == 0:
        folium.Marker([lat[i], lon[i]], popup=site[i]).add_to(map)

    folium.Marker([lat[i+1], lon[i+1]], popup=site[i+1]).add_to(map)
    



directions_response=gmaps.directions(origin,destination,mode='driving',waypoints=point,optimize_waypoints = True)

if len(directions_response) > 0 and 'legs' in directions_response[0]:
    for i in range(n-1):
        route = directions_response[0]['legs'][i]

        points = []
        for step in route['steps']:
            start = (step['start_location']['lat'], step['start_location']['lng'])
            end = (step['end_location']['lat'], step['end_location']['lng'])
            points.extend([start, end])

        
       
        folium.PolyLine(points, color='blue', weight=1).add_to(map)
           
    
else:
    print(f"No directions found for the route from {site[i]} to {site[i+1]}")


