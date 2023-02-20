from .InvertedIndex import preProcessing
## Module to store retreive document ids in sorted set
from sortedcontainers import SortedSet
import math

#index_dict = {}
# ****START: Some basic utils for avoiding code replication **** #

# Method to return term frequency in a particular document
# Return -1 if term does not exist in given doc
def getTermFreqInDoc(term, docId, index_dict):
    if term in index_dict:
        pair_val = index_dict[term]
        if docId in pair_val.details:
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
    print ("Getting call in fetchDocIds, dict length ", len(index_dict))
    rsl = SortedSet()
    if term in index_dict:
        print ("Term found in index_dict")
        vpair = index_dict[term]
        print (vpair.details)
        for d in vpair.details.keys():
            rsl.add(int(d))

    if is_negation == True:
       all_ids = fetchAllDocIds(index_dict)
       if len(all_ids) > 0 and len(rsl) > 0:
           rsl = all_ids.difference(rsl)

    return rsl

# ****END: Some basic utils for avoiding code replication **** #

## Method for computing the TFIDF score for a query with respect to a document id
## Results are written out in a file, sorted by score
#def processRankedQuery(query, fout):
def processRankedQuery(query, indexObj):
  index_dict = indexObj.getIndexDict()
  print ("Getting call in index_dict")
  print ("Length of dictionary ", len(index_dict))
  terms_list = preProcessing(query)
  print(terms_list)
  tmp = set()
  rsl = {}
  if (len(terms_list) > 0):
      for term in terms_list:
          tmp = fetchDocIds(term, False, index_dict)
          print(tmp)
          dft = len(tmp)
          if dft > 0:
              for doc_id in tmp:
                  tfd = getTermFreqInDoc(term, doc_id, index_dict)
                  new_score = (1 + math.log10(tfd)) * math.log10(5000/dft)
                  cur_score = 0
                  if doc_id in rsl:
                      cur_score = rsl[doc_id]
                  rsl[doc_id] = cur_score + new_score

  if len(rsl) > 0:
    sorted_dict = dict(sorted(rsl.items(), key=lambda item: item[1], reverse = True))
    #cnt = 1
    #for k,v in sorted_dict.items():
    #    if (cnt == 151): break
    #    fout.write(str(k) + ',%.4f' %v + '\n')
    #    cnt += 1

    return sorted_dict
   

