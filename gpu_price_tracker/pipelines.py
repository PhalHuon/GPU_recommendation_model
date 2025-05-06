#when import modules, also look at the parent directory of this file
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gpu_price_tracker.database import Database
from datetime import datetime

class CleanDataPipeline:
    def process_item(self, item, spider):
        # Ensure price is a float
        if 'price' in item and item['price']:
            try:
                item['price'] = float(item['price'])
            except (ValueError, TypeError):
                item['price'] = None
        
        # Ensure original_price is a float if present
        if 'original_price' in item and item['original_price']:
            try:
                item['original_price'] = float(item['original_price'])
            except (ValueError, TypeError):
                item['original_price'] = None
        
        # Clean up model names
        if 'name' in item and item['name']:
            item['name'] = item['name'].strip()
        
        # Add timestamp if not present
        if 'timestamp' not in item:
            item['timestamp'] = datetime.now().isoformat()
        
        return item

class MySQLPipeline:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.db = None
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            connection_string=crawler.settings.get('MYSQL_CONNECTION_STRING')
        )
    
    def open_spider(self, spider):
        self.db = Database(self.connection_string)
        spider.logger.info("Connected to MySQL database")
    
    def close_spider(self, spider):
        spider.logger.info("Closed MySQL database connection")
    
    def process_item(self, item, spider):
        self.db.store_gpu(item)
        return item