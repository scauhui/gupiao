import json
import requests
from requests.exceptions import RequestException
from pymongo import MongoClient


client = MongoClient()  ##连接数据库
db = client['hmt']  #指定数据库
collection = db['gdzrs'] #声明对象


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
		h['股东户数统计截止日期'] = item.get('EndDate')
		h['股东户数公告日期'] = item.get('NoticeDate')
		h['区间涨跌幅%'] = item.get('RangeChangeRate')
		h['本次股东户数'] = item.get('HolderNum')
		h['上次股东户数'] = item.get('PreviousHolderNum')
		h['股东户数增减'] = item.get('HolderNumChange')
		h['股东户数增减比例%'] = item.get('HolderNumChangeRate')
		h['户均持股市值'] = item.get('HolderAvgCapitalisation')
		h['户均持股数量'] = item.get('HolderAvgStockQuantity')
		h['总市值'] = item.get('TotalCapitalisation')
		h['总股本'] = item.get('CapitalStock')
		h['股本变动'] = item.get('CapitalStockChange')
		h['股本变动原因'] = item.get('CapitalStockChangeEvent')
		yield h
		#print(item)



if __name__ == '__main__':
	url = 'http://data.eastmoney.com/DataCenter_V3/gdhs/GetDetial.ashx?code=000725'
	json = get_one_page(url)
	results = parse_page(json)
	#i = 0
	for result in results:
		#print(result)
		if collection.insert_one(result):
			#i = i + 1
			print('save to mongo')
			print(i)
