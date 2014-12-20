from bs4 import BeautifulSoup
import requests
import os
import sys
import getpass
import re
from threading import Thread

def readWeb(url):
	req = requests.get(url)
	return req.text

def tagList(tag, attr, webString):
	arrList = []
	soup = BeautifulSoup(webString)
	if(attr != 999) :
		arrList = soup.find_all(tag, attrs=attr)
	else :
		arrList = soup.find_all(tag)
	return arrList

class DownloadThread(Thread):
	def __init__(self, targetPageUrl):
		Thread.__init__(self)
		self.targetPageUrl = targetPageUrl

	def run(self):
		downloadPicture(self.targetPageUrl)
	
def downloadPicture(targetPageUrl):
	targetWebString = readWeb(targetPageUrl)
	soup = BeautifulSoup(targetWebString)
	targetAttr = {'id' : 'wallpaper'}
	targetPictureTag = soup.find_all('img', targetAttr)[0]
	picturueUrlString = targetPictureTag.get('src')

	tempList = re.split('\/', picturueUrlString)
	pictureName = tempList[len(tempList)-1]
	absoluteFileName = folderName +'/'+ pictureName
	
	picturueUrlString = 'http:' + picturueUrlString
	pictureStreamRequest = requests.get(picturueUrlString, stream = True)
	with open(absoluteFileName, 'wb') as pictureFile:
		for chunk in pictureStreamRequest.iter_content(1024):
			if(chunk):
				pictureFile.write(chunk)
				pictureFile.flush()

#---------Start of program--------------
#numberOfwallpapers = sys.argv[1]
picturePerPage = 24
pictureCount = 0
folderName = '/home/'+getpass.getuser()+'/Desktop/Wallhaven'
if not os.path.exists(folderName) :
	os.mkdir(folderName)
#this is gonna be a loop with count of pictures
#for pages in range (0, int(numberOfwallpapers)):

#find all link in 1 string
webString = readWeb('http://alpha.wallhaven.cc/random')
attr = {'id' : 'thumbs'}
webString = str(tagList('div', attr, webString)[0])
#print webString

#find and get all wallpaper links
attr = {'class' : 'preview'}
arrListAllLink = tagList('a', attr, webString)
arrDownloadList = []
f1 = 0
for element in arrListAllLink :
	arrDownloadList.append(arrListAllLink[f1].get('href'))
	f1 += 1;

for targetPageUrl in arrDownloadList :
	DownloadThread(targetPageUrl).start()
	pass

