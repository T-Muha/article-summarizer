# article-summarizer
Summarizes news articles using a [prebuilt transformer model by huggingface](https://github.com/huggingface/transformers). article-summarizer.py summarizes the articles given in refract_data_engineering_articles.csv, then scrapes/summarizes front-page articles from Tech Crunch and puts them in TechCrunch_Summaries.csv

To run, you will need the following modules installed:
* transformers
* requests
* beautifulsoup4
* html5lib
