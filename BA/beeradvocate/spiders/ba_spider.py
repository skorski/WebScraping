import scrapy
import re
from scrapy import log
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from beeradvocate.items import BeeradvocateItem, breweryInfo
from scrapy.shell import inspect_response
import SQLmodels
from scrapy.exceptions import DropItem
from parse_functions import parseBrewery, parseReview, isInt

# scrapy crawl beeradvocate


class storeInDBPipeline(object):
	var_item = 1

	def process_item(self, object, spider):
		var_item = 2
		if (var_item == "crap"):
			raise DropItem('this one stinks %s' %item)
		else:
			db.add(breweryInstance)
			db.commit()
			return item

class BASpider(CrawlSpider):
	name = "beeradvocate"
	# start_urls = ["http://www.beeradvocate.com/beer/style/", "http://www.beeradvocate.com/beer/"]   
	start_urls = ["http://www.beeradvocate.com/place/"]  


	# rules = (
	#Rule (LinkExtractor(allow=("http://www.beeradvocate.com/beer/style/", "http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{3,6}/", "http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{0,6}/{0,1}?view=beers",), deny=("http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/?ba=", "http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/\?sort=low","http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/\?sort=[a-z]{1,9}", "http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/\?ba=",),), 'parse_page', follow = True),)

	rules = (
	Rule (LinkExtractor(
		allow=("http://www.beeradvocate.com/beer/zzzzzstyle/", 
			"http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{0,1}/", 
			"http://www.beeradvocate.com/beer/profile/\d{2,6}/\?view=ratings",
			), 
		deny=(
			"http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/\?ba=", 
			"http://www.beeradvocate.com/beer/profile/\d{2,6}/\?ba", 
			"http://www.beeradvocate.com/beer/profile/\d{2,6}/\?sort", 
			"http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{3,6}/\?sort=low",
			"http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{3,6}/\?sort=[a-z]{1,9}", 
			"http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{3,6}/\?ba=",
			),), 'parse_page', follow = True),)

#  ,
#		Rule (LinkExtractor(allow=("http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/?view=beers&sort=&start=.*", ),
#											deny=("http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/?ba=", )), 'parse_page', follow= True)

# Rule (LinkExtractor(allow=("http://www.beeradvocate.com/beer/profile/345/104028/\?view=beer&sort=&start=.*", ),
# 											deny=("http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/?ba=", ))
# 	, 'parse_page', follow= True),

# Rule (LinkExtractor(allow=("http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/", ),), 'parse_beer', follow= True) ,
#http://www.beeradvocate.com/beer/profile/345/?view=beers
#Rule (LinkExtractor(allow=("http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/", ),), 'parse_page', follow= True)

	def parse_page(self, response):
		self.log('==Entrered Inner Parse==')
		url = response.url
		if url: 
			hxs = scrapy.Selector(response)
			# See what we are going to be parsing
			# Is it a store / brewery / bar
			try: 
				print url
				print "6:" + url.split('/')[6] + " 4:" + url.split('/')[4]
				if (not isInt(url.split('/')[6]) and url.split('/')[4] == 'profile'):
					# if there is no final value and it is a profile... it's a place page
					print ('==Place==')
					item = parseBrewery(hxs)
					yield item
				elif (not isInt(url.split('/')[6]) and url.split('/')[4] == 'style'): 
					# this is a style of beer, only get the links.
					print ('==Style Page==')
					yield BeeradvocateItem()
				elif (isInt(url.split('/')[6]) and url.split('/')[4] == 'profile'):
					# this is a beer review page
					print ('==Review Page==')
					item = parseReview(hxs)
					yield item
	
			except IndexError:
				print ('==index error==')
				yield BeeradvocateItem()
			# else:
			# 	print ('==else==')
			# 	yield BeeradvocateItem()
