###
### Subida de encosta randômico (gulosa)
### Busca para tentar resolver um tabuleiro 9x9 Sudoku
###

import random
import sys

class Sudoku:
    def __init__(self, board):
        """
        board: lista 9x9 com números de 0 a 9
        0 representa célula vazia
        """
        self.board = [row[:] for row in board]  # cópia
        # posições fixas são as diferentes de zero
        self.fixed = {(i, j) for i in range(9) for j in range(9) if board[i][j] != 0}

    def play(self, row, col, value):
        """
        Faz uma jogada substituindo posição (row, col) por value (1 a 9)
        Somente se a posição não for fixa.
        """
        if (row, col) in self.fixed:
            raise ValueError(f"Posição ({row}, {col}) é fixa e não pode ser alterada.")
        if not (1 <= value <= 9):
            raise ValueError("O valor deve estar entre 1 e 9.")
        self.board[row][col] = value

    def violations(self):
        """
        Retorna o número total de violações das regras do Sudoku:
        - Números repetidos na mesma linha
        - Números repetidos na mesma coluna
        - Números repetidos no mesmo bloco 3x3
        - Zeros (posições vazias)
        Cada violação é contada separadamente.
        """
        v = 0

        # conta zeros
        v += sum(cell == 0 for row in self.board for cell in row)

        # checa linhas
        for i in range(9):
            v += self._count_duplicates(self.board[i])

        # checa colunas
        for j in range(9):
            col = [self.board[i][j] for i in range(9)]
            v += self._count_duplicates(col)

        # checa blocos 3x3
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                block = [
                    self.board[r][c]
                    for r in range(br, br + 3)
                    for c in range(bc, bc + 3)
                ]
                v += self._count_duplicates(block)

        return v

    def _count_duplicates(self, values):
        """
        Conta quantas repetições (violação) existem em uma sequência,
        desconsiderando zeros.
        Exemplo: [5,5,3,0,3] → duas violações (5 repetido e 3 repetido)
        """
        from collections import Counter
        counts = Counter(v for v in values if v != 0)
        return sum(c - 1 for c in counts.values() if c > 1)

    def is_solved(self):
        """
        Retorna True se o tabuleiro estiver completamente resolvido:
        - Nenhuma violação (violations() == 0)
        - Nenhum zero
        """
        return self.violations() == 0

    def get_current_moves(self):
        """
        Retorna uma lista de tuplas (linha, coluna, valor)
        para todas as posições que NÃO fazem parte do estado inicial.
        O valor é o número atual (pode ser 0 se ainda não preenchido).
        """
        moves=[]
    
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.fixed:
                    moves.append((i, j, self.board[i][j]))
        return moves

    def __str__(self):
        """
        Representação textual do tabuleiro para visualização.
        """
        lines = []
        for i, row in enumerate(self.board):
            if i % 3 == 0 and i > 0:
                lines.append("-" * 21)
            line = ""
            for j, val in enumerate(row):
                if j % 3 == 0 and j > 0:
                    line += "| "
                line += (str(val) if val != 0 else ".") + " "
            lines.append(line)
        return "\n".join(lines)


# ===== MAIN =====

##########################################
### Estratégias de geração de vizinhos
##########################################

def gerar_vizinhos1(sudoku, modifiable_positions):
    """
    Estratégia 1: altera diretamente o valor de uma célula modificável.
    Retorna a posição alterada e o novo valor.
    """
    i, j, _ = random.choice(modifiable_positions)
    novo_valor = random.randint(1, 9)
    sudoku.play(i, j, novo_valor)
    return (i, j, novo_valor)

def gerar_vizinhos2(sudoku, modifiable_positions):
    """
    Estratégia 2:  a fazer
    """
    return


##########################################
### MAIN  
##########################################


# a solução do tabuleiro
board1_sol = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

# o tabuleiro a ser resolvido (colocar zero nas posições para aumentar a 
# dificulade)

board = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 0, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 0, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

s = Sudoku(board)
print("\n*** Estado inicial ***")
modifiable_positions = s.get_current_moves()
print(f"Posições a serem preenchidas: {len(modifiable_positions)}")
prev_violations = s.violations()
print(f"Violações: {prev_violations}\n")
print(s)

calc_vizinhanca = 1    # define a escolha da estrategia de calc. de vizinhança

# === Preenchimento inicial aleatório ===
for i, j, _ in modifiable_positions:
    s.play(i, j, random.randint(1, 9))
    
print("\n-----------------------------------------------------")
print("Preenchimento aleatório inicial")
prev_violations = s.violations()
print("Violações:", prev_violations)
print(s)
print()
if  s.is_solved():
    print("*** solução encontrada ***")
    sys.exit(0)
print("\n")

# === Calculo da vizinhanca ===
for step in range(1, 10000):  # limite de segurança
    match calc_vizinhanca: 
        case 1:
            new_val = gerar_vizinhos1(s, modifiable_positions)
            current_violations = s.violations()   
            print(f"Iter. {step}: pos. ({i},{j}) ← {new_val} Violações: {current_violations}")
        case 2:     
            chg_pos = gerar_vizinhos2(s, modifiable_positions)
            current_violations = s.violations()
            print(f"iter. {step}: pos {chg_pos[0]}<>{chg_pos[1]} Violações: {current_violations}")
    
    if  s.is_solved():
        print("\nsolução encontrada")
        print(s)
        break

    if current_violations > prev_violations:
        print("\nNúmero de violações aumentou — sol. não encontrada.")
        print("Estado do tabuleiro\n")
        print(s)
        break

    prev_violations = current_violations

