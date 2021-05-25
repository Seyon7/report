from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="report6-OleksiiLeshchenko",
    version="0.1.0",
    packages=find_packages(),
    description="Script reads data from 2 files, sort racers by time "
                "and print report that shows the top 15 racers and the rest after underline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.foxminded.com.ua/oleksii.leshchenko/report6",
    author="Oleksii Leshchenko",
    author_email="leshchenko.o91@gmail.com",
    license="MIT",
    classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        'atomicwrites==1.4.0',
        'attrs==20.2.0',
        'click==7.1.2',
        'colorama==0.4.4',
        'coverage==5.3',
        'importlib-metadata==3.4.0',
        'iniconfig==1.1.1',
        'packaging==20.4',
        'pluggy==0.13.1',
        'py==1.9.0',
        'pyparsing==2.4.7',
        'pytest==6.1.1',
        'pytest-cov==2.10.1',
        'python-dateutil==2.8.1',
        'six==1.15.0',
        'toml==0.10.1',
        'typing-extensions==3.7.4.3',
        'zipp==3.4.0'
    ],
    entry_points="""
    [console_scripts]
    report=modules.report6:cli_root
    """,
)
