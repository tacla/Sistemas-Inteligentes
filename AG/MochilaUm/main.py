## Problema da Mochila
##
## Uma mochila com capacidade de massa limitada deve receber itens, cada qual com sua massa
## e valor. O problema consiste em encontrar a melhor combinação de itens de forma a maximizar o
## valor dos itens colocados na mochila respeitando a capacidade em Kg da mochila.
##
## Se desejar visualizar o melhor indivíduo por geração, faça PLOTAR_MELHOR = True. Ao término
## de cada execução, o programa plota o melhor fitness geração a geração. Feche a janela do gráfico
## e o programa seguirá automaticamente.
##
## A cada execução, o programa imprime a melhor mochila:
## <número de itens>, <somatória dos pesos>, <somatória dos valores>, <lista de itens presentes/ausentes>
##


import random
import matplotlib.pyplot as plt
from ag_operadores import AGOperadores
from mochila import Mochila

class AGMochila:
    NUM_EXECUCOES = 10        # número de execuções
    TAM_POP = 32              # tamanho da população
    MAX_GERACOES = 200        # máximo de gerações por execução
    PROB_CROSSOVER = 0.75     # probabilidade de cruzamento entre dois indivíduos
    PROB_MUTACAO = 0.04       # probabilidade de mutação sobre um indivíduo
    PENALIZACAO = True        # penalizar (True) ou reparar (False)
    OTIMO = 206               # se conhecido o valor otimo, coloque aqui para fazer contagem de quantas vezes encontrou o ótimo
    PLOTAR_MELHOR = False     # mostra um grafico com o melhor individuo de cada geracao
    ct_execucoes = 0          # conta as execucoes

    def __init__(self):
        self.m = [Mochila() for _ in range(2 * self.TAM_POP)]  # aloca espaço para pais e descendentes
        self.fitness = [0] * self.TAM_POP
        
        ## calcula o fitness da populacao inicial - somente para os pais
        for i in range(self.TAM_POP):
            self.m[i].encher_aleatoriamente() ## solucao factivel
        
        self.melhor_fit = 0              #
        self.melhor_mochila = None

        if AGMochila.PLOTAR_MELHOR:
            plt.title('Melhor individuo x geracao')
            plt.xlabel('Geracao')
            plt.ylabel('Melhor Fitness')

    def quick_sort(self, lower_index, higher_index):
        i = lower_index
        j = higher_index
        pivot = self.m_aux[lower_index + (higher_index - lower_index) // 2]
        while i <= j:
            while self.m_aux[i].valor > pivot.valor:
                i += 1
            while self.m_aux[j].valor < pivot.valor:
                j -= 1
            if i <= j:
                self.exchange_numbers(i, j)
                i += 1
                j -= 1
        if lower_index < j:
            self.quick_sort(lower_index, j)
        if i < higher_index:
            self.quick_sort(i, higher_index)

    def exchange_numbers(self, i, j):
        self.m_aux[i], self.m_aux[j] = self.m_aux[j], self.m_aux[i]

    def sort(self):
        if not self.m or len(self.m) == 0:
            return
        self.m_aux = self.m
        self.quick_sort(0, len(self.m) - 1)

    def executar_ag(self):
        geracao = 0
        sel = [0] * self.TAM_POP

        # para visualizar graficamente
        x_geracao = []
        y_melhor_fit = []

        while geracao < self.MAX_GERACOES:
            for i in range(self.TAM_POP):
                self.fitness[i] = self.m[i].valor
                
            sel = AGOperadores.sel_roleta(self.fitness, self.TAM_POP)
            j = 0
            while j < self.TAM_POP:
                a = j + self.TAM_POP
                b = j + self.TAM_POP + 1
                self.m[a] = self.m[sel[j]].clonar()
                self.m[b] = self.m[sel[j + 1]].clonar()
                
                AGOperadores.cross_um_ponto(self.m[a].colocado, self.m[b].colocado, Mochila.NUM_ITENS_DISPON, self.PROB_CROSSOVER)
                j += 2
                
            for i in range(self.TAM_POP, 2 * self.TAM_POP):
                AGOperadores.mutar(self.m[i].colocado, Mochila.NUM_ITENS_DISPON, self.PROB_MUTACAO)
                self.m[i].calcular_fitness(self.PENALIZACAO)
                
            self.sort()
            
            if self.m[0].valor > self.melhor_fit:
                self.melhor_fit = self.m[0].valor
                self.melhor_mochila = self.m[0]     

            if self.PLOTAR_MELHOR:
                x_geracao.append(geracao)
                y_melhor_fit.append(self.melhor_fit)
                #print(f"{geracao},{self.melhor_fit}")
                            
            geracao += 1
           

        if AGMochila.PLOTAR_MELHOR:
           plt.title(f'Melhor individuo x geracao (exec {AGMochila.ct_execucoes+1:d})')
           plt.plot(x_geracao, y_melhor_fit, marker='o', color='blue', markersize='2')
           plt.grid('y')
           plt.show()            # mostra a versao final do grafico
           
        return self.melhor_mochila  

if __name__ == "__main__":
    print(f"Capacidade em Kg da mochila: {Mochila.CAPACIDADE_KG}")
    print(f"Numero de itens disponiveis: {Mochila.NUM_ITENS_DISPON}")
    print()
    print(" A cada execução, o programa imprime a melhor mochila:\n")
    print("<número de itens>, <somatória dos pesos>, <somatória dos valores>, <lista de itens presentes/ausentes>")
    print()

    ct_otimo = 0
    melhor_mochila_geral = None  # de todas as execucoes
    melhor_fit_geral = 0
    melhor_num_itens_geral = 0
    
    AGMochila.ct_execucoes = 0
    while AGMochila.ct_execucoes < AGMochila.NUM_EXECUCOES:
        ag = AGMochila()
        best = ag.executar_ag()
        if best:
            print(best.imprimir_csv())

            if best.valor > melhor_fit_geral:
                if best.num_itens > melhor_num_itens_geral:
                    melhor_mochila_geral = best
            
            if best.valor == ag.OTIMO:
                ct_otimo += 1

               
            AGMochila.ct_execucoes += 1
    print()
    print(f"Encontradas {ct_otimo} sols otimas em {AGMochila.NUM_EXECUCOES} execucoes.\n")
    print(f"Melhor mochila em todas as execucoes")
    print(f"criterios: maior fitness > maior num. de itens > ordem de descoberta")
    if melhor_mochila_geral:
        melhor_mochila_geral.imprimir()
