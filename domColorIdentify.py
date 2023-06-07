#------------------------import important packages-----------------------------#
import glob
import os
from math import sqrt
import csv
import pandas as pd
import PIL
from PIL import Image
from PIL import ImageColor
from PIL import ImageEnhance
from tqdm import tqdm
PIL.Image.MAX_IMAGE_PIXELS = 99933120000

#---------------------------Create Colors List--------------------------------#
if not os.path.exists('colors.txt'):
    df = pd.read_excel('colors.xlsx', index_col=False)
    COLORS = []
    for i, j,  in df.iterrows():
        RGB_ = ImageColor.getcolor(j[0], "RGB")
        COLORS.append(tuple((j[1], RGB_, j[2])))
    df2 = pd.read_excel('SCRIPT-string-color-key.xlsx', index_col=False)
    colorStr = []
    for i, j,  in df2.iterrows():
        match = [(e[0], e[1], e[2], j[1]) for e in COLORS if e[0] == j[0]]
        colorStr.append(match[0])
    
    with open("colors.txt", "w") as file:
        file.write(str(colorStr))

with open("colors.txt", "r") as file:
    colors = eval(file.readline())
#-------------------------CLASS DOMINANT_COLORS--------------------------------#
class DOMINAN_COLORS:
    # inti function
    def __init__(self):
        
        # defining path
        self.pth = input('Enter path to the images folder: ')
        self.color_ = colors
                
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
        try:
            img = Image.open(pth)              # Open image
            curr_col = ImageEnhance.Color(img)
            new_col = 2.5
            img_colored = curr_col.enhance(new_col)
            reduced = img_colored.convert("P", palette=Image.ADAPTIVE, colors=5) # convert to web palette (216 colors)
            palette = reduced.getpalette() # get palette as [r,g,b,r,g,b,...]
            palette = [palette[3*n:3*n+3] for n in range(256)] # group 3 by 3 = [[r,g,b],[r,g,b],...]
            color_count = [(n, palette[m]) for n,m in reduced.getcolors()]
            color_count.sort(reverse=True)
            F_max = tuple(color_count[0][1])
            S_max = tuple(color_count[1][1])
            
        except:
            img = Image.open(pth).convert('RGBA')              # Open image
            reduced = img.convert("P", palette=Image.ADAPTIVE, colors=5) # convert to web palette (216 colors)
            palette = reduced.getpalette() # get palette as [r,g,b,r,g,b,...]
            palette = [palette[3*n:3*n+3] for n in range(256)] # group 3 by 3 = [[r,g,b],[r,g,b],...]
            color_count = [(n, palette[m]) for n,m in reduced.getcolors()]
            color_count.sort(reverse=True)
            F_max = tuple(color_count[1][1])
            S_max = tuple(color_count[2][1])
        finally:
            pass
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
        color = self.color_
        LST = []  
        # define temprary empty list
        temp_lst = []
        # empty list to store unques colors names and its codes
        
        # itterate over colors list
        for c in set(color):
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
        
        S_COL_NEAR = self.closest_color(S_COL, COLORS)
        
        # itterate over colors list
        for col in color:
            # if color match with 1st color
            if F_COL_NEAR == col[1]:
                # append 1st color name to LST
                LST.append(col[0])
                LST.append(col[2])
                LST.append(col[3])
            # if color match to second closest color code
            if S_COL_NEAR == col[1]:
                # appent color name to LST
                LST.append(col[0])  
                LST.append(col[2])
                LST.append(col[3])
        # return list of all reuqured data
        return LST

    #-----------------------------main FUNCTION---------------------------------#
    def main(self):
        # all the fields names in a list
        header = ["Image Name", "First Dominant Color", "First Dominant Color Primary", "First dominant string color", "Second Dominant Color", "Second Dominant Primary", "Second dominant string color"]
        # call load_imgs function to get list of images paths in path variable
        path = self.LOAD_IMGS(self.pth)
        # create and open output.csv file
        with open('Output.csv', 'w', newline = '') as output_csv:
            # initialize rows writer
            csv_writer = csv.writer(output_csv)
            # write headers to the file
            csv_writer.writerow(header)
            # itterate over images paths
            for PTH in tqdm(path):
                # display number of images processed
                # call IMAGE_DATA function to get list of image data for each image
                try:
                    lst = self.IMAGE_DATA(PTH)
                    # write one row of data for each image file
                    csv_writer.writerow(lst)
                except:
                    print('Process failed for:', PTH)
        return














