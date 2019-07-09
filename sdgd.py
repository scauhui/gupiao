import json
import requests
from requests.exceptions import RequestException
from pymongo import MongoClient


client = MongoClient()  ##连接数据库
db = client['hmt']  #指定数据库
collection = db['sdgd'] #声明对象

L = ['2019-03-31', '2018-12-31', '2018-09-30', '2018-06-30', '2018-03-31', '2017-12-31', '2017-09-30', '2017-06-30', '2017-03-31', '2016-12-31', '2016-09-30', '2016-06-30', '2016-03-31', '2015-09-30', '2015-06-30', '2015-03-31', '2014-12-31', '2014-09-30', '2014-06-30', '2014-03-31', '2013-12-31', '2013-09-30', '2013-06-30', '2013-03-31', '2012-12-31']



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
	for a in range(0, 26):
		url = 'http://data.eastmoney.com/DataCenter_V3/gdfx/stockholder.ashx?code=000725&date=' + str(L[a])
		json = get_one_page(url)
		results = parse_page(json)
		i = 0
		for result in results:
			#print(result)
			if collection.insert_one(result):
				i = i + 1
				print('save to mongo')
				print(i)
