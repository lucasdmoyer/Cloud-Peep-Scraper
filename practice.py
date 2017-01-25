import requests
from bs4 import BeautifulSoup
import pickle 
import csv

names = [ashtonwright, petertrapasso, scaleup]

def getSearch(term):
    search_url = 'https://www.cloudpeeps.com/search/peeps#?order_by=relevance&text=' + term +'&minimum_hours_available=&address=&latitude=&longitude='
    source_code = requests.get(search_url)
    html_doc = source_code.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    print soup.prettify()

#builds csv file of all US and Canada cities in place, link
def buildplacesdic():
    with open('cloudpeeps.csv', 'w') as csvfile:
        fieldnames = ['Image', 'Name', 'Location', 'Linkedin', 'Facebook', 'Twitter', 'Instagram', 'Instagram Followers', "Instagram Following", "Instagram username"]
        write = csv.DictWriter(csvfile, fieldnames=fieldnames)

from selenium import webdriver


driver = webdriver.PhantomJS(executable_path=r'C:\PhantomJs\bin\phantomjs.exe')
#driver = webdriver.PhantomJS("C:\PhantomJs\bin\phantomjs")
##driver = webdriver.PhantomJS()
driver.get("https://www.cloudpeeps.com/search/peeps#?order_by=relevance&text=aaa&minimum_hours_available=&address=&latitude=&longitude=")

# This will get the initial html - before javascript
html1 = driver.page_source

# This will get the html after on-load javascript
html2 = driver.execute_script("return document.documentElement.innerHTML;")

print html2
