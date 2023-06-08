import os
from dotenv import find_dotenv, dotenv_values

# Find an environment file, either given by the env `CY_ENV_FILE` or find a file
# called `.env`. Same for goes for an override file.
CY_ENV_FILE = os.environ.get('CY_ENV_FILE', find_dotenv('.env'))
CY_ENV_OVERRIDE_FILE = os.environ.get('CY_ENV_OVERRIDE_FILE', find_dotenv('.env.override'))

def env_values():
    """Retrieve environment variables by combining `os.environ`, `CY_ENV_FILE` and `CY_ENV_OVERRIDE_FILE`.

    Get environment variables by looking at (in order):
        1. os.environ
        2. .env.override
        3. .env

    When a variable is present in `os.environ` and `.env`, the one in `.env` will be ignored and the one in `os.environ`
    will "win".

    Calling `env_values()` has no side effects, eg `os.environ` not be altered.

    Returns:
        :dict: Env values.

    Examples:
        >>> env = env_values()
        >>>
        >>> env.get('CY_DEBUG')
        >>> env.get('CY_DEBUG', False)
        >>> env['CY_DEBUG']
    """
    env_file = dotenv_values(CY_ENV_FILE) if CY_ENV_FILE else {}
    env_override_file = dotenv_values(CY_ENV_OVERRIDE_FILE) if CY_ENV_OVERRIDE_FILE else {}

    return {
        **env_file,
        **env_override_file,
        **os.environ,
    }
