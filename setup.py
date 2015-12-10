from setuptools import setup

setup(
    name='PyDisdrometer',
    version='0.1.12.0',
    author='Joseph C. Hardin',
    author_email='josephhardinee@gmail.com',
    packages=['pydisdrometer',
              'pydisdrometer.io',
              'pydisdrometer.partition',
              'pydisdrometer.plot',
              'pydisdrometer.utility',
              'pydsd',],
    url='http://pypi.python.org/pypi/PyDisdrometer/',
    license='LICENSE.txt',
    description='Python Disdrometer Processing',
    long_description=open('description.txt').read(),
    install_requires=['pytmatrix>=0.2.0'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console"
        ],

)
