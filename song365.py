import sys, re
from bs4 import BeautifulSoup
from mechanize import Browser
import urllib2
import cookielib

def grablinks(pageurl):
	dllinks = []
	br = Browser()
	br2 = Browser()
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	br2.set_handle_referer(True)
	br2.set_handle_robots(False)
	br2.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	
	br.open(sys.argv[1])
	grabbed = 0
	for link in br.links(url_regex='/download/'):
		print "Working..."
		req = br.click_link(url=link.url)
		br2.open(req)
		soup = BeautifulSoup(br2.response().read(),'lxml')
		scripts = soup.find_all('script',{'type':'text/javascript'})
		dllinks.append(str.replace(str.replace(re.search('var hqurl = \'.*\'',str(scripts[5])).group(0),"var hqurl =",""),"'",""))
		print "Grabbed link "+str(grabbed+1)
		grabbed = grabbed + 1
	return dllinks

def download(url):
	

	file_name = url.split('/')[-1]
	request = urllib2.Request(url,headers=request_headers)
	u = urllib2.urlopen(request)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_name, file_size)
	
	file_size_dl = 0
	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break
	
	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print status,
	
	f.close()	

if (__name__ == "__main__"):
	
	request_headers = {
		"Accept-Language": "en-US,en;q=0.5",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Referer": "http://thewebsite.com",
		"Connection": "keep-alive"
	}
	
	if(len(sys.argv)>1 and len(sys.argv)<4):
		if(len(sys.argv)==3):
			links = ([link for link in grablinks(sys.argv[1])][:int(sys.argv[2])])
			print "Got first %s links" % sys.argv[2]
		else:
			links = (grablinks(sys.argv[1]))
			
		for link in links:
			download(link)
		print "Done."

	else:
		print "This program takes 2 arguments: An album URL and (optionally) the first number of tracks to fetch"

