#
# helper libraries
#
import pprint as pp    # pretty print library is better to print list and dictionary structures
import os
import  matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pandas as pd

#
# pma_python library
#
from pma_python import core
print("pma_python library loaded; version", core.__version__)

# connection parameters to be used throughout this notebook
pma_start_slide_dir = "C:/wsi"

if core.is_lite():
    print ("Connected to PMA.start")
else:
    raise Exception("Unable to detect PMA.start! Please start PMA.start, or download it from http://free.pathomation.com")