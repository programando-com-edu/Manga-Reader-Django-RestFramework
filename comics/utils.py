import requests
from django.db import transaction
from tqdm import tqdm
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from .models import Comic, TypeCatalog, Chapter


class AsuraCatalog:

    def __init__(self):
        self.name = 'Asura'
        self.url = 'https://asuratoon.com/manga/list-mode/'
        self.content = []

        self._get_content()

    def _get_content(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')

            try:
                mrgn_div = soup.find('div', class_='mrgn')
                soralist_div = mrgn_div.find('div', class_='soralist')
                blix_divs = soralist_div.find_all('div', class_='blix')

                for div in tqdm(blix_divs):
                    div_content = div.find_all('a', class_='series')

                    for content in tqdm(div_content):
                        title = content.get_text(strip=True)
                        url = content.get('href', '')
                        AsuraContent(title, url)

            except AttributeError as e:
                print('Erro ao encontrar elementos: ', e)

        else:
            print('Erro ao acessar a URL. Código de status: ', response.status_code)


class AsuraContent:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.chapters = {}

        self._get_content_chapters()

    def _get_content_chapters(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')

            try:
                banner_img = soup.find('img', class_='wp-post-image').get('src', '')
                comic_description = soup.find('div', class_='entry-content').find('p').get_text()
                comic_data = {
                    'title': self.title,
                    'description': comic_description,
                    'banner': banner_img,
                    'link': self.url,
                    'catalog': 1
                }

                eplister_div = soup.find('div', class_='eplister', id='chapterlist')
                clstyle_ul = eplister_div.find('ul', class_='clstyle')
                li_items = clstyle_ul.find_all('li')

                with transaction.atomic():
                    comic, created = Comic.objects.get_or_create(**comic_data)
                    chapter_list = []
                    for item in li_items:
                        number = item.get('data-num', -1)
                        url = item.find('a').get('href', '')

                        if number == -1:
                            raise ValueError('Invalid chapter number on: ', self.title)

                        chapter_data = {
                            'number': number,
                            'link': url,
                            'comic': comic
                        }
                        chapter_list.append(Chapter(**chapter_data))
                    Chapter.objects.bulk_create(chapter_list)
                    print(comic.title + 'criado com sucesso')

            except AttributeError as e:
                print('Erro ao encontrar elementos: ', e)

            except Exception as e:
                print(e)

        else:
            print('Erro ao acessar a URL. Código de status: ', response.status_code)