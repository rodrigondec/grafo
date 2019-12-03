from models.db import UniqueCachedModel


class Materia(UniqueCachedModel):
    def __init__(self, value):
        self.value = value
        if not hasattr(self, 'vertices'):
            self.vertices = []

    def __str__(self):
        return f'{self.value}'

    def add_vertice(self, value):
        self.vertices.append(value)
