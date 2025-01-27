from setuptools import setup, find_packages

setup(
    name='repl',
    version='0.1.0',
    description='A Python REPL wrapper that saves inputs to a .py file.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'repl=repl.cli:main',
        ],
    },
    install_requires=[],  # Add dependencies here if needed
    python_requires='>=3.6',
)
