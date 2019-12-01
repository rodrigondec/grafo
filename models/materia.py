from db import UniqueCachedModel


class Materia(UniqueCachedModel):
    def __init__(self, value):
        self.value = value
        self.vertices = []

    def add_vertice(self, value):
        self.vertices.append(value)