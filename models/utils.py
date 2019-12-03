from models.horario import Hora, Horario
from models.materia import Materia
from models.professor import Professor
from models.turma import Turma
from models.vertice import Vertice, CopiaVertice


def clean_db():
    """
    Método auxiliar que reseta a persistência de todos os modelos.
    """
    Professor._instances = {}
    Turma._instances = {}
    Materia._instances = {}
    Hora._instances = {}
    Horario._instances = {}
    Vertice._instances = []
    CopiaVertice._instances = []
