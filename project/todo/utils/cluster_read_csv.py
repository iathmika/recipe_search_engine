#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd
from pymongo import MongoClient


# In[23]:


cluster_df = pd.read_csv('cluster.csv')


# In[ ]:


client = MongoClient("mongodb://localhost:27017/")
db = client["TTDS"]
collection = db["cluster"]
collection1 = db["recipe"]


# In[24]:


rows = []
for data in cluster_df.groupby('cluster_id'):
    d = {}
    cluster_id = (int) (data[1]["cluster_id"].unique()[0])
    doc_ids = data[1]["doc_id"].to_numpy(dtype = "int64")
    d["cluster_id"] = cluster_id
    d["doc_id"] = doc_ids.tolist()
    rows.append(d)


# In[ ]:


collection.insert_many(rows)


# In[12]:


l = list(df['cluster_id'].to_numpy(dtype = 'int64'))


# In[11]:


collection1.update_many(
  {},
  { "$set": {"cluster_id": -1} },
)


# In[ ]:


counter = 1
for i in l:
    
    cluster_id = int(i)
    collection1.update_one(
    {"id": counter},
      { "$set": {"cluster_id": cluster_id} },
    )
    counter += 1

