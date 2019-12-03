from models.horario import Hora, Horario
from models.materia import Materia
from models.professor import Professor
from models.turma import Turma
from models.vertice import VerticeDados, CopiaVerticeDados


def clean_db():
    Professor._instances = {}
    Turma._instances = {}
    Materia._instances = {}
    Hora._instances = {}
    Horario._instances = {}
    VerticeDados._instances = []
    CopiaVerticeDados._instances = []