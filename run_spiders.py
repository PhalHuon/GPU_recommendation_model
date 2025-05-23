# run_spiders.py

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from gpu_price_tracker.spiders.amazon_spider import AmazonSpider
# from gpu_price_tracker.spiders.ebay_spider import EbaySpider
# from gpu_price_tracker.spiders.walmart_spider import WalmartSpider

def main():
    # Get settings
    settings = get_project_settings()
    
    # Set your MySQL connection string if you want to override the default
    # settings.set('MYSQL_CONNECTION_STRING', "mysql+pymysql://user:password@localhost/gpu_tracker")
    
    # Create process
    process = CrawlerProcess(settings)
    
    # Add spiders to process
    process.crawl(AmazonSpider)
    # process.crawl(EbaySpider)
    # process.crawl(WalmartSpider)
    
    # Start crawling
    print("Starting GPU price crawling...")
    process.start()
    print("Crawling completed!")

if __name__ == "__main__":
    main()