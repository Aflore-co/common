import pkgutil
import unittest
import itertools

from common.test import BaseFlaskTestCase


class IntegrationTest(unittest.TestCase):

    def test_imports(self):
        """
        Catch dependencies missing from setup.py by checking that all submodules can be imported without error.
        """

        submodules = list(pkgutil.iter_modules(['common']))
        assert 'text_messaging' in itertools.chain.from_iterable(submodules)  # Sanity check

        for file_finder, name, _ in submodules:
            file_finder.find_module(name).load_module(name)

    def test_canonical_repr(self):
        x1 = {'type': 'x', 'id': 1, 'attributes': {'name': 'John'}, 'relationships': {}}
        x2 = {'type': 'x', 'id': 2, 'attributes': {'name': 'Neil'}, 'relationships': {}}
        x3 = {'type': 'x', 'id': 3, 'attributes': {'name': 'Doug'}, 'relationships': {}}
        y1 = {'type': 'y', 'id': 1, 'attributes': {'name': 'Mike'}}
        z1 = {'type': 'z', 'id': 1, 'attributes': {'name': 'Frank', 'a': 1, 'b': 2}, 'relationships': {}}

        t = BaseFlaskTestCase()
        assert t.canonicalRepr({'data': x2, 'included': [z1, x1, y1, x3,]}) == {'data': x2, 'included': [x1, y1, z1, x3]}
