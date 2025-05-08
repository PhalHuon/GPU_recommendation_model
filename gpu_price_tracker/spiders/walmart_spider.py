
import scrapy
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from items import GPUItem
from gpus import GPU_MODELS
import json
import re

class WalmartSpider(scrapy.Spider):
    name = "walmart"
    allowed_domains = ["walmart.com"]
    
    def start_requests(self):
        for gpu in GPU_MODELS:
            search_query = f"{gpu['brand']} {gpu['model']}"
            # URL encode the search query
            encoded_query = search_query.replace(' ', '+')
            url = f"https://www.walmart.com/search?q={encoded_query}&cat_id=3944_3951_1231879"
            yield scrapy.Request(
                url=url,
                callback=self.parse_search_results,
                meta={'gpu': gpu}
            )
    
    def parse_search_results(self, response):
        gpu = response.meta['gpu']
        
        # Extract product cards from search results
        products = response.css('div[data-item-id]')
        
        for product in products:
            # Check if product title contains both brand and model
            title = product.css('span.lh-title::text').get()
            if not title:
                continue
                
            title_lower = title.lower()
            if gpu['brand'].lower() in title_lower and gpu['model'].lower() in title_lower:
                # Extract product URL and follow it
                product_url = product.css('a::attr(href)').get()
                if product_url:
                    full_url = response.urljoin(product_url)
                    yield scrapy.Request(
                        url=full_url,
                        callback=self.parse_product_page,
                        meta={'gpu': gpu, 'title': title}
                    )
        
        # Check for next page and follow it
        next_page = response.css('a[aria-label="Next Page"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_search_results,
                meta={'gpu': gpu}
            )
    
    def parse_product_page(self, response):
        gpu = response.meta['gpu']
        title = response.meta['title']
        
        # Create GPU item
        item = GPUItem()
        
        # Basic information
        item['brand'] = gpu['brand']
        item['model'] = gpu['model']
        item['name'] = title
        
        # Try to find JSON data in script tags
        script_data = response.css('script#__NEXT_DATA__::text').get()
        if script_data:
            try:
                data = json.loads(script_data)
                product_data = data.get('props', {}).get('pageProps', {}).get('initialData', {}).get('data', {}).get('product', {})
                
                # Extract price
                price_block = product_data.get('priceInfo', {})
                if price_block:
                    current_price = price_block.get('currentPrice', {}).get('price')
                    if current_price:
                        item['price'] = float(current_price)
                        item['currency'] = price_block.get('currentPrice', {}).get('currencyUnit', 'USD')
                    
                    was_price = price_block.get('wasPrice', {}).get('price')
                    if was_price:
                        item['original_price'] = float(was_price)
                
                # Extract manufacturer
                manufacturer = product_data.get('manufacturerName')
                if manufacturer:
                    item['manufacturer'] = manufacturer
                
                # Extract specifications
                specs = {}
                specifications = product_data.get('detailedSpecs', [])
                for spec in specifications:
                    key = spec.get('name')
                    value = spec.get('value')
                    if key and value:
                        specs[key] = value
                
                if specs:
                    item['specifications'] = specs
                
                # Extract availability
                if 'availabilityStatus' in product_data:
                    item['availability'] = product_data['availabilityStatus']
                
                # Extract ratings
                rating = product_data.get('averageRating')
                if rating:
                    item['rating'] = float(rating)
                
                review_count = product_data.get('numberOfReviews')
                if review_count:
                    item['num_reviews'] = int(review_count)
                
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.error(f"Error parsing JSON data: {e}")
        
        # If JSON parsing failed, try CSS selectors
        if 'price' not in item:
            price_str = response.css('.price-characteristic::text').get()
            price_fraction = response.css('.price-mantissa::text').get()
            if price_str:
                try:
                    price = float(price_str)
                    if price_fraction:
                        price = price + float(price_fraction) / 100
                    item['price'] = price
                    item['currency'] = 'USD'
                except ValueError:
                    pass
        
        # Retailer information
        item['retailer'] = 'Walmart'
        item['url'] = response.url
        
        # Shipping information
        shipping = response.css('.fulfillment-shipping-text::text').get()
        if shipping:
            item['shipping_cost'] = shipping.strip()
        
        yield item