import bs4
import requests

res = requests.get('http://sadatjubayer.com/')

res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'html.parser')

elements = soup.select(
    '#resume > div > div.row > div > div > div.timeline-category.edu-cagegory > a')

print(elements[0].text)
