from dataclasses import dataclass
from typing import List
from datetime import datetime
'''Todo List'''
''' Colocar um __repr__ para printar os dados se tiver e nome da série'''


@dataclass
class SerieTemporal:

    nome: str
    datas: List[datetime]
    valores: List[float]

