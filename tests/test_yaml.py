import unittest
from env_values import *

class SimpleYamlTest(unittest.TestCase):
    
    def setUp(self):
        self.env = env_values('tests/fixtures/simple.yml')
    
    def test_values(self):
        self.assertEqual(self.env['FOO'], 'foo')
        self.assertEqual(self.env['BAR'], 123)
        self.assertEqual(self.env['BAZ'], 1.23)
        self.assertEqual(self.env['FOO_BAR'], False)
        self.assertEqual(self.env['FOO_BAZ'], None)
        self.assertEqual(self.env['FOO_BAR_BAZ'], ['foo', 'bar', 'baz'])
        self.assertFalse('TEST' in self.env)
    
class NestedYamlTest(unittest.TestCase):
    
    def setUp(self):
        self.env = env_values('tests/fixtures/nested.yml')
    
    def test_nesting(self):
        self.assertEqual(self.env['FOO'], {'BAR': {'BAZ': 'foobarbaz'}})
        self.assertEqual(self.env['FOO_BAR'], {'BAZ': 'foobarbaz'})
        self.assertEqual(self.env['FOO_BAR_BAZ'], 'foobarbaz')
    
    def test_duplicate_keys(self):
        self.assertEqual(self.env['BAR'], {'BAZ': 'barbaz'})
        self.assertNotEqual(self.env['BAR_BAZ'], 'barbaz')
        self.assertEqual(self.env['BAR_BAZ'], 'baz')
    
    def test_nonstring_keys(self):
        self.assertEqual(self.env['BAZ'], {69: {1337: '1337', True: 'True', None: 'None'}})
        self.assertEqual(self.env['BAZ_69'], {1337: '1337', True: 'True', None: 'None'})
        self.assertEqual(self.env['BAZ_69_1337'], '1337')
        self.assertEqual(self.env['BAZ_69_True'], 'True')
        self.assertEqual(self.env['BAZ_69_None'], 'None')
