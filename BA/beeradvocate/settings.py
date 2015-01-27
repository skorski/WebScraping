# -*- coding: utf-8 -*-

# Scrapy settings for beeradvocate project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'beeradvocate'

SPIDER_MODULES = ['beeradvocate.spiders']
NEWSPIDER_MODULE = 'beeradvocate.spiders'
CONCURRENT_REQUESTS_PER_DOMAIN = 10
DOWNLOAD_DELAY = 0

LOG_LEVEL = 'INFO'

COOKIES_ENABLED = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'beeradvocate (+http://www.yourdomain.com)'


#this will theoretically stop it from crawling the same url twice
# SPIDER_MIDDLEWARES = { 'project.middlewares.ignore.IgnoreVisitedItems': 560 }
