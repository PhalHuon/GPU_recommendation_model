## GPU Price Tracker
A web scraping project that collects and analyzes GPU prices from major online retailers.

### Overview
This project uses Scrapy to crawl popular e-commerce websites (Amazon, eBay, and Walmart) to extract current GPU prices and specifications. The data can be stored in a MongoDB database or exported directly to CSV files for analysis, helping users find the best deals on graphics cards and track price trends over time.

* Automated scraping of GPU listings from multiple retailers
* Extraction of key information (price, model, manufacturer, specs)
* Data cleaning
* Normalization pipelines
* Export to both MongoDB and CSV formats

### Requirements
* Python 3.8+
* Scrapy
* pymongo (MongoDB support)
* urllib.parse (url encoding)

### Installation
1. Clone repository:
`git clone [repo-url]`
`cd gpu_price_tracker`
