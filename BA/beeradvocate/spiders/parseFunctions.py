#import SQLmodels
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from beeradvocate.items import BeeradvocateItem, breweryInfo
from pygeocoder import Geocoder
import datetime

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
		locationMess = hxs.select('//td/b/text()').extract()
		for e in locationMess:
			if 'brewery' in e.lower():
				item['brewery'] = "True"
			elif 'bar' in e.lower():
				item['bar'] = "True"
			elif 'store' in e.lower():
				item['store'] = "True"
	except:
		pass

	item['numReviews'] = hxs.select('//span[@class="ba-reviews"]/text()').extract()[0]
	item['numRatings'] = hxs.select('//span[@class="ba-ratings"]/text()').extract()[1].split(' ')[0]

	try:
		rightTable = hxs.select('//td[@align="left"][@width="33%"]/text()').extract()

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
		beerCount = hxs.select('//h6').extract()
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


def parseReview(hxs):
	breweryID = url.split('/')[5]
	beerID = url.split('/')[6]
	self.log(url)

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
		result = beerReview()
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
