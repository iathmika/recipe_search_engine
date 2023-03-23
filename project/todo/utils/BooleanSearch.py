from porter2stemmer import Porter2Stemmer
from .RankSearch import fetchAllDocIds
import re
stemmer = Porter2Stemmer()

def boolean_search(query, indexObj):
    d = indexObj.getIndexDict()
    # query = query.replace('\n','') #Replacing new line in readlines with nothing
    ans = set() #Set to store final document IDs for the query search
    # full = set(ids) # Set which has Document IDs for the whole collection
    full = indexObj.getDocLenDict().keys()
    query = query.replace('"','')
    res = re.split(' |, |,', query)
    # query_no = res.pop(0) #Storing query number by popping first element of query as first element is query_num
    operators = [] #Stack to store operators
    #Iterating the query
    while(res):
        val = res.pop(0)
        #If the element is a operator then store it in the stack and continue iterating the next elements
        if(val == 'NOT' or val == 'AND' or val == 'OR'):
            operators.append(val)
        #Otherwise it is a term
        else:
            curr = set() #Set to store document IDs of the current word
            num = 1 #Phrase search distance
            #If word is empty continue and see next words
            if(val == ''):
                continue
            #If it has a '#' then it is proximity search and we update num with distance
            if(val[0] == '#'):
                target  = val[1:].split('(')
                num, val = int(target[0]), target[1]
            #Check if the word is in dictionary     
            if(stemmer.stem(val.lower()) in d):
                #Add all the documents of that word in the set
                for i in d[stemmer.stem(val.lower())].details:
                    curr.add(i)
                #If the next term is again a word then it has to be either pharse or proximity search
                if(res and res[0] != 'AND' and res[0] != 'OR' and res[0] != 'NOT'):
                    curr.clear()
                    val2 = res.pop(0) #Getting the next term
                    if(val2[-1] == ')'):
                        val2 = val2[:-1]
                    #Check if the other term is in dictionary
                    if(stemmer.stem(val2.lower()) in d):
                        first = set(d[stemmer.stem(val.lower())].details.keys())
                        second = set(d[stemmer.stem(val2.lower())].details.keys())
                        common = first.intersection(second) #Getting common documents for the two words
                        #Iterating the positions of common documents for the two words
                        for i in common:
                            pos1 = d[stemmer.stem(val.lower())].details[i]
                            pos2 = d[stemmer.stem(val2.lower())].details[i]
                            p1, p2 = 0, 0
                            #Iterating till a match for phrase or proximity search or till one of the positions are exhausted(no match)
                            while(p1<len(pos1) and p2<len(pos2)):
                                if(num == 1):#It iis a phrase search
                                    if((pos2[p2] - pos1[p1]) == num):#If the words are together and in that order add the document in the set and break to check for remaining common documents
                                        curr.add(i)
                                        break
                                    elif(pos1[p1]<pos2[p2]):
                                        p1 += 1
                                    else:
                                        p2 += 1
                                else:#It is a proximity search
                                    if(abs(pos1[p1] - pos2[p2]) <= num):
                                        curr.add(i)#If it is within proximity range then add the document in the set and break to check for remaining common documents
                                        break
                                    elif(pos1[p1]<pos2[p2]):
                                        p1 += 1
                                    else:
                                        p2 += 1
            #Check if there are any operators in stack and do operations for all still stack becomes empty
            while(operators):
                op = operators.pop()
                if(op == 'NOT'):
                    curr = full - curr #NOT operation
                elif(op == 'AND'):
                    curr = ans.intersection(curr) #AND operation
                else:
                    curr = ans.union(curr) #OR operation
            ans = curr
    #print(ans)
    return ans
        #If the query has output then sort on basis of document IDs and store it in the file
        # if(ans):                   
        #     for i in sorted(ans):
        #         with open('results.boolean.txt','a') as file_obj:
        #             file_obj.write(str(query_no) + ',' + str(i) + '\n')
