from lxml import etree
import re
import asyncio
import aiohttp
import json


class Themes(object):
    def __init__(self, title, url, author, text='', price=0, currency='грн'):
        self.title = title
        self.url = url
        self.author = author
        self.text = text
        self.price = price
        self.currency = currency

    @asyncio.coroutine
    def parsetheme(self):
        currency = ["usd", "грн", "гривен", "гривень", "uah", "eur", "євро", "евро"]
        url = self.url
        page = yield from get(url)
        root = etree.HTML(page)
        text = root.xpath('//div[@class="content"]')[0].xpath('./text()')
        text = " ".join(text)
        expr = re.compile(r'([\d,.]+)\s*([a-zA-Zа-яА-Я]+)')
        price = re.findall(expr, text)
        price = list(filter(lambda x: True if x[1] in currency else False, price))
        if len(price) == 1:
            self.price = price[0][0]
            self.currency = price[0][1]
        self.text = text

    def tojson(self):
        return json.dumps({'title': self.title, 'url': self.url, 'author': self.author,
                           'text': self.text, 'price': self.price, 'currency': self.currency})


@asyncio.coroutine
def get(url):
    response = aiohttp.request(method='GET', url=url)
    result = yield from asyncio.wait_for(response, timeout=60)
    body = yield from result.read()
    return body


@asyncio.coroutine
def parsepage(url):
    """parse everything except for announces"""
    page = yield from get(url)
    root = etree.HTML(page)
    themes = root.xpath('//li[contains(@class, "row bg")]/dl[not(contains(@class, "announce"))]')
    instances = []
    for i in themes:
        theme = i.xpath('.//dt/div/a[@class="topictitle"]')[0]
        title = theme.text
        themeurl = "http://forum.overclockers.ua/" + theme.attrib['href'][2:]
        author = i.xpath('.//dd[@class="author"]/a/text()')[0]
        instances.append(Themes(title, themeurl, author))
    return instances


@asyncio.coroutine
def parseannounces(url):
    """parse only announces"""
    page = yield from get(url)
    root = etree.HTML(page)
    themes = root.xpath('//li[contains(@class, "row bg")]/dl[contains(@class, "announce")]')
    instances = []
    for i in themes:
        theme = i.xpath('.//dt/div/a[@class="topictitle"]')[0]
        title = theme.text
        themeurl = "http://forum.overclockers.ua/" + theme.attrib['href'][2:]
        author = i.xpath('.//dd[@class="author"]/a/text()')[0]
        instances.append(Themes(title, themeurl, author))
    return instances


loop = asyncio.get_event_loop()
url = "http://forum.overclockers.ua/viewforum.php?f=26&start="

try:
    pages = int(input("How many pages to parse? "))
except:
    pages = 1

tasks = [parseannounces(url)]
for i in range(pages):
    tasks.append(parsepage(url + str(i*40)))

results = loop.run_until_complete(asyncio.wait(tasks))[0]

instances = []
for i in results:
    instances += i.result()

print("{0} results".format(len(instances)))

tasks = []
for i in instances:
    tasks.append(i.parsetheme())

results = loop.run_until_complete(asyncio.wait(tasks))

string = ''
for i in instances:
    string += i.tojson()

with open("json.txt", 'w') as file:
    file.write(string)

print("Done")
loop.close()
