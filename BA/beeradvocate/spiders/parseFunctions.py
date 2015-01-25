# import SQLmodels
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from beeradvocate.items import BeeradvocateItem, breweryInfo, beerInfo, beerReview
from SQLmodels import DBbeerInfo, DBbeerReview
import unicodedata
from pygeocoder import Geocoder
import re
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def isInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


def parseBrewery(hxs, url):
	item = breweryInfo()
	item['breweryName'] = hxs.xpath('//*[@id="content"]/div/div/div[1]/div/div[3]/h1/text()').extract()[0]
	item['placeScore'] = hxs.xpath('//span[@class="BAscore_big ba-score"]/text()').extract()[0]
	item['breweryID'] = url.split('/')[5]
	# # check the DB to see if it already exists

	# # if not, get the rest of the info
	try:
		locationMess = hxs.xpath('//td/b/text()').extract()
		for e in locationMess:
			if 'brewery' in e.lower():
				item['brewery'] = "True"
			elif 'bar' in e.lower():
				item['bar'] = "True"
			elif 'store' in e.lower():
				item['store'] = "True"
	except:
		pass

	item['numReviews'] = int(hxs.xpath('//span[@class="ba-reviews"]/text()').extract()[0].replace(',',''))
	item['numRatings'] = int(hxs.xpath('//span[@class="ba-ratings"]/text()').extract()[1].split(' ')[0].replace(',',''))

	try:
		rightTable = hxs.xpath('//td[@align="left"][@width="33%"]/text()').extract()

		for e in rightTable:
			if 'Taps:' in e:
				item['numTaps'] = e.split(' ')[1]
			elif 'Bottles:' in e:
				item['numBottles'] = e.split(' ')[1]
			elif 'Cask:' in e:
				item['caskBeer'] = e.split(' ')[1]
			elif 'Beer-to-Go' in e:
				item['beerToGo'] = e.split(' ')[1]
	except:
		pass

	try:
		beerCount = hxs.xpath('//h6').extract()
		p1 = re.compile('Current \(\d*\)')
		item['currentBeers'] = str(p1.findall(beerCount[0])[0]).split('(')[1][:-1]
		p1 = re.compile('Archived \(\d*\)')
		item['archivedBeers'] = str(p1.findall(beerCount[0])[0]).split('(')[1][:-1]
	except:
		pass

	try:
		locationBlock = hxs.xpath('//td[@align="left"][@valign="top"]/a/text()').extract()
		item['city'] = locationBlock[0]
		item['state'] = locationBlock[1]
		item['country'] = locationBlock[2]
		item['twitter'] = locationBlock[5]
		item['streetAddress'] = hxs.xpath('//td[@align="left"][@valign="top"][@style="padding:10px;"]/text()').extract()[1]
		item['gcAddress'] = item['breweryName'] + " " + item['streetAddress'] + " " + item['city'] + ", " + item['state']
	except:
		pass

	try:
		item['phone'] = hxs.xpath('//td[@align="left"][@valign="top"][@style="padding:10px;"]/text()').extract()[4].split(':')[1]
	except:
		pass

	try:
		googleResult = Geocoder.geocode(item['gcAddress'])
		item['latc'] = googleResult[0].coordinates[0]
		item['longc'] = googleResult[0].coordinates[1]
	except:
		pass

	item['retriveDate'] = datetime.datetime.now()

	return item


