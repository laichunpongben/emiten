#!/usr/bin/python3

import time
import json
import requests
from bs4 import BeautifulSoup
import database as db


class KaggleCrawler(object):
    def __init__(self):
        self.base_url = 'https://www.kaggle.com'
        self.urls = self.get_urls()

    def get_urls(self):
        with open('url.json', 'r') as f:
            data = json.load(f)
        for url in data['kaggle']:
            yield url

    def crawl(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        for url in self.urls:
            time.sleep(3)
            print(url)
            response = requests.get(url, headers=headers)
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            for row in soup.findAll(class_=['job-post-row']):
                title = row.find(class_=['position']).get_text().replace('\n', '').strip()
                description = ''
                company = row.find(['img']).get('alt', '')
                url = ''
                keyword = ''
                yield title, description, company, url, keyword

    def save(self, **kwargs):
        db.save(**kwargs)

    def run(self):
        for match in self.crawl():
            title, description, company, url, keyword = match
            self.save(title=title,
                      description=description,
                      company=company,
                      url=url,
                      keyword=keyword)

if __name__ == '__main__':
    crawler = KaggleCrawler()
    crawler.run()
