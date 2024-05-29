import json
import matplotlib.pyplot as plt
import os

def save_plot(file):

	data = json.load(open('data/' + file))

	year = file.split('.')[0]

	# Extrair os dados para plotagem
	x = []
	y = []
	info = []  # Lista para armazenar informações adicionais

	for idx, row in enumerate(data):
		x.append(row['std'])
		y.append(row['cagr'])

	# Reset plot
	plt.clf()

	# Desenhar gráfico
	plt.scatter(x, y)
	plt.xlabel('Standard deviation')
	plt.ylabel('CAGR')
	plt.title('CAGR x Standard deviation')

	plt.savefig(f"charts/{year}.png")

files = sorted(os.listdir('data'))

for file in files:
	save_plot(file)