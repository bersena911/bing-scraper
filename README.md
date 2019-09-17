# bing-scraper
Just Scrape It

## Instructions

### Install Requirements
- ```cd collector```
- ```virtualenv venv --python=python```
- ```source venv/bin/activate```
- ```pip install -r requirements.txt```
- ```cd ..```

# Bing Parser

```scrapy crawl bing -a target=instagram.com -a length=2 -t jsonlines -o filename.out```

#### Last argument must be an output filename
