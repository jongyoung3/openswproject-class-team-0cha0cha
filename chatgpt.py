from apikey import OPENAI_API_KEY, RapidAPI_KEY  # 보안을 위해, 따로 저장한 apikey
import json


def gpt(topic, n=10, except_list=[], retry=0, add=0):
    # topic = 토픽, n = 탐색 개수, except_list = 중복 검색 방지를 위해, 제외하고 검색할 장소 목록,
    # retry = 재귀 횟수, add = gpt함수 내 갯수 부족 등으로 result extend 필요시 활용위한 표시 변수
    if retry >= 3:
        return [-99]  # 다차례 오류 발생시 공백리스트 리턴
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
        "Tokyo is known for its unique shopping culture, offering everything from luxury brands to quirky accessories and traditional crafts. Don't miss out on the chance to discover the latest trends and bring home one-of-a-kind souvenirs from this vibrant city."
        ]
    }
    """

    prev3 = """
    {
        "destinations": [
        {
            "name": "Eiffel Tower",
            "location": "Paris, France",
            "description": "The Eiffel Tower is an iconic landmark in Paris, France. Standing at 330 meters tall, it offers breathtaking views of the city and is a must-visit attraction for tourists from around the world."
        },
        {
            "name": "Machu Picchu",
            "location": "Cusco Region, Peru",
            "description": "Machu Picchu is an ancient Incan citadel located in the Cusco Region of Peru. Surrounded by majestic mountains, it is known for its remarkable architecture and mystical atmosphere, attracting countless visitors each year."
        },
        {
            "name": "Great Wall of China",
            "location": "Beijing, China",
            "description": "The Great Wall of China is an awe-inspiring fortification that stretches across the northern part of China. With a history spanning over 2,000 years, it is a UNESCO World Heritage site and a testament to human engineering and ingenuity."
        },
        {
            "name": "Santorini",
            "location": "Cyclades, Greece",
            "description": "Santorini is a breathtaking island in the Cyclades archipelago of Greece. Famous for its stunning sunsets, whitewashed buildings, and blue-domed churches, it offers a romantic and picturesque setting that attracts travelers from all over."
        },
        {
            "name": "Taj Mahal",
            "location": "Agra, India",
            "description": "The Taj Mahal is a magnificent mausoleum located in Agra, India. Built by Emperor Shah Jahan in memory of his beloved wife, it is regarded as one of the new Seven Wonders of the World and showcases exquisite Mughal architecture."
        },
        {
            "name": "Grand Canyon",
            "location": "Arizona, USA",
            "description": "The Grand Canyon is a vast and awe-inspiring natural wonder situated in Arizona, USA. Carved by the Colorado River, its colorful rock formations and steep cliffs offer breathtaking vistas that leave visitors in awe of its grandeur."
        },
        {
            "name": "Petra",
            "location": "Ma'an Governorate, Jordan",
            "description": "Petra is an ancient city nestled in the Ma'an Governorate of Jordan. Famous for its intricate rock-cut architecture and the iconic Treasury, it is a UNESCO World Heritage site and a symbol of Jordan's rich history and heritage."
        },
        {
            "name": "Machu Picchu",
            "location": "Cusco Region, Peru",
            "description": "Machu Picchu is an ancient Incan citadel located in the Cusco Region of Peru. Surrounded by majestic mountains, it is known for its remarkable architecture and mystical atmosphere, attracting countless visitors each year."
        },
        {
            "name": "Colosseum",
            "location": "Rome, Italy",
            "description": "The Colosseum is a magnificent amphitheater situated in the heart of Rome, Italy. Dating back to the Roman Empire, it is a testament to ancient engineering and hosts millions of tourists who come to admire its grandeur and historical significance."
        },
        {
         "name": "Pyramids of Giza",
        "location": "Giza Governorate, Egypt",
        "description": "The Pyramids of Giza are ancient pyramid structures located in the Giza Governorate of Egypt. Constructed as tombs for pharaohs, they are an incredible testament to the Egyptian civilization's architectural prowess and continue to fascinate visitors."
        }
    ],
    "topic_introduction": [
        "Travel destinations offer incredible experiences and insights into different cultures and historical wonders. Whether you seek natural beauty, architectural marvels, or cultural landmarks, these destinations will captivate your senses and create unforgettable memories."
        ]
    }
