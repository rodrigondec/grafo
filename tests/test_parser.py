from unittest import TestCase

from data_parser import DataParser
from models.professor import Professor
from models.turma import Turma
from models.materia import Materia
from models.horario import Hora, Horario
from grafo.vertice import VerticeDados


class DataParserTestCase(TestCase):
    def tearDown(self):
        Professor._instances = {}
        Turma._instances = {}
        Materia._instances = {}
        Hora._instances = {}
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
        self.assertEqual(len(Hora.instances.values()), 0)
        self.assertEqual(len(Horario.instances), 0)

        dt = DataParser("data/Escola_A.xlsx")
        dt.parse_configuracoes()

        self.assertEqual(len(Hora.instances.values()), 6)
        self.assertEqual(len(Horario.instances), 30)

        lista_cores = [horario.cor for horario in Horario.instances]

        for cor in range(30):
            self.assertIn(cor, lista_cores)


