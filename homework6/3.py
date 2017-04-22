from lxml import etree
import re
import asyncio
import aiohttp
import psycopg2
import time


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
        text = root.xpath('//div[@class="content"]')[0].xpath('./descendant-or-self::text()')
        text = " ".join(text)
        expr = re.compile(r'([\d,.]+)\s*([a-zA-Zа-яА-Я]+)')
        prices = re.findall(expr, text)
        prices = list(filter(lambda x: True if x[1] in currency else False, prices))
        if len(prices) == 1:
            self.price = prices[0][0]
            self.currency = prices[0][1]
        elif len(prices) > 1:
            maxprice = ('0', "")
            for price in prices:
                if price[0] > maxprice[0]:
                    maxprice = price
            self.price = maxprice[0]
            self.currency = maxprice[1]
        self.text = text

    def todb(self, cur):
        cur.execute("INSERT INTO theme (title, url, author, text, price, currency) SELECT %s, %s, %s, %s, %s, %s "
                    "WHERE NOT EXISTS (SELECT * FROM theme where title = %s and author = %s)",
                    (self.title, self.url, self.author, self.text, self.price, self.currency, self.title, self.author))


@asyncio.coroutine
def get(url):
    response = aiohttp.request(method='GET', url=url)
    result = yield from asyncio.wait_for(response, timeout=60)
    body = yield from result.read()
    return body


@asyncio.coroutine
def parsepage(url, announces=False):
    """parse everything except for announces"""
    page = yield from get(url)
    root = etree.HTML(page)
    if announces:
        themes = root.xpath('//li[contains(@class, "row bg")]/dl[contains(@class, "announce")]')
    else:
        themes = root.xpath('//li[contains(@class, "row bg")]/dl[not(contains(@class, "announce"))]')
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

t0 = time.time()
tasks = [parsepage(url, announces=True)]
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

with psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='1'") as conn:
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS theme(
           id SERIAL PRIMARY KEY,
           title TEXT NOT NULL,
           url TEXT NOT NULL,
           author TEXT NOT NULL,
           text TEXT NOT NULL,
           price TEXT NOT NULL,
           currency TEXT NOT NULL)""")
    cur.execute("""CREATE INDEX IF NOT EXISTS title_author_index ON theme(title, author);""")
    for i in instances:
        i.todb(cur)
    conn.commit()

print("Done in {0} seconds".format(time.time() - t0))
loop.close()
