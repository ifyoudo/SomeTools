# coding=utf-8

import sys
import re
import json
import requests
from Login import Login
from utils import Utils
from prettytable import PrettyTable

baseurl='https://www.qixintong.cn/'
req=requests.session()
def get_cookie():
	cookies={}
	try:
		cookief=open('cookie/cookies.txt','r')
		cookies=json.loads(cookief.read().strip('\n').replace('\'','"'))
	except Exception as e:
		print(e)
		pass
	finally:
		cookief.close()
	return cookies

def check_islogin():
	islogin=False
	headers=Utils().baseheader()
	headers.pop('X-Requested-With')
	url=baseurl+'qxtsearch/?key=%E7%99%BE%E5%BA%A6&typestr=0'
	try:
		cookies=get_cookie()
		res=requests.get(url,headers=headers,cookies=cookies,allow_redirects=False)
		print(res.status_code)
		if res.status_code == 302:
			print('relogin...')
			login=Login().save_cookies()
			islogin=True
		else:
			islogin=True
	except Exception as e:
		print(e)
	return islogin

def get_data(keyword):
	phone_list=[]
	email_list=[]
	gw=''
	headers=Utils().baseheader()
	headers.pop('X-Requested-With')
	url=baseurl+'qxtsearch/?key={key}&typestr=0'.format(key=keyword)
	qy_url_pattern='<a target="_blank" href="/company/(.*?)/"'
	if check_islogin():
		try:
			cookies=get_cookie()
			html_data=req.get(url,headers=headers,cookies=cookies).text
			qy_url=re.findall(qy_url_pattern,html_data)[0]
			#qy_url='56535433717945554d61'
			# 获取电话
			phone_table=PrettyTable(['电话'])
			phone_req_data='entid={qyurl}&contact_type=1'.format(qyurl=qy_url)
			headers['X-Requested-With']='XMLHttpRequest'
			headers['Content-Type']='application/x-www-form-urlencoded; charset=UTF-8'
			phonedata=json.loads(req.post(url=baseurl+'/ent/contact_pc/',data=phone_req_data,headers=headers,cookies=cookies).text)
			for i in phonedata['data']['contact']:
				phone_table.add_row([i['contact']])
			#print([i['contact'] for i in phonedata['data']['contact']])
			print(phone_table)
			# 获取邮箱
			email_table=PrettyTable(['邮箱'])
			email_req_data='entid={qyurl}&contact_type=2'.format(qyurl=qy_url)
			emaildata=json.loads(req.post(url=baseurl+'/ent/contact_pc/',data=email_req_data,headers=headers,cookies=cookies).text)
			for i in emaildata['data']['contact']:
				email_table.add_row([i['contact']])
			#print([i['contact'] for i in emaildata['data']['contact']])
			print(email_table)
			# 获取官网
			gw_table=PrettyTable(['官网'])
			gw_req_data='entid={qyurl}&contact_type=3'.format(qyurl=qy_url)
			gwdata=json.loads(req.post(url=baseurl+'/ent/contact_pc/',data=gw_req_data,headers=headers,cookies=cookies).text)
			for i in gwdata['data']['contact']:
				gw_table.add_row([i['contact']])
			print(gw_table)
			
			# 所有数据
			all_req_data='req_id={qyurl}&req_type=0'.format(qyurl=qy_url)
			all_data=json.loads(req.post(url=baseurl+'/pc/enterprise_map/',data=all_req_data,headers=headers,cookies=cookies).text)
			# 分支机构
			print('-'*40,'分支机构','-'*40)
			branch_table = PrettyTable(['企业名称','云编号'])
			branch_ptotal=int(all_data['children'][0]['ptotal'])
			for i in all_data['children'][0]['children']:
				branch_table.add_row([i['name'],i['node_id']])
			if branch_ptotal > 1:
				for i in range(2,branch_ptotal+1):
					branch_req_data='pindex={page}&entid={qyurl}'.format(page=i,qyurl=qy_url)
					branch_data=json.loads(req.post(url=baseurl+'/pc/company_branch/',data=branch_req_data,headers=headers,cookies=cookies).text)['data']
					for j in branch_data:
						branch_table.add_row([j['ENTNAME'],j['entid']])
			print(branch_table)
			print('-'*80)
			# 对外投资
			print('-'*40,'对外投资','-'*40)
			out_table=PrettyTable(['所投企业','投资比例','云编号'])
			for i in all_data['children'][5]['children']:
				out_table.add_row([i['name'],i['CONPROP'],i['node_id']])
			out_ptotal=int(all_data['children'][5]['ptotal'])
			if out_ptotal > 1:
				for i in range(2,out_ptotal+1):
					out_req_data='pindex={page}&entid={qyurl}'.format(page=i,qyurl=qy_url)
					out_data=json.loads(req.post(url=baseurl+'/pc/out_inv/',data=out_req_data,headers=headers,cookies=cookies).text)['data']
				for j in out_data:
					out_table.add_row([j['INV'],j['CONPROP'],j['entid']])
			print(out_table)
		except Exception as e:
			print(e)

if __name__ == '__main__':
	#get_data('小米')
	try:
		qyname=sys.argv[1]
		get_data(qyname)
	except Exception as e:
		print('python qxt.py 企业名称')
		print('示例：python qxt.py 小米')