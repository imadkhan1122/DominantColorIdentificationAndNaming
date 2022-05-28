#------------------------import important packages-----------------------------#
import glob
import os
from math import sqrt
import csv
import pandas as pd
from PIL import Image
from PIL import ImageColor
from PIL import ImageEnhance

df = pd.read_excel('colors.xlsx', index_col=False)
primary_names = []
colors_ = []
for i, j,  in df.iterrows():
    RGB_ = ImageColor.getcolor(j[0], "RGB")
    colors_.append(tuple((j[1], RGB_)))
    primary_names.append(tuple((j[1], j[2])))

COLORS = colors_
PRIMARY_NAMES = primary_names

#-------------------------CLASS DOMINANT_COLORS--------------------------------#
class DOMINAN_COLORS:
    # inti function
    def __init__(self):
        
        # defining path
        self.pth = input('Enter path to the images folder: ')
        self.color_ = COLORS
        self.primaryColors = PRIMARY_NAMES
                
        # call main function
        self.main()
    #-----------------------LOADING IMAGES FUNCTION-----------------------------#
    def LOAD_IMGS(self, pth):
        # list of images possible formats
        ext = ['png', 'jpg', 'jpeg']    # Add image formats here
        # empty list variable
        files = []
        # append images path to files list
        [files.extend(glob.glob(pth + '/' + '*.' + e)) for e in ext]
        # return list of images paths
        return files
    #-----------------------DOM COLORS EXTRACTOR--------------------------------#
    def DOM_COLORS(self, pth):
        img = Image.open(pth)                   # Open image
        curr_col = ImageEnhance.Color(img)
        new_col = 2.5
        img_colored = curr_col.enhance(new_col)
        reduced = img_colored.convert("P", palette=Image.ADAPTIVE, colors=2) # convert to web palette (216 colors)
        palette = reduced.getpalette() # get palette as [r,g,b,r,g,b,...]
        palette = [palette[3*n:3*n+3] for n in range(256)] # group 3 by 3 = [[r,g,b],[r,g,b],...]
        color_count = [(n, palette[m]) for n,m in reduced.getcolors()]
        
        F_max = tuple(color_count[0][1])
        S_max = tuple(color_count[1][1])
        return F_max, S_max
    #-----------------------TO CLOSEST COLOR IN COLORS LIST---------------------#
    def closest_color(self, rgb, colors):
     
        # defining three colors code
        r, g, b = rgb
        # empty list for color codes saving
        color_diffs = []
        # itterate over colors list
        for color in colors:
            # saving three colors codes in variavle for each color
            cr, cg, cb = color
            # finding nearest color code in colors with given color code
            color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
            # append colors defference into empty list
            color_diffs.append((color_diff, color))
        # return nearest color in list
        return min(color_diffs)[1]
    #-----------------------EXTRACT IMAGE_DATA---------------------------------#
    def IMAGE_DATA(self, pth):
        # define empty list
        PRIM_NAMES = self.primaryColors
        LST = []  
        # define temprary empty list
        temp_lst = []
        # empty list to store unques colors names and its codes
        lst = []
        # itterate over colors list
        for c in set(self.color_):
            # append unique tuples of colors
            lst.append(c)
            # append unique colors codes 
            temp_lst.append(c[1])
        # convert temp_list to tuple
        COLORS = tuple(temp_lst)
        # split path to extract file name
        img_name = os.path.split(pth)[1]
        # append file path to LST
        # append file name to LST
        LST.append(img_name)
        # calling DOM_COLORS function to get first and second dominant color
        F_COL, S_COL= self.DOM_COLORS(pth)
        
        # print(F_COL, S_COL)
        # call closest_color function to get first closest color in color list
        
        F_COL_NEAR = self.closest_color(F_COL, COLORS)
        # call closest_color function to get second closest color in color list
        print(F_COL,'-', F_COL_NEAR)
        S_COL_NEAR = self.closest_color(S_COL, COLORS)
        print(S_COL,'-', S_COL_NEAR)
        # itterate over colors list
        for color in lst:
            # if color match with 1st color
            if F_COL_NEAR == color[1]:
                # append 1st color name to LST
                LST.append(color[0])
                for prim in PRIM_NAMES:
                    if color[0] == prim[0]:
                        LST.append(prim[1])
            # if color match to second closest color code
            if S_COL_NEAR == color[1]:
                # appent color name to LST
                LST.append(color[0])  
                for prim in PRIM_NAMES:
                    if color[0] == prim[0]:
                        LST.append(prim[1])
        # return list of all reuqured data
        return LST

    #-----------------------------main FUNCTION---------------------------------#
    def main(self):
        # all the fields names in a list
        header = ["Image-Name", "First-Dominant-Color", "First-Dominant-Color-Primary", "Second-Dominant-Color", "Second-Dominant-Primary"]
        # call load_imgs function to get list of images paths in path variable
        path = self.LOAD_IMGS(self.pth)
        # create and open output.csv file
        with open('Output.csv', 'w', newline = '') as output_csv:
            # initialize rows writer
            csv_writer = csv.writer(output_csv)
            # write headers to the file
            csv_writer.writerow(header)
            # itterate over images paths
            for e, PTH in enumerate(path):
                # display number of images processed
                
                # call IMAGE_DATA function to get list of image data for each image
                lst = self.IMAGE_DATA(PTH)
                # display data
                print(lst)
                # write one row of data for each image file
                csv_writer.writerow(lst)
                print(str(e+1), 'IMAGES PROCESSED')
        return














