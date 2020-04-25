import pandas as pd 
import requests
import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup

raw_df = pd.DataFrame(pd.read_csv("nytwit_v1.tsv", "\t"))
col_names = raw_df.columns


"""
1. First, access the url column
""" 

url_list = [url for url in raw_df['URL'].values]
test_url = url_list[1]
html = urlopen(test_url).read()

soup = BeautifulSoup(html, 'html.parser')
textToParse = soup.getText()


clean_url_list = [url for url in url_list if url != 'not found']
list_of_sentences = []
list_of_indexes = []
for i, vals in enumerate(raw_df[['Word', 'URL']].values):
    if str(vals[-1]) != 'not found':    
        html = urlopen(str(vals[-1])).read()
        soup = BeautifulSoup(html, 'html.parser')
        textToParse = soup.getText()
        sentence_tokenize = nltk.sent_tokenize(textToParse)
        sentence_to_add = [sent for sent in sentence_tokenize if str(vals[0]) in sent]
        list_of_sentences.append(sentence_to_add)
        list_of_indexes.append(i)
        print(len(list_of_indexes), len(list_of_sentences))
    else:
        list_of_sentences.append("null")
        list_of_indexes.append(i)
        print(len(list_of_indexes), len(list_of_sentences))
        continue

def zip_lists(list1, list2):
    return zip(list1, list2)

dict_for_data = zip_lists(list_of_indexes, list_of_sentences)

print(dict_for_data[1])


# soup = BeautifulSoup(html.content, 'html.parser')
# print("Each url appears ~ " + str(len(url_list)/len(set(url_list))) + " times.")

# filtered_soup = soup.find('h1', {
#     "itemprop": "headline"
# })
# print(filtered_soup)


def get_headline():
    article_titles = []
    for url in url_list:
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.content, 'html.parser')
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

