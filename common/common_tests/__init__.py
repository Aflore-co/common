import pkgutil
import unittest
import itertools


class IntegrationTest(unittest.TestCase):

    def test_imports(self):
        """
        Catch dependencies missing from setup.py by checking that all submodules can be imported without error.
        """

        submodules = list(pkgutil.iter_modules(['common']))
        assert 'text_messaging' in itertools.chain.from_iterable(submodules)  # Sanity check

        for file_finder, name, _ in submodules:
            file_finder.find_module(name).load_module(name)