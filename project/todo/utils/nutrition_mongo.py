#!/usr/bin/env python
# coding: utf-8


from pymongo import MongoClient
import pandas as pd


client = MongoClient("mongodb://localhost:27017/")
db = client["TTDS"]
collection = db["nutrition"]


df = pd.read_csv('nutrition.csv')



new_df = df.drop_duplicates()


mongo_df = new_df.drop_duplicates(subset='food_name', keep="last")



nutrition = []
for i in mongo_df.index:
    d = {}
    d["food_name"] = mongo_df["food_name"][i]
    d["nf_calories"] = mongo_df["nf_calories"][i]
    d["nf_protein"] = mongo_df["nf_protein"][i]
    d["nf_total_fat"] = mongo_df["nf_total_fat"][i]
    nutrition.append(d)


collection.insert_many(nutrition)




