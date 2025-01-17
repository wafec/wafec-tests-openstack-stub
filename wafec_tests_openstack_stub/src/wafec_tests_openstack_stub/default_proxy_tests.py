import unittest
import pickle
from wrapt import ObjectProxy
import copy
import json

from .default_proxy import DefaultProxy
from ._base import white_list
from ._default_proxy_iterator import DefaultProxyIterator
from wafec_tests_openstack_stub import create_proxy


class CreateProxyTests(unittest.TestCase):
    def setUp(self):
        self.dict_x = dict()
        self.dict_x['test1'] = 'value1'
        self.dict_x['test2'] = 'value2'
        self.dict_x['test3'] = dict()
        self.dict_x['test3']['test31'] = 'value31'

        self.list_x = list()
        self.list_x.append('test1')
        self.list_x.append('test2')
        self.list_x.append(list())
        self.list_x[2].append(dict())
        self.list_x[2][0]['test3'] = 'value3'

        self.inst_x = CustomTestClass('name1', 'description1')
        white_list.append(CustomTestClass.__module__)

    def test_create_proxy_with_dict(self):
        d = create_proxy(self.dict_x)
        self.assertIsInstance(d, ObjectProxy)
        self.assertIsInstance(d, dict)
        self.assertEqual('value1', d['test1'])
        self.assertNotIsInstance(d['test1'], ObjectProxy)

    def test_create_proxy_with_dict_when_keys_is_used(self):
        d = create_proxy(self.dict_x)
        for k1, k2 in zip(d.keys(), self.dict_x.keys()):
            self.assertEqual(k2, k1)
            self.assertNotIsInstance(k1, ObjectProxy)

    def test_create_proxy_with_dict_when_getting_proxy(self):
        d = create_proxy(self.dict_x)
        self.assertIsInstance(d['test3'], ObjectProxy)

    def test_create_proxy_with_dict_when_items_is_used(self):
        d = create_proxy(self.dict_x)
        for i, item1, item2 in zip(range(len(self.dict_x.keys())), self.dict_x.items(), d.items()):
            self.assertEqual(item1[0], item2[0])
            self.assertEqual(item1[1], item2[1])
            if i == 2:
                self.assertIsInstance(item2[1], DefaultProxy)
            else:
                self.assertIsNot(item2[1], DefaultProxy)
            self.assertNotIsInstance(item2[0], DefaultProxy)

    def test_create_proxy_with_list(self):
        l = create_proxy(self.list_x)
        self.assertIsInstance(l, DefaultProxy)

    def test_create_proxy_with_list_when_getting_text(self):
        l = create_proxy(self.list_x)
        text = l[0]
        self.assertNotIsInstance(text, DefaultProxy)

    def test_create_proxy_with_list_when_getting_other_list(self):
        l = create_proxy(self.list_x)
        other_list = l[2]
        self.assertIsInstance(other_list, DefaultProxy)

    def test_create_proxy_with_list_when_getting_dict(self):
        l = create_proxy(self.list_x)
        other_list = l[2]
        d = other_list[0]
        self.assertIsInstance(d, DefaultProxy)
        self.assertNotIsInstance(d['test3'], DefaultProxy)

    def test_create_proxy_with_elementary_when_int(self):
        n = create_proxy(int(10))
        self.assertIsInstance(n, int)
        self.assertNotIsInstance(n, DefaultProxy)

    def test_create_proxy_with_elementary_when_bool(self):
        b = create_proxy(bool(True))
        self.assertIsInstance(b, bool)
        self.assertNotIsInstance(b, DefaultProxy)

    def test_create_proxy_with_elementary_when_float(self):
        f = create_proxy(float(10.0))
        self.assertIsInstance(f, float)
        self.assertNotIsInstance(f, DefaultProxy)

    def test_create_proxy_with_elementary_when_text(self):
        d = create_proxy(str('test'))
        self.assertIsInstance(d, str)
        self.assertNotIsInstance(d, DefaultProxy)

    def test_create_proxy_with_obj(self):
        inst = create_proxy(self.inst_x)
        self.assertIsInstance(inst, DefaultProxy)

    def test_create_proxy_with_obj_when_getting_text(self):
        inst = create_proxy(self.inst_x)
        text = inst.name
        self.assertEqual('name1', text)
        self.assertNotIsInstance(text, DefaultProxy)

    def test_create_proxy_with_obj_when_getting_int(self):
        inst = create_proxy(self.inst_x)
        id = inst.id
        self.assertEqual(1, id)
        self.assertNotIsInstance(id, DefaultProxy)

    def test_create_proxy_with_obj_when_getting_dict(self):
        inst = create_proxy(self.inst_x)
        d = inst.data
        self.assertIsInstance(d, dict)
        self.assertIsInstance(d, DefaultProxy)

    def test_create_proxy_with_obj_when_getting_list(self):
        inst = create_proxy(self.inst_x)
        l = inst.collection
        self.assertIsInstance(l, list)
        self.assertIsInstance(l, DefaultProxy)

    def test_create_proxy_with_obj_when_callable_returns_text(self):
        inst = create_proxy(self.inst_x)
        c = inst.get_name
        text = c()
        self.assertTrue(callable(c))
        self.assertIsInstance(c, DefaultProxy)
        self.assertNotIsInstance(text, DefaultProxy)
        self.assertEqual(text, 'name1')

    def test_create_proxy_with_obj_when_callable_returns_dict(self):
        inst = create_proxy(self.inst_x)
        c = inst.get_data
        d = c()
        self.assertTrue(callable(c))
        self.assertIsInstance(d, dict)
        self.assertIsInstance(d, DefaultProxy)

    def test_create_proxy_with_obj_when_property_returns_text(self):
        inst = create_proxy(self.inst_x)
        text = inst.name_description
        self.assertNotIsInstance(text, DefaultProxy)

    def test_create_proxy_with_obj_when_property_returns_data(self):
        inst = create_proxy(self.inst_x)
        data = inst.more_data
        self.assertIsInstance(data, DefaultProxy)

    def test_create_proxy_with_dict_and_copy(self):
        d = create_proxy(self.dict_x)
        c = copy.copy(d)
        self.assertIsInstance(c, DefaultProxy)

    def test_create_proxy_with_dict_and_deep_copy(self):
        d = create_proxy(self.dict_x)
        c = copy.deepcopy(d)
        self.assertIsInstance(c, DefaultProxy)

    def test_create_proxy_with_list_and_copy(self):
        l = create_proxy(self.list_x)
        c = copy.copy(l)
        self.assertIsInstance(c, DefaultProxy)

    def test_create_proxy_with_list_and_deep_copy(self):
        l = create_proxy(self.list_x)
        c = copy.deepcopy(l)
        self.assertIsInstance(c, DefaultProxy)

    def test_create_proxy_with_dict_and_json_dumps(self):
        d = create_proxy({'test': 'value'})
        j = json.dumps(d)
        self.assertEqual('{"test": "value"}', j)

    def test_create_proxy_with_dict_and_pickle_dumps(self):
        o = {'test': 'value'}
        d = create_proxy(o)
        d_pickle_string = pickle.dumps(d)
        o_pickle_string = pickle.dumps(o)
        o_x = pickle.loads(o_pickle_string)
        d_x = pickle.loads(d_pickle_string)
        self.assertEqual(o_x['test'], d_x['test'])

    def test_create_proxy_with_obj_and_pickle_dumps(self):
        pickle_string = pickle.dumps(create_proxy(self.inst_x))
        inst = pickle.loads(pickle_string)
        self.assertIsInstance(inst, CustomTestClass)

    def test_create_proxy_with_list_when_iterable_is_used(self):
        l = create_proxy(self.list_x)
        for item in l:
            self.assertIsNotNone(item)

    def test_create_proxy_with_list_when_getting_iterable(self):
        l = create_proxy(self.list_x)
        it = iter(l)
        self.assertIsInstance(it, DefaultProxyIterator)
        self.assertTrue(hasattr(it, '__iter__'))

    def test_create_proxy_with_name(self):
        o = create_proxy(self.inst_x, 'test1')
        self.assertEqual('test1', o._self_trace)

    def test_create_proxy_with_name_when_dict(self):
        d = create_proxy(self.dict_x, 'test1')
        d3 = d['test3']
        self.assertEqual('test1 [test3]', d3._self_trace)

    def test_create_proxy_with_name_when_dict_and_first_name_is_not_provided(self):
        d = create_proxy(self.dict_x)
        d3 = d['test3']
        self.assertEqual('[test3]', d3._self_trace)

    def test_create_proxy_with_name_when_obj_is_returned_from_method(self):
        inst = create_proxy(self.inst_x, trace='test')
        result = inst.get_data()
        self.assertEqual('test .get_data', result._self_trace)


class CustomTestClassBase(object):
    def __init__(self, name):
        self.name = name


class CustomTestClass(CustomTestClassBase):
    def __init__(self, name, description):
        CustomTestClassBase.__init__(self, name)
        self.description = description
        self.data = dict()
        self.collection = list()
        self.id = int(1)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_data(self):
        return self.data

    @property
    def name_description(self):
        return f'{self.name} {self.description}'

    @property
    def more_data(self):
        return self.data