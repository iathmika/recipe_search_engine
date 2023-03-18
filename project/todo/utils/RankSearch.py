from .InvertedIndex import preProcessing
## Module to store retreive document ids in sorted set
from sortedcontainers import SortedSet
import math
import itertools

#index_dict = {}
# ****START: Some basic utils for avoiding code replication **** #

# Method to return term frequency in a particular document
# Return -1 if term does not exist in given doc
def getTermFreqInDoc(term, docId, index_dict):
    if term in index_dict:
        pair_val = index_dict[term]
        # print(pair_val.details)
        # print("Freq: ", pair_val.doc_freq)
        if docId in pair_val.details:
            # print("doc_id : "+ str(docId) +  " " + str(len(pair_val.details[docId])))
            return len(pair_val.details[docId])

    return -1

#def getTermFreqInDoc(term, docId):
#    if term in index_dict:
#        if docId in index_dict[term]:
#            return len(index_dict[term][docId])
#
#    return -1 
   
# Method to return list of all document ids in the collection
def fetchAllDocIds(index_dict):
    rsl = SortedSet()
    if len(index_dict) > 0:
        for k,vpair in index_dict.items():
            for did in vpair.details.keys():
                rsl.add(int(did))
    return rsl

#def fetchAllDocIds():
#    rsl = SortedSet()
#    if len(index_dict) > 0:
#        for k,v in index_dict.items():
#            for did in v.keys():
#                rsl.add(int(did))
#    return rsl

# Method to return list of document ids where a specific term is present
# If negation = false -> Return (Set of document ids where term is present)
# If negation = true  -> Return ((Set of all document ids) - (Set of document ids where term is present))
def fetchDocIds(term, is_negation, index_dict):
    rsl = SortedSet()
    if term in index_dict:
        vpair = index_dict[term]
        # print("Size vpair: ", len(vpair.details))
        for d in vpair.details.keys():
            rsl.add(int(d))

    if is_negation == True:
       all_ids = fetchAllDocIds(index_dict)
       if len(all_ids) > 0 and len(rsl) > 0:
           rsl = all_ids.difference(rsl)

    return rsl

# ****END: Some basic utils for avoiding code replication **** #

## Method for computing the TFIDF and BM25 score for a query with respect to a document id
## Results are sorted in descending order of the score
def processRankedQuery(query, indexObj, search_type):
  index_dict = indexObj.getIndexDict()
  ## Required for bm25 
  if (type == 0): 
    doc_len_dict = indexObj.getDocLenDict()
    docs_cnt = indexObj.getDocLenSize()

  print ("Length of dictionary ", len(index_dict))
  terms_list = preProcessing(query)
  print(terms_list)
  tmp = set()
  rsl = {}
  if (len(terms_list) > 0):
      for term in terms_list:
          tmp = fetchDocIds(term, False, index_dict)
          dft = len(tmp)
          if dft > 0:
              for doc_id in tmp:
                  tfd = getTermFreqInDoc(term, doc_id, index_dict)
                  if (search_type == 1):
                    ## Compute TFIDF score
                    new_score = (1 + math.log10(tfd)) * math.log10(5000/dft)
                  else:
                    ## Compute score for BM25
                    if str(doc_id) in doc_len_dict.keys():
                      new_score  = score_BM25(docs_cnt , dft, tfd, 1.5, doc_len_dict[str(doc_id)], 48)
                  cur_score = 0
                  if doc_id in rsl:
                      cur_score = rsl[doc_id]
                  rsl[doc_id] = cur_score + new_score
  if len(rsl) > 0:
    sorted_dict = dict(sorted(rsl.items(), key=lambda item: item[1]))
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
  
