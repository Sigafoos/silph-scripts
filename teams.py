import sys
from bs4 import BeautifulSoup
from PIL import Image

IMG_SIZE = 96

if len(sys.argv) != 2:
    print('usage: teams.py html_file')
    sys.exit(1)

with open(sys.argv[1]) as fp:
    soup = BeautifulSoup(fp, features='html.parser')

files = sys.argv[1].replace('.html', '_files/')

for player in soup.select('.playerList tr'):
    rawusername = player.find(class_='competitorUsername')
    if not rawusername:
        continue
    username = rawusername.get_text().strip()
    print(f'== {username} ==')
    team = Image.new('RGBA', (IMG_SIZE*6, IMG_SIZE))
    i = 0
    for pokemon in player.find_all(class_='pokemonEntry'):
        name = pokemon.find('p', class_=False).get_text()
        cp = pokemon.find('p', class_='cp').get_text()
        img = Image.open(files + pokemon.find('img')['src'].split('/')[-1])
        team.paste(img, (i*IMG_SIZE, 0))

        print(f'{name} ({cp} CP) {img.mode}')
        i += 1
    print()
    with open(f'{files}team_{username}.png', 'wb') as fp:
        team.save(fp)
