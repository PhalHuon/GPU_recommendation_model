BOT_NAME = 'gpu_price_tracker'

SPIDER_MODULES = ['gpu_price_tracker.spiders']
NEWSPIDER_MODULE = 'gpu_price_tracker.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# Configure a delay for requests (in seconds)
DOWNLOAD_DELAY = 1.5
RANDOMIZE_DOWNLOAD_DELAY = True

# Disable cookies
COOKIES_ENABLED = False

# Use a user agent rotation middleware
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

# Enable item pipelines
ITEM_PIPELINES = {
    'gpu_price_tracker.pipelines.CleanDataPipeline': 300,
    'gpu_price_tracker.pipelines.MongoPipeline': 400,
}

# MongoDB settings
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'gpu_tracker'

# Handling errors gracefully
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# Logging level
LOG_LEVEL = 'INFO'