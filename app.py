import requests
import json
import os
import numpy as np
from scipy.optimize import curve_fit

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
	
	return result

def create_result_file():

	# Função para representar uma parábola
	def parabola(x, a, b, c):
		return a * x**2 + b * x + c

	def get_info(data):

		x = np.array([])
		y = np.array([])

		for row in data:
			x = np.append(x, row['std'])
			y = np.append(y, row['cagr'])

		# Ajuste da parábola aos dados
		params, _ = curve_fit(parabola, x, y)

		# Coeficientes da parábola
		a, b, c = params

		# Cálculo do vértice
		h = -b / (2 * a)
		k = a * h**2 + b * h + c

		# Find index of the closest point to the vertex
		index = int(np.argmin(np.abs(x - h)))

		return h, k, index

	files = os.listdir('data')

	# Sort files by name
	files = sorted(files)

	result = []

	for file in files:

		data = json.load(open('data/' + file))

		year = int(file.split('.')[0])

		std, cagr, index = get_info(data)

		row = {
			'year': year,
			'optimized_ex_us_allocation': index,
			'optimized_row': data[index],
			'entire_us_row': data[0],
			'entire_ex_us_row': data[-1],
		}

		result.append(row)

	with open('result.json', 'w') as f:
		json.dump(result, f, indent=4)

create_result_file()

