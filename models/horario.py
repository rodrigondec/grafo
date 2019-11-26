from models.db import CachedModel


class Horario(CachedModel):
    def __init__(self, value):
        self.value = value
