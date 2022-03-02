import MetaTrader5 as Mt5
import pandas as pd
from serie_temporal import SerieTemporal
import numpy as np
from datetime import datetime


class MetaTraderRequisitor:
    """Retorna os dados requisitados pelo Meta Trader 5"""

    def __init__(self, data_inicio: datetime, data_fim: datetime, ticker: str):
        self.ticker = ticker
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def diario(self) -> np.array:
        Mt5.initialize()
        dados = Mt5.copy_rates_range(self.ticker,
                                     Mt5.TIMEFRAME_D1,
                                     self.data_inicio,
                                     self.data_fim)
        Mt5.shutdown()
        return dados

    def semanal(self) -> np.array:
        Mt5.initialize()
        dados: np.array = Mt5.copy_rates_range(self.ticker,
                                               Mt5.TIMEFRAME_W1,
                                               self.data_inicio,
                                               self.data_fim)
        Mt5.shutdown()
        return dados

    def mensal(self) -> np.array:
        Mt5.initialize()
        dados: np.array = Mt5.copy_rates_range(self.ticker,
                                               Mt5.TIMEFRAME_MN1,
                                               self.data_inicio,
                                               self.data_fim)
        Mt5.shutdown()
        return dados


class MetaTraderTratamento:

    def __init__(self, dados: np.array, nome: str):
        self.dados = dados
        self.nome = nome

    def _numpy_para_dataframe(self):
        self.dados = pd.DataFrame(self.dados)

    def _filtrar_cols(self):
        self.dados = self.dados[['time', 'close']]

    def _tempo_int_para_datetime(self):
        self.dados['time'] = pd.to_datetime(self.dados['time'],
                                            unit='s')

    def _tempo_para_index(self):
        self.dados.index = self.dados['time']
        self.dados.drop('time', axis=1, inplace=True)

    def _ordenar_index(self):
        self.dados.sort_index(ascending=True, inplace=True)

    def _renomear_dataframe(self):
        self.dados.columns = [self.nome]
        self.dados.index.name = 'data'

    def tratar(self):
        self._numpy_para_dataframe()
        self._filtrar_cols()
        self._tempo_int_para_datetime()
        self._tempo_para_index()
        self._ordenar_index()
        self._renomear_dataframe()
        datas = self.dados.index.tolist()
        valores = self.dados[self.nome].tolist()
        return datas, valores


class MetaTraderAPI:

    def __init__(self, ticker: str, data_inicio: datetime, data_fim: datetime):
        self.ticker = ticker
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def diaria(self):
        requisitador = MetaTraderRequisitor(ticker=self.ticker,
                                            data_inicio=self.data_inicio,
                                            data_fim=self.data_fim)
        dados = requisitador.diario()
        datas, valores = MetaTraderTratamento(dados, self.ticker).tratar()
        serie_temporal = SerieTemporal(nome=self.ticker, datas=datas, valores=valores)
        return serie_temporal

    def semanal(self):
        requisitador = MetaTraderRequisitor(ticker=self.ticker,
                                            data_inicio=self.data_inicio,
                                            data_fim=self.data_fim)
        dados = requisitador.semanal()
        datas, valores = MetaTraderTratamento(dados, self.ticker).tratar()
        serie_temporal = SerieTemporal(nome=self.ticker, datas=datas, valores=valores)
        return serie_temporal

    def mensal(self):
        requisitador = MetaTraderRequisitor(ticker=self.ticker,
                                            data_inicio=self.data_inicio,
                                            data_fim=self.data_fim)
        dados = requisitador.mensal()
        datas, valores = MetaTraderTratamento(dados, self.ticker).tratar()
        serie_temporal = SerieTemporal(nome=self.ticker, datas=datas, valores=valores)
        return serie_temporal
