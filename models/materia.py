from models.db import UniqueCachedModel
from models.vertice import Vertice


class Materia(UniqueCachedModel):
    """
    Classe que representa uma matéria

    Attributes:
        value: nome da matéria
        vertices: conjunto de vertices ligados à materia

    Examples:
        'Filosofia'
    """
    def __init__(self, value):
        """
        Inicializa os valores da Materia criada ou retornada.

        Args:
            value: nome da materia
        """
        self.value = value
        if not hasattr(self, 'vertices'):
            self.vertices = set()

    def __str__(self):
        """
        Cria representação como string do objeto

        Returns:
            string de representação
        """
        return f'{self.value}'

    def add_vertice(self, value: Vertice):
        """
        Adiciona um vertice conjunto de vertices da materia

        Args:
            value: Vertice passado
        """
        self.vertices.add(value)
