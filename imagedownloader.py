import requests
from bs4 import BeautifulSoup
import os
import sys
import errno
import platform
boardList = ["a", "b", "h", "v", "vr", "vg", "gif", "g", "co", "e", "u", "w", "wg"]
operatingSystem = platform.system()
imagePath = "C:/Users/Tyler -_-/Documents/4chanImages/"
if operatingSystem == "Linux":
	imagePath = "/home/ty/Pictures/4chanImages/"

def download(url, file_name, percent, total):
	completion = percent/total * 100
	if completion >= 96:
		completion = 100
	#print(str(int(completion)) + "%" + " done")
	sys.stdout.write("\r%i" % int(completion) + " %")
	with open(imagePath + file_name, 'wb') as file:
		response = requests.get(url)
		file.write(response.content)
def getImages(linkedThread, board):
	soup = BeautifulSoup(linkedThread.content, 'html.parser')
	threadHeader = soup.find('body', class_='is_thread')
	imageThumbs = threadHeader.find_all('a', class_='fileThumb')
	for x in range(0, len(imageThumbs)):
		download("http:"+imageThumbs[x]['href'], imageThumbs[x]['href'].split(board,1)[1], x, len(imageThumbs))

def chooseThread():
	global imagePath
	board = input('Enter board: ')
	board = board.replace('/', '')
	while board not in boardList:
		board = input('Not a valid board: ')
		board = board.replace('/', '')
	imagePath = imagePath + board + "/"
	os.makedirs(os.path.dirname(imagePath), exist_ok=True)
	print(imagePath)
	postNum = input('Enter OP number: ')
	createdThread = "http://boards.4chan.org/" + board + "/thread/" + postNum
	request = requests.get(createdThread)
	while request.status_code != 200:
		postNum = input('Invalid post number: ')
		createdThread = "http://boards.4chan.org/" + board + "/thread/" + postNum
		request = requests.get(createdThread)
	print("Connection made")
	getImages(request, board)

chooseThread()