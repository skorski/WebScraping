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
from scrapy.exceptions import DropItem
from parseFunctions import parseBrewery, parseBeer, parseReview, isInt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base # this is used to create the base class that can be used to create the database
Base = declarative_base()

# with base defined we can import the models
from SQLmodels import DBbreweryInfo, DBbeerReview, DBbeerInfo, createTables, duplicateBrewery, duplicateBeer

# scrapy crawl beeradvocate
# scrapy crawl beeradvocate -s JOBDIR=crawls/somespider-1

engine = create_engine('sqlite:////home/dan/foo.sqlite')

# create a configured session class
Session = sessionmaker(bind=engine)

# now create the session
db = Session()

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

	createTables(engine)

	# start_urls = ["http://www.beeradvocate.com/beer/style/", "http://www.beeradvocate.com/beer/"]   
	start_urls = [
							"http://www.beeradvocate.com/beer/profile/73/5096/",
							#"http://www.beeradvocate.com/place/"
							]  

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
				breweryID = url.split('/')[4]
				print "6:" + url.split('/')[6] + " 4:" + breweryID
				if (not isInt(url.split('/')[6]) and url.split('/')[4] == 'profile'):
					# if there is no final value and it is a profile... it's a place page	
					print '==Place=='
					# test to see if this has already been parsed
					# inspect_response(response, self)
					q = db.query(DBbreweryInfo).filter(DBbreweryInfo.breweryID == breweryID).all()
					if q:
						print 'duplicated brewery'
						# create a blank item and return it, there is no need to parse
						item = breweryInfo()
						yield item
					else:
						item = parseBrewery(hxs, url)
						try:
							newBrewery = DBbreweryInfo(item)
							db.add(newBrewery)
							db.commit()
							print "DB commit successful"
						except:
							db.rollback()
							print "DB commit failed"
						print item['breweryName']
						print "-----------"
						yield item

				elif (not isInt(url.split('/')[6]) and url.split('/')[4] == 'style'): 
					# this is a style of beer, only get the links.
					print ('==Style Page==')
					item = breweryInfo()
				 	yield item

				elif (isInt(url.split('/')[6]) and url.split('/')[4] == 'profile'):
				 	# this is a beer review page
				 	print ('==Review Page==')
					# inspect_response(response, self)
					q = db.query(DBbeerReview).filter(DBbeerReview.beerID == url.split('/')[6]).all()
					if q:
						print 'duplicate beer'
					else:
						item = parseBeer(hxs, url)
						try:
							newBeer = DBbeerInfo(item)
							db.add(newBeer)
							db.commit()
							print "Beer Successfully added to DB"

							# we pass the db to this function so it can add reviews independently.
							if parseReview(hxs, url, engine):
								print "Reviews Added Successfully"
							else:
								print "* ERROR * Problem Adding Reviews"
						
						except:
							db.rollback()
							print "* ERROR * Beer addition issue"

					item = breweryInfo
				 	yield item
	
			except IndexError:
				print ('==index error==')
				yield BeeradvocateItem()
			# else:
			# 	print ('==else==')
			# 	yield BeeradvocateItem()
