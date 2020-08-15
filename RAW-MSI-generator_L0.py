#===========================================
# import modules, defs and variables
#===========================================
exec(open("./external.py").read())
exec(open("./defs.py").read())
exec(open("./config.py").read())

print('Finish modules, defs and variables import, next step: check the dimensionality of this MSI data set.')

#===========================================
# L0.0: check dimensionality of MSI data
#===========================================
# string manipulation
NamePost = ".raw"
NumLine = n_files
InputDir = NameBody + '1' + NamePost

# import mass list
df_MassList = pd.read_excel(MassList_dir, header=None)
MassList =df_MassList.values.astype(np.float64)

# make folders for outputs
if ExtractionFolder == 0:
    ExtractionFolder = locate_ExtractionFolder(InputDir)

os.mkdir(ExtractionFolder)

#===========================================
# L0.1: check dimensionality of MSI data
#===========================================
# check dimensionality
NumLineSpe = DimCheck(n_files, NameBody)
NumSpePerLine = int(NumLineSpe.mean())

# for interpolation
x_aligned = np.linspace(1,NumSpePerLine,NumSpePerLine)

print('Finish checking the dimensionality of this MSI data set, next step: extract images from each line scans')

#===========================================
# L0.2: extract images from each line scans 
#===========================================
# initiate accumulator
pixels=np.empty([0,(MassList.shape[0]+3)])

for i in range(1, NumLine+1):
    # x-axis array for alignment
    NumSpePerLine_meta = NumLineSpe['# of spectra'][i]
    x_meta = np.linspace(1,NumSpePerLine,NumSpePerLine_meta)
    # 2D accumulator for 1 line (position in line, channel)
    pixelsPerLine_meta = np.zeros(shape = (NumSpePerLine_meta,(MassList.shape[0]+3))) # line index, spectrum index, and TIC
    pixelsPerLine = np.zeros(shape = (NumSpePerLine,(MassList.shape[0]+3)))
    # file name and timing
    StaTime=time.time()
    Name = NameBody + str(i) + NamePost
    RawFile = MSFileReader(Name)
    
    for j in range(1,NumSpePerLine_meta+1):     # loop in line
        # grab data points and header
        mzlist = RawFile.GetMassListFromScanNum(j)
        header = RawFile.GetScanHeaderInfoForScanNum(j)
        mz = np.array(mzlist[0][0])
        IntensityPoints = np.array(mzlist[0][1])
        TIC = header["TIC"]
        
        for k in range(MassList.shape[0]):
            PeakPoints = IntensityPoints[(mz > MassList[k]*(1-MassTolerance*0.000001))&(mz < MassList[k]*(1+MassTolerance*0.000001))]
            Intensity = PeakPoints.sum()
            pixelsPerLine_meta[j-1,k+3] = Intensity
        pixelsPerLine_meta[j-1,2] = TIC
            
    RawFile.Close()
    
    # after you have data for that line, do interpolation (including TIC)
    for l in range(pixelsPerLine.shape[1]):
        pixelsPerLine[:,l] = np.interp(x_aligned, x_meta, pixelsPerLine_meta[:,l])
    # take care coordinates
    pixelsPerLine[:,0] = i-1                   # 0 column line index, start from 0 
    pixelsPerLine[:,1] = x_aligned-1           # 1 column spectrum index, start from 0 
    
    # stack PixelsPerLine vertically onto total pixels
    pixels = np.append(pixels,pixelsPerLine,axis=0)
    # wrap up this line
    SpenTime = (time.time()-StaTime)        
    print("\nline {} is done, running time is:\n{}\n ".format(i,SpenTime))
    
df_pixels = pd.DataFrame(pixels)

print('Finish extraction of images from all line scans, next step: export .csv file')

#===========================================
# L0.3: extract images from each line scans 
#===========================================
SaveDir = ExtractionFolder + '\\pixels.csv'
df_pixels.to_csv(SaveDir, index=False, header=False, sep=',')

print('L0 extraction is done, please check output results at: \n{}'.format(ExtractionFolder))