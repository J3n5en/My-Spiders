# -*- coding: utf-8 -*-
import requests,re,os
from bs4 import BeautifulSoup
def down_torrent(hash,path,j):#下载种子
	headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
	session = requests.session()
	get = session.get("http://www.rmdown.com/link.php?hash="+hash,headers=headers).content
	soup = BeautifulSoup(get)
	reff = soup.find(type="hidden")['value']
	post = {
		'reff':reff,
		'ref':hash
	}
	data = session.post("http://www.rmdown.com/download.php",headers=headers,data=post).content
	open(path+"/"+str(j)+".torrent", 'wb').write(data)
def get_file(link):
	session = requests.session()
	html = session.get(link).content
	soup = BeautifulSoup(html)
	links = soup.find_all('a',href=re.compile("hash"))
	title = soup.find('h1').text
	pathname = re.sub('\s|\n|\*|\?|>|<|/|"|:', "", title).replace("\\","")
	# .encode("gbk")
	imgs = soup.find_all(src="/res/image/loader.gif")
	i = 0
	# print pathname.decode("gbk")
	try:
		os.mkdir(pathname)
		print pathname
	except Exception, e:
		print e
		return
	for img in imgs:
		i+=1
		try:
			data = requests.get("http:"+img["data-src"],timeout=5).content
			open(pathname+"/"+str(i)+".jpg", 'wb').write(data)
		except Exception, e:
			pass
	j=0
	for link in links:
		print link
		j+=1
		down_torrent(link.text.split("hash=")[1],pathname,j)
def get_links(page):
	html = requests.get("http://209.141.50.47/read/list1/g/1.htm").content
	soup = BeautifulSoup(html)
	links = soup.find_all('a',href=re.compile("/read/g"),target="_blank")
	for link in links:
		url = "http://209.141.50.47/"+link['href']
		print url
		get_file(url)
get_links(1)
