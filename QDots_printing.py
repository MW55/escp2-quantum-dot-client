import os
import binascii
import math
from hex_functions import *
from esc_functions import *
import numpy as np
from collections import OrderedDict
import subprocess


curr_dir = os.path.dirname(os.path.realpath(__file__))



# one of the printers for which the header and footer files are available in
# the 'prns' folder
printer = 'EPSON_ET-2750_Series'
outputfolder = 'output'

# LOAD HEADER AND FOOTER FOR SELECTED PRINTER
header = load_prn_file(curr_dir + '/prns/et2750/et2750-header.prn')
footer = load_prn_file(curr_dir + '/prns/et2750/et2750-footer.prn')

# unit parameters
pmgmt = 720
vert = 720
hor = 720
mbase = 2880 #2816
nozzles = 60

# colors
black = b'\x00'
black2 = b'\x05'
black3 = b'\x06'
cyan = b'\x02'
magenta = b'\x01'
yellow = b'\x04'

# select dot size
d = b'\x10'
# set page method ID
esc_m = ESC_m(b'\x20')
# set uni or bi directional mode
unim = b'\x00'  # 01 uni, 00 bi


def create_dot_matrix(x, y, color, mat, spacing=3, size=0):
    """
    A Matrix represents dots of a single color that are to be printed in close proximity
    The matrix is created using a list of lists in Python, with each nested list representing all nozzles of the choosen color, for the ET-2750, each nozzle group (color) has 59 nozzles, with black having three groups with 59 nozzles (black, black2, black3). Each element of the matrix represents a single nozzle, with 0 = no printing, 1 = small dot, 2 = medium dot, 3 = large dot.
    As an example, for a printer with 3 nozzles per color, a matrix that would print 3 small dots in a diagonal line would look like this: [[100], [010] ,[001]]
    The amount of nested lists inside the main list are the amount of nozzles needed in the printhead travel direction
    """
    color_matrix = ESC_i_matrix(color, mat, spacing, fan=size)
    rasterdata = ESC_v(pmgmt, y) + ESC_dollar(hor, x) + color_matrix
    return rasterdata


def create_single_dot(color, size, x, y):
    """
    Create a single dot of "color", of a size (1=small, 2=medium, 3=big)
    at position x,y
    the vertical position is relative to the last position!
    """
    # createnozzlelist(nozzles,activen,spacing,firstnozzle=1)
    # with activen = number of activate nozzles
    # and spacing = number of inactivate nozzles between acitvate nozzles

    nozzlelist = createnozzlelist(nozzles, 1, 0, 1)
    rasterdata = ESC_v(pmgmt, y) + ESC_dollar(hor, x) + ESC_i_nrs(nozzlelist, color, size)

    return rasterdata


def create_printfile(filename, raster):
    rasterdata = raster + b'\x0c'

    body = ESC_Graph() + ESC_Units(pmgmt, vert, hor, mbase) + ESC_Kmode() + \
        ESC_imode(n=b'\x00') + ESC_Umode(unim) + ESC_edot(d) + \
        ESC_Dras(v=240/3, h=120/3) + ESC_C(pmgmt) + ESC_c(pmgmt) + ESC_S(pmgmt)  # + esc_m

    # COMBINE
    total = header + body + rasterdata + footer
    fname = outputfolder + '/' + filename + '.prn'

    return (total, fname)


def save_prn_file(total, fname):
    with open(fname, "wb") as f:
        f.write(total)
    print("Written the raw print file to: " + fname)


def unprint(filename):
    uprint = subprocess.call("gutenprint/unprint " + filename + " " + filename[:-3] + "pnm", shell=True)
    if uprint == 0:
        print("The unprinted image was written to: " + filename[:-3] + "pnm")
    else:
        print("Unprinting failed, error code: " + str(uprint))


#if __name__ == "__main__":
#    # SAVE PRN FILE
#    total, fname = create_printfile(filename, raster)
#    save_prn_file(total, fname)
#    print('DONE!')
#    print('path: ' + fname)
