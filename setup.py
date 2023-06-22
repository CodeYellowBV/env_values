from setuptools import setup

version = '2.0'

with open("README.md") as f:
    long_description = f.read()

setup(
    name='env_values',
    version=version,
    description="Load env values",
    long_description=long_description,
    keywords='env',
    author='Burhan Zainuddin',
    author_email='burhan@codeyellow.nl',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    python_requires='~=3.3',
    include_package_data=True,
    zip_safe=True,
    install_requires=['python-dotenv', 'pyyaml'],
    py_modules=['env_values'],
)