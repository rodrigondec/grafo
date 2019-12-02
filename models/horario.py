from db import UniqueCachedModel, CachedModel


class Horario(CachedModel):
    dias = [
        'segunda', 'terça', 'quarta', 'quinta', 'sexta'
    ]

    def __init__(self, hora, dia):
        self.hora = hora
        self.dia = dia

    @property
    def cor(self):
        return self.index


class Hora(UniqueCachedModel):
    def __init__(self, value):
        self.value = value


def popular_horarios():
    aulas_por_dia = len(Hora.instances.values())
    if aulas_por_dia == 0:
        raise ValueError('Classe horário não tem nenhum horário para popular os dias')

    for dia in Horario.dias:
        for hora in Hora.instances.values():
            Horario(hora, dia)
