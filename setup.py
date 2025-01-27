from setuptools import setup, find_packages

setup(
    name="repl",
    version="0.1.2",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'repl = repl.cli:main',
        ],
    },
)
