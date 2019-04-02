# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
#from scrapy.conf import settings 读取settings文件
from scrapy.conf import settings

class Jiangbei2Pipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    """docstring for MongoPiplne"""

    #表名，写死的，可以用来区分不同的mongodb表，整个项目都是这一个数据表。
    collection_name = 'scrapy_items'

    #来初始化新创建对象的状态，在一个对象呗创建以后会立即调用，比如像实例化一个类：
    def __init__(self, mongo_uri,mongo_db):
        self.mongo_uri= mongo_uri
        self.mongo_db = mongo_db

    #类方法，需要返回一个类对象，这里返回构造函数的调用
    @classmethod
    #从settings获取配置信息
    def from_crawler(cls,crawler):
    #返回一个class
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )
    
    #链接数据库
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    #把item插入到mongodb
    def  process_item(self, item, spider):
        #name = item.__class__.__name__
        #self.db[name].insert(dict(item))

        #先将item转换为字典形式，然后插入数据库

        #（小疑问：scrapy里面item本来就是字典，为什么再存数据库这里还要再转换一次dict(item)）

        self.db['jiangbei_information'].insert(dict(item))
        #return item可以在控制台上面显示插入的item数据
        return item

    def close_spider (self,spider):
        self.client.close()
