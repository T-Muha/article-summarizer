from transformers import pipeline
import csv
import requests
from bs4 import BeautifulSoup

csv_file = 'refract_data_engineering_articles.csv'

# read the articles from the csv file and put them in the list
articles = []
with open(csv_file, 'r') as csv_in:
    csv_reader = csv.reader(csv_in, delimiter=',')
    for row_num, row_content in enumerate(csv_reader):
        if row_num != 0:
            articles.append(row_content)

# run the articles through the model and get the summaries
print('Summarizing the assignment articles...')
summaries = []
summarizer = pipeline('summarization', model='t5-small', tokenizer='t5-small')
for article in articles:
    summaries.append(summarizer(article, max_length=20, min_length=0, do_sample=False, clean_up_tokenization_spaces=True))
    print('...')

# store the summaries in the csv file
with open(csv_file, 'w') as csv_out:
    csv_writer = csv.writer(csv_out, lineterminator='\n')
    new_content = [['source_content', 'ml_summary']]
    for i, summary in enumerate(summaries):
        new_content.append([articles[i][0], summary[0]['summary_text']])
    csv_writer.writerows(new_content)

print('Scraping TechCrunch for articles and generating summaries...')

# scrape TechCrunch for front-page article links
max_articles = 6
tech_crunch = requests.get('https://techcrunch.com/')
soup = BeautifulSoup(tech_crunch.content, 'html5lib')
article_links = soup.find_all('a', class_='post-block__title__link')

# assemble the content for the csv file
csv_content = [['TechCrunch Summaries']]
for link in article_links[0:max_articles]:
    # get the text content from each article link
    article = requests.get(link['href'])
    article_page = BeautifulSoup(article.content, 'html5lib')
    paragraphs = article_page.find_all('p')
    article_text = ''.join(map((lambda x: x.get_text()), paragraphs))

    # generate the summary and add it to the csv contents
    summary = summarizer(article_text, max_length=100, min_length=20, do_sample=False, clean_up_tokenization_spaces=True)
    print('...')
    csv_content.append([summary[0]['summary_text']])

with open('TechCrunch_Summaries.csv', 'w') as csv_out:
    csv_writer = csv.writer(csv_out, lineterminator='\n')
    csv_writer.writerows(csv_content)

print('Done')