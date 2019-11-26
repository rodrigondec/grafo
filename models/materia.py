from models.db import CachedModel


class Materia(CachedModel):
    def __init__(self, value):
        self.value = value
