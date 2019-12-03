

class classproperty(object):
    """
    Classproperty utils
    """
    def __init__(self, getter):
        """
        Inicializa o classproperty
        Args:
            getter:
        """
        self.getter = getter

    def __get__(self, instance, owner):
        """
        Método get do classproperty
        Args:
            instance:
            owner:

        Returns:

        """
        return self.getter(owner)
