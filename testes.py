# Testes de estacionariedade
from statsmodels.tsa.stattools import adfuller
from typing import List


# Teste de Raiz Unitária
def eh_integrada(timeseries: list):
    """
    :timeseries: Tem que ser pd.series do close.
    """
    adf_c = adfuller(timeseries, autolag='AIC', regression='c')
    adf_ct = adfuller(timeseries, autolag='AIC', regression='ct')
    if adf_c[1] > 0.05 and adf_ct[1] > 0.05:
        unitroot = True
    else:
        # Pegando os p_valores da variável 'const'
        adf_c = adfuller(timeseries, autolag='AIC', regression='c', regresults=True)
        lags = adfuller(timeseries, autolag='AIC', regression='c')[2]
        c_pvalue = list(adf_c[-1].autolag_results.values())[lags].pvalues[0]

        adf_ct = adfuller(timeseries, autolag='AIC', regression='ct', regresults=True)
        lags = adfuller(timeseries, autolag='AIC', regression='ct')[2]
        ct_pvalue = list(adf_ct[-1].autolag_results.values())[lags].pvalues[0]
        if c_pvalue < ct_pvalue:
            if adf_c[1] > 0.05:
                unitroot = True
            else:
                unitroot = False
        else:
            if adf_ct[1] > 0.05:
                unitroot = True
            else:
                unitroot = False
    return unitroot
