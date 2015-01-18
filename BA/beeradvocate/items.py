# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeeradvocateItem(scrapy.Item):
		# define the fields for your item here like:
		# name = scrapy.Field()
		name = scrapy.Field()
		brewery = scrapy.Field()
		breweryID = scrapy.Field()
		beerID = scrapy.Field()
		rating = scrapy.Field()
		user = scrapy.Field()
		full_review = scrapy.Field()
		date = scrapy.Field()
		url = scrapy.Field()
		visit_id = scrapy.Field()
		visit_status = scrapy.Field()