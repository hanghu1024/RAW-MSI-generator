#===========================================
# import modules, defs and variables
#===========================================
exec(open("./external.py").read())
exec(open("./defs.py").read())
exec(open("./config.py").read())

print('Finish modules, defs and variables import, next step: check the dimensionality of this MSI data set.')

#===========================================
# import data 
#===========================================
df_pixels = pd.read_csv(InputDir, header = None) # use pandas, cause the print is interpretable
if MassList_dir != 0: 
    df_MassList = pd.read_excel(MassList_dir, header = None)
    MassList = df_MassList.values.astype(np.float64)

print('Finish pixel raw data import')

#===========================================
# L1.0: data process
#===========================================
# data organization
pixels = df_pixels.values.astype(np.float64)
MassList = np.insert(MassList, 0, 0, axis = 0) # elements in np array should be same type, so 0 -> TIC

# parse info
NumLine = int(np.max(df_pixels[0]) + 1)
NumSpePerLine = int(np.max(df_pixels[1]) + 1)

# organize img (first 3 are indexes and TIC)
img = pixels.T.reshape(pixels.shape[1], NumLine, NumSpePerLine)
img_feature = np.delete(img, [0,1], axis=0)

# parameter for plotting
aspect = AspectRatio*NumSpePerLine/NumLine

# make folders for outputs
if ImageFolder == 0:
    folder_name = 'images-' + str(Norm) + '-norm'
    ImageFolder = locate_ImageFolder(InputDir, folder_name)

os.mkdir(ImageFolder) # include 'norm' name into folder name
os.mkdir(ImageFolder + '\\png files')

# also save .csv files?
if csv == 1:
    os.mkdir(ImageFolder + '\\csv files')
    
print('Finish raw data processing')

#===========================================
# L1.1: normalization 
#===========================================
# work with img
if type(Norm) == str:
    if Norm == 'none':
        img_feature_norm = img_feature.copy()
    if Norm == 'TIC':
        img_feature_norm = img_feature/img_feature[0]
else:
    std_index = np.where(MassList == Norm)
    img_feature_norm = img_feature/img_feature[std_index]

# flatten to get pixels
pixels_feature_norm = img_feature_norm.reshape(img_feature_norm.shape[0], -1).T

print('Finish normalization, next step: exporting plots')

#===========================================
# L1.2: plotting
#===========================================
# visualization scale
scale = round(NumLine*NumSpePerLine*VisuScale)

for i in range(img_feature_norm.shape[0]):        
    ### plot
    vmax = pixels_feature_norm[:,i][np.argsort(pixels_feature_norm[:,i])[scale]]
    plt.figure(figsize=[20,10])
    plt.imshow(img_feature_norm[i], aspect = aspect, cmap=colormap, vmax = vmax)
    
    # title and save path
    if MassList[i][0] == 0:
        title = 'No.' + str(i) + '  ' + 'TIC'
    else:
        title = 'No.' + str(i) + '  ' + str(MassList[i][0])
    SaveDir = ImageFolder + '\\png files\\' + title + '.png'
    
    # theme
    if colorbar != 0: plt.colorbar()
    if ticks == 0: plt.xticks([]), plt.yticks([])
    
    #plt.show()
    plt.savefig(SaveDir)
    plt.close()
    
    ### .csv save
    df_img = pd.DataFrame(img_feature_norm[i])
    SaveDir = ImageFolder + '\\csv files\\' + title + '.csv'
    df_img.to_csv(SaveDir, index=False, header=False, sep=',')
    
    ### progressbar
    if i != 0:
        if i % 20 ==0:
            print('Finish generating {}/{} ion images'.format(i, img_feature_norm.shape[0]))
        if i % (img_feature_norm.shape[0]-1) ==0:
            print('Finish L1.2 ion images export, next step: L1.3 show mosaic ion images')
    
#===========================================
# L1.3: plot ion image collection
#===========================================
# parameters:
w_fig = 20 # default setting
ncols = ncols
nrows = math.ceil((img_feature_norm.shape[0])/ncols)
h_fig = w_fig * nrows * (AspectRatio + 0.2) / ncols # 0.2 is the space for title parameters

fig = plt.figure(figsize=(w_fig,h_fig))
fig.subplots_adjust(hspace= -0.15, wspace=0.03)
for i in range(img_feature_norm.shape[0]):          
    vmax = pixels_feature_norm[:,i][np.argsort(pixels_feature_norm[:,i])[scale]]
    ax = fig.add_subplot(nrows, ncols, i+1) # start from 1
    ax.imshow(img_feature_norm[i], cmap=colormap, aspect = aspect, vmax = vmax)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # title
    if MassList[i][0] == 0:
        title = str(i) + '_' + 'TIC'
    else:
        title = str(i) + '_' + str(MassList[i][0])        
    ax.set_title(title, pad=3, fontsize = 7)

#plt.show()    
SaveDir = ImageFolder + '\\png files\\ion_image_mosaic.png'
plt.savefig(SaveDir, dpi=dpi)
plt.close()

print('Finish L1 image plotting, please check output results at: \n{}'.format(ImageFolder))