#Import required functions
from setuptools import setup, find_packages

#Call setup function
setup(
    author="Fabian Tito Arandia Martinez",
    description="Package pour téléchargement et traitement des prévisions d'EC",
    name="previs",
    version="0.1.0",
    packages=find_packages(include=["previs","previs.*"])
)