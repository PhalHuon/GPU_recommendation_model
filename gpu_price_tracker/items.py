# gpu_price_tracker/items.py

import scrapy

class GPUItem(scrapy.Item):
    # Basic information
    brand = scrapy.Field()
    model = scrapy.Field()
    name = scrapy.Field()
    manufacturer = scrapy.Field()  # ASUS, MSI, EVGA, etc.
    
    # Price information
    price = scrapy.Field()
    currency = scrapy.Field()
    original_price = scrapy.Field()  # If there's a discount
    
    # Retailer information
    retailer = scrapy.Field()
    url = scrapy.Field()
    
    # Other useful data
    availability = scrapy.Field()
    shipping_cost = scrapy.Field()
    rating = scrapy.Field()
    num_reviews = scrapy.Field()
    
    # Metadata
    timestamp = scrapy.Field()
    specifications = scrapy.Field()  # Dict of technical specs