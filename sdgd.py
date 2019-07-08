import json
import requests
from requests.exceptions import RequestException
from pymongo import MongoClient


client = MongoClient()  ##连接数据库
db = client['hmt']  #指定数据库
collection = db['sdgd'] #声明对象


def get_one_page(url):
	headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
	response = requests.get(url, headers=headers)
	try:
		response = requests.get(url, headers=headers)
		if response.status_code == 200:  # 响应码
			#print(response.json().get('gdrs'))
			return response.json()
	except requests.ConnectionError as e:
		print('Error', e.args)

def parse_page(json):
	items = json.get('data')
	for item in items:
		h = {}
		h['日期'] = item.get('RDATE')
		h['排名'] = item.get('RANK')
		h['股东名称'] = item.get('SHAREHDNAME')
		h['股东类型'] = item.get('SHAREHDTYPE')
		h['股份类型'] = item.get('SHARESTYPE')
		h['持股数'] = item.get('SHAREHDNUM')
		h['占股比例'] = item.get('SHAREHDRATIO')
		yield h
		#print(item)



if __name__ == '__main__':
	url = 'http://data.eastmoney.com/DataCenter_V3/gdfx/stockholder.ashx?code=000725&date=2010-06-30&type=Sd'
	json = get_one_page(url)
	results = parse_page(json)
	i = 0
	for result in results:
		#print(result)
		if collection.insert_one(result):
			i = i + 1
			print('save to mongo')
			print(i)



##时间处要注意url变化（在xhr文件里），还有时间可以写一个规律算法
