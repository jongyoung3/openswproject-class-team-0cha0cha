import googlemaps
import folium
import webbrowser
import requests
from geopy.distance import geodesic
#lat,lon구하기
def FindLatLon(API_KEY,site):
    lat=[]
    lon=[]
    
    #지점 개수
    n=len(site)
    
    
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
    site=[]
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

#맵 생성
def CreateMap(origin):
    map = folium.Map(location=origin, zoom_start=11)
    return map

#마커찍기
def mark(map,point,n):
    for i in range(n):
        folium.Marker([point[i][0],point[i][1]]).add_to(map)
        
#경로 그리기        
def DrawDirec(origin,destination,locations,gmaps,map,opt,n):
    
    directions_response=gmaps.directions(origin,destination,mode='driving',waypoints=locations,optimize_waypoints = opt)

    
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
        print("No directions found")

# HTML 파일로 저장
def ReturnHTML(map):
    map.save('route.html')
    
    return 'route.html'

# 생성된 HTML 파일 열기
def OpenMap(html):
    webbrowser.open(html)
    
# 총괄 함수
def MainFunc(API_KEY,point,opt=0):
    n=len(point)
    gmaps = googlemaps.Client(key=API_KEY)
    locations=[]
    # 시작점, 도착점
    if (opt==1):
        origin,destination,locations=FindOriDes(point,n)
    else:
        origin=point[0]
        destination=point[n-1]
        for i in range(1,n-1):
            locations.append(point[i])
            
    map=CreateMap(origin)

    #마커 찍기 함수
    mark(map,point,n)
    
    DrawDirec(origin,destination,locations,gmaps,map,opt,n)
    
    html=ReturnHTML(map)
    OpenMap(html)
    return html
