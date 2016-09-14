"""Setuptools for steve-zissou service"""
from setuptools import setup, find_packages

reqs = []

with open('requirements.txt') as inf:
    for line in inf:
        line = line.strip()
        reqs.append(line)


setup(
    name='steve-zissou',
    version='0.0.0.5',
    description='Web app for displaying data collected from various sources',
    author='Brett Smythe',
    author_email='smythebrett@gmail.com',
    maintainer='Brett Smythe',
    maintainer_email='smythebrett@gmail.com',
    packages=find_packages(),
    install_reqs=reqs,
    entry_points={
        'console_scripts': [
            'steve-zissou=steve_zissou.app:test'
        ]
    }
)
