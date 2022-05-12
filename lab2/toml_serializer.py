from packing_tool import convert, deconvert, turn_obj_into_dict, restore_object_from_dict
import toml


class Toml:
    @staticmethod
    def dumps(obj):
        return toml.dumps(turn_obj_into_dict(convert(obj)))

    @staticmethod
    def dump(obj, file):
        with open(file, 'w+') as f:
            f.write(Toml.dumps(obj))

    @staticmethod
    def loads(s):
        return deconvert(restore_object_from_dict(toml.loads(s)))

    @staticmethod
    def load(file):
        with open(file, 'r') as f:
            return Toml.loads(f.read())






