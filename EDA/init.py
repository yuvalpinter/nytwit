"""
@title Exploratory Data Analysis for NYTWIT_v1 data
@author Dan Murphy
@created Tuesday, March 10, 2020

The purpose of this python file is to explore the NYTWIT_v1 dataset, 
perform data preprocessing and EDA on it, and introduce important takeaways 
that other developers can build onto over time. My goal is to build a 
foundation program that I (and others) can continue to add to over time.
"""
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle
import re
import nltk
from datetime import datetime as d
import time
# important note: tsv stands for tab separated values. Therefore, we can load this as a csv in pandas with sep="\t"
data = pd.read_csv("/Users/danielmurphy/Desktop/nytwit/nytwit_v1.tsv", sep= "\t", header=0)
df= pd.DataFrame(data)
# print(df.head(5))

def viewCols(data):
    """
    loop through columns in dataset, view the first 5 rows
    """
    for val in data:
         print((data[[val]].head(5)))
# viewCols(df)



"""
1. Histogram of the different values in df[[Category]]

"""
def retrieveUniqueVals(data):
    """
    Find the unique values in df[["Category"]] and append them to an array, uiqueArr
    """
    uniqueArr = []
    for val in data:
        if val[-1][0] not in uniqueArr:
            uniqueArr.append(val[-1][0])
    return uniqueArr

def countVals(data):
    """
    Find the frequency of each unique value in df[["Category]]
    """
    categoryCumulativeSum = [] # cumulative sum of count
    categoryRelativeSum = [] # relative sum of count
    count = 0
    i=0
    for c in retrieveUniqueVals(data):
        for v in df[["Category"]].iterrows():
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

def mapVals(list1, list2):
    """
    zip two lists of equal length together
    """
    try:
        return dict(zip(list1,list2))
    except IndexError:
        print("IndexError exception... lists should be same size!")
    
def hist():
    """
    Create a histogram for the categories of new words used in NYT articles. 
    For this scenario we can use plt.bar() with height equal to the frequency of each word,
    it'll work the same!
    """
    plt.bar(mapVals(retrieveUniqueVals(df[["Category"]].iterrows()), countVals(df[["Category"]].iterrows())).keys(), mapVals(retrieveUniqueVals(df[["Category"]].iterrows()), countVals(df[["Category"]].iterrows())).values(), color='g')
    plt.xticks(rotation=45)
    plt.show()
# hist()


"""
2. Lets do something similar with the URL column now.... 
"""

# first, check to see if num of row entries < length of unique rows in df[["URL"]]
# If it is "<" then we know there are repeat URLs! 
print("Testing if count of unique values in df[[\"URL\"]] is less then the total number of rows")
print("************************************************************************************** \n")
print(len(retrieveUniqueVals(df[["URL"]].iterrows())) < len(df.index))


uniqueURLs = []
for url in retrieveUniqueVals(df[["URL"]].iterrows()):
    if url not in uniqueURLs:
        uniqueURLs.append(url)

# n = 0
# for w in df[["Word"]].iterrows():
#     print("testing " + w[-1][0] + " #" + str(n) + " \n")
#     n += 1
#     if w[-1][0] not in retrieveUniqueVals(df[["Word"]].iterrows()):
#         print(w[-1][0])
#         n += 1

"""
3. find and print words with duplicate characters repeated at least twice in a row
"""
# duplicateCharArr = []
# for w in (retrieveUniqueVals(df[["Word"]].iterrows())):
#     for char in str(w):
#         for i in range(len(w)):
            

"""
4. Other EDA
"""
df.rename(columns = {"Time":"Date"}, inplace=True)


def uniqueDates(col1):
    uniqueDates = []
    for date in df[[col1]].iterrows():
        if date[-1][0][0:10] not in uniqueDates:
            uniqueDates.append(date[-1][0][0:10])
    print(len(uniqueDates))
uniqueDates("Date")