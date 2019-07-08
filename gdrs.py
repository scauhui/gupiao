import json
import requests
from requests.exceptions import RequestException
from pymongo import MongoClient


client = MongoClient()  ##连接数据库
db = client['hmt']  #指定数据库
collection = db['gdrs'] #声明对象


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
	items = json.get('gdrs')
	for item in items:
		h = {}
		h['日期'] = item.get('rq')
		h['股东人数'] = item.get('gdrs')
		h['股东人数较上期变化%'] = item.get('gdrs_jsqbh')
		h['人均流通股'] = item.get('rjltg')
		h['人均流通股较上期变化%'] = item.get('rjltg_jsqbh')
		h['筹码集中度'] = item.get('cmjzd')
		h['股价'] = item.get('gj')
		h['人均持股金额'] = item.get('rjcgje')
		h['前十大股东持股合计%'] = item.get('qsdgdcghj')
		h['前十大流通股东持股合计%'] = item.get('qsdltgdcghj')
		yield h
		#print(item)



if __name__ == '__main__':
	url = 'http://f10.eastmoney.com/ShareholderResearch/ShareholderResearchAjax?code=SZ000725'
	json = get_one_page(url)
	results = parse_page(json)
	for result in results:
		print(result)
		if collection.insert_one(result):
			print('save to mongo')
