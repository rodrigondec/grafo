from models.db import CachedModel


class Vertice(CachedModel):
    """
    Classe que representa um vértice

    Attributes:
        professor: Professor do vertice
        materia: Materia do vertice
        turma: Turma do vertice
        horario: Horario do vertice (cor)
        copia: Copia do vertice
    """
    def __init__(self, professor, turma, materia):
        """
        Inicializa os valores do Vertice criado

        Args:
            professor: Professor passado
            turma: Turma passada
            materia: Materia passada
        """
        self.professor = professor
        self.turma = turma
        self.materia = materia
        self.horario = None
        self.copia = None

    def __str__(self):
        """
        Cria representação como string do objeto

        Returns:
            string de representação
        """
        string = f'{self.professor} {self.turma} {self.materia} {self.horario}'
        if self.colorido:
            string += f' {self.copia.horario}'
        return string

    @property
    def id(self):
        return f'{self.professor} {self.turma} {self.materia}'

    @property
    def professor(self):
        """
        Método para pegar o professor do vertice

        Returns:
            professor
        """
        return self._professor

    @professor.setter
    def professor(self, value):
        """
        Método para atribuir o professor do vertice.
        E adiciona o vertice na lista de vertices do professor

        Args:
            value: professor
        """
        self._professor = value
        value.add_vertice(self)

    @property
    def turma(self):
        """
        Método para pegar a turma do vertice

        Returns:
            turma
        """
        return self._turma

    @turma.setter
    def turma(self, value):
        """
        Método para atribuir a turma do vertice.
        E adiciona o vertice na lista de vertices da turma

        Args:
            value: turma
        """
        self._turma = value
        value.add_vertice(self)

    @property
    def materia(self):
        """
        Método para pegar a materia do vertice

        Returns:
            materia
        """
        return self._materia

    @materia.setter
    def materia(self, value):
        """
        Método para atribuir a turma do vertice.
        E adiciona o vertice na lista de vertices da turma

        Args:
            value: turma
        """
        self._materia = value
        value.add_vertice(self)

    def colorir(self):
        """
        Método que colore o vertice baseado na sua cópia.
        """
        if self.copia is not None:
            self.horario = self.copia.horario

    @property
    def colorido(self):
        """
        Propriedade de verificação se o vertice foi colorido ou não

        Returns:
            (boolean) se o vertice possui cor ou não
        """
        return self.copia is not None and self.copia.horario is not None


class CopiaVertice(CachedModel):
    """
    Classe que representa uma copia de um vértice

    Attributes:
        vertice: Vertice original
        horario: Horario da copia (cor)
    """
    def __init__(self, vertice: Vertice):
        """
        Inicializa os valores da Cópia de Vertice criada
        :param vertice: Vertice passado
        """
        vertice.copia = self
        self.vertice = vertice
        self.horario = None

    def __str__(self):
        """
        Cria representação como string do objeto

        Returns:
            string de representação
        """
        return f'{self.vertice} | {self.horario}'

    @property
    def professor(self):
        """
        Método para pegar o professor do vertice original
        Returns:
            professor
        """
        return self.vertice.professor

    @property
    def turma(self):
        """
        Método para pegar a turma do vertice original

        Returns:
            turma
        """
        return self.vertice.turma

    @property
    def materia(self):
        """
        Método para pegar a materia do vertice original

        Returns:
            materia
        """
        return self.vertice.materia
