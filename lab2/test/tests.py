import unittest
from serializer.factory import Factory
import test_value


class SerializerTest(unittest.TestCase):
    def test_json_int(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.int_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_float(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.float_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_bool(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.bool_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_none(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.none_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_str(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.str_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_list(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.list1_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_tuple(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.tuple1_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_set(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.set1_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_dict(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.dict1_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_lambda(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.lambda_fanc
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(1), new_obj(1))

    def test_json_simple_func(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.simple_func
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(2), new_obj(2))

    def test_json_complex_func(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.complex_func
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(2), new_obj(2))

    def test_json_lib_func(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.math_func
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(2), new_obj(2))

    def test_json_simple_class_(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.Counter
        new_obj = factory.loads(factory.dumps(old_obj))
        a = old_obj()
        b = new_obj()
        a.inc()
        b.inc()
        self.assertEqual(a.value, b.value)

    def test_json_heritage_class_(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.DoubleCounter
        new_obj = factory.loads(factory.dumps(old_obj))
        first_object = old_obj()
        second_object = new_obj()
        first_object.inc()
        second_object.inc()
        self.assertEqual(first_object.value, second_object.value)

    def test_json_class_method(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.Employee
        new_obj = factory.loads(factory.dumps(old_obj))
        a = old_obj("dd", 2)
        b = new_obj("df", 4)
        self.assertEqual(a.display_count(), b.display_count())

    def test_json_inner_func(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.inner_func
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(2), new_obj(2))

    def test_json_recursive_func(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.factorial_recursive
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(5), new_obj(5))

    def test_json_class_method(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.Employee("dd", 2)
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj.name, new_obj.name)

    def test_yaml_int(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.int_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_float(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.float_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_bool(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.bool_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_none(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.none_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_str(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.str_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_list(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.list1_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_tuple(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.tuple1_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_set(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.set1_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_dict(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.dict1_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_lambda(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.lambda_fanc
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(1), new_obj(1))

    def test_yaml_simple_func(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.simple_func
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(2), new_obj(2))

    def test_yaml_complex_func(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.complex_func
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(2), new_obj(2))

    def test_yaml_lib_func(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.math_func
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(2), new_obj(2))

    def test_yaml_simple_class_(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.Counter
        new_obj = factory.loads(factory.dumps(old_obj))
        a = old_obj()
        b = new_obj()
        a.inc()
        b.inc()
        self.assertEqual(a.value, b.value)

    def test_yaml_heritage_class_(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.DoubleCounter
        new_obj = factory.loads(factory.dumps(old_obj))
        first_object = old_obj()
        second_object = new_obj()
        first_object.inc()
        second_object.inc()
        self.assertEqual(first_object.value, second_object.value)

    def test_yaml_class_method(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.Employee
        new_obj = factory.loads(factory.dumps(old_obj))
        a = old_obj("dd", 2)
        b = new_obj("df", 4)
        self.assertEqual(a.display_count(), b.display_count())

    def test_yaml_inner_func(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.inner_func
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(2), new_obj(2))

    def test_yaml_recursive_func(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.factorial_recursive
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(5), new_obj(5))

    def test_yaml_class_method(self):
        factory = Factory.create_serializer('.yaml')
        old_obj = test_value.Employee("dd", 2)
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj.name, new_obj.name)

    def test_toml_int(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.int_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_float(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.float_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_bool(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.bool_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_none(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.none_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_str(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.str_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_list(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.list1_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_tuple(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.tuple1_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_set(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.set1_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_dict(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.dict1_test
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_unknown_type(self):
        with self.assertRaises(Exception) as e:
            factory = Factory.create_serializer('.gggv')
        self.assertEqual("Unknown type of serialization", e.exception.args[0])

    def test_toml_lambda(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.lambda_fanc
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(1), new_obj(1))

    def test_toml_simple_func(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.simple_func
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(2), new_obj(2))

    def test_toml_complex_func(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.complex_func
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(2), new_obj(2))

    def test_toml_lib_func(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.math_func
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(2), new_obj(2))

    def test_json_simple_class_(self):
        factory = Factory.create_serializer('.json')
        old_obj = test_value.Counter
        new_obj = factory.loads(factory.dumps(old_obj))
        a = old_obj()
        b = new_obj()
        a.inc()
        b.inc()
        self.assertEqual(a.value, b.value)

    def test_toml_inner_func(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.inner_func
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(2), new_obj(2))

    def test_toml_recursive_func(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.factorial_recursive
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj(5), new_obj(5))

    def test_toml_class_method(self):
        factory = Factory.create_serializer('.toml')
        old_obj = test_value.Employee("dd", 2)
        new_obj = factory.loads(factory.dumps(old_obj))
        self.assertEqual(old_obj.name, new_obj.name)

    def test_yaml_from_file(self):
        factory = Factory.create_serializer('.yaml')
        with open("./test/test.yaml", "r") as f:
            new_obj = factory.load(f)
        old_obj = test_value.g
        with open("test/new.yaml", "w") as output_file:
            factory.dump(object, output_file)
        self.assertEqual(old_obj(), new_obj())

    def test_toml_from_file(self):
        factory = Factory.create_serializer('.toml')
        with open("./test/test.toml", "r") as f:
            new_obj = factory.load(f)
        old_obj = test_value.g
        with open("test/new.toml", "w") as output_file:
            factory.dump(object, output_file)
        self.assertEqual(old_obj(), new_obj())

    def test_json_from_file(self):
        factory = Factory.create_serializer('.json')
        with open("./test/test.json", "r") as f:
            new_obj = factory.load(f)
        old_obj = test_value.g
        with open("test/new.json", "w") as output_file:
            factory.dump(object, output_file)
        self.assertEqual(old_obj(), new_obj())


if __name__ == '__main__':
    unittest.main()
