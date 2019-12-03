from models.db import UniqueCachedModel


class Horario(UniqueCachedModel):
    """Horario.
    Classe que representa um horário (com coloração).

    Examples:
        Segunda 07:00

    Attributes:
        identificador: identificador único
        dia: dia
        hora: hora
    """

    DIAS = [
        'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'
    ]

    def __init__(self, identificador, dia, hora):
        """
        Inicializa os valores do horário criado ou retornado

        Args:
            identificador: Identificador único do horário
            dia: Dia do horário
            hora: Hora do horário
        """
        self.cor = list(self.instances.values()).index(self)
        self.identificador = identificador
        self.hora = hora
        self.dia = dia

    def __str__(self):
        """
        Cria representação como string do objeto

        Returns:
            string de representação
        """
        return f'{self.identificador} {self.cor}'

    @staticmethod
    def construir_identificador(dia, hora):
        """
        Constroi um identificador único para o horário baseado em um dia e hora.

        Args:
            dia: Dia passado
            hora: Hora passada

        Returns:
            identificador único
        """
        return f'{dia} {hora}'


class Hora(UniqueCachedModel):
    """Hora.

    Classe que representa uma hora.

    Examples:
         '07:00'
    """

    def __init__(self, value):
        """
        Inicializa os valores da Hora criada ou retornada.

        Args:
            value: Hora
        """
        self.value = value

    def __str__(self):
        """
        Cria representação como string do objeto

        Returns:
            string de representação
        """
        return f'{self.value}'


def popular_horarios():
    """
    Método auxiliar para pupular todos os horário possíveis baseado nas 'Horas' existentes.
    """
    aulas_por_dia = len(Hora.instances.values())
    if aulas_por_dia == 0:
        raise ValueError('Classe horário não tem nenhum horário para popular os dias')

    for dia in Horario.DIAS:
        for hora in Hora.instances.values():
            Horario(Horario.construir_identificador(dia, hora), dia, hora)
