import random

# tempo de carregamento dos veiculos nos talhoes
TC = 2
# tempo de descarregamentos dos veiculos na fabrica
TD = 1

# valores utilizados no algoritmo genetico
TAM_POPULACAO = 100
NUM_GERACOES = 1000
TAXA_MUTACAO = 0.1
PROB_MELHOR = 0.8

# variaveis para guardar o melhor resultado encontrado pelo GA
MELHOR_TEMPO = 100000000000
MELHOR_MATRIZ_VEICULO = []
MELHOR_MATRIZ_EMPILHADEIRA = []

# quantidade de caminhoes disponiveis
QTD_CAMINHAO = 7
# quantidade de empilhadeiras disponiveis
QTD_EMPILHADEIRA = 4


# funcao que calcula a disponibilidade de cada veiculo
def calc_disponibilidade(disponibilidade, distancia_vazio, distancia_cheio, tempo_talhao):
	# se o talhão não espera pelo veículo
	if (disponibilidade + distancia_vazio) <= tempo_talhao:
		return 0
	else:
	# se o talhão precisa esperar pelo veículo
		return (disponibilidade + distancia_vazio + distancia_cheio + TD) - tempo_talhao


# funcao que calcula a disponibilidade de cada empilhadeira
def calc_tempo_empilhadeira(distancia, matriz_empilhadeira, tempo_talhao):
	# inicia cada empilhadeira com valor zero
	tempo_empilhadeira = []
	for i in range(QTD_EMPILHADEIRA):
		tempo_empilhadeira.append(0)
	
	for i in range(len(matriz_empilhadeira)):
		# se a empilhadeira atender apenas um talhao, sua disponibilidade sera igual ao tempo do talhao
		if len(matriz_empilhadeira[i]) == 1:
			tempo_empilhadeira[i] = tempo_talhao[matriz_empilhadeira[i][0] - 1]
		# se a empilhadeira atender varios talhoes, a disponibilidade sera igual ao tempo de cada talhao + a distancia até o próximo talhao
		else:
			for j in range(len(matriz_empilhadeira[i])):
				# verifica se eh o ultimo talhao atendido
				if j == len(matriz_empilhadeira[i]) - 1:
					tempo_empilhadeira[i] += tempo_talhao[matriz_empilhadeira[i][j] - 1]
				# tempo do talhao atual + a distancia até o próximo
				else:
					tempo_empilhadeira[i] += tempo_talhao[matriz_empilhadeira[i][j] - 1] + distancia[matriz_empilhadeira[j][0] - 1][matriz_empilhadeira[j][1] - 1]
					tempo_talhao[matriz_empilhadeira[i][j] - 1] = tempo_empilhadeira[i]
		

# funcao que calcula o tempo maximo da matriz de talhoes
def calc_maior_tempo(distancia_vazio, distancia_cheio, matriz_veiculo, matriz_empilhadeira, distancia_talhoes):
	global MELHOR_TEMPO, MELHOR_MATRIZ_VEICULO, MELHOR_MATRIZ_EMPILHADEIRA
	
	# lista de disponibilidade de cada veiculo
	disponibilidade = []
	for i in range(QTD_CAMINHAO):
		disponibilidade.append(0)
	
	# inicia todos os talhoes com o tempo igual a zero
	tempo_talhao = []
	for i in range(len(matriz_veiculo)):
		tempo_talhao.append(0)
	
	# se a empilhadeira estiver no talhao atualiza o tempo inicial igual a distancia do veiculo vazio
	for i in range(len(matriz_empilhadeira)):
		tempo_talhao[matriz_empilhadeira[i][0] - 1] = distancia_vazio[matriz_empilhadeira[i][0] - 1]

	# para todo talhao na matriz de talhoes
	for i in range(len(matriz_veiculo)):
		# para todo veiculo em cada talhao
		for j in matriz_veiculo[i]:
			tempo_talhao[i] += ((calc_disponibilidade(disponibilidade[j - 1], distancia_vazio[i], distancia_cheio[i], tempo_talhao[i])) + TC)
			disponibilidade[j - 1] = tempo_talhao[i] + distancia_cheio[i]

	# atualiza o tempo do talhao de acordo com a disponibilidade da empilhadeira
	calc_tempo_empilhadeira(distancia_talhoes, matriz_empilhadeira, tempo_talhao)

	# armazena o melhor resultado encontrado 
	if max(tempo_talhao) < MELHOR_TEMPO:
		MELHOR_TEMPO = max(tempo_talhao)
		MELHOR_MATRIZ_VEICULO = matriz_veiculo
		MELHOR_MATRIZ_EMPILHADEIRA = matriz_empilhadeira
	
	return max(tempo_talhao)
		

