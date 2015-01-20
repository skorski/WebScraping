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

class breweryInfo(scrapy.Item):
	breweryID = scrapy.Field()
	place_Score = scrapy.Field()
	locationType = scrapy.Field()
	numReviews = scrapy.Field()
	numRatings = scrapy.Field()
	numTaps = scrapy.Field()
	numBottles = scrapy.Field()
	caskBeer = scrapy.Field()
	beerToGo = scrapy.Field()
	activeBeers = scrapy.Field()
	archivedBeers = scrapy.Field()
	streetAddress = scrapy.Field()
	city = scrapy.Field()
	state = scrapy.Field()
	zip = scrapy.Field()
	country = scrapy.Field()
	lat = scrapy.Field()
	long = scrapy.Field()
	phone = scrapy.Field()
	website = scrapy.Field()
	twitter = scrapy.Field()
	instagram = scrapy.Field()
	notes = scrapy.Field()
	retriveDate = scrapy.Field()
	

	def __init__(self, breweryID, place_Score, locationType, numReviews, numRatings, numTaps, numBottles, caskBeer, beerToGo, activeBeers, archivedBeers, streetAddress, city, state, zip, country, lat, long, phone, website, twitter, instagram, notes):
		self['breweryID'] = breweryID
		self['place_Score'] = place_Score
		self['locationType'] = locationType
		self['numReviews'] = numReviews
		self['numRatings'] = numRatings
		self['numTaps'] = numTaps 
		self['numBottles'] = numBottles
		self['caskBeer'] = caskBeer
		self['beerToGo'] = beerToGo
		self['activeBeers'] = activeBeers
		self['archivedBeers'] = archivedBeers
		self['streetAddress'] = streetAddress
		self['city'] = city
		self['state'] = state
		self['zip'] = zip
		self['country'] = country
		self['lat'] = lat
		self['long'] = long
		self['phone'] = phone
		self['website'] = website
		self['twitter'] = twitter
		self['instagram'] = instagram
		self['notes'] = notes
		self['retriveDate'] = datetime.datetime.now()