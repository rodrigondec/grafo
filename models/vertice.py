from models.db import CachedModel


class Vertice(CachedModel):
    def __init__(self, professor, turma, materia):
        self.professor = professor
        self.turma = turma
        self.materia = materia
        self.horario = None

    def __str__(self):
        return f'{self.professor} {self.turma} {self.materia} {self.horario}'

    @property
    def professor(self):
        return self._professor

    @professor.setter
    def professor(self, value):
        self._professor = value
        value.add_vertice(self)

    @property
    def turma(self):
        return self._turma

    @turma.setter
    def turma(self, value):
        self._turma = value
        value.add_vertice(self)

    @property
    def materia(self):
        return self._materia

    @materia.setter
    def materia(self, value):
        self._materia = value
        value.add_vertice(self)


class CopiaVertice(CachedModel):
    def __init__(self, vertice: Vertice):
        self.vertice = vertice
        self.horario = None

    def __str__(self):
        return f'{self.vertice} | {self.horario}'

    @property
    def professor(self):
        return self.vertice.professor

    @property
    def turma(self):
        return self.vertice.turma

    @property
    def materia(self):
        return self.vertice.materia
