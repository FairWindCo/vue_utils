import unittest

from vue_utils.access_object.transform import get_obj_member


class TestStringMethods(unittest.TestCase):
    class TestClass:
        name = 50

        def get_name(self):
            return self.name

    def test_get_object_field(self):
        a = self.TestClass()
        self.assertEqual(50, get_obj_member(a, 'name'))

    def test_get_object_method(self):
        a = self.TestClass()
        self.assertEqual(a.get_name, get_obj_member(a, 'get_name'))

    def test_get_dict_value(self):
        a = {
            '10': 10
        }
        self.assertEqual(10, get_obj_member(a, '10'))

    def test_get_dict_incorrect_key(self):
        a = {
            '10': 10
        }
        self.assertIsNone(get_obj_member(a, 10))

    def test_get_list_item(self):
        a = [el for el in range(10)]
        self.assertEqual(9, get_obj_member(a, 9))

    def test_get_list_item_out_of_range(self):
        a = [el for el in range(10)]
        self.assertIsNone(get_obj_member(a, 11))

    def test_get_list_item_out_of_range_2(self):
        a = [el for el in range(10)]
        self.assertIsNone(get_obj_member(a, -11))

    def test_get_list_item_error_name(self):
        a = [el for el in range(10)]
        self.assertIsNone(get_obj_member(a, '-11'))

    def test_get_simple_int_object(self):
        a = 10
        self.assertIsNone(get_obj_member(a, '-11'))

    def test_get_simple_float_object(self):
        a = 10.0
        self.assertIsNone(get_obj_member(a, '-11'))

    def test_get_simple_bool_object(self):
        a = True
        self.assertIsNone(get_obj_member(a, '-11'))

    def test_get_simple_str_object(self):
        a = 'dfdg'
        self.assertIsNone(get_obj_member(a, '-11'))
