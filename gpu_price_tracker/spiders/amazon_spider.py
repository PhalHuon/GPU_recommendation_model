import os
import sys
#when import modules, also look at the parent directory of this file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import scrapy
from items import GPUItem
from gpus import GPU_MODELS
import re

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    
    def start_requests(self):
        for gpu in GPU_MODELS:
            search_query = f"{gpu['brand']} {gpu['model']}"
            # URL encode the search query
            encoded_query = search_query.replace(' ', '+')
            url = f"https://www.amazon.com/s?k={encoded_query}&i=electronics"
            yield scrapy.Request(
                url=url,
                callback=self.parse_search_results,
                meta={'gpu': gpu}
            )
    
    def parse_search_results(self, response):
        gpu = response.meta['gpu']
        
        # Extract product cards from search results
        products = response.css('div[data-component-type="s-search-result"]')
        
        for product in products:
            # Check if product title contains both brand and model
            title = product.css('h2 a span.a-text-normal::text').get()
            if not title:
                continue
                
            title_lower = title.lower()
            if gpu['brand'].lower() in title_lower and gpu['model'].lower() in title_lower:
                # Extract product URL and follow it
                product_url = product.css('h2 a::attr(href)').get()
                if product_url:
                    full_url = response.urljoin(product_url)
                    yield scrapy.Request(
                        url=full_url,
                        callback=self.parse_product_page,
                        meta={'gpu': gpu, 'title': title}
                    )
        
        # Check for next page and follow it
        next_page = response.css('a.s-pagination-next::attr(href)').get()
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
        
        # Try to extract manufacturer
        manufacturer = response.css('#bylineInfo::text').get()
        if manufacturer:
            item['manufacturer'] = manufacturer.strip().replace('Visit the ', '').replace(' Store', '')
        
        # Price information
        price_str = response.css('.a-price .a-offscreen::text').get()
        if price_str:
            # Remove currency symbol and convert to float
            try:
                item['price'] = float(re.sub(r'[^\d.]', '', price_str))
                item['currency'] = 'USD'  # Assuming USD, adjust as needed
            except:
                self.logger.warning(f"Could not parse price: {price_str}")
        
        # Original price if discounted
        original_price_str = response.css('.a-text-price .a-offscreen::text').get()
        if original_price_str:
            try:
                item['original_price'] = float(re.sub(r'[^\d.]', '', original_price_str))
            except:
                pass
        
        # Retailer information
        item['retailer'] = 'Amazon'
        item['url'] = response.url
        
        # Availability
        availability = response.css('#availability span::text').get()
        if availability:
            item['availability'] = availability.strip()
        
        # Shipping cost
        shipping = response.css('#deliveryBlockMessage::text').get()
        if shipping:
            item['shipping_cost'] = shipping.strip()
        
        # Rating
        rating_str = response.css('.a-icon-star-small .a-icon-alt::text').get()
        if rating_str and 'out of' in rating_str:
            try:
                item['rating'] = float(rating_str.split('out of')[0].strip())
            except (ValueError, IndexError):
                pass
        
        # Number of reviews
        reviews_str = response.css('#acrCustomerReviewText::text').get()
        if reviews_str and 'ratings' in reviews_str:
            try:
                item['num_reviews'] = int(re.sub(r'[^\d]', '', reviews_str))
            except ValueError:
                pass
        
        # Specifications
        specs = {}
        tech_details = response.css('#productDetails_techSpec_section_1 tr')
        for detail in tech_details:
            key = detail.css('th::text').get()
            value = detail.css('td::text').get()
            if key and value:
                specs[key.strip()] = value.strip()
        
        if specs:
            item['specifications'] = specs
        
        yield item
