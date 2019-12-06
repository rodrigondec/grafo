from models.db import UniqueCachedModel
from models.vertice import Vertice
from models.horario import Horario


class Professor(UniqueCachedModel):
    """
    Classe que representa um professor

    Attributes:
        value: Nome do professor
        vertices: Conjunto de vertices ligados ao professor
        restricoes: Conjunto de horarios de restrição do professor
        preferencias: Conjunto de horarios de preferência do professor

    Examples:
        'Aurélio'
    """
    def __init__(self, value):
        """
        Inicializa os valores do professor criado ou retornado.

        Args:
            value: nome do professor
        """
        self.value = value
        if not hasattr(self, 'vertices'):
            self.vertices = set()
        if not hasattr(self, 'restricoes'):
            self.restricoes = set()
        if not hasattr(self, 'preferencias'):
            self.preferencias = set()

    def __str__(self):
        """
        Cria representação como string do objeto

        Returns:
            string de representação
        """
        return f'{self.value}'

    def add_vertice(self, value: Vertice):
        """
        Adiciona um vertice ao conjunto de vertices do professor

        Args:
            value: Vertice passado
        """
        self.vertices.add(value)

    def add_restricao(self, value: Horario):
        """
        Adiciona um Horario de restrição ao conjunto de restrições do professor

        Args:
            value: Horario passado
        """
        self.restricoes.add(value)

    def add_preferencia(self, value: Horario):
        """
        Adiciona um Horario de preferência ao conjunto de preferẽncias do professor

        Args:
            value: Horario passado
        """
        self.preferencias.add(value)
