from models.db import UniqueCachedModel


class Turma(UniqueCachedModel):
    def __init__(self, value):
        self.value = value
        if not hasattr(self, 'vertices'):
            self.vertices = []
            if not hasattr(self, 'restricoes'):
                self.restricoes = []

    def __str__(self):
        return f'{self.value}'

    def add_vertice(self, value):
        self.vertices.append(value)

    def add_restricao(self, value):
        self.restricoes.append(value)
