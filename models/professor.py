from models.db import UniqueCachedModel
from models.vertice import Vertice
from models.horario import Horario


class Professor(UniqueCachedModel):
    """
    Classe que representa um professor. Ex.: 'Aurélio'
    """
    def __init__(self, value):
        """
        Inicializa os valores do professor criado ou retornado.
        :param value: nome do professor
        """
        self.value = value
        if not hasattr(self, 'vertices'):
            self.vertices = []
        if not hasattr(self, 'restricoes'):
            self.restricoes = []
        if not hasattr(self, 'preferencias'):
            self.preferencias = []

    def __str__(self):
        """
        Cria representação como string do objeto
        :return: string de representação
        """
        return f'{self.value}'

    def add_vertice(self, value: Vertice):
        """
        Adiciona um vertice à lista de vertices do professor
        :param value: Vertice passado
        :return: NA
        """
        self.vertices.append(value)

    def add_restricao(self, value: Horario):
        """
        Adiciona um Horario de restrição à lista de restrições do professor
        :param value: Horario passado
        :return: NA
        """
        self.restricoes.append(value)

    def add_preferencia(self, value: Horario):
        """
        Adiciona um Horario de preferência à lista de preferẽncias do professor
        :param value: Horario passado
        :return: NA
        """
        self.preferencias.append(value)
