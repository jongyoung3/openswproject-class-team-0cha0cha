from apikey import OPENAI_API_KEY, RapidAPI_KEY  # 보안을 위해, 따로 저장한 apikey
import json


def gpt(topic, n=10, except_list=[], retry=0, add=0):
    # topic = 토픽, n = 탐색 개수, except_list = 중복 검색 방지를 위해, 제외하고 검색할 장소 목록,
    # retry = 재귀 횟수, add = gpt함수 내 갯수 부족 등으로 result extend 필요시 활용위한 표시 변수
    if retry >= 3:
        return []  # 다차례 오류 발생시 공백리스트 리턴
    import openai

    openai.api_key = OPENAI_API_KEY

    model = "gpt-3.5-turbo"

    # 학습 데이터들
    train_topic = "'''tokyo shopping travel'''"

    prev2 = """
    {
    "destinations": [
        {
            "name": "Shibuya Crossing",
            "region": "Shibuya, Tokyo, Japan",
            "description": "One of the most famous and busiest intersections in Tokyo, Shibuya Crossing is a must-visit destination for any shopper. Featuring a vast array of department stores, boutiques, and specialty shops, it's the perfect place to find the latest fashion trends and unique souvenirs."
        },
        {
            "name": "Ginza",
            "region": "Chuo City, Tokyo, Japan",
            "description": "Known as one of the most luxurious shopping districts in the world, Ginza is home to high-end stores like Chanel, Gucci, and Dior. Apart from luxury boutiques, the area is also home to department stores, art galleries, and traditional Japanese craft shops."
        },
        {
            "name": "Shinjuku",
            "region": "Shinjuku City, Tokyo, Japan",
            "description": "A shopping mecca, Shinjuku offers an incredible variety of stores, restaurants, and entertainment venues. Its bustling streets and towering skyscrapers house a seemingly endless range of shopping options, from major department stores like Isetan and Takashimaya to unique local boutiques."
        },
        {
            "name": "Harajuku",
            "region": "Shibuya City, Tokyo, Japan",
            "description": "Famous for its vibrant street fashion, Harajuku is a haven for shoppers seeking the latest trends. Takeshita-dori street is the place to go for kawaii accessories, while Omotesando Avenue offers high-end designer shops and sleek modern architecture."
        },
        {
            "name": "Ameyoko Market",
            "region": "Taito City, Tokyo, Japan",
            "description": "Located beneath the railway tracks near Ueno Station, Ameyoko Market is a bustling location famous for its vibrant street market atmosphere. With over 400 shops selling everything from clothing to seafood, this is the perfect place to discover a unique shopping experience."
        },
        {
            "name": "Nakamise Shopping Street",
            "region": "Asakusa, Tokyo, Japan",
            "description": "One of Tokyo's oldest shopping districts, Nakamise Shopping Street is a pedestrian street lined with traditional stores selling sweets, souvenirs, and other Japanese trinkets. Located directly in front of the ancient Senso-ji Temple, this is a destination not to be missed."
        },
        {
            "name": "Odaiba",
            "region": "Minato City, Tokyo, Japan",
            "description": "A popular shopping and entertainment district, Odaiba offers something for everyone. From high-end boutiques and gourmet restaurants to family-friendly attractions like Legoland Discovery Center and Sega Joypolis, this futuristic island in Tokyo Bay is a must-visit."
        },
        {
            "name": "Musashi-Kosugi",
            "region": "Kawasaki, Kanagawa Prefecture, Japan",
            "description": "Located just outside of Tokyo in the city of Kawasaki, Musashi-Kosugi is a popular destination for shopping and dining. With a large selection of department stores, restaurants, and specialty shops, this bustling area is frequented by both locals and tourists alike."
        },
        {
            "name": "Ikebukuro",
            "region": "Toshima City, Tokyo, Japan",
            "description": "One of Tokyo's three major hubs, Ikebukuro is a lively district with abundant shopping and dining options. Featuring several large department stores, specialty shops like the Pokemon Center, and the Sunshine City complex, there's no shortage of things to explore here."
        },
        {
            "name": "Kappabashi-dori",
            "region": "Taito City, Tokyo, Japan",
            "description": "Known as the 'Kitchen Town' of Tokyo, Kappabashi-dori is home to over 170 shops selling cooking supplies and equipment. From exquisite Japanese knives to elaborate plastic food replicas, this unique shopping district is a must-visit for any food lover."
        }
    ],
    "topic_introduction": [
        "Tokyo is known for its unique shopping culture, offering everything from luxury brands to quirky accessories and traditional crafts. Whether you're looking for stylish boutiques or bustling street markets, Tokyo has something for every shopping enthusiast. Don't miss out on the chance to discover the latest trends and bring home one-of-a-kind souvenirs from this vibrant city."
        ]
    }
    """
    # 사전학습 데이터
    systemsay = f"""
    You are in the middle of a preliminary study to answer the following questions:
    Find me Exactly 10 of travel destinations related to the topic.
    In the following user query, topic will be provided wrapped in triple backticks.
    Topic can be provided in a variety of languages. Translate the topic to English for you.
    Provide the results in the following order :
    Step 0. Imagine yourself as an expert travel guide AI speaking English. Do not say any other languages.
    Step 1. Follow the following conditions wrapped in angle brackets and find 10 of travel destinations related to topic in English :
    < You must only write places that can be cited and verified on Google Maps.
    You must only write places you can drive to.
    You should include places that are heavily visited and has high ratings by tourists.
    destinations must be close each other. So, The distances between all of each travel destinations must be less than 10km.
    You must write close destinations(destinations in same or close administrative region, district or area) back-to-back.
    You must arrange the destinations order so that all destinations are visited in an optimal path. >
    Step 2. Be sure to follow the precautions in Step 1 to ensure that condition is complete at all of each destination and if any of the conditions are not met, fix what you find.
    Step 3. Follow the following conditions wrapped in angle brackets and find region name where the travel destinations belongs to.
    < If the region is multiple, write the only one region that is most representative. >
    Step 4. write 3 sentences introductions and to each destination.
    Step 5. lastly, write 2 sentences introductions about topic.
    Step 6. provide the output that is 10 of travel destinations related to topic in English and only json format. The order of the output must satisfy the conditions in Step 1.
    Your output should be in json format with two list and have the following fields in first list :
     'name', 'region', 'description'. first list key is "destinations".
    In second list, You should write only introduction about topic. Second list key is "topic_introduction".
    """

    # 아래 오류목록 참고해서, 확인 후 고쳐보고.

    # 하시마 섬 등 드라이빙으로 경로를 알아낼 수 없는 경우. #############

    # 2. 먼거리 추천 에러 step1 요구사항 3,4,5번 라인###





    # 재검색시 지역전체소개는 빼도록 하면 속도개선 가능. (0으로 대충 답변하게 추가는 했지만, 잘 x), 주요기능은 x
    # 3. 특정 지역 제외 후 재검색 기능 비작동 ( 영국 시계탑 중복 추천 등 일부 chatgpt가 실수하는 경우 있음. 드문 빈도. 다만, 관찰 필요. 무시해도 가능할 정도로 보임.) 주요문제는 x
    # 번역에서의 오류. 왜 나는거지.? 해결된 것으로 보이나, 관찰 필요
    # 개수 체크 필요 자꾸 1개 달라는데 최초 케이스에서, 5개 주고 막 그럼. 아마 prev 데이터 때문에 헷갈려하는거 같아. 해결된 것으로 보이나, 관찰 필요
    prev_query = f"""
    in next answer, You must find Exactly {n} of travel destinations related to topic in English. 
    So, your output has {n} of travel destinations related to topic.
    The rest of the instructions are the same as preliminary study.
    """

    query = f"```{topic} ```in English"

    messages = [
        {"role": "system", "content": systemsay},
        {"role": "user", "content": train_topic},
        {"role": "assistant", "content": prev2},
        {"role": "user", "content" : prev_query},
        {"role": "user", "content": query}
    ]

    # 중복제거가 필요할 시, 추가 학습 진행
    if except_list != []:
        except_destination = ", ".join(except_list)
        systemsay2 = f"""
        in next answer, You must find Exactly {n} of travel destinations related to topic in English, And You should follow the following conditions wrapped in angle brackets too.
        < First, You must exclude the destinations wrapped in following double backticks. So, you must find the destinations that is not provided in following double backticks.
        ``{except_destination}``. this is Top priority requirement.
        Second, You don't need to write 2 sentences introductions about topic. Instead, Just write '0'. > 
        The rest of the instructions are the same as preliminary study.
        """
        messages = [
            {"role": "system", "content": systemsay},
            {"role": "user", "content": train_topic},
            {"role": "assistant", "content": prev2},
            {"role": "user", "content": systemsay2},
            {"role": "user", "content": query}
        ]

    response = openai.ChatCompletion.create(model=model, messages=messages)

    answer = response['choices'][0]['message']['content']  # 응답 부분

    result = {}

    if answer[0] == '`' or answer[len(answer) - 1] == '`':  # 아주 적은 빈도로, chatgpt 응답에 ```가 양쪽에 붙는 문제 해결
        answer.strip('`').strip().strip('`')

    try:  # json 변환을 통해 변환 시도후, 적절한 문법 형식이 맞춰지지 않았다면 재귀 진행
        result = json.loads(answer)
    except:
        print("re-try\n\n")
        print(response['choices'][0]['message']['content'])
        retry += 1
        return gpt(topic, n, except_list, retry)

    ### 개수 점검기

    if len(result['destinations']) > n:  # 요구 갯수보다 많이 탐색해온 경우
        for i in range(len(result['destinations']) - n):
            result['destinations'].pop()  # result에 len개만큼만 남기도록 하고 뒤로 넘김
    elif len(result['destinations']) < n:  # 요구 갯수보다 적게 탐색해온 경우
        new_except_list = except_list[:]
        for i in result["destinations"]:
            name_with_region = i['name'] + '(' + i['region'] + ')'
            new_except_list.append(name_with_region)
        new_n = n - len(result['destinations'])
        result['destinations'].extend(gpt(topic, new_n, new_except_list, 0, 1))
        # new_except_list에 현재 검색한 양만큼 추가 후, new_n 은 n-len으로 맞춘 후, gpt를 새로 호출해서 받아온 뒤, 진행중이던 곳에 추가하기.
        # 디폴트 인자로 해당케이스 속성값을 줘서, 얘에 추가하는 전용으로 영문값만 받아오는 케이스

    ### 추가용 gpt버전으로 들어왔는지 점검기

    if add == 1:  # 갯수 오류시 extend를 위한 체크 변수
        return result['destinations']
        # 번역 없이, 영어값 그대로 정리해서 리턴

    ### 영문 여행지명 리스트 생성기

    eng_name = []
    for dest in result['destinations']:  # 장소명과 지역명 결합
        eng_name.append(dest['name'] + '(' + dest['region'] + ')')

    ### 번역을 위한 데이터 처리 부분

    text = ""

    for dest in result['destinations']:  # 통으로 번역하기 위해 모든 결과값 한 문자열로 통합
        text = text + dest['name'] + ' :: ' + dest['region'] + ' :: ' + dest['description'] + '\n'

    text += result['topic_introduction'][0]  # 같은 과정

    ### deepl api(번역)

    import requests

    url = "https://deepl-translator.p.rapidapi.com/translate"

    payload = {
        "text": text,
        "source": "EN",
        "target": "KO"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RapidAPI_KEY,
        "X-RapidAPI-Host": "deepl-translator.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    try:
        translated_text = response.json()['text']  # 번역받아온 결과 변환하여 저장  ########################################### 번역도 종종 에러가 난다. 확인 필요.
    except:
        print(response)
        response = requests.post(url, json=payload, headers=headers)
        translated_text = response.json()['text']
    try:  # api 관련하여, 번역 과정에서의 혹시 모를 오류 방지를 위해 try except 사용

        ### 아래는 리턴을 위한 데이터 처리 부분

        textlist = translated_text.split('\n')  # 다시 쪼개는 과정
        name = []
        introduce = []
        PS = textlist.pop()  # PS는 마지막 줄이므로, 따로 제거
        for texts in textlist:  # 그외 내용들은 장소이름과 지역이름, 설명을 따로 분리해낸 후, 다시 적절한 형식으로 합치어 리스트로 만듬
            temp_name, temp_region, temp_introduce = texts.split("::")
            name.append(temp_name.strip().strip(":") + '(' + temp_region.strip().strip(":") + ')')
            introduce.append(temp_introduce.strip().strip(":"))

        return [eng_name, name, introduce, PS]  # 결과값들 리턴

    except:  # 해당 번역 과정에서 문제시 함수 재진입 ( 차후 번역만 재실행 하는 방식으로 변경하면 좋음)))))))))))))))))))))))))))))
        retry += 1
        print("re-try in translate\n\n")
        print(response['choices'][0]['message']['content'], '\n\n\n')
        print(translated_text)
        return gpt(topic, n, except_list, retry)


# # ! 테스팅
# topic = input()
# # ans, res = gpt(topic)
# eng_name, name, introduce, PS = gpt(topic)
# print(eng_name)
# print(name)
# print(introduce)
# print(PS)

# print("제외후 재 테스트\n")
# a, b, c, d = gpt(topic, 1, eng_name)
# print(a, b, c, d, sep="\n")
# # print(gpt(topic, 1, ans))
