## Prof. Cesar Tacla, UTFPR
## Sistemas Inteligentes

## Ilustracao do funcionamento feedfoward de uma Rede Multilayer Perceptron
## para classificacao binaria. Faz uma passagem da entrada ate a saida
## (nao implementa algoritmo de treinamento)
## Topologia da Rede [2 3 1] com funcao de ativacao sigmoide


# para criação de eixos 3D
from mpl_toolkits import mplot3d

import matplotlib.pyplot as plt
import numpy as np
import math


#ax = plt.axes(projection='3d')

# Implementa o feedforward 
def ff(X, W1, W2):
    """ X  vetor de caracteristicas para um exemplo ou instancia [x1, x2]
        W1 matriz de pesos para a camada escondida 1
        W2 matriz de pesos para a camada de saida
        retorna o valor de saida para o exemplo [x1, x2]
    """
    y = [0, 0, 0]

    # neuronio 1..3 da camada 1
    for i in range(0, len(W1)):
        u = (W1[i][0] * -1 + W1[i][1] * X[0] + W1[i][2]* X[1])
        y[i] = 1 / (1 + math.e**(-1 * u))


    u = W2[0][0] * -1 + W2[0][1] * y[0] + W2[0][2]* y[1] + W2[0][3]*y[2]
    y_out = 1 / (1 + math.e**(-1 * u))
    
    return y_out



# Cria duas features de entrada
x1 = np.arange(-6, 6, 0.025)
x2 = np.arange(-6, 6, 0.025)

# vetor de pesos para a camada escondida 1
W1 = [[-4.2, -2.3, -0.76],      # pesos para neuronio 1
      [-3.6, 1.3, -1.2],        # 2
      [-3.1, 0.39, 1.6]]        # 3

# vetor de pesos para a camada de saida
W2 = [[7.2, 3.4, 3.3, 3.4]]

# calcular a saida da rede para (X1, X2)
X1, X2 = np.meshgrid(x1, x2)
Y1 = ff([X1, X2], W1, W2)

# plotar saida do passo feedforward
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(X1, X2, Y1, 50, cmap='Reds')

ax.set_xlabel('X1')
ax.set_ylabel('X2')
ax.set_zlabel('Y')

# Procedimento de decisao - definir um threshold = 0.5
# Todos que estao acima de 0.5 sao exemplos positivos
Z = np.full_like(X1, 0.5)
ax.plot_surface(X1, X2, Z)

## simular inputs
for i in range(-6, 6, 1):
    print(f" Saida para [{i}, 0] = {ff([i, 0], W1, W2):.3f}")

plt.show()


