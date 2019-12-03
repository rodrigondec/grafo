import pandas

from models.horario import Hora, popular_horarios, Horario
from models.materia import Materia
from models.professor import Professor
from models.turma import Turma
from models.vertice import Vertice

DATA = [
    "data/Escola_A.xlsx",
    "data/Escola_B.xlsx",
    "data/Escola_C.xlsx",
    "data/Escola_D.xlsx"
]


class DataParser:
    DADOS = {'name': 'Dados', 'columns': ['materia', 'turma', 'professor', 'quantidade_aulas']}
    CONFIGURACOES = {'name': 'Configuracoes', 'columns': ['horario_inicio']}
    RESTRICOES_PROFESSOR = {'name': 'Restricao', 'columns': ['professor', 'hora', 'dia_semana']}
    RESTRICOES_TURMA = {'name': 'Restricoes Turma', 'columns': ['turma', 'hora', 'dia_semana']}
    PREFERENCIAS = {'name': 'Preferencias', 'columns': ['professor', 'hora', 'dia_semana']}

    def __init__(self, file_path):
        self.name = file_path
        self.file = pandas.ExcelFile(file_path)

    def get_data_frame(self, sheet_options):
        return self.file.parse(sheet_options.get('name'), names=sheet_options.get('columns'))

    def parse(self):
        self.parse_dados()
        self.parse_configuracoes()
        self.parse_restricoes_professor()
        self.parse_restricoes_turma()
        self.parse_preferencias()

    def parse_dados(self):
        df = self.get_data_frame(self.DADOS)

        for i in range(len(df)):
            serie = df.iloc[i, :]
            materia = Materia(serie.get('materia'))
            turma = Turma(serie.get('turma'))
            professor = Professor(serie.get('professor'))
            quantidade_aulas = serie.get('quantidade_aulas')

            for aula in range(quantidade_aulas):
                Vertice(professor, turma, materia)

    def parse_configuracoes(self):
        df = self.get_data_frame(self.CONFIGURACOES)

        for timedelta in df.get('horario_inicio'):
            Hora(timedelta)

        popular_horarios()

    def parse_restricoes_professor(self):
        df = self.get_data_frame(self.RESTRICOES_PROFESSOR)

        for i in range(len(df)):
            serie = df.iloc[i, :]
            professor = Professor(serie.get('professor'))
            hora = Hora(serie.get('hora'))
            dia = serie.get('dia_semana')

            professor.add_restricao(Horario.get(Horario.construir_identificador(dia, hora)))

    def parse_restricoes_turma(self):
        df = self.get_data_frame(self.RESTRICOES_TURMA)

        for i in range(len(df)):
            serie = df.iloc[i, :]
            turma = Turma(serie.get('turma'))
            hora = Hora(serie.get('hora'))
            dia = serie.get('dia_semana')

            turma.add_restricao(Horario.get(Horario.construir_identificador(dia, hora)))

    def parse_preferencias(self):
        df = self.get_data_frame(self.PREFERENCIAS)

        for i in range(len(df)):
            serie = df.iloc[i, :]
            professor = Professor(serie.get('professor'))
            hora = Hora(serie.get('hora'))
            dia = serie.get('dia_semana')

            professor.add_preferencia(Horario.get(Horario.construir_identificador(dia, hora)))


def parse(file_path):
    dt = DataParser(file_path)
    dt.parse()


if __name__ == "__main__":
    parse(DATA[0])

