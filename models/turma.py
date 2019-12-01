from db import UniqueCachedModel


class Turma(UniqueCachedModel):
    def __init__(self, value):
        self.value = value
        self.vertices = []

    def add_vertice(self, value):
        self.vertices.append(value)
