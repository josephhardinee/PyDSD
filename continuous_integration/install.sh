#!/bin/bash
# This script was adpated from the pyart install.sh script.
# This script is adapted from the install.sh script from the scikit-learn
# project: https://github.com/scikit-learn/scikit-learn

# This script is meant to be called by the "install" step defined in
# .travis.yml. See http://docs.travis-ci.com/ for more details.
# The behavior of the script is controlled by environment variabled defined
# in the .travis.yml in the top level folder of the project.

set -e
# use next line to debug this script
#set -x

# Use Miniconda to provide a Python environment.  This allows us to perform
# a conda based install of the SciPy stack on multiple versions of Python
# as well as use conda and binstar to install additional modules which are not
# in the default repository.
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    -O miniconda.sh
chmod +x miniconda.sh
./miniconda.sh -b
export PATH=/home/travis/miniconda3/bin:$PATH

conda config --set always_yes yes
conda config --set show_channel_urls true
conda update -q conda

# Create a testenv with the correct Python version
conda create -n testenv --yes pip python=$PYTHON_VERSION
source activate testenv

# Install dependencies

conda install -c conda-forge pytmatrix pytest pytest-cov sphinx_rtd_theme numpy scipy matplotlib netcdf4 nose sphinx numpydoc hdf4=4.2.12

pip install sphinx-gallery nose-cov

if [[ $PYTHON_VERSION == '2.7' ]]; then
    pip install sphinxcontrib-bibtex
    pip install xmltodict
fi


# install coverage modules
if [[ "$COVERALLS" == "true" ]]; then
    pip install python-coveralls
fi

pip install -e .
