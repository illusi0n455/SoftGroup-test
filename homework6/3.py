from lxml import html
import requests
import re
import asyncio


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
        root = html.fromstring(requests.get(url).text)
        text = root.xpath('//div[@class="content"]')[0].xpath('./text()')
        text = " ".join(text)
        expr = re.compile(r'(\d+)\s*([a-zA-Zа-яА-Я]+)')
        price = re.findall(expr, text)
        price = list(filter(lambda x: True if x[1] in currency else False, price))
        if len(price) == 1:  # я не знав що робити в випадках коли знайшлось декілька цін, тому вибирав лише де 1.
            self.price = price[0][0]
            self.currency = price[0][1]
        self.text = text

    def tojson(self):
        """todo"""
        pass


@asyncio.coroutine
def parsepage(url):
    """parse everything except for announces"""
    root = html.fromstring(requests.get(url).text)
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
    root = html.fromstring(requests.get(url).text)
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

# маэ бути вивід в json але покищо просто print
for i in instances:
    print(i.title, i.url, i.author, i.text, i.price, i.currency)

loop.close()