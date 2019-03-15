#! python3
# downloadXkcd.py - downlaod comics form the http://xkcd.com/#
import requests
import os
import bs4

url = 'http://xkcd.com'
os.makedirs('xkcdImgs', exist_ok=True)
while not url.endswith('#'):

    #  Download the page.
    print('Downlaoding web page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text)

    #  Find the URL of the comic image.

    comicElement = soup.select('#comic img')
    if comicElement == []:
        print('Could not find the image! :( ')

    else:
        comicURL = 'http:' + comicElement[0].get('src')
        # Download the image.
        print('Downloading image %s...' % (comicURL))
        res = requests.get(comicURL)
        res.raise_for_status()
        #  Save the image to ./xkcd.
        imageFile = open(os.path.join(
            'xkcdImgs', os.path.basename(comicURL)), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    #  Get the Prev button's url.
    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')


print('Done.')
