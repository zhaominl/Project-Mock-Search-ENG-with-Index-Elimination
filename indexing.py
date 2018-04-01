import indexer
import sys
import json
from indexer import term_indexing
#import search


def json_process(fileaddress):
    infile = open(fileaddress)
    jload = json.load(infile)
    infile.close()
    return jload

if __name__ == "__main__":
    indexing_doc = {}
    doc_count = 0
    data=json_process("WEBPAGES_RAW/bookkeeping.json")
   # try:
    for subpath in data:#subpath--> key
        
        filename = 'WEBPAGES_RAW/'+subpath
        file_doc =  indexer.term_indexing(filename)
        if (file_doc !={}):
            doc_count+=1 # get rid of dummy html
            print doc_count
        indexing_doc = indexer.posting(subpath, file_doc, indexing_doc)#gaimingzi
        #count += 1
            #if count>3:
               # break
        print subpath+" captured"
   # except:
    #    pass#shandiao
    
    print "Document # count: ", doc_count
    for term in indexing_doc:
        indexer.tf_idf(indexing_doc, term,doc_count)
 
    
    with open("output.json",'a') as outfile:
        outfile.seek(0)
        outfile.truncate()
        json.dump(indexing_doc, outfile)
        #json.dump({"The number of unique words" : len(indexing_doc.keys())},outfile)
        
    outfile.close()

     
    # write the indexing doc to database
        
    
    ''' import each file by appending the key of data to the path, and open each file,
    read the html doc, apply the indexing to get a local index. Merge the local index 
    to global Index'''
