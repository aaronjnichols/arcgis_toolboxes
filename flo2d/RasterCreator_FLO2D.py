import os
import gdal     #gdal would need to be installed on computer in order to use this tool
import shutil

#SRS layer will need to be changed dependent on projection layer. Use prj4 from https://www.spatialreference.org/ for insertion. Setup for Cent AZ

#Environment the project is functioning in
Space = "C:/Users/jthies/Documents/FLO-2D Data"

#Boundary Shape that the grid would like to be clipped to (AKA Model Boundary)
BoundaryShp = "4624_Boundary_North.shp"

#Reset of program, necessary in order for it to run properly. 
try:
    shutil.rmtree(Space + "//maxdepth")
    shutil.rmtree(Space + "//peakflow")
    shutil.rmtree(Space + "//maxvelocity")
    shutil.rmtree(Space + "//maxwse")
    shutil.rmtree(Space + "//peakdir")
    shutil.rmtree(Space + "//peaktime")
    shutil.rmtree(Space + "//peakflowwse")
    shutil.rmtree(Space + "//peakflowdepth")
    shutil.rmtree(Space + "//peakqvel")
    shutil.rmtree(Space + "//finaldepth")
    shutil.rmtree(Space + "//info")
    shutil.rmtree(Space + "//extract_maxd1")
    os.remove(Space + "/MaxDepth.aux.xml")
    os.remove(Space + "/PeakFlow.aux.xml")
    os.remove(Space + "/MaxVelocity.aux.xml")
    os.remove(Space + "/MaxWSE.aux.xml")
    os.remove(Space + "/PeakDir.aux.xml")
    os.remove(Space + "/PeakTime.aux.xml")
    os.remove(Space + "/PeakFlowWSE.aux.xml")
    os.remove(Space + "/PeakFlowDepth.aux.xml")
    os.remove(Space + "/PeakQVel.aux.xml")
    os.remove(Space + "/FinalDepth.aux.xml")
    os.remove(Space + "/Extract_MaxD1.aux.xml")
    os.remove(Space + "/log")
    os.remove(Space + "\MaxD.tif")
    os.remove(Space + "\PeakQ.tif")
    os.remove(Space + "\MaxVel.tif")
    os.remove(Space + "\MaxWSEL.tif")
    os.remove(Space + "\PeakQDir.tif")
    os.remove(Space + "\PeakQTime.tif")
    os.remove(Space + "\PeakQWSE.tif")
    os.remove(Space + "\PeakQDepth.tif")
    os.remove(Space + "\PeakQVelocity.tif")
    os.remove(Space + "\FinalDep.tif")
except:
    pass

# In order for the function to work, makesure the output data is located in the bottom folder
dir_with_csvs = Space
os.chdir(dir_with_csvs)

def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = os.listdir(path_to_dir)
    filename = "Output_Data"                #This .csv file is used to make the following .tif's. This naming output is consistent with FLO-2D results
    return [ filename for filename in filenames if filename.endswith(suffix) ]
csvfiles = find_csv_filenames(dir_with_csvs)