# funcao que cria a matriz de talhoes de acordo com a demanda de cada talhao
def gera_matriz_talhao(demanda_talhao):
	m = []
	for i in range(len(demanda_talhao)):
		n = []
		for j in range(demanda_talhao[i]):
			n.append((random.randint(1, QTD_CAMINHAO)))
		m.append(n)
	
	return m


#funcao que cria a matriz de empilhadeiras
def gera_matriz_empilhadeira(demanda_talhao):
	# lista que armazena a matriz de empilhadeiras
	m = []
	# lista que contem os atendimentos das empilhadeiras
	atendidos = []
	for i in range(QTD_EMPILHADEIRA):
		n = []
		while True:
			t = random.randint(1, len(demanda_talhao))
			if t not in atendidos:
				atendidos.append(t)
				break
		n.append(t)
		m.append(n)
	
	# variavel que percorre a matriz de empilhadeira para acresentar os talhoes restantes
	emp = 0
	for j in range(QTD_EMPILHADEIRA, len(demanda_talhao)):
		k = []
		# verifica se o talhao esta fora da matriz inicial de atendimento
		while True:
			t = random.randint(1, len(demanda_talhao))
			if t not in atendidos:
				atendidos.append(t)
				break		
		k.append(t)
		# escolhe qual empilhadeira ira atender o talhao escolhido
		e = random.randint(0, QTD_EMPILHADEIRA-1)
		m[emp] += k

		emp += 1
		if emp > QTD_EMPILHADEIRA:
			emp = 0
		
	return m


# funcao que gera a populacao inicial
def gera_populacao_inicial(demanda_talhao):
	populacao = []
	for i in range(TAM_POPULACAO):
		l = []
		t = gera_matriz_talhao(demanda_talhao)
		e = gera_matriz_empilhadeira(demanda_talhao)
		l.append(t)
		l.append(e)
		populacao.append(l)
			
	return populacao


# funcao que move o vagalume para o proximo mais brilhante
def move_vagalume(vagalume_1, vagalume_2):
	# escolhe qual matriz sofrera a mudanca
	r1 = random.randint(0, 1)
	# se for 1, a matriz de veiculos que sofrera mudanca
	if r1 == 0:
		tam = len(vagalume_1[0]) - 1
	# se for 2, a matriz de empilhadeiras que sofrera mudanca
	else:
		tam = len(vagalume_1[1]) - 1
	
	# escolhe uma das listas da matriz 
	r2 = random.randint(0, tam)
	# escolhe a posicao do elemento que sera trocado
	pos1 = random.randint(0, len(vagalume_1[r1][r2]) - 1)
	# procura o elemento no vagalume_2
	pos2 = 0
	for i in range(len(vagalume_1[r1][r2])):
		if vagalume_2[r1][r2][i] == vagalume_1[r1][r2][pos1]:
			pos2 = i
		
	aux1 = vagalume_2[r1][r2][pos1]
	aux2 = vagalume_2[r1][r2][pos2]
	vagalume_2[r1][r2][pos1] = aux2
	vagalume_2[r1][r2][pos2] = aux1


def main():
	# distancia da fábrica até os talhões (veiculo vazio)
	distancia_vazio = [1, 2, 3, 4, 5, 6, 7]
	
	# distancia do talhao até a fabrica (veiculo cheio)
	distancia_cheio = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]
	
	# demanda de cada talhão
	demanda = [3, 5, 4, 2, 3, 6, 2]

	# distancia entre os talhões
	distancia_talhoes = [[0, 1, 3, 6, 7, 9, 13], [1, 0, 2, 5, 6, 8, 12], [3, 2, 0, 3, 4, 6, 10], [6, 5, 3, 0, 1, 3, 7],
	[7, 6, 4, 1, 0, 2, 6], [9, 8, 6, 3, 2, 0, 4], [13, 12, 10, 7, 6, 4, 0]]
	
	populacao = gera_populacao_inicial(demanda)
	
	# intensidade de luz de cada indivíduo
	brilho = []
	for i in range(len(populacao)):
		brilho.append(calc_maior_tempo(distancia_vazio, distancia_cheio, populacao[i][0], populacao[i][1], distancia_talhoes))
	
	# coeficiente de absorção de luz	
	c = 2

	t = 0
	while t < NUM_GERACOES:
		for i in range(TAM_POPULACAO):
			for j in range(i):
				if brilho[j] < brilho[i]:
					move_vagalume(populacao[j], populacao[i])
					calc_maior_tempo(distancia_vazio, distancia_cheio, populacao[i][0], populacao[i][1], distancia_talhoes)
									
		t += 1

	print(MELHOR_TEMPO)
	print(MELHOR_MATRIZ_VEICULO)
	print(MELHOR_MATRIZ_EMPILHADEIRA)
	
	return 0

if __name__ == '__main__':
	main()
