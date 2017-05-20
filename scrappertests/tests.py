import unittest
import asyncio
from scrappertests import scrapper


class MyTests(unittest.TestCase):

    def setUp(self):
        self.url = "https://coinmarketcap.com/all/views/all"
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.testlist = ['#', 'Name', 'Symbol', 'Market Cap', 'Price',
                         'Circulating Supply', 'Volume (24h)', '% 1h', '% 24h', '% 7d']

    def test_wrapper(self):
        @asyncio.coroutine
        def test_parsepage(url):
            res = yield from scrapper.parsepage(url)
            self.assertIsInstance(res, list)
        self.loop.run_until_complete(test_parsepage(self.url))

    def test_out(self):
        self.assertTrue(scrapper.to_xlsx(self.testlist))

    def tearDown(self):
        self.loop.close()


if __name__ == '__main__':
    unittest.main()
