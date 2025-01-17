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
    """
    Classe responsável por processar as informações das planilhas excell e salvar as
    informções em suas devidas classes

    Attributes:
        file_path: Caminho do arquivo
        file: Arquivo do tipo Pandas
    """

    DADOS = {'name': 'Dados', 'columns': ['materia', 'turma', 'professor', 'quantidade_aulas']}
    CONFIGURACOES = {'name': 'Configuracoes', 'columns': ['horario_inicio']}
    RESTRICOES_PROFESSOR = {'name': 'Restricao', 'columns': ['professor', 'hora', 'dia_semana']}
    RESTRICOES_TURMA = {'name': 'Restricoes Turma', 'columns': ['turma', 'hora', 'dia_semana']}
    PREFERENCIAS = {'name': 'Preferencias', 'columns': ['professor', 'hora', 'dia_semana']}

    def __init__(self, file_path):
        """
        Inicializa o DataParser para um arquivo específico.

        Args:
            file_path: Arquivo a ser processado.
        """
        self.file_path = file_path
        self.file = pandas.ExcelFile(file_path)

    def get_data_frame(self, sheet_options):
        """
        Metodo para retornar um DataFrame do pandas (biblioteca de analise de
        planilhas) para uma das folhas do arquivo do DataParser.

        Args:
            sheet_options: variável que possui as configuracoes da folha da planilha

        Returns:
            DataFrame da folha escolhida da planilha
        """
        return self.file.parse(sheet_options.get('name'), names=sheet_options.get('columns'))

    def parse(self):
        """
        Metodo para chamar o processamento de todas as folhas do arquivo do
        DataParser
        """
        self.parse_dados()
        self.parse_configuracoes()
        self.parse_restricoes_professor()
        self.parse_restricoes_turma()
        self.parse_preferencias()

    def parse_dados(self):
        """
        Analisa e salva todas as informações que estão na planilha Dados do
        arquivo. Criando os modelos 'Materia', 'Turma', 'Professor' e 'Vertice'.
        """
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
        """
        Analisa e salva todas as informações que estão na planilha
        Configuracoes do arquivo. Criando os modelos 'Hora' e 'Horario'
        """
        df = self.get_data_frame(self.CONFIGURACOES)

        for timedelta in df.get('horario_inicio'):
            Hora(timedelta)

        popular_horarios()

    def parse_restricoes_professor(self):
        """
        Analisa e salva todas as informações que estão na planilha
        Restricoes do arquivo. Salvando as restricoes de Horario no devido
        Professor
        """
        df = self.get_data_frame(self.RESTRICOES_PROFESSOR)

        for i in range(len(df)):
            serie = df.iloc[i, :]
            professor = Professor(serie.get('professor'))
            hora = Hora(serie.get('hora'))
            dia = serie.get('dia_semana')

            professor.add_restricao(Horario.get(Horario.construir_identificador(dia, hora)))

    def parse_restricoes_turma(self):
        """
        Analisa e salva todas as informações que estão na planilha
        Restricoes Turma do arquivo. Salvando as restricoes de Horario na
        devida Turma
        """
        df = self.get_data_frame(self.RESTRICOES_TURMA)

        for i in range(len(df)):
            serie = df.iloc[i, :]

            turma = Turma(serie.get('turma'))
            hora = Hora(serie.get('hora'))
            dia = serie.get('dia_semana')

            turma.add_restricao(Horario.get(Horario.construir_identificador(dia, hora)))

    def parse_preferencias(self):
        """Analisa e salva todas as informações que estão na planilha
        'Preferencias' do arquivo. Salvando as preferências de 'Horario' no
        devido 'Professor'
        """
        df = self.get_data_frame(self.PREFERENCIAS)

        for i in range(len(df)):
            serie = df.iloc[i, :]

            professor = Professor(serie.get('professor'))
            hora = Hora(serie.get('hora'))
            dia = serie.get('dia_semana')

            professor.add_preferencia(Horario.get(Horario.construir_identificador(dia, hora)))


def parse(file_path):
    """
    Função auxiliar para criar um DataParser e processar seu arquivo.

    Args:
        file_path: Arquivo a ser processado
    """
    dt = DataParser(file_path)
    dt.parse()