"""

    # 로케이션 제공 요청.


    systemsay2 = """
    You are in the middle of a preliminary study to answer the following questions:
    Find me Exactly 10 of travel destinations related to the topic.
    In the following user query, topic will be provided wrapped in triple backticks.
    Topic can be provided in a variety of languages. But Internally, you should using this topic by translating to English for query.
    Provide the results in the following order :
    Step 0. Imagine yourself as an expert travel guide AI speaking English. Do not say any other languages.
    Step 1. Follow the following conditions wrapped in angle brackets and find 10 of travel destinations related to topic in English :
    < You must only write places that can be cited and verified on Google Maps.
    You should include places that are heavily visited and has high ratings by tourists. >
    Step 2. Follow the following conditions wrapped in angle brackets and find location where the travel destinations belongs to.
    < If the location is multiple, write the only one location that is most representative.
     location data should be based on Google Maps data. 
     Be specific the location so it can be searched on Google maps easily. 
     Similarize the way locations are written for each destination. > 
    Step 3. write 3 sentences of introductions to each destination.
    Step 4. lastly, write 2 sentences introductions to topic.
    Step 5. provide the output that is 10 of travel destinations related to topic in English and only json format. The output must satisfy the conditions. 
    Your output should be in json format with two list and have the following fields in first list :
     'name', 'location', 'description'. first list key is "destinations".
    In second list, You should write only introduction about topic. Second list key is "topic_introduction".
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
    You should include places that are heavily visited and has high ratings by tourists. >
    Step 2. Follow the following conditions wrapped in angle brackets and find region where the travel destinations belongs to.
    < If the region is multiple, write the only one region that is most representative.
     Region data should be based on Google Maps data. 
     Be specific the region so it can be searched on Google maps easily. 
     Similarize the way locations are written for each destination. > 
    Step 3. write 3 sentences of introductions to each destination.
    Step 4. lastly, write 2 sentences introductions to topic.
    Step 5. provide the output that is 10 of travel destinations related to topic in English and only json format. The output must satisfy the conditions.
    Your output should be in json format with two list and have the following fields in first list :
     'name', 'region', 'description'. first list key is "destinations".
    In second list, You should write only introduction about topic. Second list key is "topic_introduction".
    """
    # 95,96번줄 추가
    # 일부 무의미한 문장 제거

    # 아래 오류목록 참고해서, 확인 후 고쳐보고.

    # 하시마 섬 등 드라이빙으로 경로를 알아낼 수 없는 경우. ############# 해결불가. 가능한 한 그렇게 추천하지만, 말을 못 알아 들음.

    # 2. 먼거리 추천 에러 step1 요구사항 3,4,5번 라인  ###


    prev_query = f"""
    in next answer, You must find Exactly {n} of travel destinations related to topic in English. 
    So, your output has {n} of travel destinations related to topic.
    The rest of the instructions are the same as preliminary study.
    """

    query = f"```{topic} ```in English"

    messages = [
        # {"role": "system", "content": systemsay},
        {"role": "system", "content": systemsay2},
    #    {"role": "user", "content": train_topic},
    #    {"role": "assistant", "content": prev2},
        {"role": "assistant", "content": prev3},
        {"role": "user", "content" : prev_query},
        {"role": "user", "content": query}
    ]

    # 중복제거가 필요할 시, 추가 학습 진행
    if except_list != []:
        except_destination = ", ".join(except_list) # systemsay3가 위의 prev_query 성격도 가짐
        systemsay3 = f"""
        in next answer, You must find Exactly {n} of travel destinations related to topic in English, And You should follow the following conditions wrapped in angle brackets too.
        < First, You must exclude the destinations wrapped in following double backticks. So, you must find the destinations that is not provided in following double backticks.
        ``{except_destination}``. this is Top priority requirement.
        Second, You don't need to write 2 sentences introductions to topic. Instead, Just write '0'. > 
        The rest of the instructions are the same as preliminary study.
        """
        messages = [
            # {"role": "system", "content": systemsay},
            {"role": "system", "content": systemsay2},
            # {"role": "user", "content": train_topic},
            # {"role": "assistant", "content": prev2},
            {"role": "assistant", "content": prev3},
            {"role": "user", "content": systemsay3},
            {"role": "user", "content": query}
        ]

    try:
        response = openai.ChatCompletion.create(model=model, messages=messages)
    except:
        print("re-try\n\n")
        print("Error in chat")
        retry += 1
        return gpt(topic, n, except_list, retry)

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

    try:
        if len(result['destinations']) > n:  # 요구 갯수보다 많이 탐색해온 경우
            for i in range(len(result['destinations']) - n):
                result['destinations'].pop()  # result에 len개만큼만 남기도록 하고 뒤로 넘김
        elif len(result['destinations']) < n:  # 요구 갯수보다 적게 탐색해온 경우
            new_except_list = except_list[:]
            for i in result["destinations"]:
                name_with_region = i['name'] + '(' + i['location'] + ')'
                new_except_list.append(name_with_region)
            new_n = n - len(result['destinations'])
            result['destinations'].extend(gpt(topic, new_n, new_except_list, 0, 1))
        # new_except_list에 현재 검색한 양만큼 추가 후, new_n 은 n-len으로 맞춘 후, gpt를 새로 호출해서 받아온 뒤, 진행중이던 곳에 추가하기.
        # 디폴트 인자로 해당케이스 속성값을 줘서, 얘에 추가하는 전용으로 영문값만 받아오는 케이스
    except:
        print("error in 개수 점검기\n\n")
        print(answer)
        retry += 1
        return gpt(topic, n, except_list, retry)
    ### 추가용 gpt버전으로 들어왔는지 점검기

    if add == 1:  # 갯수 오류시 extend를 위한 체크 변수
        return result['destinations']
        # 번역 없이, 영어값 그대로 정리해서 리턴

    ### 영문 여행지명 리스트 생성기

    eng_name = []
    for dest in result['destinations']:  # 장소명과 지역명 결합
        eng_name.append(dest['name'] + '(' + dest['location'] + ')')

    ### 번역을 위한 데이터 처리 부분

    text = ""

    for dest in result['destinations']:  # 통으로 번역하기 위해 모든 결과값 한 문자열로 통합
        text = text + dest['name'] + ' :: ' + dest['location'] + ' :: ' + dest['description'] + '\n'

    if except_list == []:
        text += result['topic_introduction'][0]  # 같은 과정
    else:
        text += "0"

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

    try:
        response = requests.post(url, json=payload, headers=headers)
    except:
        print('error in translate requests')
        try:
            response = requests.post(url, json=payload, headers=headers)
        except:
            print("error in translate request 2, retry")
            retry += 1
            return gpt(topic, n, except_list, retry)

    try:
        translated_text = response.json()['text']  # 번역받아온 결과 변환하여 저장  ########################################### 번역도 종종 에러가 난다. 확인 필요.
    except:
        print(response)
        print('error after translated to json')
        try:
            response = requests.post(url, json=payload, headers=headers)
            translated_text = response.json()['text']
        except:
            print('error after translated to json 2, retry')
            retry += 1
            return gpt(topic, n, except_list, retry)
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
        # print(response['choices'][0]['message']['content'], '\n\n\n')
        print('answer :: \n', answer, sep='')
        print('translated_text :: \n', translated_text, sep='')
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
