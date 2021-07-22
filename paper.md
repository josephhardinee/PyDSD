---
title: 'PyDSD - A Python Library for Working with Disdrometers, Particle Probes, and Drop Size Distribution Data.'
tags:
  - Python
  - drop size distribution
  - weather
  - radar
  - T-Matrix
  - disdrometer
authors:
  - name: Joseph C. Hardin^[correspond author]
    orcid: https://orcid.org/0000-0002-8489-4763
    affiliation: "1"
  - name: Nick Guy 
    affiliation: 2
  - name: Jussi Leinonen 
    affiliation: 3
  - name: V. Chandrasekar
    affiliation: 4
affiliations:
 - name: Atmospheric Science and Global Change Division, Pacific Northwest National Laboratory
   index: 1
 - name: Verisk Weather Solutions
   index: 2
 - name:  Federal Office of Meteorology and Climatology MeteoSwiss
   index: 3
 - name: Colorado State University
   index: 4
date: 22 July 2021
---
Much of atmospheric science is driven by the generation, interaction, and precipitation of liquid and frozen particles in the atmosphere. The processes that govern the generation and interaction of these particles give rise to a wide distribution of possible sizes and shapes. The distribution of these particles is often represented as a particle size distribution (PSD) in the case of ice, or a drop size distribution (DSD) in the case of liquid particles.  Information about these distributions is important to understand the processes that are occurring in the atmosphere. 

These distributions of particles are measured by sets of instruments called disdrometers, or particle probes, using a wide variety of methods with the most common being acoustic, laser-optical, or video. A primary difference between the different type of instruments is the amount of information they measure about the drops, ranging from just size, to size and velocity, up to images of individual drops. Additionally, the range of drop sizes that can be accurately recorded varies between devices and measurement modalities. Disdrometers can be deployed on ground- or ship-based platforms while particle probes are often deployed on aerial platforms. Ground and ship-based platforms most often focus on measuring the larger size distributions associated with precipitation at the ground. Aerial platforms more commonly include devices extending to a smaller range of particles. Hereafter we will use the term disdrometers for simplicity to refer to both classes of instruments unless specifically differentiated. 

# Statement of Need
The wide variety of disdrometers in existence, and their increasingly commonplace occurrence in field campaigns, has resulted in a wealth of DSD data from around the world. Unfortunately, working with the resulting data is not always so simple. File formats vary between instruments, and even between facilities releasing data from the same instruments. Commonly what is wanted is not the raw DSD measurements, but rather secondary, derived products such as various parameterized distributions, rain rates and other macro properties, and radar equivalent parameters. 

PyDSD is an open source Python library that aims to simplify the process of working with this data with the express goal of both reading and processing of the data, as well as creating publication ready plots of the data. Its goal is to make many of the common tasks researchers face when dealing with these datasets easy to perform. PyDSD focuses on a robust set of algorithms and operations for liquid drop size distributions. PyDSD has formed the basis of DSD processing workflows in research and operations in the field

# Acknowledgements
Although most of PyDSD was written in the authors free time, it has been lucky enough to receive funding from many different sources at various times for small features. Originally PyDisdrometer resulted from work at Colorado State University funded by the Department of Energy’s Atmospheric Systems Research Program. Afterwards follow-up funding has been provided by the Climate Model Development and Validation program funded by BER in the U.S. DOE Office of Science
including extensions for ARM Parsivel processing. Finally, the writing of this paper, as well as the improvements of PyDSD to support 2DVD product generation and spectral processing was provided by the U.S. Department of Energy Office of Science Biological and Environmental Research as part of the Atmospheric Systems Research Program through the ICLASS project. The original pyparticleprobe code base was largely developed while funded by a National Science Foundation - University of Wyoming joint Lower Atmosphere Observing Facility grant. 


We would like to thank the numerous users who submitted bug reports, feature requests, and words of support. Additionally, PyDSD was transitioned into operational products for the Department of Energy’s Atmospheric Radiation Measurement (ARM) program in collaboration with Scott Giangrande, Die Wang, and Aifang Zhou. 

