from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='gQiwiAPI',
    version='1.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README_EN.md')).read(),
)


import setuptools

with open('README_EN.md', 'r') as fh:
	long_description = fh.read()

with open('requirements.txt', 'r') as fr:
    requirements = map(lambda line: line.strip(), fr.readlines())


setuptools.setup(
	name = "gQiwiAPI",
	version = "1.1",
	author = "Gnifajio None",
	author_email = "gnifajio@gmail.com",
	description = "A simple API for creating a payment link",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/gnifajio/gQiwiAPI",
	packages = setuptools.find_packages(),
	install_requires = requirements,
	classifiers = [
		"Programming Language :: Python :: 3.10",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires = '>=3.6',
)