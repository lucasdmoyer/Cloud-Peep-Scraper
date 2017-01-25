import requests
from bs4 import BeautifulSoup
import pickle 
import csv
from selenium import webdriver

#names = ['ashtonwright', 'petertrapasso', 'scaleup']
alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']
from itertools import product 
keywords = [''.join(i) for i in product(alphabets, repeat = 16)]
print keywords

thefile = open('test.txt', 'w')
for item in keywords:
  thefile.write("%s\n" % item)

'''
thelist = open('test.txt', 'r')
for item in thelist:
	print item
'''

#builds csv file of all US and Canada cities in place, link
def buildplacesdic():
    with open('cloudpeeps.csv', 'w') as csvfile:
        fieldnames = ['Image', 'Name', 'Location', 'Linkedin', 'Facebook', 'Twitter', 'Instagram', 'Instagram Followers', "Instagram Following", "Instagram username"]
        write = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for entry in keywords:
        	info = getSearch(entry)
        	Image = info[0]
        	Name = info[1]
        	Location = info[2]
        	Linkedin = info[3]
        	Facebook = info[4]
        	Twitter = info[5]
        	Instagram = info[6]
        	Followers = info[7]
        	Following = info[8]
        	InstagramUserName = info[9]
        	write.writerow({'Image':Image, 'Name':Name, 'Location':Location, 'Linkedin':Linkedin, 'Facebook':Facebook, 'Twitter':Twitter, 'Instagram':Instagram, 'Instagram Followers': Followers, 'Instagram Following':Following, "Instagram username" :InstagramUserName})

def getSearch(user):
	search_url = 'https://www.cloudpeeps.com/' + user
	source_code = requests.get(search_url)
	html_doc = source_code.text
	soup = BeautifulSoup(html_doc, 'html.parser')
	

	#Get image
	startOfImage = soup.text.index("https://s3.amazonaws")
	endOfImage = soup.text[startOfImage:].index('make') + startOfImage - 3
	Image =  "=URL(" + soup.text[startOfImage:endOfImage] + ",4,50,50)"

	#Get Name
	nameString = str(soup.find('h1'))
	lengthName = len(nameString)
	Name = nameString[4:lengthName - 5]

	#Get location
	locationString = str(soup.find("div", { "class" : "location" }))
	startOfLocation = locationString.index(">")
	endOfLocation = locationString.index("</")
	Location = locationString[startOfLocation+2:endOfLocation].strip()

	#Get Linkedin
	startOfLinkedin = soup.text.index("linkedin")
	endOfLinkedin = soup.text[startOfLinkedin:].index('"')
	Linkedin = soup.text[startOfLinkedin-12:startOfLinkedin + endOfLinkedin]

	#Get Facebook
	startOfFacebook = soup.text.index("facebook")
	endOfFacebook = soup.text[startOfFacebook:].index('"')
	Facebook = soup.text[startOfFacebook-12:startOfFacebook+endOfFacebook]
	print Facebook
	if 'connect' in Facebook:
		Facebook = "Facebook Not Provided"
	print Facebook

	#Get Twitter
	startOfTwitter = soup.text.index("twitter")
	endOfTwitter = soup.text[startOfTwitter:].index('"')
	Twitter = soup.text[startOfTwitter-8:startOfTwitter+ endOfTwitter]

	#Get Instagram
	Instagram = ''
	try:
		startOfInstagram = soup.text.index("instagram")
		endOfInstagram = soup.text[startOfInstagram:].index('"')
		Instagram = soup.text[startOfInstagram-12:startOfInstagram+endOfInstagram]
		if (Instagram[len(Instagram)-1:] != '/'):
			Instagram = Instagram + '/'
	except ValueError:
		Instagram = 'Instagram Not Provided'
	#Get Insta username

	InstaUser=''
	try:
		startOfUsername = Instagram.index("com") + 4
		endOfUsername = Instagram[startOfUsername:].index('/')
		InstaUser = Instagram[startOfUsername: startOfUsername+ endOfUsername]
	except ValueError:
		InstaUser = 'Instagram Username Not Provided'

	#Get Instagram followers
	driver = webdriver.PhantomJS(executable_path=r'C:\PhantomJs\bin\phantomjs.exe')
	driver.get(Instagram)
	# This will get the html after on-load javascript
	html2 = driver.execute_script("return document.documentElement.innerHTML;")
	htmltext = html2.encode('utf-8')
	
	Followers =''
	Followed =''
	try:
		startOfFollowers = htmltext.index("follows")
		endOfFollowers = htmltext[startOfFollowers:].index("}")
		Followers = htmltext[startOfFollowers+20:startOfFollowers+endOfFollowers]

		startOfFollowed = htmltext.index("followed_by")
		endOfFollowed = htmltext[startOfFollowed:].index("}")
		Followed = htmltext[startOfFollowed+24: startOfFollowed+endOfFollowed]
	except ValueError:
		Followers = 'Followers Not Provided'
		Followed = 'Following Not Provided'
	result = [Image, Name, Location, Linkedin, Facebook, Twitter, Instagram, Followers, Followed, InstaUser]
	return result


#print getSearch('ashtonwright')
#buildplacesdic()