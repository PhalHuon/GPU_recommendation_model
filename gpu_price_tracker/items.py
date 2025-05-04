import scrapy
from datetime import datetime

class GPUItem(scrapy.Item):
    #basic info
    brand = scrapy.Field()
    model = scrapy.Field()
    name = scrapy.Field()
    manufacturer = scrapy.Field()

    #price
    price = scrapy.Field()
    currency = scrapy.Field()
    original_price = scrapy.Field()

    #retail info
    retailer = scrapy.Field()
    url = scrapy.Field()

    #others
    availability = scrapy.Field()
    shipping_cost = scrapy.Field()
    rating = scrapy.Field()
    num_reviews = scrapy.Field()

    #metadata
    timestamp = scrapy.Field(default = datetime.now().isoformat())
    specifications = scrapy.Field() #dictionary techinical specs
    