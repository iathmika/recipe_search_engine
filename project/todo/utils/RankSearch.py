from .InvertedIndex import preProcessing
## Module to store retreive document ids in sorted set
from sortedcontainers import SortedSet
import math
import itertools
import time

## Method for computing the TFIDF and BM25 score for a query with respect to a document id
## Results are sorted in descending order of the score
def processRankedQuery(query, indexObj, search_type):
  print ("Getting a call inside in processRankedQuery")
  index_dict = indexObj.getIndexDict()
  doc_len_dict = indexObj.getDocLenDict()

  new_score = 0
  docs_cnt = indexObj.getDocLenSize()
  ## Required for bm25 
  if (search_type == 0):
    doc_len_dict = indexObj.getDocLenDict()

  print ("Length of dictionary ", len(index_dict))
  #start = time.time()
  terms_list = preProcessing(query)
  #print("Preprocessing runtime: ", time.time() - start)
#   print(terms_list)
  rsl = {}
  if (len(terms_list) > 0):
      for term in terms_list:
        #  start = time.time()
        #   print ("In the main : ", id(index_dict))
          if (term not in index_dict): continue
          dft = index_dict[term].doc_freq
        # print ("Document count : ", dft)
          if dft > 0:
              #start = time.time()
              for doc_id in index_dict[term].details:
                  tfd = len(index_dict[term].details[doc_id])
                  if (search_type == 1):
                    ## Compute TFIDF score
                    new_score = (1 + math.log10(tfd)) * math.log10(docs_cnt/dft)
                  else:
                    ## Compute score for BM25
                    new_score  = score_BM25(docs_cnt , dft, tfd, 1.5, doc_len_dict[doc_id], 48)
                  cur_score = 0
                  if doc_id in rsl:
                      cur_score = rsl[doc_id]
                  rsl[doc_id] = cur_score + new_score
          #print (f"Iterating sub loop , Term {term} : time : {time.time() - start}")
  if len(rsl) > 0:
    #start = time.time() 
    sorted_dict = dict(sorted(rsl.items(), key=lambda item: item[1], reverse= True))
    #print (f"Sorting time : {time.time() - start}")
    return sorted_dict

def score_BM25(doc_nums, doc_nums_term, term_freq, k1, dl, avgdl):
    K = compute_K(k1, dl, avgdl)
    idf_param = math.log( (doc_nums-doc_nums_term+0.5) / (doc_nums_term+0.5) )
    next_param = (term_freq) / (K + term_freq + 0.5)
    return float("{0:.4f}".format(next_param * idf_param))

def compute_K(k1, dl, avgdl):
    return k1 * dl / avgdl

def rankByTFIDF(query, indexObj):
    return processRankedQuery(query, indexObj, 1)

def rankByBM25(query, indexObj):
    return processRankedQuery(query, indexObj, 0)
  
