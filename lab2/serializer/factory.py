from serializer.json_serializer import Json
from serializer.toml_serializer import Toml
from serializer.yaml_serializer import Yaml


class Factory:
    @staticmethod
    def create_serializer(format):
        if format == ".json":
            return Json()

        elif format == ".toml":
            return Toml()

        elif format == ".yaml":
            return Yaml()

        else:
            raise Exception("Unknown type of serialization")
