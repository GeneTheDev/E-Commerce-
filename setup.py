from setuptools import setup, find_packages

setup(
    name='web_store',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'psycopg2',
        # other dependencies here
    ],
)
