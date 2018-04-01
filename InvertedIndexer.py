import sys
from bs4 import BeautifulSoup
import nltk
import re
import math
#from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

#totaldoc = 37497
#nltk.download('wordnet')
#nltk.download('punkt')
def term_indexing(filename): # API: {term name : frequency in html}

    token_dic = {}
    htmlDoc = open(filename,'r').read()
    soup = BeautifulSoup(htmlDoc, 'html.parser')
    for deleteTag in soup(["script","link","style","a"]):
        deleteTag.clear()
    
    wordnet_lemmatizer = WordNetLemmatizer()
    
    useful_ls_w1 = soup.find_all(["body","h3"])
    
    
    
    for tag in useful_ls_w1:
        token_list = [wordnet_lemmatizer.lemmatize(unstem) for unstem in nltk.word_tokenize(tag.text)]
        for token in token_list:
            if not re.match("^.*\w.*$", token): # get rid of the token which only contains signs
                continue
            lotoken = token.lower()
            if lotoken not in token_dic:
                token_dic[lotoken] = 1
            else: 
                token_dic[lotoken] += 1 
                
    useful_ls_w2 = soup.find_all(["b","h2","strong"])
    

    for tag in useful_ls_w2:
        token_list = [wordnet_lemmatizer.lemmatize(unstem) for unstem in nltk.word_tokenize(tag.text)]
        for token in token_list:
            if not re.match("^.*\w.*$", token): # get rid of the token which only contains signs
                continue
            lotoken = token.lower()
            if lotoken not in token_dic:
                token_dic[lotoken] = 2
            else: 
                token_dic[lotoken] += 1
                
    
    useful_ls_w3 = soup.find_all(["title","h1"])
    
    
    for tag in useful_ls_w3:
        token_list = [wordnet_lemmatizer.lemmatize(unstem) for unstem in nltk.word_tokenize(tag.text)]
        for token in token_list:
            if not re.match("^.*\w.*$", token): # get rid of the token which only contains signs
                continue
            lotoken = token.lower()
            if lotoken not in token_dic:
                token_dic[lotoken] = 3
            else: 
                token_dic[lotoken] += 2
    
    return token_dic



def posting(doc_name, add_dic, posting_dic): # do the posting after tokenizing each html doc
    for key in add_dic.keys():
        if key not in posting_dic:
            posting_dic[key] = [{"doc":doc_name, "weight": add_dic[key], "tfidf": None}]
        else:
            posting_dic[key].append({"doc":doc_name, "weight": add_dic[key], "tfidf": None})
    return posting_dic


            
def tf_idf(posting_dic, term, totaldoc): 
    # do the tf_idf after finishing all the html, term_posting is the posting list for this term
    idf = math.log10(totaldoc / len(posting_dic[term]))
    for i in range(len(posting_dic[term])):
        #term_posting[i] is a dict {"doc":doc_name, "weight":, "tfidf":}, tf-idf = [1+ log(tf)] x log(N/df)
        posting_dic[term][i]["tfidf"] = (1+ math.log10(posting_dic[term][i]["weight"])) * idf


