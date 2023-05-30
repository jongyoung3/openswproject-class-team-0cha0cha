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
distance=[]
site=['Tokyo(Kanto Region, Japan)', 'Kyoto(Kansai Region, Japan)', 'Osaka(Kansai Region, Japan)', 'Hiroshima(Chugoku Region, Japan)', 'Nara(Kansai Region, Japan)']
n=len(site)
waypoints=[site[1],site[2],site[3]]
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

    
origin=(lat[0],lon[0])
# 지도 생성
map = folium.Map(location=origin, zoom_start=5)

for i in range(n-1):
    
    
    #마커 찍기
    if i == 0:
        folium.Marker([lat[i], lon[i]], popup=site[i]).add_to(map)

    folium.Marker([lat[i+1], lon[i+1]], popup=site[i+1]).add_to(map)
    
origin=(lat[0],lon[0])
destination=(lat[4],lon[4])



directions_response=gmaps.directions(origin,destination,mode='driving',waypoints=waypoints,optimize_waypoints = True)

if len(directions_response) > 0 and 'legs' in directions_response[0]:
    for i in range(n-1):
        route = directions_response[0]['legs'][i]

        points = []
        for step in route['steps']:
            start = (step['start_location']['lat'], step['start_location']['lng'])
            end = (step['end_location']['lat'], step['end_location']['lng'])
            points.extend([start, end])

        print(points)
        # 경로 그리기
        for i in range(n-1):
            folium.PolyLine(points, color='blue', weight=i+1).add_to(map)
           
    
else:
    print(f"No directions found for the route from {site[i]} to {site[i+1]}")
    
    

        
# HTML 파일로 저장
map.save('route.html')

# 생성된 HTML 파일 열기
webbrowser.open('route.html')


