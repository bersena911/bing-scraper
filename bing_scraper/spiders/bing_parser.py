import os
import sys
from itertools import product
from urllib.parse import quote
import json

import scrapy


class BingParser(scrapy.Spider):
    name = 'bing'
    permutations_file = 'perms.txt'
    LINKS_XPATH = '//ol[@id="b_results"]/li/h2/a/@href'
    allowed_domains = ['bing.com']
    input_alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789@!_-.*#'
    start_urls = []

    headers = {
        'authority': 'www.bing.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'accept': 'text/html',
        'accept-language': 'en-US,en;q=0.9,fr;q=0.8,ka;q=0.7,ru;q=0.6,es;q=0.5,uk;q=0.4,hy;q=0.3,de;q=0.2',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_webpage = kwargs['target']
        self.OUTPUT_FILE = sys.argv[-1]
        self.query_length = int(kwargs['length'])
        self.input_alphabet = kwargs.get('input_alphabet', self.input_alphabet)

        # Create visited links set
        self.links_set = set()
        if os.path.exists(self.OUTPUT_FILE):
            with open(self.OUTPUT_FILE, 'r') as f:
                for item in f:
                    item = json.loads(item)
                    self.links_set.add(item['link'])

        # Create crawled queries set
        self.queries_set = set()
        if os.path.exists(self.permutations_file):
            with open(self.permutations_file, 'r') as f:
                for query in f:
                    self.queries_set.add(query.strip())

    def start_requests(self):
        for length in range(1, self.query_length):
            queries = product(self.input_alphabet, repeat=length)
            for query in queries:
                query = quote(''.join(query))
                if query not in self.queries_set:
                    yield scrapy.Request(
                        url=f'https://www.bing.com/search?q={query}+site%3A{self.target_webpage}&first=2&FORM=PERE',
                        callback=self.parse,
                        dont_filter=True,
                        meta={
                            'query': query
                        },
                        headers=self.headers,
                    )

    def parse(self, response):
        query = response.meta['query']
        print(query)

        # Get number of results
        results = response.xpath(
            "//span[@class='sb_count']/text()").extract_first()
        if not results:
            print("No result")
            return

        # Save crawled query
        with open(self.permutations_file, 'a') as f:
            f.write(f"{query}\n")
            f.flush()

        results_list = results.split(' ')
        number_of_results = results_list[0]
        if len(results_list) > 2:
            number_of_results = results_list[2].replace(
                ',', '').replace('.', '').replace(u'\xa0', '')

        number_of_results = int(number_of_results)

        # Bing doesn't return more than 100 pages so restrict to 1000 results

        if number_of_results > 1000:
            number_of_results = 1000
        page = 1
        while page < number_of_results:
            page += 11
            yield scrapy.Request(
                url=f'https://www.bing.com/search?q={query}+site%3A{self.target_webpage}&first={page}&FORM=PORE',
                callback=self.parse_pages,
                dont_filter=True,
                headers=self.headers,
                meta={
                    'query': query
                },
            )

    def parse_pages(self, response):
        query = response.meta['query']

        # Get all links
        links = response.xpath(self.LINKS_XPATH).extract()
        if not links:
            print("No result")

        # Write links to file

        for link in links:
            if link not in self.links_set:
                item = dict(query=query, link=link)
                yield item
