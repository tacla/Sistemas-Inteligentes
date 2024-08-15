#####################################################################
## Adaline com regra delta
## Cesar Tacla, 15/8/2024
##
## Implementa um neurônio com uma entrada (x1= nota) e a entrada do limiar (x0)
## O neurônio deve aprender a regra 'se nota >= 0,6 então 1 (aprovado)'
##
## O programa:
## - plota a superfície de erro variando x1 de 0 até 1 para combinações
##   cartesianas dos pesos, w0 x w1, que estão no intervalo [-2, 2]
## - simula o treinamento com regra delta para um dataset (train_file) e
##   plota o ajuste dos pesos x erro mostrando o caminho seguido pelo
##   método da descida do gradiente (algortimo LSM)
##
## Para usar o programa, configure as variáveis da seção configuração abaixo.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

##################
## Configuracao
##################

## Parametros configuracao do neuronio adaline
w0_ini = -1        # peso inicial sinapse do limiar  x0
w1_ini = -1        # peso inicial sinapse da entrada x1
lr = 0.75          # learning rate
batch_size = 3     # tamanho do lote
train_file = 'adaline_nota.csv' # arquivo com dados de treinamento com 2 colunas x1, y_target

def train_adaline(csv_file, w0, w1, learning_rate, batch_size=1):
    # Leitura do arquivo CSV
    data = pd.read_csv(csv_file)

    # Lista para armazenar as triplas (w0, w1, E)
    results = []
    d_w0 = 0
    d_w1 = 0
    E = 0

    # Iteração sobre as linhas do arquivo
    for index, row in data.iterrows():
        x1 = row['x1']
        y_target = row['y_target']

        # Atualização dos pesos
        if index == 0  or (index % batch_size) != 0:
            # nao ajusta
            u = -1 * w0 + x1 * w1
            E += (y_target - u) ** 2
            if index == 0:
                results.append((w0, w1, E)) # para ver o ponto de partida
            d_w0 = d_w0 + (y_target - u) * -1
            d_w1 = d_w1 + (y_target - u) * x1
            print(f'{index}: u={u:.3f} w0={w0:.3f}, w1={w1:.3f} d_w0={d_w0:.3f} d_w1={d_w1:.3f}')
        else:
            # ajusta pesos
            w0 = w0 + learning_rate * d_w0/batch_size
            w1 = w1 + learning_rate * d_w1/batch_size
            u = -1 * w0 + x1 * w1
            E += (y_target - u) ** 2
            E = E/(2*batch_size)
            # Armazenamento da tripla (w0, w1, E)
            results.append((w0, w1, E))
            print(f'{index}: u={u:.3f} w0={w0:.3f}, w1={w1:.3f}\n')
            d_w0 = (y_target - u) * -1
            d_w1 = (y_target - u) * x1
            E = 0

    return results

# Define ranges for w_0 and w_1
w0 = np.linspace(-2, 2, 50)
w1 = np.linspace(-2, 2, 50)

# Meshgrid for w_0 and w_1
W0, W1 = np.meshgrid(w0, w1)

# Initialize E
E = np.zeros_like(W0)

# Compute the gradient of E with respect to w_0 and w_1
dE_dw0 = np.zeros_like(W0)
dE_dw1 = np.zeros_like(W1)

# Iterate over x1 values and accumulate the gradients
x1_values = np.arange(0, 1.01, 0.02)
for x1 in x1_values:
    y_targ = 1 if x1 >= 0.6 else 0     
    u = -1 * W0 + x1 * W1
    E += ((y_targ - u) ** 2)       
    dE_dw0 += -(y_targ - u)
    dE_dw1 += (y_targ - u) * x1
 
E = E/len(x1_values)*2  ## calcula o erro medio (acima estah acumulado)
dE_dw0 = dE_dw0/len(x1_values)*2
dE_dw1 = dE_dw1/len(x1_values)*2

# Plotting the 3D surface
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plotting
ax.plot_surface(W0, W1, E, cmap='gnuplot',  alpha=0.5)

### Simulate the training of one Adaline neuron
### separar os valores de w0, w1, e E para plotar o gráfico
results = train_adaline(train_file, w0_ini, w1_ini, lr, batch_size)
w0_values, w1_values, E_values = zip(*results)
ax.scatter(w0_values, w1_values, E_values, color='red')
ax.plot(w0_values, w1_values, E_values, marker='o')

# Setting labels
ax.set_xlabel(r'$w_0$')
ax.set_ylabel(r'$w_1$')
ax.set_zlabel(r'$E$')

# Show the plot
plt.show()


###
### VETOR GRADIENTE
###

# Set labels
ax.set_xlabel(r'$w_0$')
ax.set_ylabel(r'$w_1$')
ax.set_title(r'Contour plot of $E$')

# Show the plot
plt.show()

# Plot the gradient vectors


# Plot the contour (f-contour) of the function E
fig, ax = plt.subplots(figsize=(10, 7))
contour = ax.contour(W0, W1, E, levels=50, cmap='hsv')

# Add a colorbar
plt.colorbar(contour)

# Plot the gradient vectors
# coloquei -de_dw0 e -de_dw1 porque os vetores estavam no sentido do minimo da função E
ax.quiver(W0, W1, -dE_dw0, -dE_dw1, color='blue')

ax.scatter(w0_values, w1_values, color='blue')
# plotar a sequencia de ajuste dos pesos
ax.plot(w0_values, w1_values)

# Adicionar diferentes marcadores e cores para cada ponto
colors = plt.cm.viridis(np.linspace(0, 1, len(results)))
for i in range(len(results)):
    if i == len(results) - 1:
        label = f'X'
    else:
        label = f'{i}'
    ax.scatter(w0_values[i], w1_values[i], color=colors[i])
    ax.text(w0_values[i], w1_values[i], label)


# Set labels and title
ax.set_xlabel(r'$w_0$')
ax.set_ylabel(r'$w_1$')
ax.set_title(r'Contour plot of $E$ with Gradient Vectors')

# Show the plot
plt.show()
