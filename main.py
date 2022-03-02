from requester import MetaTraderAPI
from datetime import datetime, timedelta
from testes import eh_integrada
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from numpy import array
from serie_temporal import SerieTemporal
import numpy as np
from correlograma import correlogram

date_inicio = datetime(day=1, month=1, year=2021)
date_fim = datetime(day=1, month=3, year=2022)
dolar = MetaTraderAPI("WDO$", data_inicio=date_inicio, data_fim=date_fim).diaria()


# # Cai exponencialmente nos lags 1,2,3.
# plot_acf(array(dolar.valores))
# plt.show()
#
# # Results: Trunca no lag 1
# plot_pacf(array(dolar.valores))
# plt.show()
#
# plt.scatter(x=dolar.datas, y=dolar.valores)
# plt.show()
#
# print(eh_integrada(dolar.valores))
# # Teste de integração deu Verdadeiro.
#
# # Tirando a primeira ordem da série integrada
# dolar_diff = [np.nan]
# for index in range(len(dolar.valores)-1):
#     index_post = index + 1
#     valor = np.log(dolar.valores[index_post]) - np.log(dolar.valores[index])
#     dolar_diff.append(valor)
#
# dolar_diff = SerieTemporal(dolar.nome, dolar.datas, dolar_diff)
# print(dolar_diff)
#
# # Gráfico normal
# plt.scatter(x=dolar_diff.datas, y=dolar_diff.valores)
# plt.show()
#
# # Results: Trunca no lag 1
# plot_acf(array(dolar_diff.valores[1:]))
# plt.show()
#
# plot_pacf(array(dolar_diff.valores[1:]))
# plt.show()
# # Cai exponencialmente nos lags 1,2,3.
#
# correlogram(dolar_diff.datas[1:], dolar_diff.valores[1:])

# Modelos
# Modelo 1: ARIMA(1,1,0)
# Modelo 2: ARIMA(1,1,1)
# Modelo 3: ARIMA(1,1,2)
# Modelo 4: ARIMA(2,1,0)
# Modelo 5: ARIMA(2,1,1)
# Modelo 6: ARIMA(2,1,2)
# Modelo 7: ARIMA(0,1,1)
# Modelo 8: ARIMA(0,1,2)

orders = [(1, 1, 0), (1, 1, 1), (1, 1, 2), (2, 1, 0), (2, 1, 1), (2, 1, 2), (0, 1, 1), (0, 1, 2)]


# Modelo Escolhido
# Modelo ARIMA(1,1,1)
from statsmodels.tsa.arima.model import ARIMA
model = ARIMA(dolar.valores, order=(1, 1, 1)).fit()
pred = model.predict()
plt.plot(pred[1:])
plt.plot(dolar.valores[1:])
plt.show()
previsao = model.forecast()
if previsao > dolar.valores[-1]:
    sugestao = 'compre dólares'
else:
    sugestao = 'venda dólares'
print(f'Preço Estimado para o dia {dolar.datas[-1] + timedelta(days=1)}: {previsao}. Ou seja, {sugestao}')
