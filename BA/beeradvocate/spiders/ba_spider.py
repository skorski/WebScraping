import scrapy
import re
from scrapy import log
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from beeradvocate.items import BeeradvocateItem, breweryInfo, beerReview, beerInfo
from scrapy.shell import inspect_response
import SQLmodels
from scrapy.exceptions import DropItem
from parseFunctions import parseBrewery, parseReview, isInt

# scrapy crawl beeradvocate
# scrapy crawl beeradvocate -s JOBDIR=crawls/somespider-1


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
	start_urls = [
							"http://www.beeradvocate.com/beer/profile/73/5096/",
							#"http://www.beeradvocate.com/place/"
							]  


	# rules = (
	#Rule (LinkExtractor(allow=("http://www.beeradvocate.com/beer/style/", "http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{3,6}/", "http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{0,6}/{0,1}?view=beers",), deny=("http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/?ba=", "http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/\?sort=low","http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/\?sort=[a-z]{1,9}", "http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/\?ba=",),), 'parse_page', follow = True),)

	rules = (
	Rule (LinkExtractor(
		allow=(
			"http://www.beeradvocate.com/beer/profile/\d{2,6}/",
		#	"http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{2,6}/",
		#	"\S*\?view=beer&sort=&start=\d{1,6}",
			), 
		deny=(
			"\S*\?ba=\S*",
			"\S*\?sort=\S*",
			"\S*\?view=events\S*",
			"\S*\?view=ratings\S*",
			# "\S*\?view=",
			),), 'parse_page', follow = True),)


# Allow
			# "http://www.beeradvocate.com/beer/zzzzzstyle/", 
			# "http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{0,1}/", 


# Deny

			# "http://www.beeradvocate.com/beer/profile/\d{2,6}/\?ba=", 
			# "http://www.beeradvocate.com/beer/profile/\d{2,6}/\?sort=", 
			# "http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{3,6}/\?ba=", 
			# "http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{3,6}/\?sort=",
			# "http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{3,6}/\?sort=", 
			# "http://www.beeradvocate.com/beer/profile/\d{2,6}/\d{3,6}/\?ba=",


	def parse_page(self, response):
		print '==Entrered Inner Parse=='
		# inspect_response(response, self)
		url = response.url
		if url: 
			hxs = Selector(response)
			# See what we are going to be parsing
			# Is it a store / brewery / bar
			try: 
				print url
				print "6:" + url.split('/')[6] + " 4:" + url.split('/')[4]
				if (not isInt(url.split('/')[6]) and url.split('/')[4] == 'profile'):
					# if there is no final value and it is a profile... it's a place page
					print ('==Place==')
					item = parseBrewery(hxs, url)
					print "Called Parse"
					print item
					print "-----------"
					yield item

				# elif (not isInt(url.split('/')[6]) and url.split('/')[4] == 'style'): 
				# 	# this is a style of beer, only get the links.
				# 	print ('==Style Page==')
				# 	item = BeeradvocateItem()
				# 	yield item
				# elif (isInt(url.split('/')[6]) and url.split('/')[4] == 'profile'):
				# 	# this is a beer review page
				# 	print ('==Review Page==')
				# 	item = parseReview(hxs)
				# 	yield item
	
			except IndexError:
				print ('==index error==')
				yield BeeradvocateItem()
			# else:
			# 	print ('==else==')
			# 	yield BeeradvocateItem()
