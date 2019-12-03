from unittest import TestCase

from data_parser import DataParser
from models.professor import Professor
from models.turma import Turma
from models.materia import Materia
from models.horario import Hora, Horario
from models.vertice import Vertice
from models.utils import clean_db


class DataParserTestCase(TestCase):
    def tearDown(self):
        clean_db()

    def test_parse_dados(self):
        self.assertEqual(len(Professor.instances.values()), 0)
        self.assertEqual(len(Turma.instances.values()), 0)
        self.assertEqual(len(Materia.instances.values()), 0)
        self.assertEqual(len(Vertice.instances), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_dados()

        self.assertEqual(len(Professor.instances.values()), 28)
        self.assertEqual(len(Turma.instances.values()), 11)
        self.assertEqual(len(Materia.instances.values()), 11)
        self.assertEqual(len(Vertice.instances), 302)

    def test_parse_dados_turma(self):
        self.assertEqual(len(Turma.instances.values()), 0)
        self.assertEqual(len(Vertice.instances), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_dados()

        self.assertEqual(len(Turma.instances.values()), 11)
        self.assertEqual(len(Vertice.instances), 302)

        for instance in Turma.instances.values():
            lista_vertices = [vertice for vertice in Vertice.instances if vertice.turma == instance]
            self.assertEqual(lista_vertices, instance.vertices)

    def test_parse_dados_professor(self):
        self.assertEqual(len(Professor.instances.values()), 0)
        self.assertEqual(len(Vertice.instances), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_dados()

        self.assertEqual(len(Professor.instances.values()), 28)
        self.assertEqual(len(Vertice.instances), 302)

        for instance in Professor.instances.values():
            lista_vertices = [vertice for vertice in Vertice.instances if vertice.professor == instance]
            self.assertEqual(lista_vertices, instance.vertices)

    def test_parse_dados_materia(self):
        self.assertEqual(len(Materia.instances.values()), 0)
        self.assertEqual(len(Vertice.instances), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_dados()

        self.assertEqual(len(Materia.instances.values()), 11)
        self.assertEqual(len(Vertice.instances), 302)

        for instance in Materia.instances.values():
            lista_vertices = [vertice for vertice in Vertice.instances if vertice.materia == instance]
            self.assertEqual(lista_vertices, instance.vertices)

    def test_parse_configuracoes(self):
        self.assertEqual(len(Hora.instances.values()), 0)
        self.assertEqual(len(Horario.instances.values()), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_configuracoes()

        self.assertEqual(len(Hora.instances.values()), 6)
        self.assertEqual(len(Horario.instances.values()), 30)

        lista_cores = [horario.cor for horario in Horario.instances.values()]

        for cor in range(30):
            self.assertIn(cor, lista_cores)

    def test_parse_restricoes_professor(self):
        self.assertEqual(len(Hora.instances.values()), 0)
        self.assertEqual(len(Horario.instances.values()), 0)
        self.assertEqual(len(Professor.instances.values()), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_dados()
        dt.parse_configuracoes()
        dt.parse_restricoes_professor()

        self.assertEqual(len(Hora.instances.values()), 6)
        self.assertEqual(len(Horario.instances.values()), 30)
        self.assertEqual(len(Professor.instances.values()), 28)

        professor_1 = Professor('Professor 1')
        self.assertEqual(len(professor_1.restricoes), 1)
        self.assertIn(Horario.get(Horario.construir_identificador('Terça', Hora('10:40:00'))),
                      professor_1.restricoes)

        professor_2 = Professor('Professor 2')
        self.assertEqual(len(professor_2.restricoes), 2)
        self.assertIn(Horario.get(Horario.construir_identificador('Segunda', Hora('11:30:00'))),
                      professor_2.restricoes)
        self.assertIn(Horario.get(Horario.construir_identificador('Segunda', Hora('07:00:00'))),
                      professor_2.restricoes)

    def test_parse_restricoes_turma(self):
        self.assertEqual(len(Hora.instances.values()), 0)
        self.assertEqual(len(Horario.instances.values()), 0)
        self.assertEqual(len(Turma.instances.values()), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_dados()
        dt.parse_configuracoes()
        dt.parse_restricoes_turma()

        self.assertEqual(len(Hora.instances.values()), 6)
        self.assertEqual(len(Horario.instances.values()), 30)
        self.assertEqual(len(Turma.instances.values()), 11)

        turma_1 = Turma('1')
        self.assertEqual(len(turma_1.restricoes), 2)
        self.assertIn(Horario.get(Horario.construir_identificador('Terça', Hora('11:30:00'))),
                      turma_1.restricoes)
        self.assertIn(Horario.get(Horario.construir_identificador('Segunda', Hora('11:30:00'))),
                      turma_1.restricoes)

        turma_8 = Turma('8')
        self.assertEqual(len(turma_8.restricoes), 3)
        self.assertIn(Horario.get(Horario.construir_identificador('Quarta', Hora('11:30:00'))),
                      turma_8.restricoes)
        self.assertIn(Horario.get(Horario.construir_identificador('Segunda', Hora('11:30:00'))),
                      turma_8.restricoes)
        self.assertIn(Horario.get(Horario.construir_identificador('Quarta', Hora('10:40:00'))),
                      turma_8.restricoes)

    def test_parse_preferencias_professor(self):
        self.assertEqual(len(Hora.instances.values()), 0)
        self.assertEqual(len(Horario.instances.values()), 0)
        self.assertEqual(len(Professor.instances.values()), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_dados()
        dt.parse_configuracoes()
        dt.parse_preferencias()

        self.assertEqual(len(Hora.instances.values()), 6)
        self.assertEqual(len(Horario.instances.values()), 30)
        self.assertEqual(len(Professor.instances.values()), 28)

        professor_1 = Professor('Professor 1')
        self.assertEqual(len(professor_1.preferencias), 1)
        self.assertIn(Horario.get(Horario.construir_identificador('Segunda', Hora('10:40:00'))),
                      professor_1.preferencias)

        professor_2 = Professor('Professor 2')
        self.assertEqual(len(professor_2.preferencias), 2)
        self.assertIn(Horario.get(Horario.construir_identificador('Quarta', Hora('11:30:00'))),
                      professor_2.preferencias)
        self.assertIn(Horario.get(Horario.construir_identificador('Quarta', Hora('07:00:00'))),
                      professor_2.preferencias)
