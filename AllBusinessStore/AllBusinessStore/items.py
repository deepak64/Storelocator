# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AllbusinessstoreItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	business_name = scrapy.Field()
	city = scrapy.Field()
	state = scrapy.Field()
	zipcode = scrapy.Field()
	country = scrapy.Field()
	phone = scrapy.Field()
	latitude = scrapy.Field()
	longitude = scrapy.Field()
	address = scrapy.Field()
	address_after_parse = scrapy.Field()

	pass
