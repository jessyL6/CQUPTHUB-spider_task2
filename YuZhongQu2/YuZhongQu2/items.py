# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Jiangbei2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    工程名称 = scrapy.Field()
    项目名称 = scrapy.Field()
    中标时间 = scrapy.Field()
    招标人 = scrapy.Field()
    招标代理机构 = scrapy.Field()
    发包人 = scrapy.Field()
    发包价 = scrapy.Field()
    项目批准文号 = scrapy.Field()
    第一侯选人 = scrapy.Field()
    营业执照注册号 = scrapy.Field()
    第二侯选人 = scrapy.Field()
    第三侯选人 = scrapy.Field()
    投诉受理部门 = scrapy.Field()
    工商注册号 = scrapy.Field()
    中选承包价 = scrapy.Field()
    中选承包商 = scrapy.Field()
    项目编号 = scrapy.Field()
