import pandas

from models.horario import Horario
from models.materia import Materia
from models.professor import Professor
from models.turma import Turma


class DataParser:
    DADOS = {'name': 'Dados', 'columns': ['materia', 'turma', 'professor', 'quantidade_aulas']}
    CONFIGURACOES = {'name': 'Configuracoes', 'columns': ['horario_inicio']}
    RESTRICAO = {'name': 'Restricao', 'columns': ['professor', 'horario', 'dia_semana']}
    RESTRICOES_TURMA = {'name': 'Restricoes Turma', 'columns': ['turma', 'horario', 'dia_semana']}
    PREFERENCIAS = {'name': 'Preferencias', 'columns': ['professor', 'horario', 'dia_semana']}

    def __init__(self, file_path):
        self.name = file_path
        self.file = pandas.ExcelFile(file_path)

        self.parse_dados()
        self.parse_configuracoes()
        self.parse_preferencias()
        self.parse_restricao()
        self.parse_restricoes_turma()

    def get_data_frame(self, sheet_options):
        return self.file.parse(sheet_options.get('name'), names=sheet_options.get('columns'))

    def parse_dados(self):
        df = self.get_data_frame(self.DADOS)

        for i in range(len(df)):
            serie = df.iloc[i, :]
            materia = Materia(serie.get('materia'))
            turma = Turma(serie.get('turma'))
            professor = Professor(serie.get('professor'))
            quantidade_aulas = serie.get('quantidade_aulas')

            #TODO link data

    def parse_configuracoes(self):
        df = self.get_data_frame(self.CONFIGURACOES)

        for timedelta in df.get('horario_inicio'):
            Horario(timedelta)

    def parse_restricao(self):
        df = self.get_data_frame(self.RESTRICAO)

        for i in range(len(df)):
            serie = df.iloc[i, :]
            professor = Professor(serie.get('professor'))
            horario = serie.get('horario')
            dia_semana = serie.get('dia_semana')

            # TODO link data

    def parse_restricoes_turma(self):
        df = self.get_data_frame(self.RESTRICOES_TURMA)

        for i in range(len(df)):
            serie = df.iloc[i, :]
            turma = Turma(serie.get('turma'))
            horario = serie.get('horario')
            dia_semana = serie.get('dia_semana')

            # TODO link data

    def parse_preferencias(self):
        df = self.get_data_frame(self.RESTRICAO)

        for i in range(len(df)):
            serie = df.iloc[i, :]
            professor = Professor(serie.get('professor'))
            horario = serie.get('horario')
            dia_semana = serie.get('dia_semana')

            # TODO link data


if __name__ == "__main__":
    dt = DataParser("data/Escola_A.xlsx")
