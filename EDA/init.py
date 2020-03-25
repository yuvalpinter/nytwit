"""
@title Exploratory Data Analysis for NYTWIT_v1 data
@author Dan Murphy
@created Tuesday, March 10, 2020

The purpose of this python file is to explore the NYTWIT_v1 dataset, 
perform data preprocessing and EDA on it, and introduce important takeaways 
that other developers can build onto over time. My goal is to build a 
foundational program that I (and others) can continue to add to over time.
"""
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle
import re
import nltk
from datetime import datetime as d
import time
import seaborn as sns
import numpy as np
# important note: tsv stands for tab separated values. Therefore, we can load this as a csv in pandas with sep="\t"
data = pd.read_csv("/Users/danielmurphy/Desktop/nytwit/nytwit_v1.tsv", sep= "\t", header=0)
df= pd.DataFrame(data)

def viewCols(data):
    """
    loop through columns in dataframe, view the first 5 rows
    @params data, a dataframe
    @returns the first 5 rows in the dataframe for each column
    """
    for col in data:
         print((data[[col]].head(5)))
# viewCols(df)
"""
1. Histogram of the different values in df[[Category]]

"""

def retrieveUniqueVals(data):
    """
    Find the unique values in df[["Category"]] and append them to an array, uniqueArr
    @params data, a subcolumn of a dataframe (followed by .iterrows()). I.E. data[['subcolumn']].iterrows()
    @returns list of unique values for the given column
    """
    uniqueList = []
    for val in data:
        if val[-1][0] not in uniqueList:
            uniqueList.append(val[-1][0])
    return uniqueList
# retrieveUniqueVals(df[['Category ']].iterrows())

def countVals():
    """
    Find the frequency of each unique value in the defined category
    @params none
    @returns the relative sum for each value in a column. Below, this function is pre-programmed to perform the actions to the "Category " column (Notice the space after Category).
     Can also be changed to df[["Time"]] for the given dataframe.
    """
    categoryCumulativeSum = [] # cumulative sum of count
    categoryRelativeSum = [] # relative sum of count
    count = 0
    i=0
    for c in retrieveUniqueVals(df[["Category "]].iterrows()):
        for v in df[["Category "]].iterrows():
            if v[-1][0] == c:
                count += 1
        categoryCumulativeSum.append(count)
        if i == 0:
            categoryRelativeSum.append(categoryCumulativeSum[0])
            i+= 1
        else:
            categoryRelativeSum.append(categoryCumulativeSum[i] - categoryCumulativeSum[i-1])
            i+=1
    return categoryRelativeSum
# print(countVals())

def mapVals(list1, list2):
    """
    zip two lists of equal length together
    @params two lists, list1 and list2, which should be equal sizes
    @returns a dictionary of two lists mapped together with each value at the same index in list1 and list2 being mapped to each other. 
    """
    try:
        return dict(zip(list1,list2))
    except IndexError:
        print("IndexError exception... lists should be same size!")
# mapVals(retrieveUniqueVals(df[["Category "]].iterrows()), countVals())
    
def hist():
    """
    Create a histogram for the categories of new words used in NYT articles. 
    For this scenario we can use plt.bar() with height equal to the frequency of each word,
    it'll work the same!
    @params none
    @returns a histogram (bar chart of the frequencies for each value in the Category column)
    """
    plt.bar(mapVals(retrieveUniqueVals(df[["Category "]].iterrows()), countVals()).keys(), mapVals(retrieveUniqueVals(df[["Category "]].iterrows()), countVals()).values(), color='g')
    plt.xticks(rotation=45)
    plt.show()
# hist()

"""
2. Lets do something similar with the URL column now.... 
"""
# for url in link_df.iterrows(): # loop through urls, determine if there are http and https
#     print(url[-1][0])
    # print(url[-1][0][:5])

def classifyLinksCounts(data):
    """
    A function that returns the total count of https, http, and other ('not found') links
    @params a dataframe, data, which is used to iterate through and determine which links are http and https. Can be applied to columns containing urls
    @returns the total sum of http, https, and other links
    """
    http_count = 0
    https_count = 0
    other = 0
    for url in data.iterrows():
        if url[-1][0][:5] == 'http:':
            http_count += 1
        elif url[-1][0][:5] == 'https':
            https_count += 1
        else:
            other += 1
    # print(http_count)
    # print(https_count)
    # print(other)
    print(http_count + https_count + other)
# classifyLinksCounts(df[["URL"]])

link_df = df[["URL", "Word"]]
https_links = []
http_links = []
repeated_links = []
other_link = []
def classifyLinks(data):
    """
    a function that splits links into https and http lists. Additionally,
    this function creates a list for urls that appear more than once in the dataframe
    @params a dataframe, data, which we iterate through and classify the urls within into http, https, other, and repeated lists. 
    @returns the sum of the lengths of the lists we are storing the links in (http, https, repeated, and other)
    """
    for url in data.iterrows():
        if url[-1][0][:5] == 'https':
            if (url[-1][0] in https_links) & (url[-1][0] not in repeated_links):
                repeated_links.append(url[-1][0])
            else:
                https_links.append(url[-1][0])
        elif url[-1][0][:5] == "http:":
            if (url[-1][0] in http_links) & (url[-1][0] not in repeated_links):
                repeated_links.append(url[-1][0])
            else:
                http_links.append(url[-1][0])
        else:
            other_link.append(url[-1][0])
    # print(len(https_links)) # 1821 sites with SSL certificates
    # print(len(http_links)) # 440 sites without SSL certificate
    # print(len(repeated_links)) # 321 links contain multiple new words
    # print(len(other_link)) # 5 unclassified links ("Not found" in the dataframe)
    print(len(repeated_links) + len(http_links) + len(https_links) + len(other_link))
# classifyLinks(link_df)

if classifyLinksCounts(df[['URL']]) == classifyLinks(link_df):
    print('true') # check if the number of rows is equal
def mplHist(dictionary):
    """
    A short function to create a mpl (matplotlib) histogram
    @params a dictionary, dictionary, that is used to label and determine the frequency of the labels
    @returns a plotted histogram
    """
    plt.bar(dictionary.keys(), dictionary.values())
    plt.title('Frequency of Link Types')
    plt.show()

mplHist(dictionary = {
        'https count': 1821, 
        'http count': 440,
        'repeated link count': 321,
        'other count': 5 
        })

"""
3. Other EDA
"""
df.rename(columns = {"Time":"Date"}, inplace=True)
def uniqueDates(col):
    """
    A function that returns the unique dates that new words were added to the data
    @params a column, col, that is used to create a sub-dataframe that we can then iterate through
    @returns list of unique dates
    """
    uniqueDates = []
    for date in df[[col]].iterrows():
        if date[-1][0][0:10] not in uniqueDates:
            uniqueDates.append(date[-1][0][0:10])
    return uniqueDates
# print(uniqueDates("Date"))


"""
4. Lets focus on the word column
"""

sub_df = df[["Word"]]
def determineInAlphabet(data):
    """
    This function will determine if the first character within a word are in the alphabet
    or, for example, they are emojis or non-alphabetical characters like ?,=, ., etc.
    @params a dataframe, data, that we iterate through
    @returns lists, alphabet and non_alphabet, that contains the corresponding words that start with alphabetical and non-alphabetical characters. 
    """
    non_alphabet = []
    alphabet = []
    for w in data.iterrows():
        if str(w[-1][0][0]).isalpha():
            alphabet.append(w[-1][0])
        else:
            non_alphabet.append(w[-1][0])
    print(non_alphabet)
    print(alphabet)
# determineInAlphabet(sub_df)

