import scrapy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import GPUItem
from gpus import GPU_MODELS
import re

class EbaySpider(scrapy.Spider):
    name = "ebay"
    allowed_domains = ["ebay.com"]
    
    def start_requests(self):
        for gpu in GPU_MODELS:
            search_query = f"{gpu['brand']} {gpu['model']}"
            # URL encode the search query
            encoded_query = search_query.replace(' ', '+')
            url = f"https://www.ebay.com/sch/i.html?_nkw={encoded_query}&_sacat=0"
            yield scrapy.Request(
                url=url,
                callback=self.parse_search_results,
                meta={'gpu': gpu}
            )
    
    def parse_search_results(self, response):
        gpu = response.meta['gpu']
        
        # Extract product listings from search results
        products = response.css('li.s-item')
        
        for product in products:
            # Check if product title contains both brand and model
            title = product.css('.s-item__title span::text').get()
            if not title or 'Shop on eBay' in title:  # Skip the first "Shop on eBay" item
                continue
                
            title_lower = title.lower()
            if gpu['brand'].lower() in title_lower and gpu['model'].lower() in title_lower:
                # Extract price
                price_str = product.css('.s-item__price::text').get()
                
                # Check if it's "Buy It Now" (avoid auctions)
                buying_format = product.css('.s-item__purchaseOptions::text').get()
                is_buy_it_now = buying_format and 'Buy It Now' in buying_format
                
                if price_str and is_buy_it_now:
                    product_url = product.css('.s-item__link::attr(href)').get()
                    if product_url:
                        yield scrapy.Request(
                            url=product_url,
                            callback=self.parse_product_page,
                            meta={
                                'gpu': gpu, 
                                'title': title,
                                'price_str': price_str
                            }
                        )
        
        # Check for next page and follow it
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse_search_results,
                meta={'gpu': gpu}
            )
    
    def parse_product_page(self, response):
        gpu = response.meta['gpu']
        title = response.meta['title']
        price_str = response.meta['price_str']
        
        # Create GPU item
        item = GPUItem()
        
        # Basic information
        item['brand'] = gpu['brand']
        item['model'] = gpu['model']
        item['name'] = title
        
        # Price information
        if price_str:
            # Remove currency symbol and convert to float
            # Handle ranges like "$900.00 to $1,200.00"
            if 'to' in price_str:
                price_str = price_str.split('to')[0]
            
            try:
                price_clean = re.sub(r'[^\d.]', '', price_str)
                item['price'] = float(price_clean)
                item['currency'] = 'USD'  # Assuming USD, adjust as needed
            except (ValueError, IndexError):
                self.logger.warning(f"Could not parse price: {price_str}")
        
        # Retailer information
        item['retailer'] = 'eBay'
        item['url'] = response.url
        
        # Availability
        quantity_str = response.css('span[itemprop="offerCount"]::text').get()
        if quantity_str:
            item['availability'] = f"{quantity_str.strip()} available"
        
        # Shipping cost
        shipping = response.css('#shSummary::text').get()
        if shipping:
            item['shipping_cost'] = shipping.strip()
        
        # Seller information (as manufacturer in this case)
        seller = response.css('.user-information a::text').get()
        if seller:
            item['manufacturer'] = seller.strip()
        
        # Specifications (from item specifics)
        specs = {}
        spec_rows = response.css('.ux-labels-values__labels-content')
        for row in spec_rows:
            key = row.css('.ux-labels-values__labels::text').get()
            value = row.css('.ux-labels-values__values::text').get()
            if key and value:
                specs[key.strip()] = value.strip()
        
        if specs:
            item['specifications'] = specs
        
        yield item