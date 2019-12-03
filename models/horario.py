from models.db import UniqueCachedModel


class Horario(UniqueCachedModel):
    dias = [
        'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'
    ]

    def __init__(self, identificador, dia, hora):
        self.cor = list(self.instances.values()).index(self)
        self.identificador = identificador
        self.hora = hora
        self.dia = dia

    def __str__(self):
        return f'{self.identificador} {self.cor}'

    @staticmethod
    def construir_identificador(dia, hora):
        return f'{dia} {hora}'


class Hora(UniqueCachedModel):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'


def popular_horarios():
    aulas_por_dia = len(Hora.instances.values())
    if aulas_por_dia == 0:
        raise ValueError('Classe horário não tem nenhum horário para popular os dias')

    for dia in Horario.dias:
        for hora in Hora.instances.values():
            Horario(Horario.construir_identificador(dia, hora), dia, hora)
