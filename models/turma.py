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

        Args:
            value: nome da materia
        """
        self.value = value
        if not hasattr(self, 'vertices'):
            self.vertices = set()
            if not hasattr(self, 'restricoes'):
                self.restricoes = set()

    def __str__(self):
        """
        Cria representação como string do objeto

        Returns:
            string de representação
        """
        return f'{self.value}'

    def add_vertice(self, value: Vertice):
        """
        Adiciona um vertice à lista de vertices da turma

        Args:
            value: Vertice passado
        """
        self.vertices.add(value)

    def add_restricao(self, value: Horario):
        """
        Adiciona um Horario de restrição à lista de restrições vertices da turma

        Args:
            value: Horario passado
        """
        self.restricoes.add(value)
