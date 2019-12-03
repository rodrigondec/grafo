import copy

from data_parser import parse, DATA
from models.horario import Horario
from models.vertice import Vertice, CopiaVertice
from models.utils import clean_db


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
        pass


if __name__ == "__main__":
    for data in DATA:
        g = Grafo(data)
        g.process()
        print(g)
        clean_db()
