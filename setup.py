import os

from setuptools import setup

cwd = os.path.dirname(os.path.realpath(__file__))
file = os.path.join(cwd, 'requirements.txt')
# with open(file) as f:
#     dependencies = list(map(lambda x: x.replace("\n", ""), f.readlines()))

with open("README.md", 'r') as f:
    long_description = f.read()

setup(name='orderbook',
      version='0.1.1',
      description='Cryptocurrency LOB trading environment in gym format.',
      long_description=long_description,
      author='Milo Carroll',
      url='https://github.com/',
      install_requires=['numpy', 'pandas'],
      packages=['order_book'])
