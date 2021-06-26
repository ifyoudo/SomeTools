import json
import requests
import qrcode
import time
import os
from utils import Utils
from PIL import Image

class Login(object):
	"""docstring for Login"""
	def __init__(self, ):
		super(Login, self).__init__()
		self.baseurl='https://www.qixintong.cn'
		self.req=requests.Session()
		self.cookiePath='cookie/cookies.txt'
	def get_qrcode(self,):
		qrcode=''
		qr_headers=Utils().baseheader()
		try:
			url_qr='/get_QR_code/'
			qr_res=json.loads(self.req.post(url=self.baseurl+url_qr,headers=qr_headers).text)
			qrcode=qr_res['data'][0]['QRCode']
			qrcode_url=qr_res['data'][0]['QRCode_url']
			self.genera_code(qrcode_url)
		except Exception as e:
			print(e)
		return qrcode

	def check_login(self,qrcode):
		check_header=Utils().baseheader()
		check_header['Content-Type']='application/x-www-form-urlencoded; charset=UTF-8'
		try:
			data='QRCode=%s'%qrcode
			url_check='/login_response/'
			check_login_url='/login_qxt/'
			check_res=self.req.post(url=self.baseurl+url_check,data=data,headers=check_header).text
			if '200' in check_res and 'ok' in check_res:
				print('scan success...')
				login_res=self.req.post(url=self.baseurl+check_login_url,data=data,headers=check_header).text
				print(login_res)
				return True
			else:
				return False
		except Exception as e:
			print(e)


	def genera_code(self,url):
		print(url)
		img=qrcode.make(data=url)
		imgName='login.jpg'
		with open(imgName,'wb') as f:
			img.save(f)
		codeImg=Image.open(imgName)
		codeImg.show()

	def save_cookies(self,):
		qrcode=self.get_qrcode()
		for i in range(20):
			time.sleep(1)
			if self.check_login(qrcode):
				break
		print(self.req.cookies)
		cookieStr=str(requests.utils.dict_from_cookiejar(self.req.cookies))
		with open(self.cookiePath,'w') as cookief:
			cookief.write(cookieStr)