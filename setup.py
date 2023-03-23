from setuptools import find_packages,setup
from typing import List

HYPHON_E_DOT = '-e .'

def get_requirements(file_name)->List[str]:
    with open(file_name) as file_name:
        requirements = file_name.readlines()
    requirements = [requires.replace('\n','') for requires in requirements]
    if HYPHON_E_DOT in requirements:
        requirements.remove(HYPHON_E_DOT)
    return requirements

setup(
    name = 'Flight Fare Prediction',
    version = '0.0.1',
    author='Sakshit Attri',
    author_email = 'sakshit2000@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)