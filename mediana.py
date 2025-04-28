import statistics
import matplotlib.pyplot as plt

dados = [ 3.9,	7.4, 10, 11.8, 2.3, 4.5, 10.5, 8.4, 15.6, 7.5, 18.8, 2.9, 2.3, 0.4, 5, 9, 5.5, 9.2, 
         12.4, 8.7, 4.5, 4.4, 10.6, 5.6, 8.5, 2.4, 17.8, 11.6, 9.8, 4.4, 7.1, 3.2, 
         2.7, 16.2, 2.7, 9.5, 13.1, 3.8, 6.3, 7.9, 4.8, 5.3, 12.9, 6.9, 6.3, 7.5, 2.6, 3.3, 7.5, 2.6]
#dados.sort()
#print(dados)

mediana = statistics.median(dados)
media = statistics.mean(dados)
moda = statistics.mode(dados)
print(mediana, '\n',media, '\n', moda)

plt.hist(dados, bins=3, edgecolor = 'black')

plt.xlabel('Valor')
plt.ylabel('Frequência')

plt.show()

