import random
from multiprocessing import freeze_support

import rawpy
import numpy as np
from PIL import Image
from tqdm import tqdm
from renderer import Renderer

def main():
    r = Renderer(4, "DSC_0896.NEF")
    img_arr = r.render_multicore()
    Image.fromarray(img_arr).save("DSC_0896_GENERATED.tiff")
    print("DONE!")

if __name__ == '__main__':
    freeze_support()
    main()