import setuptools

with open('README_EN.md', 'r') as fh:
	long_description = fh.read()

with open('requirements.txt', 'r') as fr:
    requirements = map(lambda line: line.strip(), fr.readlines())


setuptools.setup(
	name = "gQiwiAPI",
	version = "1.2",
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
	python_requires = '>=3.7',
)