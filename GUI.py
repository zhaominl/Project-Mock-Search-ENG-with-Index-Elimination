import search
import json
import math
import nltk
from Tkinter import *
from bs4 import BeautifulSoup

def process_query(text, indexing_doc, json_data):
    ''' Given a string, returns a string in response. '''
    totaldoc = 34627
    print(len(indexing_doc.keys()))
    text = text.strip().lower()
    if text in {'quit', 'exit'}:
        return
    else:
        return search.search(text, indexing_doc, json_data, totaldoc)

def main():
    
    indexing_doc = json.load(open("output.json"))
    json_data = json.load(open("WEBPAGES_RAW/bookkeeping.json"))
 
    Search = Tk()
    var = StringVar()
    
    
 
    text = Label(Search, textvariable=var, relief=RAISED, height = 100, width=100, anchor=NW, bg="white", justify=LEFT)
 

    def process_callback(*args):
        # figure out what the response to the input should be
        response = process_query(entry.get(),indexing_doc,json_data)
        var.set("")
        
        if response is None:
            Search.quit()
            Search.destroy()
            return
        
        if type(response) == str:
            var.set(response)
            Search.mainloop()
        
        
        # write the response
        output = u""
        for url in response:
            output = u"".join([output,u'\nLINK: {}\n'.format(str(url[1]))])
            #var.set('\n{}\n'.format(str(url[1])))
            with open('WEBPAGES_RAW/'+url[0],"r") as htmldoc:
                soup = BeautifulSoup(htmldoc.read(), 'html.parser')
                
                #find meta-description, meta-og:description, title, for snippet
                snippet = soup.find("meta",  property="description")
                if snippet:
                    output = u"".join([output,u'Description: {}\n\n'.format(snippet.text.strip())])
                    #var.set('{}\n\n'.format(snippet.text))
                else:
                    snippet = soup.find("meta",  property="og:description")
                    if snippet:
                        output = u"".join([output,u'Description: {}\n\n'.format(snippet.text.strip())])
                        #var.set('{}\n\n'.format(snippet.text))
                        
                    
                snippet = soup.find("title")
                if snippet and snippet.text!=u"":
                    output = u"".join([output,u'Title: {}\n'.format(snippet.text.strip())])
                    #var.set('{}\n\n'.format(snippet.text))
                    continue
                
                snippets = soup.find_all(["h1"])
                if snippets:
                    for snippet in snippets:
                        output = "".join([output,'{}\n\n'.format(snippet.text.strip())])
                        #var.set('{}\n'.format(snippet.text))
                    continue
                
                output = u"".join([output,u'Relating to the url: {}\n\n'.format(str(url[1]))])
                #var.set('Relating to the url: {}\n\n'.format(str(url[1])))
        var.set(output)
        text.pack()        
                #end for one link
                
                
        # clear the input field
        entry.delete(0, END)

    entry = Entry(Search, width=25, bd=2)
    entry.pack()
    entry.focus()
    entry.bind('<Return>', process_callback)
    
    btn = Button(Search,
                 width=18,
                 bd=2,
                 bg='light gray',
                 text='Search',
                 command=process_callback)
    btn.pack()
    text.pack()
 
    var.set("Search Engine.\n")
 
    Search.mainloop()
 

if __name__ == '__main__':
    main()
