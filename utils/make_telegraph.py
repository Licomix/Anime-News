import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from telegraph import Telegraph, TelegraphException

from config.config_manager import ConfigManager


def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    base_url = 'https://www.animenewsnetwork.com'
    translator = GoogleTranslator(source="en", target="uk")

    cites = soup.find_all('cite')
    for cite in cites:
        text = cite.get_text(separator=' ', strip=True)

        # Заменить <cite> на <p>
        cite.replace_with(text)

    tags_to_remove = ['div', 'em', 'span']
    # Удаляем все теги из списка
    for tag in tags_to_remove:
        for match in soup.find_all(tag):
            match.decompose()

    # Обновляем все ссылки <a>
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if not href.startswith(('http', 'https')):
            a_tag['href'] = base_url + href

    # Обновляем все изображения <img>
    for img_tag in soup.find_all('img'):
        if img_tag.has_attr('data-src'):
            # Обновляем data-src, если он есть
            data_src = img_tag['data-src']
            if not data_src.startswith(('http', 'https')):
                img_tag['data-src'] = base_url + data_src
            # Присваиваем data-src значение в src
            img_tag['src'] = img_tag['data-src']
        else:
            # Обновляем src
            src = img_tag.get('src', '')
            if src and not src.startswith(('http', 'https')):
                img_tag['src'] = base_url + src

    soup = translator.translate(str(soup))
    soup = BeautifulSoup(soup, 'html.parser')

    return str(soup)

def create_post(url: str):
    translator = GoogleTranslator(source="en", target="uk")
    response = requests.get(url)
    response.raise_for_status()

    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим div с классом 'meat'
    meat_div = soup.find('div', class_='meat')

    # Находим элемент h1 с id 'page_header'
    header = soup.find('h1', id='page_header')

    # Получаем содержимое div и заголовок
    meat_content = clean_html(meat_div.decode_contents())
    header_text = header.get_text(separator=': ', strip=True)
    header_text = translator.translate(header_text)

    # Инициализируем Telegraph с токеном
    telegraph = Telegraph(access_token=ConfigManager().get_config_value("TELEGRAPH_TOKEN", str))

    try:
        # Создаем страницу на Telegraph
        response = telegraph.create_page(
            title=header_text,
            html_content=meat_content,
            author_name='Anime/2/UA News'
        )
        return str(response['url'])
    except TelegraphException as e:
        print('Error creating post:', e)
        return None
