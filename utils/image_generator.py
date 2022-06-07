import requests
from bs4 import BeautifulSoup
import re
import random
from typing import *


class Zerochan:
    """Image parser for https://www.zerochan.net/"""

    def get_image(self, keyword: str) -> List[str]:
        base_url = "https://www.zerochan.net/"

        # Sets up URL based on what the user specified
        character = "+".join(keyword.lower().split())
        url = base_url + character
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')

        images = []
        for i in soup.find_all('a', href=re.compile('https://static')):
            images.append(i.get('href'))
        return images

    # Functionality identical to the one above except this gets the lower
    # resolution version of the image
    def get_low_image(self, keyword: str) -> List[str]:
        base_url = "https://www.zerochan.net/"

        # Sets up URL based on what the user specified
        character = "+".join(keyword.lower().split())
        url = base_url + character
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')

        images = []
        for i in soup.find_all('a'):
            for j in i.find_all('img', src=re.compile('https://s3')):
                images.append(j.get('src'))
        return images


class Wallhaven:
    """Image parser for https://wallhaven.cc"""

    def get_image(self, keyword: str) -> List[str]:
        # Sets up URL based on what the user specified
        character = "+".join(keyword.lower().split())
        url = f"https://wallhaven.cc/search?q={keyword}&categories=110&purity=100&sorting=random&order=desc"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')

        # Extracts all images in the current webpage
        images = []
        for i in soup.find_all('a', href=re.compile('https://wallhaven.cc/w')):
            images.append(i.get('href'))

        # Chooses a random image from all images in the current webpage
        chosen_url = random.choice(images)
        page = requests.get(chosen_url)
        soupSequel = BeautifulSoup(page.content, 'lxml')

        for i in soupSequel.find_all('div'):
            for j in i.find_all('img',
                                src=re.compile('https://w.wallhaven.cc/full')):
                return j.get('src')

