## AG - Problema da Mochila
## Codificação binária da mochila
## Inclui métodos de inicialização da mochila, de colocar e retirar itens

import random

class Mochila:
    CAPACIDADE_KG = 113
    NUM_ITENS_DISPON = 42
    ct_chamadas_fitness = 0

    peso_item = [3, 8, 12, 2, 8, 4, 4, 5, 1, 1, 8, 6, 4, 3,
                 3, 5, 7, 3, 5, 7, 4, 3, 7, 2, 3, 5, 4, 3,
                 7, 19, 20, 21, 11, 24, 13, 17, 18, 6, 15, 25, 12, 19]
    vlr_item = [1, 3, 1, 8, 9, 3, 2, 8, 5, 1, 1, 6, 3, 2,
                5, 2, 3, 8, 9, 3, 2, 4, 5, 4, 3, 1, 3, 2,
                14, 32, 20, 19, 15, 37, 18, 13, 19, 10, 15, 40, 17, 39]

    def __init__(self):
        self.peso = 0
        self.num_itens = 0
        self.valor = 0
        self.colocado = [False] * self.NUM_ITENS_DISPON
        self.random = random.Random()

    def clonar(self):
        clone = Mochila()
        clone.peso = self.peso
        clone.qtd_itens = self.num_itens
        clone.valor = self.valor
        clone.colocado = self.colocado[:]
        return clone

    def imprimir_csv(self):
        item_presente = [1 if self.colocado[i] else 0 for i in range(self.NUM_ITENS_DISPON)]
        return f"{self.num_itens},{self.peso},{self.valor}," + ','.join(map(str, item_presente))

    def imprimir(self):
        print("item\tpeso\tvalor")
        print("---------------------------------------------------------------")
        for i in range(self.NUM_ITENS_DISPON):
            if self.colocado[i]:
                print(f"[{i+1:03d}]\t{self.peso_item[i]}\t{self.vlr_item[i]:.2f}")
        print("---------------------------------------------------------------")
        print(f"Mochila com {self.num_itens} ITENS, {self.peso} KG e {self.valor} de VALOR")
        print("---------------------------------------------------------------")

    def calcular_fitness(self, penalizar):
        Mochila.ct_chamadas_fitness += 1
        if penalizar:
            self.calcular_fitness_penalizacao()
        else:
            self.calcular_fitness_reparacao()

    def calcular_fitness_penalizacao(self):
        self.peso = self.valor = self.num_itens = 0
        
        for i in range(self.NUM_ITENS_DISPON):
            if self.colocado[i]:
                self.peso += self.peso_item[i]
                self.valor += self.vlr_item[i]
                self.num_itens += 1
                
        if self.peso > Mochila.CAPACIDADE_KG:
            self.valor = int(self.valor * Mochila.CAPACIDADE_KG / self.peso)

    def calcular_fitness_reparacao(self):
        self.peso = self.valor = self.num_itens = 0
        
        for i in range(self.NUM_ITENS_DISPON):
            if self.colocado[i]:
                self.peso += self.peso_item[i]
                self.valor += self.vlr_item[i]
                self.num_itens += 1
                
        while self.peso > Mochila.CAPACIDADE_KG:
            self.retirar_item_aleatoriamente()

    def encher_aleatoriamente(self):
        sorteado = [False] * self.NUM_ITENS_DISPON
        qtd_sorteados = 0
        while self.peso < Mochila.CAPACIDADE_KG and qtd_sorteados < self.NUM_ITENS_DISPON:
            item = self.random.randint(0, self.NUM_ITENS_DISPON - 1)
            if not sorteado[item]:
                qtd_sorteados += 1
                sorteado[item] = True
                self.colocar_item(item)

    def retirar_item_aleatoriamente(self):
        if self.num_itens > 0:
            item = self.random.randint(0, self.NUM_ITENS_DISPON - 1)
            while not self.retirar_item(item):
                item = self.random.randint(0, self.NUM_ITENS_DISPON - 1)

    def colocar_item(self, item):
        if not self.colocado[item] and self.peso + self.peso_item[item] <= Mochila.CAPACIDADE_KG:
            self.num_itens += 1
            self.peso += self.peso_item[item]
            self.valor += self.vlr_item[item]
            self.colocado[item] = True
            return True
        return False

    def retirar_item(self, item):
        if self.colocado[item]:
            self.num_itens -= 1
            self.peso -= self.peso_item[item]
            self.valor -= self.vlr_item[item]
            self.colocado[item] = False
            return True
        return False


