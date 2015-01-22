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
	breweryID = scrapy.Field()
	rating = scrapy.Field()
	userName = scrapy.Field()
	fullReview = scrapy.Field()
	date = scrapy.Field()
	notes = scrapy.Field()
	retriveDate = scrapy.Field()


class beerInfo(scrapy.Item):	
	beerID = scrapy.Field()
	breweryID = scrapy.Field()
	BAScore = scrapy.Field()
	BROScore = scrapy.Field()
	numRatings = scrapy.Field()
	numReviews = scrapy.Field()
	rAvg = scrapy.Field()
	wants = scrapy.Field()
	gots = scrapy.Field()
	FT = scrapy.Field()
	style = scrapy.Field()
	ABV = scrapy.Field()
	availability = scrapy.Field()
	notes = scrapy.Field()
	retriveDate = scrapy.Field()


class breweryInfo(scrapy.Item):
	breweryID = scrapy.Field() # scraped
	breweryName = scrapy.Field() # scraped
	placeScore = scrapy.Field() # scraped
	brewery = scrapy.Field() # scraped
	bar = scrapy.Field() # scraped
	store = scrapy.Field() # scraped
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
	latc = scrapy.Field() # scraped
	longc = scrapy.Field() # scraped
	phone = scrapy.Field() # scraped
	twitter = scrapy.Field()  # scraped
	retriveDate = scrapy.Field()
	gcAddress = scrapy.Field()
