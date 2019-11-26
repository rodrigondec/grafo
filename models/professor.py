from models.db import CachedModel


class Professor(CachedModel):
    def __init__(self, value):
        self.value = value
