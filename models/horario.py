from models.db import UniqueCachedModel


class Horario(UniqueCachedModel):
    """
    Classe que representa um horário (com coloração). ex.: Segunda 07:00
    """

    DIAS = [
        'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'
    ]

    def __init__(self, identificador, dia, hora):
        """
        Inicializa os valores do horário criado ou retornado
        :param identificador: Identificador único do horário
        :param dia: Dia do horário
        :param hora: Hora do horário
        """
        self.cor = list(self.instances.values()).index(self)
        self.identificador = identificador
        self.hora = hora
        self.dia = dia

    def __str__(self):
        """
        Cria representação como string do objeto
        :return: string de representação
        """
        return f'{self.identificador} {self.cor}'

    @staticmethod
    def construir_identificador(dia, hora):
        """
        Constroi um identificador único para o horário baseado em um dia e hora.
        :param dia: Dia passado
        :param hora: Hora passada
        :return: identificador único
        """
        return f'{dia} {hora}'


class Hora(UniqueCachedModel):
    """
    Classe que representa uma hora. Ex.: '07:00'
    """

    def __init__(self, value):
        """
        Inicializa os valores da Hora criada ou retornada.
        :param value: Hora
        """
        self.value = value

    def __str__(self):
        """
        Cria representação como string do objeto
        :return: string de representação
        """
        return f'{self.value}'


def popular_horarios():
    """
    Método auxiliar para pupular todos os horário possíveis baseado nas 'Horas' existentes.
    :return: NA
    """
    aulas_por_dia = len(Hora.instances.values())
    if aulas_por_dia == 0:
        raise ValueError('Classe horário não tem nenhum horário para popular os dias')

    for dia in Horario.DIAS:
        for hora in Hora.instances.values():
            Horario(Horario.construir_identificador(dia, hora), dia, hora)
