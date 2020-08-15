# RAW-MSI-generator
It is a mass spectrometry imaging (MSI) data processing pipeline to generate ion images from Thermo .raw files. It is designed for line-by-line data acquisition manner exclusively. It is designed for line-by-line data acquisition manner exclusively. 

The pipeline comprises two independent data processing modules. RAW-MSI-generator_L0 extracts ion images from .raw files. In this step, the pymsfilereader reads .raw files for twice. It firstly checks the dimensionality of the MSI data sets, second it extracts ion images with a mass list and a mass window. During this step, it also aligns line scans by interpolation. Finally, the flattened ion image data is assembled and exported. The exported data format is as follows (first 3 columns, which are not specified in the scheme, are spatial indexes and TIC value).

<div align="center">
<img src="images/image1.png" width="600">
</div>

RAW-MSI-generator_L1 plots ion images. Herein, program reads L0 output and fold it into an array of ion images (3d array) for following data manipulation. Normalization is optionally adopted, you can choose to normalize to “TIC” or a specific ion image. Other image manipulations, such as spike detection, denoise, resize, etc, can be incorporated in. Processed ion images are then plotted. Many visualization options  can be set, such as colormap, visualization scale, aspect ratio, colorbar, ticks, etc. Finally, ion images are exported in the format of .png, .jpg, .csv, or txt, etc. 


## Requirements 
numpy 1.18.1<br>
pandas 1.1.0<br>
matplotlib 3.1.3<br>
pymsfilereader 1.0.1 (Please follow this package’s instruction in github for installation.)

## How to use 
### Input Data preparation
1. .raw files:
.raw files are named with numbers with respect to the acquisition sequence. The general format is “XXX_number”. Please keep description “XXX” constant throughout the data set, which is the “NameBody” variable in config.py. For example: 

<img src="images/image2.png">

2. mass list:
A excel file with only mass values in one column. For example:

<img src="images/image3.png">

### Main programs
Run RAW-MSI-generator modules sequentially, outputs of L0 is the input for L1. Edit the config.py before you run the pipeline. Jupyter notebook files are attached for reference. 

*RAW-MSI-generator_L0.py*<br>
Ion image extraction. Must-edit settings in config.py are:<br>
n_files, NameBody, MassList_dir.

*RAW-MSI-generator_L1.py*<br>
Ion image plotting. You can run multiple times with different settings. Must-edit settings in config.py are:<br>
InputDir, Norm, AspectRatio.

