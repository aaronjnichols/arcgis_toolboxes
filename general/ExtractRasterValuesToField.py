import arcpy
import numpy as np
import time



def main():
    ts = time.time()
    
    # get parameters
    fc = arcpy.GetParameterAsText(0)
    raster = arcpy.GetParameterAsText(1)
    id_field = arcpy.GetParameterAsText(2)
    add_field = arcpy.GetParameterAsText(3)

    # execute tool
    ExtractRasterValuesToField(fc, raster, id_field, add_field)
    te = time.time()
    arcpy.AddMessage('Elapsed: {}'.format(round(te-ts, 1)))
    
def ExtractRasterValuesToField(fc, raster, id_field, add_field):
    # get minimum x and maximum y values, and raster cell size.
    # this is used to calculate which row and column the raster value is located in in the numpy array
    desc = arcpy.Describe(raster)
    xmin = desc.Extent.XMin
    ymax = desc.Extent.YMax
    cell_size = desc.meanCellHeight

    # convert featue to numpy array with columns for id, centroid x and y coordinates
    fc_arr = arcpy.da.FeatureClassToNumPyArray(fc, [id_field, 'SHAPE@X', 'SHAPE@Y'])
    # convert raster to numpy array
    raster_arr = arcpy.RasterToNumPyArray(raster)

    # calculate the row and column of the raster value at each of the feature's centroids
    row_arr = ((ymax - fc_arr['SHAPE@Y']) - ((ymax - fc_arr['SHAPE@Y']) % cell_size))/cell_size
    col_arr = ((fc_arr['SHAPE@X'] - xmin) - ((fc_arr['SHAPE@X'] - xmin) % cell_size)) / cell_size

    # create list of indices (row, col) to extract values from the raster numpy array
    rowcol_list = np.vstack((row_arr, col_arr)).tolist()

    # extract values from the raster numpy array
    ras_value_arr_temp = np.vstack((raster_arr[rowcol_list], fc_arr[id_field]))
    ras_value_arr = ras_value_arr_temp.transpose()

    # add column names to the raster value numpy array
    ras_to_fc_arr = np.rec.fromrecords(ras_value_arr, names='{}, Match_field'.format(add_field))
    arcpy.AddMessage('array size {}'.format(ras_to_fc_arr.shape))
    # add the raster data to table
    #arcpy.da.ExtendTable(fc, id_field, ras_to_fc_arr, 'Match_field', True)
    arcpy.da.NumPyArrayToTable(ras_to_fc_arr, r'Z:\2019\195022\Hydro\FLO-2D\FLO2D_GDB.gdb\rain_table')
    

if __name__ == '__main__':
    main()
