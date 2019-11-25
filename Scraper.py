from urllib import request as req
from urllib import error as err # errors module in urllib.
from urllib import parse as par
from http.client import IncompleteRead
from http.client import HTTPException
import bs4 # beautiful soup, a third-party module for web-scraping.
import html.parser
import json,string,os,sys,threading,time

'''''//////////////////////globals////////////////////////////////'''''
start_time=time.time()
URLs=[] # A list, represents all URLs that are retrieved from google API.
URLsTitles=[] # A list of tuples, represents all Successfully scand URLs with their titles, in a form of ("URL","title").
URLsErrors=[] # A list of tuples, represents all URLs that reported an error durring requesting, in a form of ("URL","error code","error text"). 
tokens =[] # A list, represents all the words that fetched from all links.
search_term=""
num_of_links=0

def get_links_from_google_api(search_term, num_of_pages=0):
    global URLs
    cx = "" #your google search engine id should go here
    key ="" #and your google api key here
    page_count=int(num_of_pages/10)
    index = 1 # index of the first result in the next page
    print("Getting URLs from google ...")
    for i in range(page_count):
        try:
            #The link bellow is google's api link , it contains various parameters (more than 30), we are going to use only four of these
            #parameters which are cx,key,q and start.

            url = "https://www.googleapis.com/customsearch/v1?q="+par.quote(search_term)+"&cx="+cx+"&key="+key+"&start="+str(index) 

            response = req.urlopen(url) #send request , the urlopen method returns an object of the response class.
            response_json = json.loads(response.read()) # parse request into JSON

            for i in response_json["items"]: # get links from the JSON, it comes as an array of objects calld 'items'
                URLs.append(i["link"])

        except err.HTTPError as ex:
            print("Oops! google has refused to serve your request")
            print("Error code: "+str(ex.getcode()))
            print("Error reason: "+ex.reason)

            if ex.getcode()==400: # When there is some thing wrong with cx or key google returns a 400 error (bad request).
                print("please check your google custom search id and google API key")
            sys.exit()

        except err.URLError as ex:
            print("There might be an error in your network, please check your internet connection , error type:  "+str(ex.reason)) 
            sys.exit()

        except Exception as ex:
            print("Some thing went wrong")
            sys.exit()

        else:
            index=response_json["queries"]["nextPage"][0]["startIndex"] # get the start index of the next page
    print("Done!")
    print("If something went wrong press Ctrl+C")

def get_words_from_URLs(URL):
    global URLs
    global tokens
    global URLsTitles
    global URLsErrors
    try:
        response = req.urlopen(URL)
    except err.HTTPError as ex:
        errorCode = str(ex.getcode())
        errorReason=ex.reason
        URLsErrors.append( (URL,errorReason,errorCode) )
        sys.exit()
        
    except err.URLError as ex:
        URLsErrors.append( (URL,"0","Unknown error") )
        sys.exit()

    except IncompleteRead:
        sys.exit()
    except HTTPException:
        sys.exit() 
    except Exception as ex:
        URLsErrors.append( (URL,"0","Unknown error") )
        sys.exit()
    
    else:
        soup =bs4.BeautifulSoup(response,"html.parser")
        title= soup.find("title")
        if title == None:
            URLsTitles.append( (URL,"No title") )
        else:
            URLsTitles.append( (URL,title.text) )

        all_paragraphs = soup.find_all("p")
        for p in all_paragraphs:
            tokens +=str(p.text).lower().split()
        print(URL)
        sys.exit()

def clean_up():
    global tokens
    unwanted = string.punctuation+string.digits+string.whitespace+"؟,"
    table = str.maketrans('','',unwanted)
    for i in range(len(tokens)):
        tokens[i]=tokens[i].translate(table)
        #The following characters !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~0123456789 will be removed from each token.
            

def remove_meaningless_words(ls):
    fil =open(os.getcwd()+"\\meaningless_words.txt","r")
    words =fil.read().split("\n")
    fil.close()
    words = words + search_term.split() # removing the search term from the results as well
    temp=[]
    for i in ls:
        if words.__contains__(i):
            continue
        else:
            temp.append(i)
    return temp

def estimate_frequencies(ls):
    temp =  dict()
    for i in ls:
        if(temp.keys().__contains__(i)):
            temp[i]=temp[i]+1
        else:
            temp[i]=1
    return temp


def get_top_words_of_dictionary(dic,num_of_words=100):
    dic_items=dic.items() #This bulit-in function returns a list of tuples
    temp =[]
    for i in dic_items:
        temp.append(list(i)[::-1]) #Our dictionary is in a form of "string":int , we want it to be in int:"string" form.
    temp = sorted(temp,reverse=True) #This function sorts a list of lists (or list of tuples) by the first index of the nested list/tuple

    return temp[0:num_of_words]

            
def set_up_threads():
    global URLs
    for URL in URLs:
        thr =threading.Thread(target=get_words_from_URLs,args=(URL,),daemon=True)
        thr.start()
        #Since network operations are I/O bound operations using multi-threading -theoretically- is going to speed up the script massively.
        #Here each URL is going to be handled by a different thread, of course this could cause a band-width issues and a network bottleneck if the
        #number of URLs is huge but for a 500 URLs -or less- there will be no problems.

def args_contorol():
    global search_term
    global num_of_links
    if sys.argv.__len__()==3 and sys.argv[2].isnumeric():
        if int(sys.argv[2]) < 10:
            print("Number of pages must be more than 10")
            sys.exit()
        else:
            search_term=sys.argv[1].lower()
            num_of_links=int(sys.argv[2])
    else:
        print("Wrong input")
        print('''Scraper.py "your search term" number of likes you want to scrape''')
        sys.exit()


def print_to_files(path,mod,ls):
    try:
        fil=open(path,mod)
        for i in ls:
            try:
                print(i,file=fil)
            except:
                pass
        fil.close()
    except OSError as er:
        print(er)

#//////////////////////////////////Main/////////////////////////////////////

args_contorol()
get_links_from_google_api(search_term,num_of_pages=num_of_links)
set_up_threads()

try:
    while threading.active_count() != 1:
        pass
        #This loop will pause the main thread at the current line until all threads are finished executing.
        #Obviously this is not the best way to do that,but unfortunately i could not find any other way to
        #make the main thread wait at a specific line.
    if threading.active_count()==1:
        raise KeyboardInterrupt 
        #I've come across a problem in which a thread never finishes execution or take too long  due to some
        #network problems, in this case the script will freeze. The solution i came up with is to throw a 
        #keyboardinterrupt(Ctrl+c) to bypass the loop and continue executing the main thread
except KeyboardInterrupt:
    clean_up()
    tokens=remove_meaningless_words(tokens)
    result = get_top_words_of_dictionary(estimate_frequencies(tokens))

    print("\n--------------------------")
    for i in range(10):
        print(result[i][1]," | ",result[i][0])#print top 10 words
    print("--------------------------\n")
    print("Number of successfully fetched pages :",URLsTitles.__len__())
    print("Number of pages that reported an error:",URLsErrors.__len__())

    print_to_files(os.getcwd()+"\\words.txt","w",result)
    print_to_files(os.getcwd()+"\\URLs.txt","w",URLsTitles)
    print_to_files(os.getcwd()+"\\Errors.txt","w",URLsErrors)

    print("Time taken",time.time()-start_time,"sec")