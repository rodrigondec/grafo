from models.db import CachedModel


class Vertice(CachedModel):
    """
    Classe que representa um vértice, contendo um professor, uma matéria, uma turma e um horário (cor).
    """
    def __init__(self, professor, turma, materia):
        """
        Inicializa os valores do Vertice criado
        :param professor: Professor passado
        :param turma: Turma passada
        :param materia: Materia passada
        """
        self.professor = professor
        self.turma = turma
        self.materia = materia
        self.horario = None

    def __str__(self):
        """
        Cria representação como string do objeto
        :return: string de representação
        """
        return f'{self.professor} {self.turma} {self.materia} {self.horario}'

    @property
    def professor(self):
        """
        Método para pegar o professor do vertice
        :return: professor
        """
        return self._professor

    @professor.setter
    def professor(self, value):
        """
        Método para atribuir o professor do vertice.
        E adiciona o vertice na lista de vertices do professor
        :return: NA
        """
        self._professor = value
        value.add_vertice(self)

    @property
    def turma(self):
        """
        Método para pegar a turma do vertice
        :return: turma
        """
        return self._turma

    @turma.setter
    def turma(self, value):
        """
        Método para atribuir a turma do vertice.
        E adiciona o vertice na lista de vertices da turma
        :return: NA
        """
        self._turma = value
        value.add_vertice(self)

    @property
    def materia(self):
        """
        Método para pegar a materia do vertice
        :return: materia
        """
        return self._materia

    @materia.setter
    def materia(self, value):
        """
        Método para atribuir a materia do vertice.
        E adiciona o vertice na lista de vertices da materia
        :return: NA
        """
        self._materia = value
        value.add_vertice(self)


class CopiaVertice(CachedModel):
    """
    Classe que representa uma copia de um vértice, contendo um vertice e um horário (cor).
    """
    def __init__(self, vertice: Vertice):
        """
        Inicializa os valores da Cópia de Vertice criada
        :param vertice: Vertice passado
        """
        self.vertice = vertice
        self.horario = None

    def __str__(self):
        """
        Cria representação como string do objeto
        :return: string de representação
        """
        return f'{self.vertice} | {self.horario}'

    @property
    def professor(self):
        """
        Método para pegar o professor do vertice original
        :return: professor
        """
        return self.vertice.professor

    @property
    def turma(self):
        """
        Método para pegar a turma do vertice original
        :return: turma
        """
        return self.vertice.turma

    @property
    def materia(self):
        """
        Método para pegar a materia do vertice original
        :return: materia
        """
        return self.vertice.materia
