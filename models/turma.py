"""
.. module:: turma
   :synopsis: turma
.. moduleauthor:: Rodrigo Castro <github.com/rodrigondec>
"""

from models.db import UniqueCachedModel
from models.vertice import Vertice
from models.horario import Horario


class Turma(UniqueCachedModel):
    """
    Classe que representa uma turma. Ex.: 'Turma A'
    """
    def __init__(self, value):
        """
        Inicializa os valores da Turma criada ou retornada.
        :param value: nome da materia
        """
        self.value = value
        if not hasattr(self, 'vertices'):
            self.vertices = []
            if not hasattr(self, 'restricoes'):
                self.restricoes = []

    def __str__(self):
        """
        Cria representação como string do objeto
        :return: string de representação
        """
        return f'{self.value}'

    def add_vertice(self, value: Vertice):
        """
        Adiciona um vertice à lista de vertices da turma
        :param value: Vertice passado
        :return: NA
        """
        self.vertices.append(value)

    def add_restricao(self, value: Horario):
        """
        Adiciona um Horario de restrição à lista de restrições vertices da turma
        :param value: Horario passado
        :return: NA
        """
        self.restricoes.append(value)
