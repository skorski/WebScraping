from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlite3 import dbapi2 as sqlite3
# from ba_spider import Base
import datetime


Base = declarative_base()

def createTables(engine):
	#try:
	Base.metadata.create_all(engine)
	return True
	#except:
	#	return False

def createDB(engine):
	try:
		md = MetaData()
		connection = engine.connect()
		return True
	except:
		return False


def duplicateBrewery(compBrewID, db):
	# query the db for breweries with the num ID.
	q = db.query(DBbreweryInfo).filter(DBbreweryInfo.breweryID == compBrewID).all()
	if len(q) > 0:
		return True
	else:
		return False


def duplicateBeer(compBeerID, db):
	q = db.query(DBbeerInfo).filter(DBbeerInfo.beerID == compBeerID).all()
	if len(q) > 0:
		return True
	else:
		return False


def addBrewery(item):
	newBrewery = breweryInfo()


# ###########################
#        Declarations
# ###########################


class DBbeerReview(Base):
	__tablename__ = "beerReview"

	pk = Column(Integer, primary_key = True)
	name = Column(Text)
	brewery = Column(Text)
	fkbreweryID = Column(Integer)
	beerID = Column(Integer)
	rating = Column(Float)
	userName = Column(Text)
	fullReview = Column(Text)
	notes = Column(Text)
	date = Column(Text)
	retriveDate = Column(DateTime)

	def __init__(self, item):
		self.beerID = item.get('beerID', -9)
		self.name = item.get('name', 'NA')
		self.brewery = item.get('brewery', 'NA')
		self.fkbreweryID = item.get('breweryID', -9)
		self.rating = item.get('rating', -9)
		self.userName = item.get('userName', 'NA')
		self.fullReview = item.get('fullReview', 'NA')
		self.notes = item.get('notes', 'NA')
		self.date = item.get('date', 'NA')
		self.retriveDate = datetime.datetime.now()


class DBbreweryInfo(Base):
	__tablename__ = "breweryInfo"

	breweryID = Column(Integer, primary_key=True) # scraped
	breweryName = Column(Text) # scraped
	placeScore = Column(Float) # scraped
	brewery = Column(Text) # scraped bool for location type
	bar = Column(Text) # scraped bool for location type
	store = Column(Text) # scraped bool for location type
	numReviews = Column(Integer) # scraped
	numRatings = Column(Integer) # scraped
	numTaps = Column(Integer) # scraped
	numBottles = Column(Integer) # scraped
	caskBeer = Column(Text) # scraped
	beerToGo = Column(Text) # scraped
	activeBeers = Column(Integer) # scraped
	archivedBeers = Column(Integer) # scraped
	streetAddress = Column(Text) # scraped
	city = Column(Text) # scraped
	state = Column(Text) # scraped
	zipCode = Column(Integer)
	country = Column(Text) # scraped
	latc = Column(Float) # scraped
	longc = Column(Float) # scraped
	phone = Column(Text) # scraped
	twitter = Column(Text) # scraped
	retriveDate = Column(DateTime) # scraped

	def __init__(self, item):
		self.breweryID = item['breweryID']
		self.breweryName = item['breweryName']
		self.placeScore = item['placeScore']
		self.brewery = item.get('brewery', 'False')
		self.bar = item.get('bar', 'False')
		self.store = item.get('store', 'False')
		self.numReviews = item.get('numReviews', -1)
		self.numRatings = item.get('numRatings', -1)
		self.numTaps = item.get('numTaps', 0)
		self.numBottles = item.get('numBottles', 0)
		self.caskBeer = item.get('caskBeer', 'N')
		self.beerToGo = item.get('beerToGo', 'N')
		self.activeBeers = item.get('activeBeers', 0)
		self.archivedBeers = item.get('archivedBeers', 0)
		self.streetAddress = item.get('streetAddress', 0)
		self.city = item.get('city', 'NA')
		self.state = item.get('state', 'NA')
		self.zipCode = item.get('zipCode', 00000)
		self.country = item.get('country', 'NA')
		self.latc = item.get('latc', -999)
		self.longc = item.get('longc', -999)
		self.phone = item.get('phone', "-9")
		self.twitter = item.get('twitter', "-9")
		self.retriveDate = datetime.datetime.now()

	def __repr__(self):
		return '<DBbreweryInfo (breweryID=%r, breweryName=%r, placeScore=%r, brewery=%r, bar=%r, store=%r, numReviews=%r, numRatings=%r, numTaps=%r, numBottles=%r, caskBeer=%r, beerToGo=%r, activeBeers=%r, archivedBeers=%r, streetAddress=%r, city=%r, state=%r, zipCode=%r, country=%r, latc=%r, longc=%r, phone=%r, twitter=%r, retriveDate=%r)>' % (self.breweryID, self.breweryName , self.placeScore, self.brewery, self.bar, self.store, self.numReviews, self.numRatings, self.numTaps, self.numBottles,	self.caskBeer, self.beerToGo,	self.activeBeers,	self.archivedBeers, self.streetAddress, self.city, self.state, self.zipCode, self.country, 		self.latc, self.longc, self.phone, self.twitter, self.retriveDate)


class DBbeerInfo(Base):
	__tablename__ = "beerInfo"
	
	beerID = Column(Integer, primary_key = True)
	fkbreweryID = Column(Integer)
	BAScore = Column(Integer)
	BROScore = Column(Integer)
	numRatings = Column(Integer)
	numReviews = Column(Integer)
	rAvg = Column(Float)
	pDev = Column(Float)
	wants = Column(Integer)
	gots = Column(Integer)
	FT = Column(Integer)
	style = Column(Text)
	ABV = Column(Float)
	availability = Column(Text)
	notes = Column(Text)
	retriveDate = Column(DateTime)

	def __init__(self, item):
		self.beerName = item['beerName']
		self.breweryName = item['breweryName']
		self.breweryID = item['breweryID']
		self.beerID = item['beerID']
		self.BAScore = item.get('BAScore', -9)
		self.BROScore = item.get('BROScore', -9)
		self.numRatings = item.get('numRatings', -9)
		self.numReviews = item.get('numReviews', -9)
		self.rAvg = item.get('rAvg', -9)
		self.pDev = item.get('pDev', -9)
		self.wants = item.get('wants', -9)
		self.gots = item.get('gots', -9)
		self.FT = item.get('FT', -9)
		self.style = item.get('style', 'NA')
		self.ABV = item.get('ABV', -9)
		self.availability = item.get('availability', 'NA')
		self.notes = item.get('notes', 'NA')
		self.retriveDate = datetime.datetime.now()	

def __repr__(self):
		return '<DBbeerInfo (beerName = %r, breweryName = %r, breweryID = %r, beerID = %r, BAScore = %r, BROScore = %r, numRatings = %r )>' % (self.beerName, self.breweryName, self.breweryID, self.beerID, self.BAScore, self.BROScore, self.numRatings)