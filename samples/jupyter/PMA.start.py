import pprint as pp    # pretty print library is better to print list and dictionary structures
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pandas as pd 

# pma_python
from pma_python import core
print("pma_python library loaded; version", core.__version__)

# connection parameters to be used throughout this notebook
# pma_core_server = "https://host.pathomation.com/sandbox/2/PMA.core"
# creds = easygui.multpasswordbox('Server = ' + pma_core_server, 'Credentials', ["username", "password"])
# pma_core_user = creds[0]
# pma_core_pass = creds[1]
pma_core_slide_dir = "C:/wsi"

if   core.is_lite():
    print ("PMA.core found. Good")
else:
    raise Exception("Unable to detect PMA.core! Please update configuration parameters in this block")
core.set_debug_flag(True)
print("Are you running PMA.start? " + str(core.is_lite())) 
sessionID = core.connect( )	

if (sessionID == None):
    print("Unable to connect to PMA.core"); 
else:
    print("Successfully connected to PMA.core; sessionID", sessionID)
print("You have the following root-directories on your system: ")
rootdirs = core.get_root_directories(sessionID)
pp.pprint(rootdirs)
rootdirs = core.get_root_directories(sessionID)
print("Directories found in ", rootdirs[0],":")

dirs = core.get_directories(rootdirs[0], sessionID)
pp.pprint(dirs)
slide_dir = pma_core_slide_dir
print("Looking for slides in " + slide_dir)
print()

print ("**Non-recursive:")
print(core.get_slides(slide_dir))

print ("\n**One-level deep recursion:")
print(core.get_slides(slide_dir, recursive = 1))

print ("\n**Full recursion:")
print(core.get_slides(slide_dir, recursive = True))
slide_dir = pma_core_slide_dir

print("Looking for slides in", slide_dir)
print()

slide_dir = pma_core_slide_dir
print("Looking for slides in", slide_dir)
print()

for slide in core.get_slides(slide_dir):
    print("***", slide)
    try:
        pp.pprint(core.get_slide_info(slide))
    except:
        print("**Unable to get slide info from this one")

slide_dir = pma_core_slide_dir

for slide in core.get_slides(slide_dir):
    print("[" + slide + "]")
    try:
        xdim_pix, ydim_pix = core.get_pixel_dimensions(slide)
        xdim_phys, ydim_phys = core.get_physical_dimensions(slide)

        print("Pixel dimensions of slide: ", end="")
        print(xdim_pix, "x", ydim_pix)

        print("Slide surface area represented by image: ", end="")
        print(str(xdim_phys) + "µm x " + str(ydim_phys) + "µm = ", end="")
        print(xdim_phys * ydim_phys / 1E6, " mm2")
        
    except:
        print("**Unable to parse", slide)


slide_dir = pma_core_slide_dir

for slide in core.get_slides(slide_dir, recursive=1):
    print("[" + slide + "]")
    try:
        xdim_pix, ydim_pix = core.get_pixel_dimensions(slide)
        xdim_phys, ydim_phys = core.get_physical_dimensions(slide)

        print("Pixel dimensions of slide: ", end="")
        print(xdim_pix, "x", ydim_pix)

        print("Slide surface area represented by image: ", end="")
        print(str(xdim_phys) + "µm x " + str(ydim_phys) + "µm = ", end="")
        print(xdim_phys * ydim_phys / 1E6, " mm2")
        
    except:
        print("**Unable to parse", slide)

slide_dir = pma_core_slide_dir

for slide in core.get_slides(slide_dir, recursive=1):
    print("***", slide)
    print("  max zoomlevel:", core.get_max_zoomlevel(slide))
    print("  zoomlevel list:")
    pp.pprint(core.get_zoomlevels_list(slide))
    print("  zoomlevel dictionary:")
    pp.pprint(core.get_zoomlevels_dict(slide))

slide_dir = pma_core_slide_dir

slide_infos = []     # create blank list (to be converted into a pandas DataFrame later)

for slide in core.get_slides(slide_dir, recursive=1):
	dict = {
		"slide": core.get_slide_file_name(slide),
		"approx_mag": core.get_magnification(slide, exact=False),
		"exact_mag": core.get_magnification(slide, exact=True),
		"is_fluo": core.is_fluorescent(slide),
		"is_zstack": core.is_z_stack(slide)
		}
	slide_infos.append(dict)
	
df_slides = pd.DataFrame(slide_infos, columns=["slide","approx_mag","exact_mag", "is_fluo", "is_zstack"])
print(df_slides)
slides = core.get_slides(pma_core_slide_dir, recursive=1)
slide = slides[1]
print(slide[1])
for zl in range(0, core.get_max_zoomlevel(slide)):
    (x, y, tot) = core.get_number_of_tiles(slide, zl)
    if tot > 16 and x >= 4 and y >= 4:
        break
for i in range(1,17):
    plt.subplot(4, 4, i)
    xr = 1 + (i-1) % 4
    yr = int((i-1) / 4) + 1
    tile = core.get_tile(slide, xr, yr, zl)
    plt.imshow(tile)

plt.show()