def parseBeer(hxs, url):
	print "Parsing Beer Info"
	item = {}
	item['beerName'] = hxs.xpath('//*[@id="content"]/div/div/div[1]/div/div[3]/h1/text()').extract()[0]
	item['breweryName'] = hxs.xpath('//td/a[contains(@href,"/beer/profile")]/b/text()').extract()[0]
	item['breweryID'] = url.split('/')[5]
	item['beerID'] = url.split('/')[6]

	try:
		item['BAScore'] = int(hxs.xpath('//span[@class="BAscore_big ba-score"]/text()').extract()[0])
	except:
		item['BAScore'] = -9
		print 'BAScore ' + hxs.xpath('//span[@class="BAscore_big ba-score"]/text()').extract()[0]

	# add try/except because ommitted values are '-'
	try:
		item['BROScore'] = int(hxs.xpath('//span[@class="BAscore_big ba-bro_score"]/text()').extract()[0])
	except:
		item['BROScore'] = -9
		print 'BROScore ' + hxs.xpath('//span[@class="BAscore_big ba-bro_score"]/text()').extract()[0]

	try:
		item['numRatings'] = int(hxs.xpath('//span[@class="ba-ratings"]/text()').extract()[1].split(' ')[0].replace(',',''))
	except:
		item['numRatings'] = -9

	try:
		item['numReviews'] = int(hxs.xpath('//span[@class="ba-reviews"]/text()').extract()[0].replace(',',''))
	except:
		item['numReviews'] = -9

	try:
		item['rAvg'] = float(hxs.xpath('//span[@class="ba-ravg"]/text()').extract()[0])
	except:
		item['rAvg'] = -9

	try:
		item['pDev'] = float(hxs.xpath('//span[@class="ba-pdev"]/text()').extract()[0][:-1])
	except:
		item['pDev'] = -9

	try:
		item['wants'] = int(hxs.xpath('//a[contains(@href,"/beer/trade/")]/text()').extract()[0].split(':')[1])
	except:
		item['wants'] = -9

	try:
		item['gots'] = int(hxs.xpath('//a[contains(@href,"/beer/trade/")]/text()').extract()[1].split(':')[1])
	except:
		item['gots'] = -9

	try:
		item['FT'] = int(hxs.xpath('//a[contains(@href,"/beer/trade/")]/text()').extract()[2].split(':')[1])
	except:
		print "FT: " + hxs.xpath('//a[contains(@href,"/beer/trade/")]/text()').extract()[2].split(':')[1]

	item['style'] = hxs.xpath('//a[contains(@href,"/beer/style")]/b/text()').extract()[0]

	abvMess = hxs.xpath('//b[text()="Style | ABV"]/following-sibling::text()').extract()
	abv = [thing for thing in abvMess if '%' in thing][0]
	abv = unicodedata.normalize('NFKD', abv).encode('ascii','ignore')
	try:
		item['ABV'] = float(re.search('(\d{0,2}\.\d{0,2})\%', abv).group(0)[:-1])
	except:
		print 'ABV' + abv

	try:
		availability = unicodedata.normalize('NFKD', hxs.xpath('//b[text()="Availability:"]/following-sibling::text()').extract()[0]).encode('ascii','ignore')
		item['availability'] = availability
	except:
		print "Avail error"

	# try:
	# 	# item['notes'] = ' '.join(unicodedata.normalize('NFKD', hxs.xpath('//b[text()="Notes & Commercial Description:"]/following-sibling::text()').extract().encode('ascii','ignore')))
	# except:
	# 	print "Notes error"

	try:
		item['retriveDate'] = datetime.datetime.now()
	except:
		print datetime.datetime.now()


	print "---"
	# print item
	print "-- BP Complete --"
	return item


def parseReview(hxs, url, engine):
	# we take the DB so we can commit to it at the end of the page
	# only make a single commit after all of the reviews have been added

	# create a configured session class
	Session = sessionmaker(bind=engine)

	# now create the session
	db = Session()

	print "Parsing Review"

	breweryID = url.split('/')[5]
	beerID = url.split('/')[6]

	reviews = hxs.xpath('//*[@id="rating_fullview_container"]')
	title = hxs.xpath('//*[@id="content"]/div/div/div[1]/div/div[3]/h1/text()').extract()[0]
	brewery = hxs.xpath('//*[@id="content"]/div/div/div[1]/div/div[3]/h1/span/text()').extract()[0][3:]
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
		result = beerReview()
		#try:
		result['name'] = title
		result['brewery'] = brewery
		result['breweryID'] = breweryID
		result['beerID'] = beerID
		result['rating'] = review.xpath('//*[@id="rating_fullview_content_2"]/span[1]/text()')[i].extract()
		try:
			result['userName'] = review.xpath('//*[@id="rating_fullview_content_2"]/div/span/a[1]/text()')[i].extract()
		except IndexError:
			result['userName'] = 'NA'

		try:
			result['fullReview'] = review.xpath('//*[@id="rating_fullview_content_2"]/span[4]/text()')[i].extract()
		except IndexError:
			result['fullReview'] = "NA"
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

		print ("u: " + result['userName']+" - #" + str(i) +" " +brewery[0]+ ":"+breweryID+":"+ beerID)
		newReview = DBbeerReview(result)

		# now we will try to add the review to the DB
		db.add(newReview)
		# print "---"
		# print result
		print "-- review parse Complete --"

		# except IOError:
		# 	result = BeeradvocateItem()
		# 	yield result
		#else:
		#	result = BeeradvocateItem()
		#finally:
		db.commit()
		try:
			db.commit()
			print "Reviews added"
			# return True
		except:
			db.rollback()
			print "Review addition error"
			# return False
	return False


#hxs.xpath('//td[@align="left"][@valign="top"][@style="padding:10px;"]/td[contains(text(), "|")]/text()').extract()