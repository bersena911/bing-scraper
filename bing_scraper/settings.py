BOT_NAME = 'bing_scraper'

SPIDER_MODULES = ['bing_scraper.spiders']
NEWSPIDER_MODULE = 'bing_scraper.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

LOG_LEVEL = 'INFO'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100
}
RETRY_HTTP_CODES = [429]
