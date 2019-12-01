from db import CachedModel


class VerticeDados(CachedModel):
    def __init__(self, professor, turma, materia):
        self.professor = professor
        self.turma = turma
        self.materia = materia
        self.cor = None

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


class CopiaVerticeDados(CachedModel):
    def __init__(self, vertice: VerticeDados):
        self.vertice = vertice
        self.cor = None

    @property
    def professor(self):
        return self.vertice.professor

    @property
    def turma(self):
        return self.vertice.turma

    @property
    def materia(self):
        return self.vertice.materia
