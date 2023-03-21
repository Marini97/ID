import recordlinkage as rl
from recordlinkage.preprocessing import clean
import os
import pandas as pd
from dataprep.clean import clean_country
from dataprep.clean import clean_text
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# name,code,website,headquarter,country,ceo,founded,employees,market_value,market_cap,annual_revenue,business
# load the training set from a csv file
vals1_path = os.path.join('', 'training.csv')
vals1 = pd.read_csv(vals1_path, encoding = "ISO-8859-1")
df = pd.DataFrame(vals1)

# output_globaldata.csv name,,website,address,headquarters,,,number_of_employees,,market_cap,revenue,industry
# load dataset to append
d1_path = os.path.join('datasets', 'output_globaldata.csv', )
df1 = pd.read_csv(d1_path, encoding = "ISO-8859-1")
dfA = pd.DataFrame(df1)
# Ground truth 
ground_truth = [
    ("name", "name"),
    ("website", "website"),
    ("address", "headquarter"),
    ("headquarters", "country"),
    ("number_of_employees", "employees"),
    ("market_cap", "market_cap"),
    ("revenue", "annual_revenue"),
    ("industry", "business")
]
cols = ["name", "link", "website", "address", "headquarters", "number_of_employees", "market_cap", "revenue", "industry"]
d = dict(ground_truth)
print(dfA.head(10))
for col in dfA.columns:
    if col not in cols:
        dfA.drop(columns=[col], axis=1, inplace=True)
    
dfA =  dfA.rename(columns=d)

df_result = pd.concat([df, dfA])

print(df_result.tail(10))

df_result.to_csv('training.csv', index=False)