# Code for Max Water Depth
for fn in csvfiles:
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')
    with open(vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write('\t\t\t<LayerSRS>+proj=tmerc +lat_0=31 +lon_0=-111.9166666666667 +k=0.9999 +x_0=213360 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs </LayerSRS>\n') #Coordinate System
        fn_vrt.write('\t\t<GeometryField encoding="PointFromColumns" x="X" y="Y" z="MaxDepth"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

output = gdal.Grid('MaxD.tif','Output_Data.vrt', algorithm = "linear:nodata")

# Code for Peak Flow Raster
for fn in csvfiles:
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')
    with open(vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write('\t\t\t<LayerSRS>+proj=tmerc +lat_0=31 +lon_0=-111.9166666666667 +k=0.9999 +x_0=213360 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs </LayerSRS>\n') #Coordinate System
        fn_vrt.write('\t\t<GeometryField encoding="PointFromColumns"   x="X" y="Y" z="QPcomb"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

output = gdal.Grid('PeakQ.tif','Output_Data.vrt', algorithm = "linear:nodata")

# Code for Max Velocity Raster
for fn in csvfiles:
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')
    with open(vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write('\t\t\t<LayerSRS>+proj=tmerc +lat_0=31 +lon_0=-111.9166666666667 +k=0.9999 +x_0=213360 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs </LayerSRS>\n') #Coordinate System
        fn_vrt.write('\t\t<GeometryField encoding="PointFromColumns"   x="X" y="Y" z="MaxVel"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

output = gdal.Grid('MaxVel.tif','Output_Data.vrt', algorithm = "linear:nodata")

# Code for Max WSEL Raster
for fn in csvfiles:
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')
    with open(vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write('\t\t\t<LayerSRS>+proj=tmerc +lat_0=31 +lon_0=-111.9166666666667 +k=0.9999 +x_0=213360 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs </LayerSRS>\n') #Coordinate System
        fn_vrt.write('\t\t<GeometryField encoding="PointFromColumns"   x="X" y="Y" z="MaxWSEL"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

output = gdal.Grid('MaxWSEL.tif','Output_Data.vrt', algorithm = "linear:nodata")

# Code for Peak Direction
for fn in csvfiles:
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')
    with open(vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write('\t\t\t<LayerSRS>+proj=tmerc +lat_0=31 +lon_0=-111.9166666666667 +k=0.9999 +x_0=213360 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs </LayerSRS>\n') #Coordinate System
        fn_vrt.write('\t\t<GeometryField encoding="PointFromColumns"   x="X" y="Y" z="QPcombDir"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

output = gdal.Grid('PeakQDir.tif','Output_Data.vrt', algorithm = "linear:nodata")

# Code for Peak Time
for fn in csvfiles:
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')
    with open(vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write('\t\t\t<LayerSRS>+proj=tmerc +lat_0=31 +lon_0=-111.9166666666667 +k=0.9999 +x_0=213360 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs </LayerSRS>\n') #Coordinate System
        fn_vrt.write('\t\t<GeometryField encoding="PointFromColumns"   x="X" y="Y" z="QPTime"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

output = gdal.Grid('PeakQTime.tif','Output_Data.vrt', algorithm = "linear:nodata")

# Code for Peak WSE
for fn in csvfiles:
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')
    with open(vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write('\t\t\t<LayerSRS>+proj=tmerc +lat_0=31 +lon_0=-111.9166666666667 +k=0.9999 +x_0=213360 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs </LayerSRS>\n') #Coordinate System
        fn_vrt.write('\t\t<GeometryField encoding="PointFromColumns"   x="X" y="Y" z="QPWSE"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

output = gdal.Grid('PeakQWSE.tif','Output_Data.vrt', algorithm = "linear:nodata")

# Code for Peak Depth
for fn in csvfiles:
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')
    with open(vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write('\t\t\t<LayerSRS>+proj=tmerc +lat_0=31 +lon_0=-111.9166666666667 +k=0.9999 +x_0=213360 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs </LayerSRS>\n') #Coordinate System
        fn_vrt.write('\t\t<GeometryField encoding="PointFromColumns"   x="X" y="Y" z="QPDepth"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

output = gdal.Grid('PeakQDepth.tif','Output_Data.vrt', algorithm = "linear:nodata")

# Code for Peak Velocity
for fn in csvfiles:
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')
    with open(vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write('\t\t\t<LayerSRS>+proj=tmerc +lat_0=31 +lon_0=-111.9166666666667 +k=0.9999 +x_0=213360 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs </LayerSRS>\n') #Coordinate System
        fn_vrt.write('\t\t<GeometryField encoding="PointFromColumns"   x="X" y="Y" z="QPVel"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

output = gdal.Grid('PeakQVelocity.tif','Output_Data.vrt', algorithm = "linear:nodata")

# Code for Final Depth
for fn in csvfiles:
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')
    with open(vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write('\t\t\t<LayerSRS>+proj=tmerc +lat_0=31 +lon_0=-111.9166666666667 +k=0.9999 +x_0=213360 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs </LayerSRS>\n') #Coordinate System
        fn_vrt.write('\t\t<GeometryField encoding="PointFromColumns"   x="X" y="Y" z="FinalDepth"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

output = gdal.Grid('FinalDep.tif','Output_Data.vrt', algorithm = "linear:nodata")

# Buffer Code 
for fn in csvfiles:
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')
    with open(vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write('\t\t\t<LayerSRS>+proj=tmerc +lat_0=31 +lon_0=-111.9166666666667 +k=0.9999 +x_0=213360 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs </LayerSRS>\n') #Coordinate System
        fn_vrt.write('\t\t<GeometryField encoding="PointFromColumns"   x="X" y="Y" z="GRIDCODE"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

output = gdal.Grid('GRIDCODE.tif','Output_Data.vrt', algorithm = "linear:nodata")

#Clipping Tool Section, make sure to adjust these for each input
import arcpy
from arcpy import env
from arcpy.sa import *

#Defining workspace for the actions to be committed
env.workspace = Space

#Checking out Spatial Analyst Tool
arcpy.CheckOutExtension('Spatial')

#Masking Oustide Coordinates to Come to Boundary Results
outExtractByMask = ExtractByMask("MaxD.tif", BoundaryShp)
outExtractByMask.save(Space + "/MaxDepth")
outExtractByMask = ExtractByMask("PeakQ.tif", BoundaryShp)
outExtractByMask.save(Space + "/PeakFlow")
outExtractByMask = ExtractByMask("MaxVel.tif", BoundaryShp)
outExtractByMask.save(Space + "/MaxVelocity")
outExtractByMask = ExtractByMask("MaxWSEL.tif", BoundaryShp)
outExtractByMask.save(Space + "/MaxWSE")
outExtractByMask = ExtractByMask("PeakQDir.tif", BoundaryShp)
outExtractByMask.save(Space + "/PeakDir")
outExtractByMask = ExtractByMask("PeakQTime.tif", BoundaryShp)
outExtractByMask.save(Space + "/PeakTime")
outExtractByMask = ExtractByMask("PeakQWSE.tif", BoundaryShp)
outExtractByMask.save(Space + "/PeakFlowWSE")
outExtractByMask = ExtractByMask("PeakQDepth.tif", BoundaryShp)
outExtractByMask.save(Space + "/PeakFlowDepth")
outExtractByMask = ExtractByMask("PeakQVelocity.tif", BoundaryShp)
outExtractByMask.save(Space + "/PeakQVel")
outExtractByMask = ExtractByMask("FinalDep.tif", "4624_Boundary_North.shp")
outExtractByMask.save(Space + "/FinalDepth")

#Removing .tif grid files
os.remove(Space + "\MaxD.tif")
os.remove(Space + "\PeakQ.tif")
os.remove(Space + "\MaxVel.tif")
os.remove(Space + "\MaxWSEL.tif")
os.remove(Space + "\PeakQDir.tif")
os.remove(Space + "\PeakQTime.tif")
os.remove(Space + "\PeakQWSE.tif")
os.remove(Space + "\PeakQDepth.tif")
os.remove(Space + "\PeakQVelocity.tif")
os.remove(Space + "\FinalDep.tif")

#Check in Spatial Analyst Tool
arcpy.CheckInExtension('Spatial')

