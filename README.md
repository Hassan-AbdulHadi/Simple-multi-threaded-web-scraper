# A simple multi-threaded web scraper

I wrote this for fun and for educational purposes as well, you might not be able to find any real world uses for it however, you can come up with some really interesting results.
###### What does it do?
What it does is finds the top 10 words that occurred/repeated with a specific word –or a search term- and the frequency of each word in the first 10, 20 30 etc. sites of Google's results 
## Techs
-	Python 
-	google custom search API
## Google's API 
To use this script you need to get a search engine ID and an API key see [here]( https://developers.google.com/custom-search/v1/overview) for more information.
You need to place -between the ""- your search engine ID in the cx variable in line 21 in the script, and place the API key  in the key variable in line 22.
Google gives you 100 free requests per a day for developmental purposes, I have to mention that each 10 results represent one request so if you wanted to scrape 1000 links/results in one run you would actually drain all of your free requests for the day.
## Other dependencies
This whole script is based upon a third-party module called (beautiful soup) for web scraping, so you defiantly need to pip-install it, run the following command in your shell:
```
Pip install bs4
```
## How to use this script?
Type the following command in your shell
```
Python Scraper.py "your search term" number of sites you want to scrape
```
 (I'm assuming that you've already installed python and put it in the path and you are in the project directory)

## Workflow
-	Get links from google API.
-	Request each link and get the resulting HTML.
-	Get all paragraphs from each link.
-	Extract the words from each paragraph.
-	Remove the meaningless words, and by meaningless I mean words like (is,am,how,they etc.). 
This entire list is placed in a text file in the project directory named meaningless_words.txt so you can edit that file to meet your needs.
-	Get the frequency of each word and print the top 10 words.
## Other things
- If you are looking not only for the top 10 words, a text file will be generated containing the top 100 words along with their frequencies, named words.txt.
- All successfully fetched links will be written in a file named URLs.txt along with their titles.
- All links that reported errors will be written in a file named errors.txt along with error type and code. 
- The file results_sample.txt contains some result samples.
