from utils import classproperty


class UniqueCachedModel:
    """
    Classe a ser herdada para criar a parsistência dos objetos de sua classe
    filha em um dicionário (garantindo valor único para cada modelo)
    """
    def __new__(cls, *args, **kwargs):
        """
        Método que cria um novo objeto da classe salvando ele na persistência.
        Caso um objeto com o identificador já exista, retorna esse objeto.

        Args:
            args: list of args
            kwargs: dictionary of kwargs

        Returns:
             objeto achado ou criado
        """
        if not hasattr(cls, '_instances'):
            cls._instances = {}

        _id = str(args[0])
        instance = cls._instances.get(_id)

        if instance is None:
            instance = super().__new__(cls)
            cls._instances[_id] = instance
        return instance

    @classproperty
    def instances(cls):
        """Método que retorna o dicionário de persistência da classe.

        Returns:
            lista de objetos
        """
        return getattr(cls, '_instances', {})

    @classmethod
    def get(cls, key):
        """
        Método para pegar um objeto do dicionário de persistência da classe.

        Args:
            key: identificador do objeto.

        Returns:
            objeto do identificador OU None (caso objeto não exista)
        """
        return cls.instances.get(key)


class CachedModel:
    """
    Classe a ser herdada para criar a parsistência dos objetos de sua classe
    filha em uma lista (não garantindo valor único para cada modelo)
    """
    def __new__(cls, *args, **kwargs):
        """
        Método que cria um novo objeto da classe salvando ele na persistência.

        Args:
            args: list of args
            kwargs: dictionary of kwargs

        Returns:
             objeto criado
        """
        if not hasattr(cls, '_instances'):
            cls._instances = []

        instance = super().__new__(cls)
        cls._instances.append(instance)
        instance.index = cls.instances.index(instance)
        return instance

    @classproperty
    def instances(cls):
        """
        Método que retorna a lista de persistência da classe.

        Returns:
            lista de objetos da persistência
        """
        return getattr(cls, '_instances', [])

    @classmethod
    def get(cls, index):
        """
        Método para pegar um objeto da lista de persistência da classe.

        Args:
           index: indice do objeto.

        Returns:
            objeto do indice
        """
        return cls.instances[index]
