import requests
from bs4 import BeautifulSoup

def get_latest_news():
    # URL страницы с новостями
    url = 'https://www.animenewsnetwork.com/news/'

    # Отправляем запрос к странице
    response = requests.get(url)
    response.raise_for_status()

    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим первый div с классом 'herald box news t-news'
    news_divs = soup.find_all('div', class_='herald box news t-news')

    keywords = {'anime', 'manga', 'anime-manga'}

    for news_div in news_divs:
        # Проверяем наличие атрибута 'data-topics'
        data_topics = news_div.get('data-topics', '')

        # Проверяем, что 'data-topics' не содержит 'local' и содержит хотя бы одно ключевое слово
        if 'local' not in data_topics and any(keyword in data_topics for keyword in keywords):
            # Внутри него находим div с классом 'wrap'
            wrap_div = news_div.find('div', class_='wrap')

            if wrap_div:
                # Внутри 'wrap' находим ссылку (тег 'a')
                news_link = wrap_div.find('a', href=True)

                if news_link:
                    # Получаем URL новости
                    news_url = 'https://www.animenewsnetwork.com' + news_link['href']
                    return news_url
                    break
