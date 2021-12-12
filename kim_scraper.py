from bs4 import BeautifulSoup
import requests
import json
from string import ascii_lowercase

movies_list = []
movies_dict = {}
articles = ('The','A','An')

# Looping through the urls
for ch in ascii_lowercase:
    url = 'https://kids-in-mind.com/'+ch+'.htm'
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    movies = soup.find_all('div', class_="et_pb_text_inner")
    temp = str(movies[2]).split('<br/>\n')
    movies_list = movies_list + temp

# Cleaning the returned data
movies_list_replaced = [w.replace('–', '-') for w in movies_list]
for item in movies_list_replaced:
    title = item.split('_blank">')[1].split('</a>')[0]
    rating = item.split('_blank">')[1].split('</a>')[1].split("- ")[1].strip()
    if '</div>' in rating:
        rating = rating.split('<')[0]
    movies_dict[title] = rating

# Some movie titles in the format (Name, article) ex: (Abyss, The).
for item in movies_dict:
    if item.endswith(articles):
        item_replace = item.split(' ')
        item_replace.insert(0,item_replace[-1])
        item_replace.pop(-1)
        item_replace = ' '.join(item_replace)[:-1]

        movies_dict[item_replace] = movies_dict.pop(item)

for key, val in movies_dict.items():
    if '<br>' in val:
        new_str = val.split('<br>')[0]
        movies_dict[key] = new_str


with open('data//kinds_in_mind_data.json', 'w') as fp:
    json.dump(movies_dict, fp)