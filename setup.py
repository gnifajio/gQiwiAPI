import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

with open('requirements.txt', 'r') as req_file:
    requirements = map(lambda line: line.strip(), req_file.readlines())

setuptools.setup(
    name="gQiwiAPI",
    version="1.4.5",
    author="Gnifajio None",
    author_email="gnifajio@gmail.com",
    description="A simple API for creating a payment link",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gnifajio/gQiwiAPI",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
