from setuptools import setup
import versioneer

setup(
    name='PyDisdrometer',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Joseph C. Hardin, Nick Guy',
    author_email='josephhardinee@gmail.com',
    packages=['pydsd',
              'pydsd.aux_readers',
              'pydsd.plot',
              'pydsd.io',
              'pydsd.partition',
              'pydsd.plot',
              'pydsd.utility',
              'pydsd.fit']
    url='http://pypi.python.org/pypi/PyDisdrometer/',
    license='LICENSE.txt',
    description='Python Disdrometer Processing',
    long_description=open('description.txt').read(),
    install_requires=['pytmatrix>=0.2.0', 'numpy', 'matplotlib', 'scipy', 'versioneer'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console"
        ],
    include_package_data=True

)
