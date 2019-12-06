import copy
import logging

from data_parser import parse, DATA
from models.horario import Horario
from models.vertice import Vertice, CopiaVertice
from models.utils import clean_db
from models.turma import Turma
from models.professor import Professor


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


class Grafo:
    """
    Classe que representa um grafo
    """
    def __init__(self, file_path):
        """
        Inicializa os valores do Grafo criado. Realiza o processamento do arquivo passado.
        Args:
            file_path: local do arquivo.
        """
        self.file_path = file_path

        parse(file_path)

        self.vertices = copy.copy(Vertice.instances)
        self.copia_vertices = [CopiaVertice(vertice) for vertice in self.vertices]

    def __str__(self):
        """
        Cria representação como string do objeto
        Returns:
            String de representação
        """
        string = f"Escola {self.file_path}\n"
        string += f"Quantidade de cores: {len(Horario.instances.values())}\n"
        string += f"Quantidade de vértices não coloridos: " \
                  f"{len([vertice for vertice in self.vertices if not vertice.horario])}\n"
        string += f"Preferências atendidas sobre o total de preferências: {None}\n\n"
        return string

    def process(self):
        """
        Método responsavel por realizar a coloração do grafo.
        """
        turmas = list(Turma.instances.values())
        turmas.sort(key=lambda _turma: len(_turma.vertices))

        cores = set(Horario.instances.values())
        for turma in turmas:
            cores_possiveis_turma = cores - turma.restricoes

            logger.info(f"Turma {turma} tem {len(turma.vertices)} vertices e {len(cores_possiveis_turma)} cores possíveis!")
            string = ""
            for cor in cores_possiveis_turma:
                string += f"{cor}, "
            logger.debug(f"Cores possiveis da turma: {string}")

            for vertice in turma.vertices:
                cores_possiveis_vertice = cores_possiveis_turma - vertice.professor.restricoes
                string = ""
                for cor in cores_possiveis_vertice:
                    string += f"{cor}, "
                logger.debug(f"Cores possiveis do vertice: {string}")
                cores_preferiveis_vertice = cores_possiveis_vertice.intersection(vertice.professor.preferencias)
                string = ""
                for cor in cores_preferiveis_vertice:
                    string += f"{cor}, "
                logger.debug(f"Cores preferíveis do vertice: {string}")

                if cores_preferiveis_vertice:
                    cor_aleatoria = cores_preferiveis_vertice.pop()
                elif cores_possiveis_vertice:
                    cor_aleatoria = cores_possiveis_vertice.pop()
                else:
                    break
                cores_possiveis_turma.remove(cor_aleatoria)

                copia_vertice = CopiaVertice(vertice)
                copia_vertice.horario = cor_aleatoria

            string = ""
            for cor in cores_possiveis_turma:
                string += f"{cor}, "
            logger.debug(f"Cores que sobraram: {string}")
            string = ""
            for vertice in turma.vertices:
                string += f"{vertice} ({vertice.copia.horario}), "
            logger.debug(f"Vertices: {string}")
            logging.info(f"Vertices coloridos: "
                         f"{len([vertice for vertice in turma.vertices if vertice.copia.horario])}")
            logging.info(f"Vertices não coloridos: "
                         f"{len([vertice for vertice in turma.vertices if vertice.copia.horario is None])}")
            string = ""
            for vertice in turma.vertices:
                string += f"{vertice}, " if vertice.copia.horario is None else ""
            if string:
                logger.info(f"Vertices não coloridos: {string}")


if __name__ == "__main__":
    for data in DATA:
        g = Grafo(data)
        g.process()
        print(g)
        clean_db()
        break
