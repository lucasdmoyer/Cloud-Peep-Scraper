import requests
from bs4 import BeautifulSoup
import pickle 
import csv

def getSearch():
    search_url = 'https://www.cloudpeeps.com/ashtonwright'
    source_code = requests.get(search_url)
    html_doc = source_code.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    #Get image


    startOfImage = soup.text.index("https://s3.amazonaws")
    endOfImage = soup.text[startOfImage:].index('make') + startOfImage - 3
    print soup.text[startOfImage:endOfImage]



getSearch()