import datetime
import itertools
import logging
import os
from typing import List

import pymongo
import urllib3
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

import connection as cn


def get_site_links():
    conn = cn.dbConnection()
    return list(map(lambda item: item[0], list(itertools.chain(
            *[row.values() for row in conn.get_distinct_webpages()]))))


class DataExtractor:

    def __init__(self, urls: List[str], create_index=False):
        self.urls = urls
        self.http = urllib3.PoolManager()
        self.mongoClient = MongoInserter(os.getenv("MONGO_DB"),
                                         "tech_articles")
        self.mongoClient.create_index("url")

    def __iter__(self):
        return self

    def __next__(self):
        next_url = self.urls.pop()
        self.extract_pages_and_insert(next_url)

    def extract_pages_and_insert(self, next_url):
        response = self.http.request('GET', next_url)
        soup = BeautifulSoup(response.data, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()

        soup_text = soup.get_text(strip=True)
        item_to_insert = {"url": next_url,
                          "document": soup_text,
                          "inserttime": datetime.datetime.now()}
        collection = self.mongoClient.collection
        try:
            insert_id = collection.insert_one(item_to_insert).inserted_id
            logger.info(
                "Inserted item into {}, item url: {}, insert_id {}".format(
                    collection.name, next_url, insert_id))
        except DuplicateKeyError as e:
            logger.warning(e)


class MongoInserter:

    def __init__(self, database: str, collection: str):
        self.client = MongoClient(os.getenv("MONGO_URL"))
        self.database = self.client[database]
        self.collection = self.database[collection]

    def create_index(self, field: str):
        col = self.collection
        col.create_index([
            (field, pymongo.ASCENDING)], unique=True)
        logger.info("Index Info {}".format(str(col.index_information())))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    de = DataExtractor(get_site_links(), create_index=True)
    try:
        while True:
            next(de)
    except IndexError:
        logger.info("All URLs processed and docs inserted into MongoDB")
        logger.info("Total number of docs in collection: {} is '{}'".format(
            de.mongoClient.collection.name, de.mongoClient.collection.count()))
    print("")
    pass
