import requests
import time


mycookies=''
def getdomain():
	global mycookies
	headers={
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
	'Referer': 'http://dnslog.cn/'
	}
	url='http://dnslog.cn/getdomain.php?t=0.7648589759969944'
	res=requests.get(url=url)
	domain=res.text
	mycookies='PHPSESSID='+res.cookies['PHPSESSID']
	print(domain)

#/getrecords.php?t=0.5339624889326149
def getRecords():
	global mycookies
	ck=mycookies
	headers={
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
	'Cookie': '%s'%ck,
	'Referer': 'http://dnslog.cn/'
	}
	url='http://dnslog.cn/getrecords.php?t=0.5339624889326149'
	res=requests.get(url=url,headers=headers)
	if res.text!='[]' or len(res.text) != 2:
		print(res.text)


if __name__ == '__main__':
	n=10
	getdomain()
	while True:
		if n == 0:
			break
		getRecords()
		n=n-1
		time.sleep(1)