import json
import math
import nltk

K = 5
totaldoc = 34627

def simple_search(query, indexing_doc, json_data):
    #search for only one-token query
    result = [];
    posting_list = indexing_doc[query.lower()]
    posting_list.sort(key = lambda posting:-posting["tfidf"])
    if len(posting_list) > K:
        for posting in posting_list[:K]:
            result.append([posting["doc"],json_data[posting["doc"]]])
    else:
        for posting in posting_list:
            result.append([posting["doc"],json_data[posting["doc"]]])
    return result


def compare_cos_vector(query_norwt, docs_norwt,json_data): 
    #compare the cosine and return the top k results as urls
    prod_score = {}
    for doc in docs_norwt:
        doc_score = 0
        for token in docs_norwt[doc]:
            doc_score += (docs_norwt[doc][token] * query_norwt[token])
        prod_score[doc] = doc_score
        
    
    if prod_score == {}:
        print("No result")
        return
    else:    
        sort_score = sorted([(item[0],item[1]) for item in prod_score.items()],key=lambda pair:pair[1], reverse=True)
        top_k_result = sort_score if len(sort_score)<=K else sort_score[:5]
        print(top_k_result)
        for i in top_k_result:
            print(docs_norwt[i[0]])
            print(query_norwt)
            print("===========================")
        result = []
        for each in top_k_result:
            result.append([each[0],json_data[each[0]]])
        
        return result


def index_eliminate(query_tokens,indexing_doc): 
    # using the indexing elimination to faster the cos calculation
    elim_doc = {}
    doc_list = {}
    min_limit = int(round(len(query_tokens) / 2.0))
    for token in query_tokens:
        for doc_info in indexing_doc[token]:
            if doc_info["doc"] in doc_list:
                doc_list[doc_info["doc"]].append(token)
            else:
                doc_list[doc_info["doc"]] = [token]
                
    for key in doc_list:
        if (len(doc_list[key]) >=  min_limit):
           elim_doc[key] = doc_list[key] 
           
    # return the doc after the elimination and the contain tokens
    return elim_doc 


def search(raw_query, indexing_doc, json_data, totaldoc):
    
    #tokenize query
    query_tokens = []
    for raw_token in nltk.word_tokenize(raw_query.lower()):
        if raw_token in indexing_doc:
            print(raw_token)
            query_tokens.append(raw_token)
    
    #handle simple conditions
    if len(query_tokens) == 0:
        return "No valid query!"
    
    if len(query_tokens) == 1:
        return simple_search(query_tokens[0], indexing_doc, json_data)
    
    token_count = {}
    for token in query_tokens:
        if token in token_count:
            token_count[token] += 1
        else:
            token_count[token] = 1
    
    #calculate the idf, use tf-idf to subtract the idf and get tf
    query_norwt = {}
    for token in token_count:
        token_idf = math.log10(totaldoc / len(indexing_doc[token]))
        token_tf = 1+math.log10(token_count[token])
        query_norwt[token] = token_idf * token_tf
        
    query_length = math.sqrt(sum([i**2 for i in query_norwt.values()]))
    for key in query_norwt.keys():
        query_norwt[key] = query_norwt[key] / query_length
    
    
     # get all the available document contain enough query tokens, Index Elimination
    elim_doc = index_eliminate(query_tokens, indexing_doc)
        
    docs_norwt = {}
    for doc_pair in elim_doc.items():
        doc_norwt = {}
        for token in doc_pair[1]:
            for doc_info in indexing_doc[token]:
                if doc_info["doc"] == doc_pair[0]:
                    doc_norwt[token] = 1+ math.log10(doc_info["weight"])
                    break
        
        doc_length = math.sqrt(sum([i**2 for i in doc_norwt.values()]))
        for key in doc_norwt.keys():
            doc_norwt[key] = doc_norwt[key] / doc_length
        
        docs_norwt[doc_pair[0]] = doc_norwt
    
    # save the doc_name : the ranking score
    return compare_cos_vector(query_norwt, docs_norwt,json_data)
    
    