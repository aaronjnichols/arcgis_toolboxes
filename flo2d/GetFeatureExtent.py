import arcpy

# change fc to the name of the desired feature in the table of contents
fc = 'North_Boundary'

# create object with feature extents
ext = arcpy.Describe(fc).extent

# print xmin, xmax, ymin, ymax
print('XMIN = {}'.format(ext.XMin))
print('XMAX = {}'.format(ext.XMax))
print('YMIN = {}'.format(ext.YMin))
print('YMAX = {}'.format(ext.YMax))
