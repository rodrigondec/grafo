from models.db import UniqueCachedModel
from models.vertice import Vertice


class Materia(UniqueCachedModel):
    """
    Classe que representa uma matéria. Ex.: 'Filosofia'
    """
    def __init__(self, value):
        """
        Inicializa os valores da Materia criada ou retornada.
        :param value: nome da materia
        """
        self.value = value
        if not hasattr(self, 'vertices'):
            self.vertices = []

    def __str__(self):
        """
        Cria representação como string do objeto
        :return: string de representação
        """
        return f'{self.value}'

    def add_vertice(self, value: Vertice):
        """
        Adiciona um vertice à lista de vertices da materia
        :param value: Vertice passado
        :return: NA
        """
        self.vertices.append(value)
