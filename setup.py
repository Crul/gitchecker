#!/usr/bin/env python

from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gitchecker",
    version="0.1",
    description="Python GIT tool to check pending changes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="crul",
    author_email="rauljavier.vila@gmail.com",
    url="http://github.com/Crul/gitchecker",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["gitpython"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov", "pytest-pep8"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
    ),
)
