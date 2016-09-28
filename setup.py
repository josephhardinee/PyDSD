from setuptools import setup

MAJOR = 0
MINOR = 1
MICRO = 15
SUB = 0
ISRELEASED = False
VERSION = '%d.%d.%d.%d' % (MAJOR, MINOR, MICRO, SUB)

setup(
    name='PyDisdrometer',
    version=VERSION,
    author='Joseph C. Hardin, Nick Guy',
    author_email='josephhardinee@gmail.com',
    packages=['pydisdrometer',
              'pydisdrometer.aux_readers',
              'pydisdrometer.plot',
              'pydisdrometer.io',
              'pydisdrometer.partition',
              'pydisdrometer.plot',
              'pydisdrometer.utility'],
    url='http://pypi.python.org/pypi/PyDisdrometer/',
    license='LICENSE.txt',
    description='Python Disdrometer Processing',
    long_description=open('description.txt').read(),
    install_requires=['pytmatrix>=0.2.0'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console"
        ],
    include_package_data=True

)
