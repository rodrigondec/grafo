from utils import classproperty


class UniqueCachedModel:
    def __new__(cls, *args, **kwargs):
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
        return getattr(cls, '_instances', {})

    @classmethod
    def get(cls, key):
        return cls.instances.get(key)


class CachedModel:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instances'):
            cls._instances = []

        instance = super().__new__(cls)
        cls._instances.append(instance)
        instance.index = cls.instances.index(instance)
        return instance

    @classproperty
    def instances(cls):
        return getattr(cls, '_instances', [])

    @classmethod
    def get(cls, index):
        return cls.instances[index]