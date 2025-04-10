# read culvert geometry data from shapefile and format for RAS2D
import os
#import arcpy
import os
import numpy as np
import arcpy

#user inputs
model_path = r'U:\120_RAS2D\Training_Models' #file path to model
geo_name = r'Culvert_Automation.g02' #geometry file name
fc = r'Culvert'

fields = ['NAME', 'CULV_SHAPE', 'DIA_RISE', 'SPAN', 'MANNINGS_N', 'ENTR_LOSS', 'EXIT_LOSS', 'CHART_NUM', 'SCALE_NUM', 'US_STA', 'DS_STA', 'US_INV', 'DS_INV']
# convert feature class to numpy array
culv_arr = arcpy.da.FeatureClassToNumPyArray(fc, fields)
unknown1 = 1
unknown2 = 0

# open ras geometry file
geo = open(os.path.join(model_path, geo_name), 'r')
geo_name_new = 'culverts_added.g99'
geo_culv = open(os.path.join(model_path, geo_name_new), 'w')

i = 0
switch = 0
for line in geo:
    if switch == 1:
        geo_culv.write('                \n')
        switch = 0
    elif 'Connection Culv=' in line:
        splt = line.split(',')
        length = splt[3]
        group = splt[12]
        l = 'Connection Culv={},{:.2f},{:.2f},{},{:.3f},{:.1f},{:.1f},{},{},{:.2f},{:.2f},{},{},{},\n'.format(culv_arr['CULV_SHAPE'][i],
                                                                                                                  culv_arr['DIA_RISE'][i],
                                                                                                                  culv_arr['SPAN'][i],
                                                                                                                  length,
                                                                                                                  culv_arr['MANNINGS_N'][i],
                                                                                                                  culv_arr['ENTR_LOSS'][i],
                                                                                                                  culv_arr['EXIT_LOSS'][i],
                                                                                                                  culv_arr['CHART_NUM'][i],
                                                                                                                  culv_arr['SCALE_NUM'][i],
                                                                                                                  culv_arr['US_INV'][i],
                                                                                                                  culv_arr['DS_INV'][i],
                                                                                                                  unknown1,
                                                                                                                  group,
                                                                                                                  unknown2)
        geo_culv.write(l)
        switch = 1
    elif 'Conn Culv Bottom n=' in line:
        l = 'Conn Culv Bottom n={:.3f}\n'.format(culv_arr['MANNINGS_N'][i])
        geo_culv.write(l)
        i += 1
    else:
        geo_culv.write(line)
geo.close()
geo_culv.close()
