from db import UniqueCachedModel


class Materia(UniqueCachedModel):
    def __init__(self, value):
        self.value = value
        if not hasattr(self, 'vertices'):
            self.vertices = []

    def add_vertice(self, value):
        self.vertices.append(value)