# GPU Price Tracker
A web scraping project that collects and analyzes GPU prices from major online retailers using MySQL for data storage. In the future, the database will be used to implement a recommendation machine learning model that suggests optimal GPUs based on user preferences, budget constraints, and performance benchmarks.

## Overview
This project uses Scrapy to crawl popular e-commerce websites (Amazon, eBay, and Walmart) to extract current GPU prices and specifications. The data is stored in a MySQL database for analysis, helping users find the best deals on graphics cards and track price trends over time.

### Features

* Automated scraping of GPU listings from multiple retailers
* Extraction of key information such as price, model, manufacturer, and specifications
* Data cleaning and normalization pipeline
* MySQL database for structured data storage
* Support for tracking specific GPU models via configuration

### Requirements

* Python 3.8+
* Scrapy
* SQLAlchemy
* PyMySQL
* MySQL Server
* pandas

### Installation

1. Clone the repository:

`git clone [repository-url]`

`cd gpu_price_tracker`

2. Create and activate a virtual environment:

`python -m venv venv` 

`venv\Scripts\activate` (Windows)

`source venv/bin/activate` (Linux/macOS)

3. Install dependencies:
   
`pip install -r requirements.txt`

4. Set up MySQL database:

* Install MySQL Server if not already installed
* Create the database and tables by running:
  
`python init_database.py`


## Usage
### Initialize the Database

`python init_database.py`

### Run the Spiders

`python run_spiders.py`

This will start the crawling process for all configured retailers.

### View the Data

`python view_data.py`

This script displays statistics about the collected GPU data and offers the option to export it to CSV.

## Customization
### Database Configuration
Edit the MySQL connection string in `settings.py`:

`MYSQL_CONNECTION_STRING = "mysql+pymysql://user:password@localhost/gpu_tracker"`

### Adding New Retailers

1. Create a new spider in the spiders directory
2. Implement the required parsing logic for the new website
3. Add the spider to the run_spiders.py script

### Modifying Target GPUs
Edit the `gpus.py` file to add or remove GPU models to track.

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

## Acknowledgments
* Scrapy team for the powerful web crawling framework
* SQLAlchemy for the database ORM
* The Python community for the excellent data analysis tools




