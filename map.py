import googlemaps
import folium
import webbrowser
import requests
from apikey import GoogleMap_API_KEY
from geopy.distance import geodesic

#lat,lon구하기
# def FindLatLon(site):
#     lat=[]
#     lon=[]
#
#     #지점 개수
#     n=len(site)
#
#
#     # Geocoding API 엔드포인트
#     geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
#
#     #site 별 좌표 찾기
#     for i in range(n):
#
#         wanted=site[i]
#
#         # 요청 파라미터
#         params = {
#             'address': wanted,
#             'key': GoogleMap_API_KEY,
#         }
#
#         # geocode API 요청 보내기
#         response = requests.get(geocode_url, params=params)
#
#         # 응답 처리, 좌표 구하기
#         if response.status_code == 200:
#             data = response.json()
#             if data['status'] == 'OK':
#                 # 첫 번째 결과의 좌표 얻기
#                 location = data['results'][0]['geometry']['location']
#                 lat.append(location['lat'])
#                 lon.append(location['lng'])
#             else:
#                 print('장소를 찾을 수 없습니다.')
#         else:
#             print('API 요청 실패')
#
#     return lat,lon,gmaps,n

# 지점 저장
# def ReturnPoint(lat,lon,n):
#     point = []
#     for i in range(n):
#         point.append([lat[i], lon[i]])
#     return point

def decode_polyline(polyline):
    """Decodes a Polyline string into a list of lat/lng dicts.

    See the developer docs for a detailed description of this encoding:
    https://developers.google.com/maps/documentation/utilities/polylinealgorithm

    :param polyline: An encoded polyline
    :type polyline: string

    :rtype: list of dicts with lat/lng keys
    """
    pointse = []
    index = lat = lng = 0

    while index < len(polyline):
        result = 1
        shift = 0
        while True:
            b = ord(polyline[index]) - 63 - 1
            index += 1
            result += b << shift
            shift += 5
            if b < 0x1f:
                break
        lat += (~result >> 1) if (result & 1) != 0 else (result >> 1)

        result = 1
        shift = 0
        while True:
            b = ord(polyline[index]) - 63 - 1
            index += 1
            result += b << shift
            shift += 5
            if b < 0x1f:
                break
        lng += ~(result >> 1) if (result & 1) != 0 else (result >> 1)

        pointse.append({"lat": lat * 1e-5, "lng": lng * 1e-5})

    return pointse

#시작점, 도착점 설정 및 경유지 리스트 생성
def FindOriDes(point,n):
    loong=0
    temp=[]
    temp = point[:]
    index_ori = -1
    index_dest = -1
    for i in range(n):
        j = i + 1
        for j in range(j,n):
            distance = geodesic(temp[i], temp[j]).meters
            if(distance > loong):
                loong=distance
                origin=temp[i]
                index_ori = i
                destination=temp[j]
                index_dest = j

    temp[index_ori] = [-1]
    temp[index_dest] = [-1]

    temp.pop(temp.index([-1]))
    temp.pop(temp.index([-1]))

    return origin,destination,temp, index_ori, index_dest

#맵 생성
def CreateMap(origin):
    map = folium.Map(location=origin, zoom_start=11)
    return map

#마커찍기
def mark(map,point,names, n):
    for i in range(n):
        folium.Marker([point[i][0],point[i][1]],popup=names[i]).add_to(map) # popup= 으로 위에 글 띄우기 가능

#경로 그리기
def DrawDirec(origin,destination,locations,gmaps,map,opt,n):

    directions_response=gmaps.directions(origin,destination,mode='driving',waypoints=locations,optimize_waypoints = opt)

    if len(directions_response) > 0 and 'legs' in directions_response[0]:

        for i in range(n-1):
            route = directions_response[0]['legs'][i]

            points = []



            for step in route['steps']:
                temp = decode_polyline(step['polyline']['points'])
                for pointed in temp:
                    points.append((pointed['lat'],pointed['lng']))
                # start = (step['start_location']['lat'], step['start_location']['lng'])
                # end = (step['end_location']['lat'], step['end_location']['lng'])



            folium.PolyLine(points, color='blue', weight=4).add_to(map)



        if opt == 1: ##### 디렉션 리스폰스에서, 정렬된 데이터 관련 응답. 단, 웨이포인트 오더로 인한 갯수 오류가 있을지 우려됨
            return directions_response[0]['waypoint_order']
        return 0

    else:
        print("No directions found")
        return -1


# HTML 파일로 저장
def ReturnHTML(map):
    map.save('route.html')

    return 'route.html'

# 생성된 HTML 파일 열기
def OpenMap(html):
    webbrowser.open(html)

# 총괄 함수
def MainFunc(point,names, opt=0,retry = 0):
    if retry >= 3:
        return "-99", 0
    try:
        n=len(point)
        gmaps = googlemaps.Client(key=GoogleMap_API_KEY)
        locations=[]
        # 시작점, 도착점
        if (opt==1):
            origin,destination,locations, index_ori, index_dest=FindOriDes(point,n)
        else:
            origin=point[0]
            destination=point[n-1]
            for i in range(1,n-1):
                locations.append(point[i])

        # 맵 시작지점과 비율 관련 조절 관련 생각######
        # zoom = int(geodesic(origin, destination).meters / 50000)
        # mid_x = (origin[0] + destination[0]) / 2 # mid 대신 다른걸 찾는 방법 생각해봐야함
        # mid_y = (origin[1] + destination[1]) / 2
        # mid = (mid_x,mid_y)
        map=CreateMap(origin)

        #마커 찍기 함수

        mark(map, point, names, n)

        if opt == 1: # 웨이포인트 오더 데이터 정리 부분
            real_waypoint_order = [0, 0, 0, 0, 0]
            waypoint_order = DrawDirec(origin,destination,locations,gmaps,map,opt,n)
            temp_p = point[:]
            real_waypoint_order[0] = index_ori

            real_waypoint_order[4] = index_dest

            temp_p[index_ori] = (-1,)
            temp_p[index_dest] = (-1,)
            for i in range(len(waypoint_order)):
                k = 0
                j = 0
                while 1:
                    if temp_p[j] == (-1,):
                        j += 1
                        continue
                    if waypoint_order[i] == k:
                        break
                    else:
                        j += 1
                        k += 1
                real_waypoint_order[1 + i] = j
            html = ReturnHTML(map)
            return [html, real_waypoint_order]
        else:
            opti_checker = DrawDirec(origin, destination, locations, gmaps, map, opt, n)
            html=ReturnHTML(map)
            # OpenMap(html)
            return [html, opti_checker]
    except:
        retry += 1
        print("google map error")
        return MainFunc(point,names, opt,retry)