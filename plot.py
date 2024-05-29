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

""" files = sorted(os.listdir('data'))

for file in files:
	save_plot(file) """

# Carregar os dados do arquivo JSON
result = json.load(open('result.json'))

def plot(key):
    
    x = []
    y = [[],[],[]]
    y2 = []

    for row in result:
        x.append(row['year'])
        y[0].append(row['entire_us_row'][key])
        y[1].append(row['optimized_row'][key])
        y[2].append(row['entire_ex_us_row'][key])
        y2.append(row['optimized_ex_us_allocation'])

    plt.clf()

    fig, ax1 = plt.subplots()

    ax1.plot(x, y[0], label='US')
    ax1.plot(x, y[1], label='Optimized')
    ax1.plot(x, y[2], label='Ex-US')

    ax1.set_xlabel('Year')
    ax1.set_ylabel(key.upper())
    ax1.set_title(f"{key.upper()} Comparison")

    # Criar o segundo eixo y
    ax2 = ax1.twinx()
    ax2.plot(x, y2, label='Optimized allocation', color='black', linestyle='dotted', alpha=0.3)
    ax2.set_ylabel('Optimized allocation')

    # Adicionar as legendas
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    # Save plot
    plt.savefig(f"charts/{key}.png")

plot('cagr')
plot('std')