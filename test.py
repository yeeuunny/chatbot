# -*- coding: utf-8 -*-
import json
import urllib.request
import csv
import operator

from collections import Counter
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response

app = Flask(__name__)

slack_token = ""
slack_client_id = ""
slack_client_secret = ""
slack_verification = ""
sc = SlackClient(slack_token)

# csv 저장(미완)
def csv_save(url):

    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    keywords = []
    book = []

    for data in soup.find_all("div", class_="basicListType communtyHide"):
        data = data.get_text()
        data = data.split('>')
        for i in data:
            keywords.append(i.strip())
    book.append(keywords[1])
    # 제목
    for data in soup.find_all("h2", class_="gd_name"):
        book.append(data.get_text())
    # 저자
    for data in soup.find_all("span", class_="gd_auth"):
        book.append(data.get_text().strip())
    # 출판사
    for data in soup.find_all("span", class_="gd_pub"):
        book.append(data.get_text().strip())

    # csv 쓰기
    f = open('output.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(book)
    f.close()

# 파일에서 데이터 읽어와서 가장 많이 읽은 장르 리턴
def genre_recommendation():
    genre = []

    with open('C:/Users/student/PycharmProjects/chatbot/output.txt', 'r') as f:
        rdr = f.readlines()
        for line in rdr:
            a = line.split(',')
            genre.append(a[0])

    # genre dict
    Counter(genre)  # dict
    genre = sorted(Counter(genre).items(), key=operator.itemgetter(1), reverse=True)  # dict
    a = list(Counter(genre).keys())
    # 추천 장르(제일 많이 읽은 장르)
    return a[0][0]

# href 위한 함수
def for_hypertext(url, text):
    text = str(text)
    return "<{0} | {1}>".format(url, text)

# 검색 시 입력 데이터 파싱
def parseText(text):
    text = text.split('> ')[1]

    if "검색" in text:
        text_list = text.split('검색')

    elif "어때" in text:
        text_list = text.split('어때')

    return text_list[0]

# 추천 도서 베스트셀러 URL 리턴
def getUrl(text):
    url = "http://www.yes24.com/24/category/bestseller"

    # URL 주소에 있는 HTML 코드를 soup에 저장합니다.
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    new_url = None
    for book in soup.find_all('div', {'id': 'bestMenu'}):
        for ul in book.find_all('ul'):
            for li in ul.find_all('li'):
                if text == li.get_text().strip():
                    new_url = "http://www.yes24.com" + li.find("a")['href']

    return new_url

# 추천 - 가장 많이 읽은 장르 데이터 받아와서 해당 장르 베스트셀러 보여줌
def recommend():
    text = genre_recommendation()
    url = getUrl(text)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    new_text = "> *" + text + " 추천 도서*"
    keywords = [new_text]
    for book in soup.find_all("td", class_="goodsTxtInfo"):
        title = "<http://www.yes24.com" + str(book.find("a")['href']) + " | " + str(
            book.find("p").find("a").get_text().strip()) + ">"
        aupu = book.find("div", class_="aupu")
        atags = aupu.find_all("a")
        price = book.find("span", class_="priceB")

        if len(atags) == 2:
            keywords.append(title.strip() + " | " + atags[0].get_text().strip()
                            + " | " + atags[1].get_text().strip() + " | " + price.get_text().strip())
        elif len(atags) == 3:
            keywords.append(title.strip() + " | " + atags[0].get_text().strip() + " 저, "
                            + atags[1].get_text().strip() + "역 | " + atags[
                                2].get_text().strip() + " | " + price.get_text().strip())

    return keywords

# 검색 - 해당 키워드 검색 내용 보여줌
def search(text):
    new_text = parseText(text)
    a = new_text

    a = str(a.encode('euc-kr')).replace('\\x', '%').replace("'", '').replace(' ', '+')
    # URL 데이터를 가져올 사이트 url 입력
    url = "http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&query=" + str(a[1:])

    # URL 주소에 있는 HTML 코드를 soup에 저장합니다.
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    new_text = "> *" + new_text + " 검색 결과*"
    keywords = [new_text]
    for book in soup.find_all("td", class_="goods_infogrp"):
        bookT = book.find("p")
        url2 = "http://www.yes24.com"+bookT.find("a")['href']
        title = bookT.find("strong")
        price = book.find("p", class_="goods_price")
        infos = book.find("div", class_="goods_info")
        if infos == None:
                continue
        atags = infos.find_all("a")
        if price != None:
                price = price.find("strong")

        if len(atags) == 2:
            keywords.append(for_hypertext(url2,title.get_text().strip()) + " | " + atags[0].get_text().strip()
                            + " | " + atags[1].get_text().strip() + " | " + price.get_text().strip())
        elif len(atags) == 3:
            keywords.append(for_hypertext(url2,title.get_text().strip()) + " | " + atags[0].get_text().strip() + " 저, "
                            + atags[1].get_text().strip() + "역 | " + atags[
                                2].get_text().strip() + " | " + price.get_text().strip())


    return keywords

# 어때 - 책 한 권에 대한 정보 보여줌
def recommend_by_user(text):
    keywords = search(text)

    keywords[0] = "> *도서*"
    keyword = [keywords[0], keywords[1]]

    url = keywords[1].split()[0].replace("<", "")
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    for book in soup.find_all("div", {'id': "contents"}):
        keyword.append("\n*책소개*\n " + str(book.find_all('p')[3].get_text().strip()) + "\n")

    n = soup.find('span', class_="more_contents OZSHOW")
    if n is not None:
        keyword.append("*작가소개*\n" + n.get_text())
    else:
        keyword.append("*작가소개*\n")

    stars = soup.find("em", class_="yes_b").get_text()
    intstars = int(float(stars))
    num = '\n*평점*\n'
    for i in range(intstars):
        num += ':full_moon:'
    if float(stars) - intstars > 0:
        num += ':last_quarter_moon:'
    keyword.append(num)

    return keyword

# 베스트셀러
def bestsellers():
    url = "http://www.yes24.com/24/category/bestseller?CategoryNumber=001&sumgb=06"
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    keywords = ["> *베스트셀러*"]
    for book in soup.find_all("td", class_="goodsTxtInfo"):
        title = "<http://www.yes24.com" + str(book.find("a")['href']) + " | " + str(
            book.find("p").find("a").get_text().strip()) + ">"
        aupu = book.find("div", class_="aupu")
        atags = aupu.find_all("a")
        price = book.find("span", class_="priceB")

        if len(atags) == 2:
            keywords.append(title.strip() + " | " + atags[0].get_text().strip()
                            + " | " + atags[1].get_text().strip() + " | " + price.get_text().strip())
        elif len(atags) == 3:
            keywords.append(title.strip() + " | " + atags[0].get_text().strip() + " 저, "
                            + atags[1].get_text().strip() + "역 | " + atags[
                                2].get_text().strip() + " | " + price.get_text().strip())

    return keywords

# 스테디셀러
def steadysellers():
    url = 'http://www.yes24.com/24/category/bestseller?CategoryNumber=001&sumgb=03'
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    keywords = ["> *스테디셀러*"]

    information = {}  # 제목:작가,출판사,출판년도

    for i in soup.find_all('td', class_="goodsTxtInfo"):
        price = i.find('span', class_="priceB").get_text()
        for j in i.find_all('div', class_="aupu"):
            artist, publisher, year = j.get_text().replace('\n', '').replace('  ', '').replace('\r', '').split('|')

            if '/' in artist:
                artist = artist.replace('/', ', ')
            name = for_hypertext("http://www.yes24.com" + i.find('a')['href'], i.find('a').get_text().strip())
            information[name] = [artist, publisher.strip(), year, price]

    for name, info in information.items():
        keywords.append(name + " | " + info[0] + " | " + info[1] + " | " + info[3])

    return keywords

# 신작 예약판매 Best
def newsellers():
    url = "http://www.yes24.com/24/Category/NewProduct"
    req = urllib.request.Request(url)

    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")

    keywords = ["> *신간 예약 판매 BEST*"]
    title, author, publisher, price = [], [], [], []

    # for i in soup.find_all("div", class_="goods_info"):
    for data in soup.find_all("p", class_="goods_name"):
        title.append(for_hypertext("http://www.yes24.com" + data.find('a')['href'], data.get_text().strip()))
        if len(title) >= 10:
            break

    for data_1 in soup.find_all("span", class_="goods_auth"):
        author.append(data_1.get_text().strip())
        if len(author) >= 10:
            break

    for data_2 in soup.find_all("span", class_="goods_pub"):
        publisher.append(data_2.get_text().strip())
        if len(publisher) >= 10:
            break

    for data_3 in soup.find_all("p", class_="goods_price"):
        price.append(data_3.get_text().strip())
        if len(price) >= 10:
            break

    for a in range(len(title)):
        keywords.append(title[a] + " | " + author[a] + " | " + publisher[a] + " | " + price[a])

    return keywords

# 명령어에 따라 분기
def _crawl_keywords(text):
    # 여기에 함수를 구현해봅시다.
    keywords = []
    
    if "검색" in text:
        keywords = search(text)

    if "베스트셀러" in text:
        keywords = bestsellers()

    if "스테디셀러" in text:
        keywords = steadysellers()

    if "신간" in text:
        keywords = newsellers()

    if "추천" in text:
        keywords = recommend()

    if "어때" in text:
        keywords = recommend_by_user(text)

    # else
    #    keywords = [ "베스트셀러, 스테디셀러, 신간 중 하나로 입력하세요" ]

    # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
    return u'\n'.join(keywords)

# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]
        keywords = _crawl_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
