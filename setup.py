#!/usr/bin/env python3

from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="funance-data",
    version="0.1.0",
    description="Library for gathering external data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SudoVim/funance-data",
    author="SudoVim",
    packages=[
        "funance_data",
        "funance_data.store",
        "funance_data.tickers",
    ],
    package_data={
        "funance_data": ["py.typed"],
    },
    python_requires=">=3.10, <4",
    project_urls={
        "Bug Reports": "https://github.com/SudoVim/funance-data/issues",
        "Source": "https://github.com/SudoVim/funance-data",
    },
)
