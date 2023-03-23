#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from pymongo import MongoClient


df = pd.read_csv('project/todo/utils/full_dataset.csv')



recipes = df['NER'].to_numpy()[:18000]


import re
l = []
for recipe_inrs in recipes: 
    data = re.split("\"", recipe_inrs)
    d = {}
    for j in data[1:len(data) - 1]:
        if (j != ', '):
            d[j] = 1
    l.append(d)



#one hot encoding
from sklearn.feature_extraction import DictVectorizer
vector_dict = DictVectorizer(sparse = True)
X = vector_dict.fit_transform(l)


from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=100, random_state=0)
kmeans.fit(X)


kmeans.labels_.shape


from sklearn import metrics
labels = kmeans.labels_
silhouette_score = metrics.silhouette_score(X, labels, metric='euclidean')
print("Silhouette_score: ", silhouette_score)

l = kmeans.labels_


documents = np.arange(1,18001)



client = MongoClient("mongodb://localhost:27017/")
db = client["TTDS"]
collection = db["cluster"]
collection.drop()



cluster_df = pd.DataFrame(columns = ['doc_id', 'cluster_id'])


cluster_df['doc_id'] = documents
cluster_df['cluster_id'] = l


rows = []
for data in cluster_df.groupby('cluster_id'):
    d = {}
    cluster_id = (int) (data[1]["cluster_id"].unique()[0])
    doc_ids = data[1]["doc_id"].to_numpy(dtype = "int64")
    d["cluster_id"] = cluster_id
    d["doc_id"] = doc_ids.tolist()
    rows.append(d)



collection.insert_many(rows)


collection.find({"cluster_id" : 4})


for i in collection.find({"cluster_id" : 1}):
    print(i)


collection1 = db["recipe"]


collection1.update_many(
  {},
  { "$set": {"cluster_id": -1} },
)


counter = 1
for i in l:
    
    cluster_id = int(i)
    collection1.update_one(
    {"id": counter},
      { "$set": {"cluster_id": cluster_id} },
    )
    counter += 1



