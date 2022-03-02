import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf

def image(ac, time, timeseries):
    fig, ax = plt.subplots(nrows=1, ncols=4)
    fig.patch.set_visible(False)
    ax[0].barh(ac.lag, ac.AC)
    ax[0].invert_yaxis()
    ax[0].set_title("Autocorrelation")
    ax[0].set_xlim([-1,1])
    ax[1].barh(ac.lag, ac.PAC)
    ax[1].invert_yaxis()
    ax[1].set_title("Partial Autocorrelation")
    ax[1].set_xlim([-1,1])
    #Tirando os eixos X
    ax[0].get_xaxis().set_visible(False)
    ax[1].get_xaxis().set_visible(False)

    #Pegando os valores da tabela
    columns = ['lag','AC','PAC','Qstat', 'pvalue']
    ax[2].axis('off')
    ax[2].axis('tight')
    table = ax[2].table(
        cellText = np.round(ac[columns].values, decimals = 2),
        colLabels = np.array(columns),
        loc = 'center')

    table.auto_set_font_size(False)
    table.set_fontsize(8)
    ax[3].plot(time, timeseries)
    fig.tight_layout()
    plt.show()

def get_table(timeseries):
    #Calculando função de autocorrelação, Qstat e pvalue
    acfdf = pd.DataFrame(acf(timeseries, qstat = True), index = ['AC', 'Qstat','pvalue']).transpose()
    #Arredondando os pvalores para duas casas decimais
    acfdf.pvalue = acfdf.pvalue.round(2)

    pacfdf = pd.DataFrame(pacf(timeseries), columns = ['PAC'])

    #Juntando funções de autocorrelação total e parcial em um único dataframe.
    ac = pd.concat([acfdf, pacfdf], axis=1)
    ac['lag'] = ac.index

    ac = ac.iloc[1:]
    return ac

def correlogram(time,timeseries: list[float]):
    """
    :timeseries: Tem que ser pd.series do close.
    """
    # Calculando AC, Qstat e pvalue
    acfdf = pd.DataFrame(acf(timeseries, qstat=True), index=['AC', 'Qstat', 'pvalue']).transpose()
    # Arredondando pvalue para duas casas decimais
    acfdf.pvalue = acfdf.pvalue.round(2)

    pacfdf = pd.DataFrame(pacf(timeseries), columns=['PAC'])

    # Plotando
    ac = pd.concat([acfdf, pacfdf], axis=1)
    ac['lag'] = ac.index

    ac = ac.iloc[1:]

    image(ac, time, timeseries)
