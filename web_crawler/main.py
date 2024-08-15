from urllib.request import urlopen

html = urlopen('https://www.wikipedia.org')
print(html.read())