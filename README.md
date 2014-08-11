# PyDisdrometer

![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.9991.png)   

PyDisdrometer is a Python package to process disdrometer files. It currently is capable of reading several different types of disdrometers and calculating both important moment parameters, as well as radar derived parameters. It currently supports OTT Parsivel disdrometers and Joss Waldvogel Disdrometers. It is currently in alpha so functionality is limited but being expanded quickly..

Author: Joseph C. Hardin

## Usage

An quick example of using the pydisrometer package to read in a parsivel data file and calculate radar scattered parameters is: 

```python
dsd = pydisdrometer.read_parsivel(filename)

dsd.calculate_radar_parameters() 
```

If using NASA Ground Validation Parsivel Disdrometer Data, usage is more like

```python
dsd = pydisdrometer.read_parsivel_gv(filename, campaign='ifloods')
```

For more information, please see the examples in the Notebooks directory. Additionally you can find some initial documentation at [PyDisdrometer Documentation](http://josephhardinee.github.io/PyDisdrometer)

Requirements:
    This library currently requires the normal scientific python stack(numpy+scipy+matplotlib)
    It also requires the [PyTMatrix Package](https://github.com/jleinonen/pytmatrix). 

This library should see significant updates over the coming weeks. We welcome contributions from all users. Please see the examples in Notebooks for a more indepth guide on how to use PyDisdrometer.


