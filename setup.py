from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='SorosTracker9000',
    version='1.0.0',
    description='Webcrawler & Twitter bot to gather articles about Soros',
    long_description=readme,
    author='Peter Bocz',
    author_email='bocz.petya@gmail.com',
    url='https://github.com/analphagamma/SorosTracker9000',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')))
