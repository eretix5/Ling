# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pymongo

# URL сайта
base_url = 'https://vpravda.ru'

# 1 страница содержит 40 статей
page_limit = 250

# заголовки для запроса
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.77 Safari/537.36'}

# подключение к базе данных
key = 'mongodb+srv://eretix5:guy123@cluster0.ltm2k.mongodb.net/test'
client = pymongo.MongoClient(key)
collection = client.news_bd.news_collection


def main():
    for page in range(page_limit):
        response = requests.get(f'{base_url}/articles/?page={page}', headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', {'id': 'content'})
        div_list = content.find_all('div', {'class': 'views-row'})

        news_list = []
        for news in div_list:
            url = base_url + news.find('div', {'class': 'field-content'}).a['href']
            response = requests.get(url, headers=header)
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find('div', {'id': 'content'})

            # тип
            try:
                news_type = content.find('nav', {'class': 'breadcrumb'}).find_all('li')[1].text
            except Exception:
                news_type = None

            # название статьи
            try:
                title = content.find('h1', {'id': 'page-title'}).text
            except Exception:
                title = None

            # дата и время
            try:
                date = content.find('span', {'class': 'date-display-single'}).text
            except Exception:
                date = None

            # текст статьи
            try:
                text = content.find('div', {'class': 'field-name-body'}).text
                text = text.translate({ord(c): ' ' for c in '\n'}).translate({ord(c): '' for c in '\xa0'})
            except Exception:
                text = None

            # ссылка на картинку
            try:
                img = content.find('img', {'typeof': 'foaf:Image'})['src']
            except Exception:
                img = None

            news_list.append({
                'url': url,
                'img': img,
                'type': news_type,
                'title': title,
                'date': date,
                'text': text,
            })

        collection.insert_many(news_list)
        print(f'Done: {page}/{page_limit} pages')


if __name__ == '__main__':
    main()
