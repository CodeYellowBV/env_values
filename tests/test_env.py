import os
import unittest
from env_values import *
    
class OverrideTest(unittest.TestCase):
    
    def test_yaml_dotenv(self):
        env = env_values(
            'tests/fixtures/simple.yml',
            'tests/fixtures/simple.env'
        )
        self.assertEqual(env['FOO'], 'FOO')
        self.assertEqual(env['BAR'], '123')
        self.assertEqual(env['BAZ'], 1.23)
        self.assertEqual(env['QUX'], '1.23')
        self.assertEqual(env['FOO_BAR'], 'false')
        self.assertEqual(env['FOO_BAZ'], None)
        self.assertEqual(env['FOO_QUX'], 'null')
        self.assertEqual(env['FOO_BAR_BAZ'], 'foo,bar,baz')
        self.assertFalse('TEST' in env)
    
    def test_dotenv_yaml(self):
        env = env_values(
            'tests/fixtures/simple.env',
            'tests/fixtures/simple.yml',
        )
        self.assertEqual(env['FOO'], 'foo')
        self.assertEqual(env['BAR'], 123)
        self.assertEqual(env['BAZ'], 1.23)
        self.assertEqual(env['QUX'], '1.23')
        self.assertEqual(env['FOO_BAR'], False)
        self.assertEqual(env['FOO_BAZ'], None)
        self.assertEqual(env['FOO_QUX'], 'null')
        self.assertEqual(env['FOO_BAR_BAZ'], ['foo', 'bar', 'baz'])
        self.assertFalse('TEST' in env)

class NestedOverrideTest(unittest.TestCase):
    
    def setUp(self):
        self.env = env_values(
            'tests/fixtures/nested.yml',
            'tests/fixtures/nested.env',
        )
    
    def test_nesting(self):
        self.assertEqual(self.env['FOO'], {'BAR': {'BAZ': 'foobarbaz'}})
        self.assertEqual(self.env['FOO_BAR'], 'FOOBAR')
        self.assertEqual(self.env['FOO_BAR_BAZ'], 'FOOBARBAZ')
    
    def test_duplicate_keys(self):
        self.assertEqual(self.env['BAR'], {'BAZ': 'barbaz'})
        self.assertNotEqual(self.env['BAR_BAZ'], 'barbaz')
        self.assertNotEqual(self.env['BAR_BAZ'], 'baz')
        self.assertNotEqual(self.env['BAR_BAZ'], 'BAZ')
        self.assertEqual(self.env['BAR_BAZ'], 'BARBAZ')
    
    def test_nonstring_keys(self):
        self.assertEqual(self.env['BAZ'], 'BAZ')
        self.assertEqual(self.env['BAZ_69'], {1337: '1337', True: 'True', None: 'None'})
        self.assertEqual(self.env['BAZ_69_1337'], 'LEET')
        self.assertEqual(self.env['BAZ_69_True'], 'True')
        self.assertEqual(self.env['BAZ_69_False'], 'False')
        self.assertEqual(self.env['BAZ_69_None'], None)

class OsEnvTest(unittest.TestCase):

    def test_loading(self):
        environ = os.environ.copy()
        env_values(
            'tests/fixtures/simple.yml',
            'tests/fixtures/simple.env',
        )
        self.assertEqual(os.environ, environ)
    
    def test_env(self):
        os.environ.update({
            'FOO': 'foo',
            'BAR': 'bar',
            'FOO_BAR': 'foo_bar',
            'FOO_BAR_BAZ': 'foo_bar_baz',
            'TEST': 'test',
        })
        env = env_values()
        self.assertEqual(env['FOO'], 'foo')
        self.assertEqual(env['BAR'], 'bar')
        self.assertEqual(env['FOO_BAR'], 'foo_bar')
        self.assertEqual(env['FOO_BAR_BAZ'], 'foo_bar_baz')
        self.assertEqual(env['TEST'], 'test')
        os.environ.clear()
    
    def test_yaml_env(self):
        os.environ.update({
            'FOO': 'foo',
            'BAR': 'bar',
            'QUX': 'qux',
            'FOO_BAR': 'foo_bar',
            'FOO_QUX': 'foo_qux',
            'FOO_BAR_BAZ': 'foo_bar_baz',
            'TEST': 'test',
        })
        env = env_values('tests/fixtures/simple.yml')
        self.assertEqual(env['FOO'], 'foo')
        self.assertEqual(env['BAR'], 'bar')
        self.assertEqual(env['BAZ'], 1.23)
        self.assertEqual(env['QUX'], 'qux')
        self.assertEqual(env['FOO_BAR'], 'foo_bar')
        self.assertEqual(env['FOO_BAZ'], None)
        self.assertEqual(env['FOO_QUX'], 'foo_qux')
        self.assertEqual(env['FOO_BAR_BAZ'], 'foo_bar_baz')
        self.assertEqual(env['TEST'], 'test')
        os.environ.clear()
    
    def test_dotenv_env(self):
        os.environ.update({
            'FOO': 'foo',
            'BAR': 'bar',
            'BAZ': 'baz',
            'FOO_BAR': 'foo_bar',
            'FOO_BAZ': 'foo_baz',
            'FOO_BAR_BAZ': 'foo_bar_baz',
            'TEST': 'test',
        })
        env = env_values('tests/fixtures/simple.env')
        self.assertEqual(env['FOO'], 'foo')
        self.assertEqual(env['BAR'], 'bar')
        self.assertEqual(env['BAZ'], 'baz')
        self.assertEqual(env['QUX'], '1.23')
        self.assertEqual(env['FOO_BAR'], 'foo_bar')
        self.assertEqual(env['FOO_BAZ'], 'foo_baz')
        self.assertEqual(env['FOO_QUX'], 'null')
        self.assertEqual(env['FOO_BAR_BAZ'], 'foo_bar_baz')
        self.assertEqual(env['TEST'], 'test')
        os.environ.clear()
