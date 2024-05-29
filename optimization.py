import json
import numpy as np
import os
from scipy.optimize import curve_fit

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

#print(data)