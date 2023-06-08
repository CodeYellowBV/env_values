from setuptools import setup

version = '1.0'

setup(
    name='env_values',
    version=version,
    description="Load env values",
    long_description='\n'.join([
        open("README.md").read(),
    ]),
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
    install_requires=['python-dotenv'],
    py_modules=['env_values'],
)