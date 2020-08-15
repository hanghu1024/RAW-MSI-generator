#====================================================================
# RAW-MSI-generator CONFIGURATION
#====================================================================

#====================================================================
# L0: image extraction
#====================================================================
# number of line scan folders
n_files = 50

# Set number of spectra per line (Default setting: average for all lines)
# NumspePerLine

# specify .raw file dir
NameBody = "I:\\2020 work from home (5 data sets)\\Daisy muscle data\\gas_youngmale_mouse1_slide6_tissue1_positive_line_"

# specify mass list file dir
MassList_dir = "D:\\Desktop\\group meeting & report\\Hang\\2020\\machine learning\\MSI data sets\\muscle\\mass list.xlsx"

# mass window
MassTolerance = 20

# Locate the extraction output folder. (Default setting: 0 -> use parent directory) 
ExtractionFolder = 0

#====================================================================
# L1: ion image plotting
#====================================================================
# Locate the pixels.csv file
InputDir = "I:\\2020 work from home (5 data sets)\\Daisy muscle data\\Extraction\\pixels.csv"

# Locate the ion image output folder. (Default setting: 0 -> use parent parent directory) 
ImageFolder = 0

# Choose a peak (ion image) for normalization.
'''
conditions: 
== 'none': no normalization
== 'TIC': TIC normalization
== float: STD normalization
'''
Norm = 'TIC'

# visualization scale (Default setting: 0.999)
VisuScale = 0.999

# For the whole image, AspectRatio = height/width. (Default setting: 1)
AspectRatio = 1

# Assign a colormap for ion images. (Default setting: 'hot')
colormap = 'hot'

# Assign a colorbar for single ion image. (Default setting: 0, no colorbar)
colorbar = 0

# Assign ticks for single ion image. (Default setting: 0, no ticks)
ticks = 0

# dpi for mosaic plot saving. (Default setting: 600)
dpi = 600

# Export .csv for each image? (Default setting: 1 -> yes)
csv = 1

# In ion image collection, how many images in a row? (Default setting: 15)
ncols = 15

