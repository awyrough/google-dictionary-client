import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="mw-dictionary-client",
    version="0.1",
    packages=["mw-dictionary-client"],
    package_dir={"mw-dictionary-client": "src/mw-dictionary-client"},
    include_package_data=True,
    description="A Mirriam-Webset Dictionary API Client",
    long_description=README,
    author="hill wyrough",
    author_email="alexander.hill.wyrough@gmail.com",
    home_page="www.hillwyrough.com",
    license="MIT License (see within)"
)
