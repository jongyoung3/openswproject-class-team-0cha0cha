from apikey import OPENAI_API_KEY, RapidAPI_KEY # 보안을 위해, 따로 저장한 apikey


# 번역 이전의 검색및 활용 데이터리스트 1개, 번역이 완료된 출력용 데이터리스트 2개를 만들 예정.
# 데이터리스트 1개는 여행지 제목만을 제공할 것
# 나머지 데이터리스트 1개는 여행지 정보를 제공할 것
#
# 검색용 데이터리스트는 여행지 제목 영어 원문 데이터를 가질 예정.
#

## 검색할 데이터는 받아온다고 가정 ! 테스팅
topic = "도쿄 역사 여행"
def gpt(topic):
	#### chatgpt api
	import openai


	openai.api_key = OPENAI_API_KEY

	model = "gpt-3.5-turbo"

	n = 10 # 여행지 수 표현
	query = f"'{topic}' is topic. Follow the prompts to respond."




	prev = """Akihabara::Akihabara, also known as "Electric Town," is a mecca for anime and manga enthusiasts. This bustling neighborhood is filled with shops, arcades, and maid cafes, offering a wide range of anime merchandise and experiences.
	
	Studio Ghibli Museum::Visit the Studio Ghibli Museum in Mitaka to immerse yourself in the enchanting world of Hayao Miyazaki's iconic animated films. Explore the exhibits, watch exclusive short films, and marvel at the beautiful artwork and craftsmanship.
	
	Nakano Broadway::Nakano Broadway is a multi-story complex in Tokyo that houses numerous anime and manga shops. Here, you can find rare collectibles, vintage merchandise, and a vast selection of manga from various genres.
	
	Ikebukuro::Ikebukuro is another anime hotspot, featuring large-scale stores dedicated to anime, manga, and character goods. It's home to the famous Sunshine City complex, which includes an anime-themed shopping mall, an observation deck, and even an indoor theme park.
	
	Odaiba::Odaiba is not only known for its futuristic architecture and stunning views of Tokyo Bay but also for its anime-related attractions. You can visit the Gundam Base Tokyo, where you'll find a life-sized Gundam statue, or explore the Tokyo Joypolis amusement park, which features anime-themed rides and games.
	
	Pokemon Center Mega Tokyo::Pokemon fans shouldn't miss the Pokemon Center Mega Tokyo in Ikebukuro. This store offers an extensive range of Pokemon merchandise, including plush toys, trading cards, apparel, and exclusive items that you won't find elsewhere.
	
	Tokyo Character Street::Located in the basement of Tokyo Station, Tokyo Character Street is a shopping arcade lined with shops dedicated to popular anime, manga, and game characters. From Hello Kitty to Dragon Ball, you'll find a wide variety of character goods here.
	
	Mandarake Complex::The Mandarake Complex in Nakano is a treasure trove for anime and manga enthusiasts. This multi-story building houses numerous Mandarake stores, each specializing in different aspects of otaku culture, such as vintage toys, cosplay, and rare collectibles.
	
	Comiket::If you're lucky enough to visit Tokyo during the Comic Market (Comiket), it's a must-visit event for anime and manga fans. Held twice a year, Comiket is the largest self-published comic book fair in Japan, featuring thousands of doujinshi (fan-made comics) and cosplay.
	
	Shinjuku::Shinjuku is a vibrant district that offers a mix of modern entertainment and anime-related attractions. Explore the various department stores like Takashimaya and Kinokuniya, which have dedicated anime and manga sections, or visit the Animate store for a wide selection of anime merchandise.
	
	Embark on a Tokyo Anime Trip and immerse yourself in the colorful world of Japanese animation. From bustling neighborhoods like Akihabara and Ikebukuro to dedicated stores, museums, and events, Tokyo offers a paradise for anime enthusiasts. Get ready to indulge in your favorite characters, collectibles, and experiences while exploring the dynamic cityscape."""

	prev2 = """Gyeongbokgung Palace::Gyeongbokgung Palace, located in Seoul, is a majestic symbol of the Joseon Dynasty. Explore its grand architecture, intricate details, and beautiful gardens as you step back in time and learn about Korean history.
	
	Changdeokgung Palace::Changdeokgung Palace is a UNESCO World Heritage site known for its harmonious blend of architecture and natural surroundings. Discover the secret garden, stroll through the palace halls, and delve into the historical significance of this royal residence.
	
	Bulguksa Temple::Located in Gyeongju, Bulguksa Temple is one of Korea's most significant Buddhist temples. Marvel at its stunning design, including the intricate stone carvings and serene atmosphere, while appreciating its historical and cultural importance.
	
	Hwaseong Fortress::Hwaseong Fortress in Suwon is a well-preserved fortress from the Joseon Dynasty. Walk along its walls, visit the gates, and explore the various pavilions, offering insights into Korea's military architecture and defense strategies.
	
	National Museum of Korea::The National Museum of Korea in Seoul is a treasure trove of artifacts showcasing Korea's rich history. Discover ancient relics, royal treasures, and archaeological findings that span thousands of years, providing a comprehensive overview of Korean heritage.
	
	Seokguram Grotto::Located on Mount Toham, the Seokguram Grotto houses a remarkable granite Buddha statue. Appreciate the artistry and religious significance of this masterpiece, which is considered one of Korea's most important Buddhist sites.
	
	Gyeongju Historic Areas::Gyeongju, known as the "museum without walls," is a city filled with historic sites and cultural heritage. Explore the ancient tombs, temple ruins, and UNESCO-listed sites, immersing yourself in the glory of Korea's ancient capital.
	
	Jeonju Hanok Village::Jeonju Hanok Village offers a glimpse into traditional Korean architecture and culture. Wander through its narrow alleyways lined with traditional hanok houses, visit museums and craft workshops, and indulge in the city's famous bibimbap cuisine.
	
	Andong Hahoe Folk Village::Step into the past at the Andong Hahoe Folk Village, a well-preserved village that showcases traditional Korean rural life. Admire the thatched-roof houses, participate in cultural activities, and witness traditional performances like mask dances.
	
	War Memorial of Korea::The War Memorial of Korea in Seoul commemorates the history and sacrifices of the Korean War and other significant conflicts. Explore its exhibits, including military equipment, photographs, and multimedia presentations, to gain a deeper understanding of Korea's tumultuous past.
	
	Embark on a Korean history tour and uncover the rich cultural heritage of this fascinating country. From magnificent palaces and temples to historic fortresses and museums, each destination offers a unique glimpse into Korea's past. Immerse yourself in the stories, traditions, and architectural marvels that have shaped Korea's history over centuries."""

	# 현재 가장 큰 이슈는 종종 앞에 숫자를 붙여주거나, 위에 쓸데없는 잡설을 다는 경우. 해당 이슈가 가장 많이 등장함.
	# 마지막에 한줄소개를 까먹는 예
	# 오사카 맛집여행을 찾아달라니까 뜬금없이 관련없는 일본 여행지를 추천해주는 예
	# 뜬금없이 한줄만 답변해주는 예도 일어남.
	# 이런식. Jeju Island Volcanic Landscape Tour//Embark on a journey to Jeju Island, known for its unique volcanic terrain shaped by millions of years of volcanic activity. Explore the stunning natural wonders formed by the volcanic landscape, from majestic mountains to fascinating caves, craters, and beaches. Discover the geological history of the island and get ready for an adventure of a lifetime on this one-of-a-kind volcanic landscape tour.
	# '제주도 화산 지형 여행'으로 하자 저렇게 나옴
	# '프랑스 문화 여행' 에도 위와 같이 응답

	# '제주도 화산지형 여행'으로 검색하자 7가지만 추천해줌. 번호도 붙었고. 개수가 부족했나..?
	# 종종 10가지 안쓰고 덜 쓰는 경우가 일어나네?

	# 예외가 자주 잃어나지만 않는다면, try except로 잡아버린는것도 괜찮음.

	# 질문을 조금 바꾸자, 주제에 대해서 갑자기 소개를 쏼라쏼라 하기도 함.
	# 한번 더 바꾸니, 정상 작동.
	# 하는듯 싶었지만, 8개만 추천해주고 비정상 작동.

	# 제주도, 도쿄 등 검색시 그 자체에 대해서 여행지로 소개해주는 문제.

	# 오류 빈도가 적은데, try except들로 걸러주는거 괜찮을듯? 몇번 재실행 하도록 하고, 안된다면, 특정 카운트수가 넘어간다면 탈출하도록.

	# 다른 오류는 많이 줄었지만, 개수가 부족한 경우가 종종 일어난다.
	# 1. 개수 부족(주제에 대해서만 소개하거나, 부족하게 소개)
	# 2. 위에 잡설 출력 3. 앞에 숫자 붙임 4. 거리가 먼 부적절한 여행지 추천 5. 순서 부적절

	messages = [
	        {"role": "system", "content": "You are currently being pre-trained to answer the following query. Imagine you are an expert tour guide AI that provides correct answers in a structured grammatical format. You must need to list 10 travel destinations for questioner to use this informations for travel based on the topic being asked. Write a three-line introduction to your destination, tailored to the question. At last line, Write a 1-line story to introduce your topic. Your responses should be based on the question and focus on destinations that many people like. You should answer with a list of destinations that are close to each other so that the traveler can travel in a shorter period of time. To put it another way, you must never involve in list about distant from each other destinations.  the most important thing is all destinations are close each others. <<for example, The Henry Ford Museum of American Innovation is not close to Route 66. There is a significant distance between the two locations, with Route 66 primarily traversing the western states while The Henry Ford Museum is situated in the Midwest. So, you must never involve these destinations that is far from each other in your destinations list>> the order in which the destinations are displayed should allow the traveler to visit them all in the shortest amount of time without having to retrace their steps. Every element in the entire list (travel destinations) must fully satisfy the conditions for every other element. ----- Also, Your response grammatical format should be absolutely consistent. The response grammatical format is as follows: 1. Write the name of the destination and a description of the destination, nothing else. 2. Write the name of the destination immediately, followed by a '::' to separate it from the description. Immediately follow this with a description of the destination, i.e., 'Destination Name::Description of Destination', line by line. Do not write anything other than a Destination name, Description of Destination and lastly 1-line story to introduce topic . Use the format of your previous response as a writing guide for current your answer. In the previous answer, you answered the question 'Tokyo Anime Trip' and 'Korean history tour'. You should write current answer to Match the grammatical format of your previous answers without any grammatical diffrences. Do you understand? You will now be given a topic. using pre-trained things, please answer about topic."},
	        {"role": "assistant", "content": prev},
	        {"role": "assistant", "content": prev2},
	        {"role": "user", "content": query}
	]

	response = openai.ChatCompletion.create(model = model, messages=messages)

	answer = response['choices'][0]['message']['content'] # 응답 부분
	# print(answer) # !!응답 테스트

	### 영문 여행지명 리스트 생성기

	textlist = answer.split('\n\n')
	n = 10
	eng_name = []
	for i in range(0,n):
		temp_name, temp_introduce = textlist[i].split("::")
		eng_name.append(temp_name.strip())

	# print(eng_name) # !테스트 부분




	### deepl api
	import requests

	url = "https://deepl-translator.p.rapidapi.com/translate"

	payload = {
		"text": answer,
	        "source": "EN",
		"target": "KO"
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": RapidAPI_KEY,
		"X-RapidAPI-Host": "deepl-translator.p.rapidapi.com"
	}

	response = requests.post(url, json=payload, headers=headers)

	# print(response.json()['text']) # 번역 완료 내용 테스트

	textdata = response.json()['text']


	#### 아래는 데이터 처리 부분

	textlist = textdata.split('\n\n')
	# print(textlist) # !!!테스트
	# print(textdata) # !!!테스트
	name = []
	introduce = []
	PS = textlist[n]
	for i in range(0,n):
		temp_name, temp_introduce = textlist[i].split("::")
		name.append(temp_name.strip())
		introduce.append(temp_introduce.strip())

	return [eng_name, name, introduce, PS]

# ! 테스팅
gpt(topic)
a,b,c,d = gpt(topic)
print(a,b,c,d,sep="\n")

