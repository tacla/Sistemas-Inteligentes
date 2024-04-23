## Algoritmos genéticos
## Operadores de seleção, crossover e mutação para codificações binárias de indivíduos.
## Implementados:
## * crossover: um ponto, dois pontos
## 
import random
from typing import List
from bitarray import bitarray

class AGOperadores:
    @staticmethod
    def sel_roleta(fitness: List[float], qtd_cromossomos: int) -> List[int]:
        selecao = []
        fitness_rel = [f / sum(fitness) for f in fitness]
        for _ in range(qtd_cromossomos):
            r = random.random()
            acumulado = 0
            j = -1
            while acumulado < r:
                j = (j + 1) % len(fitness)
                acumulado += fitness_rel[j]
            selecao.append(j)
        return selecao
    
    @staticmethod
    def cross_dois_pontos(c1: bitarray, c2: bitarray, tam_bit_set: int, p_cross: float) -> None:
        if p_cross <= 0:
            return
        
        r = random.random()
        if r > p_cross:
            return
        
        p1, p2 = sorted(random.sample(range(tam_bit_set), 2))
        for i in range(p1, p2):
            c1[i], c2[i] = c2[i], c1[i]
        print("pontos de crossover =", p1, ",", p2)
    
    @staticmethod
    def cross_um_ponto(c1: bitarray, c2: bitarray, tam_bit_set: int, p_cross: float) -> None:
        if p_cross <= 0:
            return
        
        r = random.random()
        if r > p_cross:
            return
        
        p = random.randint(1, tam_bit_set - 1)
        for i in range(p, tam_bit_set):
            c1[i], c2[i] = c2[i], c1[i]
    
    @staticmethod
    def mutar(c: bitarray, tam_bit_set: int, p_mut: float) -> None:
        if p_mut <= 0:
            return
        
        for i in range(tam_bit_set):
            if random.random() <= p_mut:
                c[i] = not c[i]
