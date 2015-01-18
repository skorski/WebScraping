import scrapy
import re
from scrapy import log
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from beeradvocate.items import BeeradvocateItem
from scrapy.shell import inspect_response


class BASpider(CrawlSpider):
	name = "beeradvocate"
	#allowed_domains = ["http://www.beeradvocate.com/"]
	start_urls = ["http://www.beeradvocate.com/beer/style/", "http://www.beeradvocate.com/beer/"]   

	rules = (
	Rule (LinkExtractor(allow=("http://www.beeradvocate.com/beer/style/", "http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/", "http://www.beeradvocate.com/beer/profile/\d{3}/\d{0,6}/{0,1}?view=beers",), deny=("http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/?ba=", "http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/\?sort=low","http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/\?sort=[a-z]{1,9}", "http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/\?ba=",),), 'parse_page', follow = True),)

#  ,
#		Rule (LinkExtractor(allow=("http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/?view=beers&sort=&start=.*", ),
#											deny=("http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/?ba=", )), 'parse_page', follow= True)

# Rule (LinkExtractor(allow=("http://www.beeradvocate.com/beer/profile/345/104028/\?view=beer&sort=&start=.*", ),
# 											deny=("http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/?ba=", ))
# 	, 'parse_page', follow= True),

# Rule (LinkExtractor(allow=("http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/", ),), 'parse_beer', follow= True) ,
#http://www.beeradvocate.com/beer/profile/345/?view=beers
#Rule (LinkExtractor(allow=("http://www.beeradvocate.com/beer/profile/\d{3}/\d{3,6}/", ),), 'parse_page', follow= True)

	def parse_beer(self, response):
		# This function grabs all of the beer information
		# brewery, overall score, abv, style, etc.
		url = response.url

		self.log('--Beer Parse--')
		hxs = scrapy.Selector(response)
		title = hxs.xpath('//*[@id="content"]/div/div/div[1]/div/div[3]/h1/text()').extract()
		brewery = hxs.xpath('//*[@id="content"]/div/div/div[1]/div/div[3]/h1/span/text()').extract()
		yield url


	def parse_page(self, response):
		self.log('==Entrered Inner Page==')
		url = response.url

		if '/beer/style' in url:
			yield BeeradvocateItem()
		else:
			breweryID = url.split('/')[5]
			beerID = url.split('/')[6]
			self.log(url)

			hxs = scrapy.Selector(response)
			reviews = hxs.xpath('//*[@id="rating_fullview_container"]')
			title = hxs.xpath('//*[@id="content"]/div/div/div[1]/div/div[3]/h1/text()').extract()
			brewery = hxs.xpath('//*[@id="content"]/div/div/div[1]/div/div[3]/h1/span/text()').extract()
			count = 0
			items = []

			# inspect_response(response, self)
			review = reviews[0]
			resLen = len(review.xpath('//*[@id="rating_fullview_content_2"]/span[1]/text()').extract())
			
			if resLen == 0:
				print '------'
				print 'warning!! - no items found on ' + url
				print '------'

			for i in range(resLen):
				result = BeeradvocateItem()
				try:
					result['name'] = title
					result['brewery'] = brewery
					result['breweryID'] = breweryID
					result['beerID'] = beerID
					result['rating'] = review.xpath('//*[@id="rating_fullview_content_2"]/span[1]/text()')[i].extract()
					try:
						result['user'] = review.xpath('//*[@id="rating_fullview_content_2"]/div/span/a[1]/text()')[i].extract()
		 			except IndexError:
		 				result['user'] = 'NA'

		 			result['date'] = review.xpath('//*[@id="rating_fullview_content_2"]/div/span/a[2]/text()')[i].extract()

					try:
						result['full_review'] = review.xpath('//*[@id="rating_fullview_content_2"]/span[4]/text()')[i].extract()
					except IndexError:
						result['full_review'] = "NA"
					else:
						j=1
						#print "fullRevErr"

					try:
						result['date'] = review.xpath('//*[@id="rating_fullview_content_2"]/div/span/a[2]/text()')[i].extract()
					except IndexError:
						result['date'] = "NA"
					else:
						j=1
						#print "Date Else"

					print ("u: " + result['user']+" - #" + str(i) +" " +brewery[0]+ ":"+breweryID+":"+ beerID)
					yield result
				except IOError:
					result = BeeradvocateItem()
					yield result
				else:
					result = BeeradvocateItem()
					yield result
