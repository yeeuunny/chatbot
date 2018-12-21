# Slack Chatbot 
- 2018년 12월 20일 - 2018년 12월 21일  
- Slack과 웹 크롤링을 기반으로 한 도서 검색 및 추천 챗봇

## 기능
- 목록 조회
    - 베스트셀러
    - 스테디셀러
    - 신간 예약 판매 BEST
- 키워드 검색
    - [키워드] 검색 - 키워드에 해당하는 여러 목록 조회 
    - [키워드] 어때 - 키워드에 해당하는 한 권의 도서 조회
- 도서 추천
    - 추천해줘 - 본인 도서 목록 리스트를 기반으로 유사 장르의 도서 추천

## 개발 환경
| 환경 | 내용 | 버전 |
|:-----| :----- | : ---- |
| 언어 | Python | 3.7 |
| IDE  | PyCharm | 2018.3.2 |
|라이브러리| BeautifulSoup | 4 |

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

## 결과 화면
> ### 베스트셀러
![image](https://user-images.githubusercontent.com/30440457/50329219-8ab67980-0539-11e9-8eb1-f09999f0e84a.png)
> ### 검색
![image](https://user-images.githubusercontent.com/30440457/50329265-c7827080-0539-11e9-8cc7-c05b316aed77.png)
> ### 어때
![image](https://user-images.githubusercontent.com/30440457/50329163-4c20bf00-0539-11e9-97a3-0a92e9e7e61d.png)
> ### 추천
![image](https://user-images.githubusercontent.com/30440457/50329190-65c20680-0539-11e9-841f-0aae5de9c998.png)
