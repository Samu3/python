#coding=utf-8
import requests
import json
from bs4 import BeautifulSoup
import os



def start(url_token,offset):

	params = json.dumps({"url_token": url_token, "pagesize": 10, "offset": offset})
	form={'method':'next','params':params}

	headers ={
		'Host':'www.zhihu.com',
		'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
		'Referer':'https://www.zhihu.com/question/30116337',
	}
	html=requests.post("https://www.zhihu.com/node/QuestionAnswerListV2",data=form,headers=headers)

	print(html.status_code)

	print(html.content.decode())

	jsonDic = html.json()
	
	outPutList = []


	for content in jsonDic['msg']:



		soup = BeautifulSoup(content)

		outPutJson = {}

		author_src_list =[]

		author_name  = soup.find('div',class_='zm-item-rich-text').get('data-author-name')

		outPutJson['name'] = author_name

	
		mainDiv = soup.find('div',class_='zm-editable-content')
		imgTag = mainDiv.find_all('img')
		i =1
		for src in imgTag:
			imgUrl = src.find('img',class_='origin_image')
			if imgUrl:
				realImgUrl = imgUrl.get('data-original')
				author_src_list.append(realImgUrl)
				print('作者',outPutJson['name'],'有',str(i),'张图片')
				i = i +1
		if len(author_src_list):
			outPutJson['imgUrls'] = author_src_list

			outPutList.append(outPutJson)


	json.dump(outPutList, open('newjsonfile.txt', 'w'))
	print('保存json完成')

	return outPutList

def downsPic(outPutList):

	j = 1
	for dic in outPutList:


		for imgSrc in dic['imgUrls']:
			Name =  (str(j)+'.jpg')

			r = requests.get(imgSrc,stream=True)

			with open(Name, 'wb') as f:
				for chunk in r.iter_content():
					if chunk: # filter out keep-alive new chunks  
						f.write(chunk)  
			print ('下载完',str(j),'张')
			j = j +1  
				  


		



	return outPutList



if __name__ == '__main__':
	outPutList = start(url_token=30116337,offset=20)
	downsPic(outPutList)

