from napari.plugins.io import read_data_with_plugins


def read_image(imagefile):
    data, _ = read_data_with_plugins(imagefile)
    return data
    
data = read_image("/Users/cjw/Desktop/RGB11/MeOH-QS-002.tif")
data2 = read_image("Data/test.nd2")
print(data[0][0].shape, data[0][0].mean(axis=(1,2)))    
print(data2[0][0].shape, data2[0][0].mean(axis=(1,2)))    