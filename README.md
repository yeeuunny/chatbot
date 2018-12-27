# Slack Chatbot 
- 2018년 12월 20일 - 2018년 12월 21일  
- Slack과 웹 크롤링을 기반으로 한 도서 검색 및 추천 챗봇

## 스펙 Specification
- 목록 조회
    - 베스트셀러
    - 스테디셀러
    - 신간 예약 판매 BEST
- 키워드 검색
    - [키워드] 검색 - 키워드에 해당하는 여러 목록 조회 
    - [키워드] 어때 - 키워드에 해당하는 한 권의 도서 조회
- 도서 추천
    - 추천해줘 - 본인 도서 목록 리스트 파일을 기반으로 유사 장르의 도서 추천

## 개발 환경
| 환경 | 내용 | 버전 |
|:-----:| :-----: | :----: |
| 언어 | Python | 3.7 |
| IDE  | PyCharm | 2018.3.2 |
| 프레임워크  | Flask | 0.12.2 | 
|라이브러리| BeautifulSoup | 4 |
|플랫폼| Slack |  |

> ### requirements
- numpy
- click==6.7
- Flask==0.12.2
- itsdangerous==0.24
- Jinja2==2.9.6
- MarkupSafe==1.0
- pyaml==16.9.0
- PyYAML ==3.12
- requests-oauthlib==0.8.0
- requests==2.18.4
- six==1.10.0
- slackclient==1.0.2
- websocket-client==0.37.0
- Werkzeug==0.12.2
- beautifulsoup4==4.6.3

## 회고 Retrospective
- 키워드 검색 시 해당 웹사이트(yes24)는 EUC-KR 한글 인코딩 기법 사용
    - 키워드를 파이썬에서 제공하는 EUC-KR 인코딩을 통해 URL의 쿼리 스트링 값으로 사용
- 도서 추천 시 도서 목록 파일을 읽어와 장르별 소트 통해 가장 많이 읽은 장르의 URL을 크롤링하고 이후 데이터 크롤링
    - 장르를 dictionary 타입으로 저장하여 파이썬의 sorted 사용

## 결과 화면
> ### 베스트셀러
![image](https://user-images.githubusercontent.com/30440457/50330661-678ec880-053f-11e9-9a2e-879c2bdf7ce2.png)
> ### 검색
![image](https://user-images.githubusercontent.com/30440457/50329265-c7827080-0539-11e9-8cc7-c05b316aed77.png)
> ### 어때
![image](https://user-images.githubusercontent.com/30440457/50330127-74122180-053d-11e9-8f15-a57837cc90f0.png)
> ### 추천
![image](https://user-images.githubusercontent.com/30440457/50329190-65c20680-0539-11e9-841f-0aae5de9c998.png)

## 보완 계획 Feedback
- 도서 목록 추가: 본인 도서 목록 리스트를 csv파일로 만들고 새로운 도서를 추가해주는 기능
- 도서 추천 기능: 본인 도서 목록과 다른 사람들의 도서 목록들을 바탕으로 유사한 하나의 도서를 추천해주는 기능
