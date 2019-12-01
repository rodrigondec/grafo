from db import UniqueCachedModel


class Horario(UniqueCachedModel):
    def __init__(self, value):
        self.value = value
