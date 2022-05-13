from serializer.packing_tool import convert, deconvert
import yaml


class Yaml:
    @staticmethod
    def dumps(obj):
        return yaml.dump(convert(obj))

    @staticmethod
    def dump(obj, file):
        file.write(Yaml.dumps(obj))

    @staticmethod
    def loads(s):
        return deconvert(yaml.load(s, Loader=yaml.FullLoader))

    @staticmethod
    def load(file):
        return Yaml.loads(file.read())
