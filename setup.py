from setuptools import setup

with open("./README.md") as fp:
    long_description = fp.read()

setup(
    name="My Mip Solver",
    version="0.1",
    description="Implementation of homemade MIP solver.",
    long_description=long_description,
    author="Timothee RIO",
    author_email="t_rio@hotmail.fr",
    packages=["my_mip"],
)