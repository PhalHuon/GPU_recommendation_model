import pymongo
from datetime import datetime

class MongoPipeline:
    collection_name = 'gpu_prices'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', 'mongodb://localhost:27017/'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'gpu_tracker')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Add timestamp if not present
        if 'timestamp' not in item:
            item['timestamp'] = datetime.now().isoformat()
            
        # Insert the item into the MongoDB collection
        self.db[self.collection_name].insert_one(dict(item))
        return item

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
        
        return item