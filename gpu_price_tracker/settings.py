# gpu_price_tracker/settings.py

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

# Use a random user agent
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

# Enable item pipelines
ITEM_PIPELINES = {
    'gpu_price_tracker.pipelines.CleanDataPipeline': 300,
    'gpu_price_tracker.pipelines.MySQLPipeline': 400,
}

# MySQL database settings
MYSQL_CONNECTION_STRING = "mysql+pymysql://root:password@localhost/gpu_tracker"

# Logging level
LOG_LEVEL = 'INFO'