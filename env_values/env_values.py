from dotenv import dotenv_values
import os
import yaml

def _gen_values(values, prefix=''):
    for key, value in values.items():
        yield (f'{prefix}{key}', value)
        if isinstance(value, dict):
            yield from _gen_values(value, prefix=f'{prefix}{key}_')

def yaml_values(path):
    """
    Parse a JSON or YAML file and return its content as a dict.

    The returned dict will contain all nested values on the
    root level as well, identified by keys that are concatenations
    of the keys of their ancestors.

    For example, the following structure will produce four values:
    `FOO`, `FOO_BAR`, `FOO_BAR_BAZ`, and `BAZ`.
    ```
    FOO:
      BAR:
        BAZ: baz
    FOO_BAR: 1337
    BAZ: ['foo', 'bar']
    ```

    Parameters:
        path: Absolute or relative path to the file.
    """
    with open(path) as f:
        values = yaml.safe_load(f)
    if not isinstance(values, dict):
        return {}
    return dict(_gen_values(values))

def env_values(*paths):
    """Retrieve environment variables by combining `os.environ` and the provided env files.

    Get environment variables by looking at (in order):
        1. os.environ
        2. file #n
        3. file #n-1
        ...
      n+1. file #1

    When a variable is present in `os.environ` and any of the files, the ones in the files will be ignored and the one in `os.environ`
    will "win".

    Calling `env_values()` has no side effects, eg `os.environ` not be altered.

    Returns:
        :dict: Env values.

    Example:
        >>> env = env_values('.env')
        >>>
        >>> env.get('CY_DEBUG')
        >>> env.get('CY_DEBUG', False)
        >>> env['CY_DEBUG']
    """
    values = {}
    for path in paths:
        if not path:
            continue
        if path.endswith('.json') or path.endswith('.yml') or path.endswith('.yaml'):
            values.update(yaml_values(path))
        else:
            values.update(dotenv_values(path))
    
    return {
        **values,
        **os.environ
    }
