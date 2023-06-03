import googlemaps
import folium
import webbrowser
import requests
from geopy.distance import geodesic

#lat,lon
def FindLatLon(API_KEY,site):
    lat=[]
    lon=[]
    
    #지점 개수
    n=len(site)
    
    
    gmaps = googlemaps.Client(key=API_KEY)
    
    # Geocoding API 엔드포인트
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'

    #site 별 좌표 찾기   
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

    return lat,lon,gmaps,n

# 지점 저장
def ReturnPoint(lat,lon,n):
    point = []
    for i in range(n):
        point.append([lat[i], lon[i]])

    return point

#시작점, 도착점 설정 및 경유지 리스트 생성
def FindOriDes(point,n):
    loong=0
    temp=[]
    temp.extend(point)
    for i in range(n-1): 
        j=i+1
        for j in range(j,n):
            distance = geodesic(temp[i], temp[j]).meters
            if(distance > loong):
                loong=distance
                origin=temp[i]
                destination=temp[j]
                a=i
                b=j
        if (i==n-2):
            del(temp[a])
            del(temp[b-1])
    
    return origin,destination,temp

#맵 
def CreateMap(origin):
    map = folium.Map(location=origin, zoom_start=11)
    return map

#마커찍기
def mark(map,n):
    for i in range(n):
        folium.Marker([lat[i], lon[i]], popup=site[i]).add_to(map)
        
#경로 그리기        
def DrawDirec(origin,destination,locations,gmaps,map,n):
    
    directions_response=gmaps.directions(origin,destination,mode='driving',waypoints=locations,optimize_waypoints = True)

    
    if len(directions_response) > 0 and 'legs' in directions_response[0]:
        
        for i in range(n-1):
            route = directions_response[0]['legs'][i]

            points = []
            for step in route['steps']:
                start = (step['start_location']['lat'], step['start_location']['lng'])
                end = (step['end_location']['lat'], step['end_location']['lng'])
                points.extend([start, end])

            
        
            folium.PolyLine(points, color='blue', weight=5).add_to(map)
            
        
        else:
            print(f"No directions found for the route from {site[i]} to {site[i+1]}")

# HTML 파일로 저장
def ReturnHTML(map):
    map.save('route.html')
    
    return 'route.html'

# 생성된 HTML 파일 열기
def OpenMap(html):
    webbrowser.open(html)
   
#지점 입력
#site=['Ghibli Museum(Mitaka, Tokyo, Japan)', 'Akihabara(Chiyoda City, Tokyo, Japan)', 'Odaiba(Minato City, Tokyo, Japan)', 'Nakano Broadway(Nakano, Tokyo, Japan)', 'Pokemon Center Tokyo(Chuo City, Tokyo, Japan)', 'J-World Tokyo(Ikebukuro, Tokyo, Japan)', 'Animate Ikebukuro(Toshima City, Tokyo, Japan)', 'Tokyo Anime Center(Chiyoda City, Tokyo, Japan)', 'Otome Road(Ikebukuro, Tokyo, Japan)', 'Shinjuku Wald 9(Shinjuku City, Tokyo, Japan)']
 
#lat,lon,gmaps,n=FindLatLon('AIzaSyB8I74JlUYDKbZyDCQs2vAtelO9FrGKNGA',site)

# 시작점, 도착점
#origin,destination,locations=FindOriDes(ReturnPoint(lat,lon,n),n)

#map=CreateMap(origin)

#마커 찍기 함수
#mark(map,n)

#DrawDirec(origin,destination,locations,gmaps,map,n)

#html=ReturnHTML(map)
#OpenMap(html)
