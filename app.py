import requests
import json
import time
import os

def get_data(min_year, vxus_allocation):

	cache_filename = f"cache/{min_year}_{vxus_allocation}.json"

	if os.path.exists(cache_filename):
		with open(cache_filename) as f:
			return json.load(f)

	vti_allocation = 100 - vxus_allocation

	url = 'https://testfol.io/api/backtest'

	headers = {
		'authority': 'testfol.io',
		'accept': '*/*',
		'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
		'cache-control': 'no-cache',
		'content-type': 'application/json',
		'origin': 'https://testfol.io',
		'pragma': 'no-cache',
		'referer': 'https://testfol.io/',
		'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Linux"',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-origin',
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
	}

	data = {
		"start_date": str(min_year) + "-12-31",
		"end_date": "2100-01-01",
		"start_val": 10000,
		"adj_inflation": False,
		"cashflow": 0,
		"cashflow_freq": "Yearly",
		"rolling_window": 60,
		"backtests": [
			{
				"invest_dividends": True,
				"rebalance_freq": "Yearly",
				"allocation": {
					"VTITR": vti_allocation,
					"VXUSX": vxus_allocation
				},
				"drag": 0
			}
		]
	}

	response = requests.post(url, headers=headers, json=data)

	if response.status_code != 200:
		raise Exception(response.text)

	result = response.json()['stats'][0]
	result['us_allocation'] = vti_allocation

	with open(cache_filename, 'w') as f:
		json.dump(result, f, indent=4)
	
	#time.sleep(1)
	return result

start_min_year = 1980

while True:

	try:

		for min_year in range(start_min_year, 2021):

			data = []

			for i in range(0, 101):

				result = get_data(min_year, i)

				print(min_year, i, result['cagr'], result['std'])

				data.append(result)

			with open(f"data/{min_year}.json", 'w') as f:
				json.dump(data, f, indent=4)

			start_min_year = min_year + 1
	
	except Exception as e:
		print('Deu erro!', start_min_year, e)
		time.sleep(30)
		continue
	


