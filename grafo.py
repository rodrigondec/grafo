import copy
import logging
from typing import Set, Optional, Any

from data_parser import parse, DATA
from models.horario import Horario
from models.vertice import Vertice, CopiaVertice
from models.utils import clean_db
from models.turma import Turma
from models.professor import Professor


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING)

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

        self.vertices = Vertice.instances

        self._cores = set(Horario.instances.values())

        self._turmas = list(Turma.instances.values())
        self._turmas.sort(key=lambda _turma: len(_turma.vertices))

        self.context = {
            "turma": None,
            "cores_possiveis_turma": set(),
            "vertice": None
        }

    def __str__(self):
        """
        Cria representação como string do objeto
        Returns:
            String de representação
        """
        string = f"Escola {self.file_path}\n"
        string += f"Quantidade de cores: {len(Horario.instances.values())}\n"
        string += f"Quantidade de vértices: {len(self.vertices)}\n"
        string += f"Quantidade de vértices não coloridos: " \
                  f"{len([vertice for vertice in self.vertices if not vertice.horario])}\n"
        string += f"Preferências atendidas sobre o total de preferências: {self.preferencias_sobre_total}"
        return string

    @property
    def total_preferencias(self):
        total = 0
        for professor in Professor.instances.values():
            total += len(professor.preferencias)
        return total

    @property
    def preferencias_atendidas(self):
        total = 0
        for vertice in self.vertices:
            if vertice.horario is not None and vertice.horario in vertice.professor.preferencias:
                total += 1
        return total

    @property
    def preferencias_sobre_total(self):
        return self.preferencias_atendidas/self.total_preferencias

    @property
    def turmas(self):
        return self._turmas

    @property
    def turma(self) -> Turma:
        t: Optional[Turma] = self.context.get("turma")
        if t is None:
            raise ValueError("Turma é nula!")
        return t

    @turma.setter
    def turma(self, turma):
        self.context["turma"] = turma

    @property
    def todas_as_cores(self):
        return self._cores

    @property
    def vertice(self) -> Vertice:
        v: Optional[Vertice] = self.context.get("vertice")
        if v is None:
            raise ValueError("Vertice é nulo!")
        return v

    @vertice.setter
    def vertice(self, vertice):
        self.context["vertice"] = vertice

    @property
    def cores_possiveis_turma(self):
        return self.context.get("cores_possiveis_turma")

    @cores_possiveis_turma.setter
    def cores_possiveis_turma(self, cores_possiveis_turma):
        self.context["cores_possiveis_turma"] = cores_possiveis_turma

    @property
    def cores_possiveis_vertice(self):
        return self.cores_possiveis_turma - self.vertice.professor.restricoes

    @property
    def cores_preferiveis_vertice(self):
        return self.cores_possiveis_turma.intersection(self.vertice.professor.preferencias)

    def colorir(self):
        """
        Método responsavel por realizar a coloração do grafo.
        """
        for turma in self.turmas:
            self.turma = turma
            self.colorir_turma()

        self.colorir_vertices_originais()

    def colorir_turma(self):
        self.cores_possiveis_turma = self.todas_as_cores - self.turma.restricoes

        logger.info(f"Turma {self.turma} tem {len(self.turma.vertices)} vertices e {len(self.cores_possiveis_turma)} cores possíveis!")
        string = ""
        for cor in self.cores_possiveis_turma:
            string += f"{cor}, "
        logger.debug(f"Cores possiveis da turma: {string}")

        for vertice in self.turma.vertices:
            self.vertice = vertice
            self.colorir_copia_vertice()

        string = ""
        for cor in self.cores_possiveis_turma:
            string += f"{cor}, "
        logger.debug(f"Cores que sobraram: {string}")
        string = ""
        for vertice in self.turma.vertices:
            string += f"{vertice}"
            if vertice.copia is not None:
                string += f"{vertice.copia.horario}"
            string += ", "
        logger.debug(f"Vertices: {string}")
        logging.info(f"Vertices coloridos: "
                     f"{len([vertice for vertice in self.turma.vertices if vertice.copia is not None and vertice.copia.horario])}")
        logging.info(f"Vertices não coloridos: "
                     f"{len([vertice for vertice in self.turma.vertices if vertice.copia is None])}")
        string = ""
        for vertice in self.turma.vertices:
            if vertice.copia is None:
                string += f"{vertice}, "
        if string:
            logger.info(f"Vertices não coloridos: {string}")

    def colorir_copia_vertice(self):
        string = ""
        for cor in self.cores_possiveis_vertice:
            string += f"{cor}, "
        logger.debug(f"Cores possiveis do vertice: {string}")

        string = ""
        for cor in self.cores_preferiveis_vertice:
            string += f"{cor}, "
        logger.debug(f"Cores preferíveis do vertice: {string}")

        if self.cores_preferiveis_vertice:
            cor_aleatoria = self.cores_preferiveis_vertice.pop()
        elif self.cores_possiveis_vertice:
            cor_aleatoria = self.cores_possiveis_vertice.pop()
        else:
            return
        self.cores_possiveis_turma.remove(cor_aleatoria)

        copia_vertice = CopiaVertice(self.vertice)
        copia_vertice.horario = cor_aleatoria

    def colorir_vertices_originais(self):
        for vertice in self.vertices:
            vertice.colorir()


if __name__ == "__main__":
    for data in DATA:
        g = Grafo(data)
        g.colorir()
        print(g)
        clean_db()
