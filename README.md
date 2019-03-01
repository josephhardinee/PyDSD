# PyDSD

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.9991.svg)](https://doi.org/10.5281/zenodo.9991)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pydsd/badges/version.svg)](https://anaconda.org/conda-forge/pydsd)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pydsd/badges/latest_release_date.svg)](https://anaconda.org/conda-forge/pydsd)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pydsd/badges/license.svg)](https://anaconda.org/conda-forge/pydsd)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pydsd/badges/downloads.svg)](https://anaconda.org/conda-forge/pydsd)
[![Coverage Status](https://coveralls.io/repos/github/josephhardinee/PyDSD/badge.svg?branch=master)](https://coveralls.io/github/josephhardinee/PyDSD?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

PyDSD is an open source Python package to work with disdrometer, particle probe, and DSD data. It is meant to make complex workflows easy. It includes support for different aspects of the research and operational workflow. This includes parametric fitting for different distributions, file reading, and scattering support.   

## Import Links   

1. [Source Code Repository](https://github.com/josephhardinee/PyDSD)
2. [PyDSD Documentation](http://josephhardinee.github.io/PyDSD)
3. [Example Gallery](http://josephhardinee.github.io/PyDSD/source/auto_examples/index.html)
4. [Mailing List](https://groups.google.com/forum/#!forum/pydisdrometer-user-group)
4. [Issues](https://github.com/josephhardinee/PyDSD/issues)

## Citing
Currently the best way to cite PyDSD is to cite our software DOI as:
Joseph Hardin, Nick Guy. (2017, December). PyDSD , doi: http://doi.org/10.5281/zenodo.9991

## Usage
PyDSD is currently capable of reading several different file formats. As a quick example of usage:

```python
import pydsd
dsd = pydsd.read_parsivel(filename)

dsd.calculate_dsd_parameters() 
```

PyDSD includes several different readers in the io and aux_readers categories. If you are unable to find the correct reader please contact us or post an issue. 

PyDSD also supports scattering to simulate radar measured fields. The scattered fields will be stored in the fields dictionary of the dsd object. So to plot the reflectivity one can run

```python

import pydsd
dsd = pydsd.read_parsivel(filename)
dsd.calculate_dsd_parameters() 
plot(dsd.time, dsd.fields['Zh']['data'])
```
PyDSD also has built in plotting routines. Please see the example gallery linked above as well as the documentation. 

Requirements:
    This library currently requires the normal scientific python stack(numpy+scipy+matplotlib)
    It also requires the [PyTMatrix Package](https://github.com/jleinonen/pytmatrix) for scattering calculations. 

## Installing
There are two methods of installing PyDSD:

#### From Source:
```
git clone https://github.com/josephhardinee/PyDSD
cd PyDSD
python setup.py install
```
#### Using Anaconda Python Distribution
Simply type 
```conda install -c conda-forge pydsd```

This installs the latest package version and dependencies. 

## Contributing
__Imposter syndrome disclaimer__: We want your help. No, really.

There may be a little voice inside your head that is telling you that you're not ready to be an open source contributor; that your skills aren't nearly good enough to contribute. What could you possibly offer a project like this one?

We assure you - the little voice in your head is wrong. If you can write code at all, you can contribute code to open source. Contributing to open source projects is a fantastic way to advance one's coding skills. Writing perfect code isn't the measure of a good developer (that would disqualify all of us!); it's trying to create something, making mistakes, and learning from those mistakes. That's how we all improve, and we are happy to help others learn.

Being an open source contributor doesn't just mean writing code, either. You can help out by writing documentation, tests, or even giving feedback about the project (and yes - that includes giving feedback about the contribution process). Some of these contributions may be the most valuable to the project as a whole, because you're coming to the project with fresh eyes, so you can see the errors and assumptions that seasoned contributors have glossed over.

Contact us, we'll walk you through how to make a change and add it to PyDSD. Just have a complaint, notice a typo, or a rant? We love those too!


