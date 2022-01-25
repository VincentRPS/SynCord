import sys

from setuptools import find_packages, setup

from syncord import VERSION

with open("requirements.txt") as f:
    requirements = f.readlines()

with open("README.md") as f:
    readme = f.read()

extras_require = {
    "voice": ["telecom-py==0.0.4"],
    "http": ["flask==0.12.2"],
    "yaml": ["pyyaml==6.0"],
    "music": ["youtube_dl>=2018.1.21"],
    "performance": [
        "earl-etf==2.1.2",
        "ujson==1.35",
        "wsaccel==0.6.3",
    ],
    "sharding": ["gipc==1.3.0"],
    "docs": ["biblio==0.0.4"],
}

setup(
    name="syncord",
    author="b1nzy, VincentRPS",
    url="https://github.com/VincentRPS/SynCord",
    version=VERSION,
    packages=find_packages(include=["syncord*"]),
    license="MIT",
    description="A Python library for Discord, a fork of disco",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    test_suite="tests",
    setup_requires=["pytest-runner==5.3.1"],
    tests_require=[
        "pytest==6.2.5",
        "pytest-benchmark==3.1.1",
        "flake8-tuple==0.4.1",
        "flake8-quotes==1.0.0",
        "flake8-comprehensions==1.4.1",
        "flake8-commas==2.0.0",
        "flake8-builtins==1.4.1",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
