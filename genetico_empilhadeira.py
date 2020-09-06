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


# funcao que seleciona os pais, composto pelas listas de veiculos e empilhadeiras
# a funcao escolhe aleatoriamente um individuo da populacao de caminhoes e um individuo da populacao de empilhadeiras
# o metodo de selecao eh por torneio
def seleciona_pais(populacao, distancia_vazio, distancia_cheio, distancia_talhoes):
	pais = []
	for i in range(TAM_POPULACAO//2):
		l = []
		for j in range(2):
			individuo_1 = random.choice(populacao)
			maior_1 = calc_maior_tempo(distancia_vazio, distancia_cheio, individuo_1[0], individuo_1[1], distancia_talhoes)

			individuo_2 = random.choice(populacao)
			maior_2 = calc_maior_tempo(distancia_vazio, distancia_cheio, individuo_2[0], individuo_2[1], distancia_talhoes)

			if maior_1 < maior_2:
				melhor = individuo_1
				pior = individuo_2

			else:
				melhor = individuo_2
				pior = individuo_1

			r = random.uniform(0, 1)
			if r < PROB_MELHOR: l.append(melhor)
			else: l.append(pior)	

		pais.append(l)

	return pais


# funcao que gera uma nova populacao
# soma-se os filhos com os pais resultando em 200 individuos
# desses 200 os 100 melhores sao escolhidos
def gera_nova_populacao(pais, populacao, distancia_vazio, distancia_cheio, distancia_talhoes):
	for i in range(len(pais)):
		filho_1 = []
		filho_2 = []
		pai_1 = pais[i][0]
		pai_2 = pais[i][1]
		
		l1 = []
		l2 = []
		# crossover dos veiculos
		for j in range(len(pai_1[0])):
			filhos = gera_filhos_veiculo(pai_1[0][j], pai_2[0][j])
			l1.append(filhos[0])
			l2.append(filhos[1])

		filho_1.append(l1)
		filho_2.append(l2)
		
		# crossover das empilhadeiras
		filhos = gera_filhos_empilhadeira(pai_1[1], pai_2[1])
		filho_1.append(filhos[0])
		filho_2.append(filhos[1])
		
		# mutacao
		prob_mutacao = random.uniform(0, 1)
		if prob_mutacao < TAXA_MUTACAO:
			mutacao(filho_1, filho_2)

		populacao.append(filho_1)	
		populacao.append(filho_2)
	
	# seleciona os 100 melhores da populacao
	pop_and_fit = [[p, calc_maior_tempo(distancia_vazio, distancia_cheio, p[0],p[1], distancia_talhoes)] for p in populacao]
	pop_and_fit.sort(key=lambda x: x[1])
	pop = [x[0] for x in pop_and_fit[:100]]
	
	return pop
	

# funcao que retorna dois filhos para a matriz de veiculos
def gera_filhos_veiculo(pai_1, pai_2):
	# cruzamento em um ponto
	gene =	random.randint(0, len(pai_1))
	filho_1 = pai_1[:gene] + pai_2[gene:]
	filho_2 = pai_2[gene:] + pai_1[:gene]

	return filho_1, filho_2


# funcao que retorna dois filhos para a matriz de empilhadeiras
def gera_filhos_empilhadeira(pai_1, pai_2):
	# trasforma a matriz, cada pai, em uma unica lista para realizar o cruzamento
	l1 = []
	l2 = []
	for i in range(len(pai_1)):
		for j in range(len(pai_1[i])):
			l1.append(pai_1[i][j])

		for j in range(len(pai_2[i])):
			l2.append(pai_2[i][j])

	# cruzamento em um ponto
	gene =	random.randint(0, len(l1))

	# inicia os filhos com os genes de cada pai
	filho_1 = l1[:gene]
	filho_2 = l2[gene:]

	for i in range(len(l1)):
		# preenche o filho 1 com os genes restante do pai_2
		if l2[i] not in filho_1:
			filho_1.append(l2[i])
		#preenche o filho 2 com os genes restante do pai_1
		if l1[i] not in filho_2:
			filho_2.append(l1[i])
	
	f1 = []
	f2 = []
	# transforma a lista em uma matriz novamente
	elem_filho1 = 0
	elem_filho2 = 0
	for i in range(len(pai_1)):
		l1 = []
		l2 = []
		for j in range(len(pai_1[i])):
			l1.append(filho_1[elem_filho1])
			elem_filho1 += 1
		for k in range(len(pai_2[i])):
			l2.append(filho_2[elem_filho2])
			elem_filho2 += 1
		
		f1.append(l1)
		f2.append(l2)

	return f1, f2


# funcao que realiza a mutacao dos individuos
def mutacao(filho_1, filho_2):
	# mutacao 1 veiculos: troca dois elementos entre duas matrizes de talhoes diferentes
	t1 = random.randint(0, len(filho_1[0])-1)
	t2 = random.randint(0, len(filho_2[0])-1)
	a = random.randint(0, len(filho_1[0][t1])-1)
	b = random.randint(0, len(filho_2[0][t2])-1)
	
	aux = filho_1[0][t1][a]
	filho_1[0][t1][a] = filho_2[0][t2][b]
	filho_2[0][t2][b] = aux
	
	# mutacao 1 empilhadeiras: troca dois elementos em uma mesma matriz de empilhadeiras
	# escolhe qual filho sofrera a mutacao
	p = random.randint(0, 1)
	if p == 0: filho = filho_1
	else: filho = filho_2

	e1 = random.randint(0, len(filho[1])-1)
	e2 = random.randint(0, len(filho[1])-1)
	a = random.randint(0, len(filho[1][e1]) - 1)
	b = random.randint(0, len(filho[1][e2]) - 1)

	aux = filho[1][e1][a] 
	filho[1][e1][a] = filho[1][e2][b]
	filho[1][e2][b] = aux

	# calcula a probabilidade de mutacao novamente para realizar a 2 mutacao
	# a mutacao 2 so ocorre nos veiculos
	prob_mutacao = random.uniform(0, 1)
	if prob_mutacao < TAXA_MUTACAO:
		# mutacao 2: troca dois elementos em uma mesma matriz de talhoes
		p = random.randint(0, 1)
		if p == 0: filho = filho_1
		else: filho = filho_2

		t1 = random.randint(0, len(filho[0])-1)
		t2 = random.randint(0, len(filho[0])-1)
		a = random.randint(0, len(filho[0][t1]) - 1)
		b = random.randint(0, len(filho[0][t2]) - 1)

		aux = filho[0][t1][a] 
		filho[0][t1][a] = filho[0][t2][b]
		filho[0][t2][b] = aux
	

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

	# loop para achar o melhor resultado de acordo com o numero de geracoes
	for i in range(NUM_GERACOES):
		pais = seleciona_pais(populacao, distancia_vazio, distancia_cheio, distancia_talhoes)
		populacao = gera_nova_populacao(pais, populacao, distancia_vazio, distancia_cheio, distancia_talhoes)
	
	print(MELHOR_TEMPO)
	print(MELHOR_MATRIZ_VEICULO)
	print(MELHOR_MATRIZ_EMPILHADEIRA)
	
	return 0

if __name__ == '__main__':
	main()
