import numpy as np
from PIL import Image


def imgPath2mat_rRGB(path):
    imgRaw = Image.open(path)
    imgRGB = imgRaw.split()
    imgR = imgRGB[0]
    imgG = imgRGB[1]
    imgB = imgRGB[2]
    return (imgR, imgG, imgB)

def mat_rRGB2img(path, imgR, imgG, imgB):
    imgCombined = np.dstack((np.dstack((imgR, imgG)), imgB))
    imgPIL      = Image.fromarray(imgCombined)
    imgPIL.save(path)

def call_by_object(up_path, dl_path):
    # cnv img
    imgR, imgG, imgB = imgPath2mat_rRGB(dl_path)
    imgG_f64 = np.array(imgG, np.uint8).astype(np.float64)
    
    imgG_f64 = 0.5 * imgG_f64
    imgG_u8 = imgG_f64.astype(np.uint8)
    mat_rRGB2img(up_path, imgR, imgG_u8, imgB)
    
    return
