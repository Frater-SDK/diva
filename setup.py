from setuptools import setup, find_packages

packages = find_packages(exclude=['tests*'])
dependencies = list(line.strip() for line in open('requirements.txt').readlines())
setup(
    name='diva',
    version='0.1',
    packages=packages,
    url='https://github.ibm.com/john.l.henning/diva-frater',
    license='MIT',
    author='John Henning',
    author_email='john.l.henning@ibm.com',
    description='DIVA Frater library containing data types, base Component classes, and visualization tools',
    install_requires=dependencies
)
