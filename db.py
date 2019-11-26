
class CachedModel:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instances'):
            cls._instances = {}

        _id = str(args[0])
        instance = cls._instances.get(_id)

        if instance is None:
            instance = super().__new__(cls)
            cls._instances[_id] = instance
        return instance
