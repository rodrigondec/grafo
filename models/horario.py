from db import UniqueCachedModel


class Horario(UniqueCachedModel):
    dias = {
        'dia_1': [],
        'dia_2': [],
        'dia_3': [],
        'dia_4': [],
        'dia_5': [],
    }

    def __init__(self, value):
        self.value = value

    @classmethod
    def popular_dias(cls):
        aulas_por_dia = len(cls.instances.values())
        if aulas_por_dia == 0:
            raise ValueError('Classe horário não tem nenhum horário para popular os dias')

        for index, key in enumerate(cls.dias.keys()):
            for cor in range(index*aulas_por_dia, (index+1)*aulas_por_dia):
                cls.dias[key].append(cor)
