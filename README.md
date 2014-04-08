# PyDisdrometer

PyDisdrometer is a package to process disdrometer files. It currently supports OTT Parsivel disdrometers. It is currently in alpha so functionality is limited.

Author: Joseph C. Hardin

## Usage
```python
dsd = pydisdrometer.read_parsivel(filename)

dsd.calc_radar_parameters() 
```

If using Ground Validation Parsivel Disdrometer Data, usage is more like

```python
dsd = pydisdrometer.read_parsivel_gv(filename, campaign='ifloods')
```

Requirements:
    This library currently requires the normal scientific python stack(numpy+scipy+matplotlib)
    It also requires the [PyTMatrix Package](https://github.com/jleinonen/pytmatrix). 

This library should see significant updates over the coming weeks. We welcome contributions from all users. 
