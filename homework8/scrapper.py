from lxml import etree
from openpyxl import Workbook
import asyncio
import aiohttp
from apscheduler.schedulers.blocking import BlockingScheduler


@asyncio.coroutine
def get(url):
    headers = {"authority": "coinmarketcap.com", "method": "GET", "path": "/all/views/all/", "scheme": "https",
               "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "accept-encoding": "gzip, deflate, sdch, br",
               "accept-language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4,uk;q=0.2", "cache-control": "max-age=0",
               "cookie": "__cfduid=d6d0da7117b10217698d8e639ad744a701493976560; _ga=GA1.2.1114691549.1493976558; "
                         "_gid=GA1.2.604347514.1494060274; _gat=1",
               "if-modified-since": "Sat, 06 May 2017 08:40:12 GMT",
               "upgrade-insecure-requests": "1",
               "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"}
    response = aiohttp.request(method='GET', url=url, headers=headers)
    result = yield from asyncio.wait_for(response, timeout=60)
    body = yield from result.read()
    return body


@asyncio.coroutine
def parsepage(url):
    page = yield from get(url)
    root = etree.HTML(page)
    rows = root.xpath('//table')[0]
    headers = rows.xpath('./thead/tr/th/text()')
    currencies = rows.xpath('./tbody/tr/descendant-or-self::text()')
    currencies = list(filter(None, (map(lambda x: x.strip(), currencies))))
    currencies = [x for x in currencies if not x.startswith('*')]
    currencies = list((map(lambda x: 0 if x == "?" or x == "Low Vol" else x, currencies)))
    return headers+currencies


def to_xlsx(table):
    wb = Workbook()
    ws = wb.active
    for row in range(0, len(table), 10):
        ws.append(table[row:row+10])
    ws['A1'] = "N"
    wb.save("currencies.xlsx")


def refresh():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    url = "https://coinmarketcap.com/all/views/all/"
    tasks = [parsepage(url)]
    results = loop.run_until_complete(asyncio.wait(tasks))[0]
    for i in results:
        to_xlsx(i.result())
    print("Refreshed")
    loop.close()


def run():
    sched = BlockingScheduler()
    sched.add_job(refresh, 'interval', minutes=5)
    sched.start()


if __name__ == "__main__":
    run()
