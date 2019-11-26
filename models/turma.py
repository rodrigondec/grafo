from models.db import CachedModel


class Turma(CachedModel):
    def __init__(self, value):
        self.value = value
