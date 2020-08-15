#===========================================
# DEFS RAW-MSI-generator
#===========================================

## General functions

# 0. parse mass list info
'''
mass list file format: .xlsx
data format: 3 columns: m/z, compound name, adduct name

'''
def GetMassList(FileName):
    data=pd.read_excel(FileName,names=["m/z","compound","adduct"],header=None)
    Mass=data['m/z'].values.astype(np.float64)
    Comp=data['compound'].values.astype(str)
    Add=data['adduct'].values.astype(str)
    return Mass, Comp, Add

# 1. parse the dimension of the MSI data set
def DimCheck(NumLine, NameBody):
    NumLineSpectra=np.empty([0,2],int)
    NameBody=NameBody
    NamePost='.raw'
    
    for i in range(1,NumLine+1):
        Name=NameBody+str(i)+NamePost
        RawFile=MSFileReader(Name)
        NumSpectra=int(RawFile.GetNumSpectra())
        RawFile.Close()
        NumLineSpectra=np.append(NumLineSpectra,[[i,NumSpectra]],axis=0)
    
    ColName=np.array(['# of line','# of spectra'])
    NumLineSpectra=pd.DataFrame(NumLineSpectra, columns=ColName)
    NumLineSpectra=NumLineSpectra.set_index('# of line')
    print(NumLineSpectra)
    print('\nline scan spectra summary\n# of lines is: {}\nmean # of spectra is: {}'.format(NumLineSpectra.shape[0],int(NumLineSpectra.mean())))
    return NumLineSpectra

# 2. return the default folder directory for extraction outputs
def locate_ExtractionFolder(InputDir): 
    InputFolder = InputDir.replace(InputDir.split('\\')[-1], '')
    f = []
    for (dirpath, dirnames, filenames) in os.walk(InputFolder):
        f.extend(dirnames)
        break
    
    # check if 'Extraction' name exsits
    ii = 0 
    for foldernames in f:
        if foldernames.split('_')[0] == 'Extraction':
            ii += 1
    # determine the OutputFolder dir
    if ii == 0:
        OutputFolder = InputFolder + 'Extraction'
    else:
        OutputFolder = InputFolder + 'Extraction' + '_' + str(ii)
    return OutputFolder

# 3. return the default folder directory for ion image outputs
'''
L0outputDir is a str (dir), folder_name is a str.
'''
def locate_ImageFolder(L0outputDir,folder_name): 
    L0outputDir = L0outputDir.replace('\\'+L0outputDir.split('\\')[-1], '')
    OutputFolder = L0outputDir.replace('\\'+L0outputDir.split('\\')[-1], '')

    f = []
    for (dirpath, dirnames, filenames) in os.walk(OutputFolder):
        f.extend(dirnames)
        break
    
    # check if folder_name name exsits
    ii = 0 
    for foldernames in f:
        if foldernames.split('_')[0] == folder_name:
            ii += 1
    # determine the OutputFolder dir
    if ii == 0:
        OutputFolder = OutputFolder + '\\' + folder_name
    else:
        OutputFolder = OutputFolder + '\\' + folder_name + '_' + str(ii)
    return OutputFolder
#===========================================
