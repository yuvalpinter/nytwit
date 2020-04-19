import pandas as pd 
from bs4 import BeautifulSoup
import requests


raw_df = pd.DataFrame(pd.read_csv("../nytwit_v1.tsv", "\t"))
col_names = raw_df.columns


"""
1. First, access the url column
"""

url_list = [url for url in raw_df['URL'].values]
test_url = url_list[5]
web_page = requests.get(test_url)

soup = BeautifulSoup(web_page.content, 'html.parser')
print("Each url appears ~ " + str(len(url_list)/len(set(url_list))) + " times.")

filtered_soup = soup.find('h1', {
    "itemprop": "headline"
})
print(filtered_soup)
article_titles = []
def get_headline():
    for url in url_list:
        try:
            web_page = requests.get(url)
            soup = BeautifulSoup(web_page.content, 'html.parser')
            filtered_soup = soup.find(
                'h1',
                {
                    "itemprop": "headline"
                }
            )
            article_titles.append(filtered_soup)
        except:
            continue
    return article_titles

