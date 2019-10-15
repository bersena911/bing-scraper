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

```scrapy crawl bing -a target=instagram.com -a input_alphabet=abcdef -a length=2 -t jsonlines -o filename.out```

## Arguments

- ```target - Target webpage to collect information about```
- ```input_alphabet - Characters to permutate, for getting queries```
- ```length - Length of query```

#### Last argument must be an output filename
