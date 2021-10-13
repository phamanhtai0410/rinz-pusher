class BaseEnum(object):
    @classmethod
    def enums(cls):
        values = list(cls.__dict__.values())
        values.remove(None)

        return values[1:]
