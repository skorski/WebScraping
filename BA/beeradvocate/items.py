# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime


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


class beerReview(scrapy.Item):
	beerID = scrapy.Field()
	name = scrapy.Field()
	brewery = scrapy.Field()
	breweryID = scrapy.Field()
	rating = scrapy.Field()
	userName = scrapy.Field()
	fullReview = scrapy.Field()
	date = scrapy.Field()
	notes = scrapy.Field()
	retriveDate = scrapy.Field()


class beerInfo(scrapy.Item):	
	beerName = scrapy.Field() # scraped
	breweryName = scrapy.Field() # scraped
	breweryID = scrapy.Field() # scraped
	beerID = scrapy.Field() # scraped
	BAScore = scrapy.Field() # scraped
	BROScore = scrapy.Field() # scraped
	numRatings = scrapy.Field() # scraped
	numReviews = scrapy.Field() # scraped
	rAvg = scrapy.Field() # scraped
	pDev = scrapy.Field() # scraped
	wants = scrapy.Field() # scraped
	gots = scrapy.Field() # scraped
	FT = scrapy.Field() # scraped
	style = scrapy.Field() # scraped
	ABV = scrapy.Field() # scraped
	availability = scrapy.Field() # scraped
	notes = scrapy.Field() # scraped
	retriveDate = scrapy.Field() # scraped


class breweryInfo(scrapy.Item):
	breweryID = scrapy.Field() # scraped
	breweryName = scrapy.Field() # scraped
	placeScore = scrapy.Field() # scraped
	brewery = scrapy.Field() # scraped bool for location type
	bar = scrapy.Field() # scraped bool for location type
	store = scrapy.Field() # scraped bool for location type
	numReviews = scrapy.Field() # scraped
	numRatings = scrapy.Field() # scraped
	numTaps = scrapy.Field() # scraped
	numBottles = scrapy.Field() # scraped
	caskBeer = scrapy.Field() # scraped
	beerToGo = scrapy.Field() # scraped
	currentBeers = scrapy.Field() # scraped
	archivedBeers = scrapy.Field() # scraped
	streetAddress = scrapy.Field() # scraped
	city = scrapy.Field() # scraped
	state = scrapy.Field() # scraped
	country = scrapy.Field() # scraped
	zipCode = scrapy.Field() 
	latc = scrapy.Field() # scraped
	longc = scrapy.Field() # scraped
	phone = scrapy.Field() # scraped
	twitter = scrapy.Field()  # scraped
	retriveDate = scrapy.Field()
	gcAddress = scrapy.Field()

	
	# def __init__(self):
	# 	placeScore = -9
	# 	self.brewery = 'False'
	# 	self.bar = 'False'
	# 	self.store = 'False'
	# 	self.numReviews = -1
	# 	self.numRatings = -1
	# 	numTaps = -1
	# 	numBottles = -1
	# 	caskBeer = "N"
	# 	beerToGo = "N"
	# 	currentBeers = -1
	# 	archivedBeers = -1
	# 	streetAddress = "NA"
	# 	city = "NA"
	# 	state = "NA"
	# 	country ="NA"
	# 	zipCode = 00000
	# 	latc = -999
	# 	longc = -999
	# 	phone = "NA"
	# 	twitter = "NA"
	# 	gcAddress = "NA"
