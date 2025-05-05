# GPU Price Tracker
A web scraping project that collects and analyzes GPU prices from major online retailers.

## Overview
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

2. Create vitual environment:

`python -m venv venv` (windows)

`source venv/bin/activate` (macOS/Linux)

3. Install dependencies:

`pip install -r requirements.txt`

4. MongoDB setup (in the future):

## Usage
### Running the Spiders with MongoDB 

`python run_spiders.py` (run and store data in MongoDB)

### Run Spiders with CSV Export

`python direct_spider_csv.py` (export data to a csv)

### View data

`python view_data.py`

### Modifying Target GPUs
Edit `gpus.py` file to add or remove GPU models to track:

`GPU_MODELS = [
    {"brand": "NVIDIA", "model": "RTX 4090"},
    {"brand": "NVIDIA", "model": "RTX 4080"},
    # Add more models here
]`

## Customization
### Adding New Retailers
1. Create new spider in the `spiders` directory
2. Implement required parsing logic for new website
3. Add the spider to the `run_spiders.py`

### Configuring Crawl Settings
Edit `settings.py` file to adjust:

* crawl speed (DOWNLOAD_DELAY)
* concurrent requests
* user agents
* MongoDB connection settings

## License

MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgements
* [Scrapy](https://scrapy.org/) - The powerful web crawling framework that powers this project
* [MongoDB](https://www.mongodb.com/) - The database used for storing and managing GPU price data
* [Python Community](https://www.python.org/community/) - For the incredible open-source tools that make this project possible
* All GPU prices and data belong to their respective retailers (Amazon, eBay, Walmart)





