import logging
from typing import Optional

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

    Attributes:
        file_path: Caminho para o arquivo excell
        vertices: Lista de vertices pós processamento do excell
        _cores: Conjunto de cores (Horarios)
        _turmas: Lista de Turmas
        context: Dicionário de contexto para algorítmo de coloração
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
        """
        Método que calcula o total de vertices
        Returns: (int) total de vertices
        """
        return len(self.vertices)

    @property
    def preferencias_atendidas(self):
        """
        Método que calcula o total de preferências atendias na coloração dos vértices
        Returns: (int) total de preferências atendidas
        """
        total = 0
        for vertice in self.vertices:
            if vertice.colorido and vertice.horario in vertice.professor.preferencias:
                total += 1
        return total

    @property
    def preferencias_sobre_total(self):
        """
        Método que calcula a proporção de preferẽncias atendidas por preferências totais
        Returns: (float) porcentagem da proporção
        """
        return self.preferencias_atendidas/self.total_preferencias

    @property
    def turmas(self):
        """
        Método de acesso para turmas
        Returns: lista de turmas
        """
        return self._turmas

    @property
    def turma(self) -> Turma:
        """
        Método de acesso para o turma do context
        Returns: vertice
        """
        t: Optional[Turma] = self.context.get("turma")
        if t is None:
            raise ValueError("Turma é nula!")
        return t

    @turma.setter
    def turma(self, turma):
        """
        Método de atribuição da turma no context
        """
        self.context["turma"] = turma

    @property
    def todas_as_cores(self):
        """
        Método de acesso para lista de cores
        Returns: lista de cores
        """
        return self._cores

    @property
    def vertice(self) -> Vertice:
        """
        Método de acesso para o vertice do context
        Returns: vertice
        """
        v: Optional[Vertice] = self.context.get("vertice")
        if v is None:
            raise ValueError("Vertice é nulo!")
        return v

    @vertice.setter
    def vertice(self, vertice):
        """
        Método de atribuição do vertice no context
        """
        self.context["vertice"] = vertice

    @property
    def cores_possiveis_turma(self):
        """
        Método de acesso para o conjunto de cores possíveis da turma do context
        Returns: conjunto de cores possíveis para a turma
        """
        return self.context.get("cores_possiveis_turma")

    @cores_possiveis_turma.setter
    def cores_possiveis_turma(self, cores_possiveis_turma):
        """
        Método de atribuição do conjunto de cores possíveis da turma no context
        """
        self.context["cores_possiveis_turma"] = cores_possiveis_turma

    @property
    def cores_possiveis_vertice(self):
        """
        Método de acesso para o conjunto de cores possíveis da vertice do context
        Returns: conjunto de cores possíveis para o vertice
        """
        return self.cores_possiveis_turma - self.vertice.professor.restricoes

    @property
    def cores_preferiveis_vertice(self):
        """
        Método de acesso para o conjunto de cores preferíveis da vertice do context
        Returns: conjunto de cores preferíveis para o vertice
        """
        return self.cores_possiveis_turma & self.vertice.professor.preferencias

    def colorir(self):
        """
        Método responsavel por realizar a coloração do grafo.
        """
        for turma in self.turmas:
            self.turma = turma
            self.colorir_turma()

        for turma in self.turmas:
            if turma.tem_vertice_descolorido():
                self.turma = turma
                self.swap_turma()

        self.colorir_vertices_originais()

    def colorir_turma(self):
        """
        Método responsavel por realizar a coloração da turma do context.
        """
        self.cores_possiveis_turma = self.todas_as_cores - self.turma.restricoes

        self.log_turma()

        for vertice in self.turma.vertices:
            self.vertice = vertice
            self.colorir_copia_vertice()

        self.log_cores_sobrando()
        self.log_vertices_coloridos()

    def colorir_copia_vertice(self):
        """
        Método responsavel por realizar a coloração da copia do vertice do context.
        """
        self.log_vertice()

        if self.cores_preferiveis_vertice:
            cor_aleatoria = self.cores_preferiveis_vertice.pop()
        elif self.cores_possiveis_vertice:
            cor_aleatoria = self.cores_possiveis_vertice.pop()
        else:
            return
        self.cores_possiveis_turma.remove(cor_aleatoria)

        copia_vertice = CopiaVertice(self.vertice)
        copia_vertice.horario = cor_aleatoria

    def swap_turma(self):
        """
        Método responsavel por realizar o swap da dos vertices não coloridos da turma
        """
        self.cores_possiveis_turma = self.todas_as_cores - self.turma.restricoes

        vertices_nao_coloridos = {vertice for vertice in self.turma.vertices if not vertice.colorido}

        for vertice_nao_colorido in vertices_nao_coloridos:
            self.swap_vertice(vertice_nao_colorido, call_number=1)

    def swap_vertice(self, vertice_sofrendo_swap, call_number):
        """
        Método responsavel por realizar o swap de um vertice não colorido
        """
        if vertice_sofrendo_swap.copia is None:
            CopiaVertice(vertice_sofrendo_swap)

        restricoes_de_swap = vertice_sofrendo_swap.professor.restricoes | vertice_sofrendo_swap.turma.restricoes

        cores_possiveis_de_swap = self.cores_possiveis_turma - restricoes_de_swap

        vertices_coloridos = {vertice for vertice in self.turma.vertices if vertice.colorido}
        cores_utilizadas = {vertice.copia.horario for vertice in vertices_coloridos}

        vertices_possiveis_de_swap = {vertice for vertice in vertices_coloridos
                                      if vertice.copia.horario in cores_possiveis_de_swap}

        cores_que_sobraram = self.cores_possiveis_turma - cores_utilizadas

        self.log_swap_vertice(vertice_sofrendo_swap, restricoes_de_swap,
                              cores_possiveis_de_swap, vertices_possiveis_de_swap)

        vertice_escolhido = None

        if cores_que_sobraram:
            if vertices_possiveis_de_swap:
                for vertice_colorido in vertices_possiveis_de_swap:
                    if (vertice_colorido.copia.horario in cores_possiveis_de_swap and
                            cores_que_sobraram - (vertice_colorido.professor.restricoes |
                                                  vertice_colorido.turma.restricoes)):
                        vertice_sofrendo_swap.copia.horario = vertice_colorido.copia.horario
                        vertice_colorido.copia.horario = cores_que_sobraram.pop()
                        vertice_escolhido = vertice_colorido
                        break
            elif True:
                # @TODO Caso tenha vertice sobrando, e não tenha vertices possíveis de swap:
                # é preciso escolher um vertice e torná-lo um vertice possível de swap
                # através de um swap. Seria feito com recursão desse método com limitação de chamadas
                pass

        self.log_swapped_vertice(vertice_sofrendo_swap, vertice_escolhido)

        return vertice_sofrendo_swap if vertice_sofrendo_swap.colorido else None

    def colorir_vertices_originais(self):
        """
        Método responsavel por realizar a coloração dos vertices do grafo baseado em suas cópias
        """
        for vertice in self.vertices:
            vertice.colorir()

    def log_turma(self):
        """
        Método responsável pelo logging das informações iniciais da turma
        """
        logger.info(
            f"Turma {self.turma} tem {len(self.turma.vertices)} vertices e {len(self.cores_possiveis_turma)} cores possíveis!")
        string = ""
        for cor in self.cores_possiveis_turma:
            string += f"{cor}, "
        logger.debug(f"Cores possiveis da turma: {string}")

    def log_cores_sobrando(self):
        """
        Método responsável pelo logging das informações das cores que sobraram da turma
        """
        string = ""
        for cor in self.cores_possiveis_turma:
            string += f"{cor}, "
        logger.info(f"Cores que sobraram: {string}")

    def log_vertices_coloridos(self):
        """
        Método responsável pelo logging das informações dos vertices após a coloração da turma
        """
        string = ""
        for vertice in self.turma.vertices:
            string += f"{vertice}"
            if vertice.copia is not None:
                string += f"{vertice.copia.horario}"
            string += ", "
        logger.debug(f"Vertices: {string}")
        logging.info(f"Vertices coloridos: "
                     f"{len([vertice for vertice in self.turma.vertices if vertice.colorido])}")
        logging.info(f"Vertices não coloridos: "
                     f"{len([vertice for vertice in self.turma.vertices if not vertice.colorido])}")
        string = ""
        for vertice in self.turma.vertices:
            if not vertice.colorido:
                string += f"{vertice}, "
        if string:
            logger.info(f"Vertices não coloridos: {string}")

    def log_vertice(self):
        """
        Método responsável pelo logging das informações iniciais do vertice
        """
        string = ""
        for cor in self.cores_possiveis_vertice:
            string += f"{cor}, "
        logger.debug(f"Cores possiveis do vertice: {string}")

        string = ""
        for cor in self.cores_preferiveis_vertice:
            string += f"{cor}, "
        logger.debug(f"Cores preferíveis do vertice: {string}")

    @staticmethod
    def log_swap_vertice(vertice_sofrendo_swap, restricoes_de_swap,
                         cores_possiveis_de_swap, vertices_possiveis_de_swap):
        """
        Método responsável pelo logging das informações iniciais de swap
        """
        logger.info(f'Swap vertice : {vertice_sofrendo_swap}')
        string = ""
        for cor in restricoes_de_swap:
            string += f"{cor}, "
        logger.info(f'Restricoes de swap: {string}')
        string = ""
        for cor in cores_possiveis_de_swap:
            string += f"{cor}, "
        logger.info(f'Cores possiveis de swap: {string}')
        string = ""
        for vertice in vertices_possiveis_de_swap:
            string += f"{vertice}"
            if vertice.copia is not None:
                string += f"{vertice.copia.horario}"
            string += ", "
        logger.debug(f"Vertices possiveis de swap: {string}")

    @staticmethod
    def log_swapped_vertice(vertice_sofrendo_swap, vertice_escolhido):
        """
        Método responsável pelo logging das informações do swap realizado
        """
        logger.info(f'Vertice {vertice_sofrendo_swap} sofreu swap com {vertice_escolhido}')


if __name__ == "__main__":
    for data in DATA:
        g = Grafo(data)
        g.colorir()
        print(g)
        clean_db()
