# Scrapy Amazon Project

A web scraping project built with **Scrapy** that searches Amazon for a keyword (by default `ipad`), follows every product from the search results, and exports the product details to JSON.

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Output](#output)
- [Notes and Limitations](#notes-and-limitations)

## Features

- Searches Amazon for one or more keywords
- Crawls all result pages (pagination is discovered automatically)
- Visits each product page and extracts its details
- Cleans and converts numeric fields in an item pipeline
- Exports the results to a timestamped JSON file in `data/`
- Routes requests through the [ScrapeOps](https://scrapeops.io) proxy to reduce blocking

## How It Works

1. `start_requests` builds the search URL for each keyword in `keyword_list`.
2. `discover_product_urls` extracts the product links from each results page. On page 1 it also reads the pagination and queues all remaining pages.
3. `parse_product_data` opens each product page and fills an `AmazonProduct` item.
4. `AmazonScrapingPipeline` converts the price, star rating, and rating count to numbers.
5. Scrapy's feed export writes the items to `data/amazon_search_product_<time>.json`.

## Project Structure

```
.
└── amazon_scraping/
    ├── scrapy.cfg
    ├── data/                              # Exported JSON files
    └── amazon_scraping/
        ├── items.py                       # AmazonProduct item definition
        ├── middlewares.py
        ├── pipelines.py                   # Data cleaning pipeline
        ├── settings.py                    # Scrapy and proxy settings
        └── spiders/
            └── amazon_search_product.py   # The spider
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sarahmoussaoui/Scrapy-Amazon-Project.git
   cd Scrapy-Amazon-Project/amazon_scraping
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install scrapy scrapeops-scrapy-proxy-sdk
   ```

## Configuration

The project uses the ScrapeOps proxy. Create a free account at [scrapeops.io](https://scrapeops.io), get your API key, and set it in `amazon_scraping/settings.py`:

```python
SCRAPEOPS_API_KEY = 'YOUR_API_KEY'
SCRAPEOPS_PROXY_ENABLED = True
```

To search for other products, edit the list in `spiders/amazon_search_product.py`:

```python
keyword_list = ['ipad']   # e.g. ['ipad', 'laptop']
```

## Usage

From the `amazon_scraping/` folder (the one containing `scrapy.cfg`), run:

```bash
scrapy crawl amazon_search_product
```

The results are saved automatically to the `data/` folder.

## Output

Each product is saved with these fields:

| Field | Description |
|-------|-------------|
| `name` | Product title |
| `relative_url` | Product page URL |
| `price` | Price (float) |
| `stars` | Average rating (float) |
| `rating_count` | Number of ratings (float) |
| `feature_bullets` | List of feature bullet points |

Example:

```json
{
  "name": "Apple iPad (9th Generation): with A13 Bionic chip, 10.2-inch Retina Display, 64GB, ...",
  "relative_url": "https://www.amazon.com/...",
  "price": 249.0,
  "stars": 4.6,
  "rating_count": 62341.0,
  "feature_bullets": ["..."]
}
```

## Notes and Limitations

- The spider relies on Amazon's current HTML structure and CSS selectors. If Amazon changes its pages, the selectors will need updating.
- Some products have no price on the page, which makes the pipeline's float conversion fail for those items. Handling missing values would make the pipeline more robust.
- Amazon actively blocks scrapers, so results may vary even with a proxy.
- `ROBOTSTXT_OBEY` is set to `False`. Check Amazon's terms of service before scraping and keep the request rate reasonable.
- For learning purposes only.
