# -*- coding: utf-8 -*-


import pandas as pd


df = pd.read_csv("./lii3ra/symbol/stocks.csv")
japan_df = df[df["country"] == "japan"]
for row in japan_df.itertuples():
    print(row.symbol + ".T")

us_df = df[df["country"] == "united states"]
for row in us_df.itertuples():
    print(row.symbol)

hk_df = df[df["country"] == "hong kong"]
for row in hk_df.itertuples():
    print(row.symbol + ".HK")


