# setup.py
from setuptools import setup, find_packages

setup(
    name="SyntheticDHN",
    version="1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)