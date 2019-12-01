from unittest import TestCase

from data_parser import DataParser
from models.professor import Professor
from models.turma import Turma
from models.materia import Materia
from models.horario import Horario
from grafo.vertice import VerticeDados


class DataParserTestCase(TestCase):
    def tearDown(self):
        Professor._instances = {}
        Turma._instances = {}
        Materia._instances = {}
        Horario._instances = {}
        VerticeDados._instances = []

    def test_parse_dados(self):
        self.assertEqual(len(Professor.instances.values()), 0)
        self.assertEqual(len(Turma.instances.values()), 0)
        self.assertEqual(len(Materia.instances.values()), 0)
        self.assertEqual(len(VerticeDados.instances), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_dados()

        self.assertEqual(len(Professor.instances.values()), 28)
        self.assertEqual(len(Turma.instances.values()), 11)
        self.assertEqual(len(Materia.instances.values()), 11)
        self.assertEqual(len(VerticeDados.instances), 302)

    def test_parse_dados_turma(self):
        self.assertEqual(len(Turma.instances.values()), 0)
        self.assertEqual(len(VerticeDados.instances), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_dados()

        self.assertEqual(len(Turma.instances.values()), 11)
        self.assertEqual(len(VerticeDados.instances), 302)

        for instance in Turma.instances.values():
            lista_vertices = [vertice for vertice in VerticeDados.instances if vertice.turma == instance]
            self.assertEqual(lista_vertices, instance.vertices)

    def test_parse_dados_professor(self):
        self.assertEqual(len(Professor.instances.values()), 0)
        self.assertEqual(len(VerticeDados.instances), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_dados()

        self.assertEqual(len(Professor.instances.values()), 28)
        self.assertEqual(len(VerticeDados.instances), 302)

        for instance in Professor.instances.values():
            lista_vertices = [vertice for vertice in VerticeDados.instances if vertice.professor == instance]
            self.assertEqual(lista_vertices, instance.vertices)

    def test_parse_dados_materia(self):
        self.assertEqual(len(Materia.instances.values()), 0)
        self.assertEqual(len(VerticeDados.instances), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_dados()

        self.assertEqual(len(Materia.instances.values()), 11)
        self.assertEqual(len(VerticeDados.instances), 302)

        for instance in Materia.instances.values():
            lista_vertices = [vertice for vertice in VerticeDados.instances if vertice.materia == instance]
            self.assertEqual(lista_vertices, instance.vertices)

    def test_configuracoes(self):
        self.assertEqual(len(Horario.instances.values()), 0)
        self.assertEqual(len(Horario.dias['dia_1']), 0)
        self.assertEqual(len(Horario.dias['dia_2']), 0)
        self.assertEqual(len(Horario.dias['dia_3']), 0)
        self.assertEqual(len(Horario.dias['dia_4']), 0)
        self.assertEqual(len(Horario.dias['dia_5']), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_configuracoes()

        self.assertEqual(len(Horario.instances.values()), 6)

        self.assertEqual(len(Horario.dias['dia_1']), 6)
        self.assertEqual(Horario.dias['dia_1'], [0, 1, 2, 3, 4, 5])

        self.assertEqual(len(Horario.dias['dia_2']), 6)
        self.assertEqual(Horario.dias['dia_2'], [6, 7, 8, 9, 10, 11])

        self.assertEqual(len(Horario.dias['dia_3']), 6)
        self.assertEqual(Horario.dias['dia_3'], [12, 13, 14, 15, 16, 17])

        self.assertEqual(len(Horario.dias['dia_4']), 6)
        self.assertEqual(Horario.dias['dia_4'], [18, 19, 20, 21, 22, 23])

        self.assertEqual(len(Horario.dias['dia_5']), 6)
        self.assertEqual(Horario.dias['dia_5'], [24, 25, 26, 27, 28, 29])

