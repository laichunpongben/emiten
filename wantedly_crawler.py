#!/usr/bin/python3

import time
import json
import requests
from bs4 import BeautifulSoup
import database as db


class WantedlyCrawler(object):
    def __init__(self):
        self.base_url = 'https://www.wantedly.com'
        self.urls = self.get_urls()

    def get_urls(self):
        with open('url.json', 'r') as f:
            data = json.load(f)
        for url in data['wantedly']:
            for i in range(1, 11):
                yield url + '?page=' + str(i)

    def crawl(self):
        for url in self.urls:
            time.sleep(3)
            print(url)
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            for tag in soup.findAll(class_=['projects-index-single']):
                title = tag.find(class_=['job-type-tag']).get_text().replace('\n', '').strip()
                tag_description = tag.find(class_=['project-title'])
                description = tag_description.get_text().replace('\n', '').strip()
                company = tag.find(class_=['company-name']).get_text().replace('\n', '').strip()
                url = tag_description.find(['a'], href=True)['href']
                url = self.base_url + url
                keyword = tag.find(class_=['strong']).get_text().replace('\n', '').strip()
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
    crawler = WantedlyCrawler()
    crawler.run()
