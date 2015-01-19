from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from sqlite3 import dbapi2 as sqlite3

from pygeocoder import Geocoder  # this is used to convert the address to lat long
import datetime

from app import db, oembed

db = SQLAlchemy(app)
engine = create_engine('sqlite:////absolute/path/to/foo.db')

class beerReview(db.Model):
	beerID = Column(db.Integer, primary_key=True)
	breweryID = Column(db.Integer, db.ForeignKey(''))
	rating = Column(Float)
	userName = Column(Text)
	fullReview = Column(Text)
	date = Column(DateTime)
	notes = Column(Text)
	retriveDate = Column(DateTime)

	def __init__(self, beerID, breweryID, rating, userName, fullReview, date)
		self.beerID = beerID
		self.breweryID = breweryID
		self.rating = rating
		self.userName = userName
		self.fullReview = fullReview
		self.retriveDate = datetime.datetime.now()


class breweryInfo(db.Model)
	breweryID = Column(Integer, primary_key = True)
	place_Score = Column(Integer)
	locationType = Column(Text) # bar, store, brewery...
	numReviews = Column(Integer)
	numRatings = Column(Integer)
	numTaps = Column(Integer)
	numBottles = Column(Integer)
	caskBeer = Column(Text)
	beerToGo = Column(Text)
	activeBeers = Column(Integer)
	archivedBeers = Column(Integer)
	streetAddress = Column(Text)
	city = Column(Text)
	state = Column(Text)
	zip = Column(Integer)
	country = Column(Text)
	lat = Column(Float)
	long = Column(Float)
	phone = Column(Text)
	website = Column(Text)
	twitter = Column(Text)
	instagram = Column(Text)
	notes = Column(Text)
	retriveDate = Column(DateTime) 

	def __init__(self, breweryID, place_Score, locationType, numReviews, numRatings, numTaps, numBottles, caskBeer, beerToGo, activeBeers, archivedBeers, streetAddress, city, state, zip, country, lat, long, phone, website, twitter, instagram, notes)
		self.breweryID = breweryID
		self.place_Score = place_Score
		self.locationType = locationType
		self.numReviews = numReviews
		self.numRatings = numRatings
		self.numTaps = numTaps 
		self.numBottles = numBottles
		self.caskBeer = caskBeer
		self.beerToGo = beerToGo
		self.activeBeers = activeBeers
		self.archivedBeers = archivedBeers
		self.streetAddress = streetAddress
		self.city = city
		self.state = state
		self.zip = zip
		self.country = country
		self.lat = lat
		self.long = long
		self.phone = phone
		self.website = website
		self.twitter = twitter
		self.instagram = instagram
		self.notes = notes
		self.retriveDate = datetime.datetime.now()



class beerInfo(db.Model)
	beerID = Column(Integer, primary_key = True)
	breweryID = Column(Integer, db.ForeignKey(''))
	BAScore = Column(Integer)
	BROScore = Column(Integer)
	numRatings = Column(Integer)
	numReviews = Column(Integer)
	rAvg = Column(Float)
	wants = Column(Integer)
	gots = Column(Integer)
	FT = Column(Integer)
	style = Column(Text)
	ABV = Column(Float)
	availability = Column(Text)
	notes = Column(Text)
	retriveDate = Column(DateTime)

	def __init__(self, beerID, breweryID, BAScore, BROScore, numRatings, numReviews, rAvg, wants, gots, FT, style, ABV, availability, notes)
		self.beerID = beerID
		self.breweryID = breweryID
		self.BAScore = BAScore
		self.BROScore = BROScore
		self.numRatings = numRatings
		self.numReviews = numReviews
		self.rAvg = rAvg
		self.wants = wants
		self.gots = gots
		self.FT = FT
		self.style = style
		self.ABV = ABV
		self.availability = availability
		self.notes = notes
		self.date = datetime.datetime.now()