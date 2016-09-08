#coding=utf-8
import requests
import json
from bs4 import BeautifulSoup
import os
import time


Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                  'Referer': 'http://www.zhihu.com',
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0',
                  'Host': 'www.zhihu.com'}
_session = requests.session()
_session.headers.update(Default_Header) 

BASE_URL = 'https://www.zhihu.com'
CAPTURE_URL = BASE_URL+'/captcha.gif?r='+str(int(time.time())*1000)+'&type=login'
PHONE_LOGIN = BASE_URL + '/login/phone_num'
BASE_ZHUANLAN_API = 'https://zhuanlan.zhihu.com/api/columns/'
BASE_ZHUANLAN = 'https://zhuanlan.zhihu.com'
limit = 20


def login():
    '''登录知乎'''
    username = ''#你得帐号密码（此处为手机帐号）
    password = ''
    cap_content = _session.get(CAPTURE_URL).content
    cap_file = open('cap.gif','wb')
    cap_file.write(cap_content)
    cap_file.close()
    captcha = raw_input('capture:')
    data = {"phone_num":username,"password":password,"captcha":captcha}
    r = _session.post(PHONE_LOGIN, data)
    print (r.json())['msg']

def postData(url_token,pagenum):

	

	allOutPutList = []

	for i in range(0,pagenum):
		offset = i * limit
		print('第',str(i),'页',str(offset))

		outPutList = start(url_token,offset)
		allOutPutList.append(outPutList)
		time.sleep(10)

	json.dump(allOutPutList, open('newjsonfile.txt', 'w'))
	print('保存json完成')

	return allOutPutList

def start(url_token,offset):



	params = json.dumps({"url_token": url_token, "pagesize": 10, "offset": offset})
	form={'method':'next','params':params}

	headers ={
		'Host':'www.zhihu.com',
		'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
		'Referer':'https://www.zhihu.com/question/30116337',
		'X-Requested-With': 'XMLHttpRequest',
	}
	print('开始爬虫')

	html=requests.post("https://www.zhihu.com/node/QuestionAnswerListV2",data=form,headers=Default_Header)

	print(html.status_code)

	jsonDic = html.json()
	
	outPutList = []


	for content in jsonDic['msg']:



		soup = BeautifulSoup(content)

		outPutJson = {}

		author_src_list =[]

		author_name  = soup.find('div',class_='zm-item-rich-text').get('data-author-name')

		print (author_name)

		outPutJson['name'] = author_name

	
		mainDiv = soup.find('div',class_='zm-editable-content')
		imgTag = mainDiv.find_all('img',class_='lazy')
		i =1
		for src in imgTag:
			
			
			realImgUrl = src.get('data-original')
			realImgUrl1 = src.get('data-actualsrc')
			if realImgUrl:
				author_src_list.append(realImgUrl)
				print('作者',outPutJson['name'],'有',str(i),'张图片','realImgUrl',realImgUrl)
				i = i +1
			elif realImgUrl1:
				author_src_list.append(realImgUrl1)
				print('作者',outPutJson['name'],'有',str(i),'张图片','realImgUrl1',realImgUrl1)
				i = i +1

		if len(author_src_list):
			outPutJson['imgUrls'] = author_src_list

			outPutList.append(outPutJson)




	return outPutList

def downsPic(outPutList):

	j = 1

	for outPutLists in outPutList:


		for dic in outPutLists:


			for imgSrc in dic['imgUrls']:
				Name =  dic['name'] + str(j)

				r = requests.get(imgSrc,stream=True)

				with open(Name, 'wb') as f:
					for chunk in r.iter_content():
						if chunk: # filter out keep-alive new chunks  
							f.write(chunk)  
				print ('下载完',str(j),'张')
				j = j +1  
				  


		

	print ('Down!')

	return outPutList



if __name__ == '__main__':
	#outPutList = start(url_token=30116337,offset=20)
	
	outPutList = postData(url_token=30116337,pagenum=2)
	downsPic(outPutList)

