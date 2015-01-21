#import SQLmodels
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from beeradvocate.items import BeeradvocateItem, breweryInfo

def isInt(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

def parseBrewery(hxs):
	# placeScore = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/a/b').extract()
	# breweryID = url.split('/')[5]
	# # check the DB to see if it already exists

	# # if not, get the rest of the info
	# locationType = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/b[1]').extract()
	# numReviews = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/span[2]/text()').extract()
	# numRatings = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/span[1]/text()').extract()
	# numTaps = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[3]/text()[1]').extract()
	# numBottles = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[3]/text()[2]').extract()
	# caskBeer = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[3]/text()[3]').extract()
	# beerToGo = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[3]/text()[4]').extract()
	# activeBeers = hxs.xpath('//*[@id="baContent"]/div[3]/table/tbody/tr[1]/td/h6/text()[1]').extract()
	# archivedBeers = hxs.xpath('//*[@id="baContent"]/div[3]/table/tbody/tr[1]/td/h6/a[1]').extract()
	# streetAddress = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/text()[1]').extract()
	# city = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/a[1]/text()').extract()
	# state = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/a[2]/text()').extract()
	# zip = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/text()[3]').extract()
	# country = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/a[3]').extract()
	# try:
	# 	phone = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/text()[4]').extract()
	# except IndexError:
	# 	phone = -9
	# else:
	# 	phone = -9
	# try:	
	# 	website = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/a[4]').extract()
	# except IndexError:
	# 	website = "none"
	# else:
	# 	website = "none"

	# try:
	# 	twitter = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/a[6]/text()').extract()
	# except IndexError:
	# 	twitter = "none"
	# else:
	# 	twitter = "none"

	# try:
	# 	instagram = "NYS"
	# except IndexError:
	# 	instagram = "none"
	# else:
	# 	instagram = "none"

	# try:
	# 	notes = hxs.xpath('//*[@id="baContent"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/text()[7]/text()').extract()
	# except IndexError:
	# 	notes = "none"
	# else: 
	# 	notes = "none"

# breweryID, placeScore, locationType, numReviews, numRatings, numTaps, numBottles, caskBeer, beerToGo, activeBeers, archivedBeers, streetAddress, city, state, zip, country, -999, -999, phone, website, twitter, instagram, notes

	item = breweryInfo()

	#item = SQLmodels.breweryInfo()
	#item['breweryID'] = breweryID
	#item['placeScore'] = placeScore

	yield item

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
