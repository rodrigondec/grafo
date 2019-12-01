from unittest import TestCase

from data_parser import DataParser
from models.professor import Professor
from models.turma import Turma
from models.materia import Materia
from grafo.vertice import VerticeDados


class DataParserTestCase(TestCase):
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
