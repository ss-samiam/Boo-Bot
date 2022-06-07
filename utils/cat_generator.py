import requests
from bs4 import BeautifulSoup
import re
import random


def adopt_cat():
    """Returns the link to a random cat image from the provided URL"""

    # Initialises BeautifulSoup
    url = "https://www.randomkittengenerator.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    # Parses webpage to get source image
    for i in soup.find_all('div'):
        for j in i.find_all('img', src=re.compile('https://www.randomkittengenerator.com/cats')):
            return j.get('src')


def adopt_anime_cat():
    """Returns the link to a random anime cat image from the provided URL"""

    # Initialises BeautifulSoup
    url = "https://safebooru.donmai.us/posts?tags=order%3Arandom+cat_ears"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    # Adds all images in the current webpage to list
    images = []
    for i in soup.find_all('a', href=re.compile('/posts/')):
        images.append(i.get('href'))

    # Parses the chosen image webpage to get source image
    chosen_post = random.choice(images)
    chosen_url = "https://safebooru.donmai.us" + chosen_post
    page = requests.get(chosen_url)
    soup = BeautifulSoup(page.content, 'lxml')
    for i in soup.find_all('source'):
        return i.get('srcset').split()[0]

