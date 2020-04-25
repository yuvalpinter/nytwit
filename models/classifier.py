# -*- coding: utf-8 -*-
"""
Script file with the purpose of classifying
NYT novel words into their proper 

"""

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

raw_df = pd.read_csv('../nytwit_v1.tsv', '\t')

raw_df.head(10)


# check out some stats before building the model

category_counts = dict(pd.value_counts(raw_df.Category))

figure(figsize=(15, 10))
plt.plot(list(category_counts.keys()), list(category_counts.values()))
plt.xticks(rotation=70)


# setup data for building our model
categories = raw_df.Category
categories_ohe = pd.get_dummies(categories)

unique_categories = set(categories_ohe)
unique_cat_list = [c for c in unique_categories]
num_range = [n for n in np.arange(1, 20)]

unique_cat_dict = {unique_cat_list[i]:num_range[i] for i in range(0, len(num_range))}
# could also use zip for this  ^

y_vals = categories.values
y_nums = [unique_cat_dict.get(i) for i in y_vals]

y = y_nums
X = raw_df.Word.values






