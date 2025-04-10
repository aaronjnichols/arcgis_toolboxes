import arcpy
import os

def WriteFPXSEC(fpxs, case_field, dirField, grid, idField, datPath):

    # Create dictionary of flow directions and count number of fpxs in shapefile
    dirDict = {}
    with arcpy.da.SearchCursor(fpxs, [case_field, dirField]) as cursor:
        for row in cursor:
            dirDict[str(row[0])] = row[1]
    count = len(dirDict.keys())

    arcpy.AddMessage('Number of floodplain cross sections = {}'.format(count))
    # Select grid by location and write to FPXSEC.DAT for each floodplain cross section.
    arcpy.MakeFeatureLayer_management(fpxs, 'fpxs_lyr')

    f_path = os.path.join(datPath, 'FPXSEC.DAT')
    FPXSEC = open(f_path, 'w')
    FPXSEC.write('{} {}\n'.format('P', '0'))
    for i in dirDict.keys():
        arcpy.SelectLayerByAttribute_management(fpxs, 'NEW_SELECTION', """"{}" = {}""".format(case_field, i))
        arcpy.SelectLayerByLocation_management(grid, 'HAVE_THEIR_CENTER_IN', fpxs, 10)
        with arcpy.da.SearchCursor(grid, idField) as cursor:
            grid_ids = [int(row[0]) for row in cursor]
            direction = dirDict[str(i)]
            num_grids = len(grid_ids)
            formatted_grid_ids = ''.join(str(j)+' ' for j in grid_ids)
            FPXSEC.write('{} {} {} {}\n'.format('X', direction, num_grids, formatted_grid_ids))

    FPXSEC.close()

if __name__ == '__main__':
    fpxs = arcpy.GetParameterAsText(0)
    dirField = arcpy.GetParameterAsText(1)
    case_field =  arcpy.GetParameterAsText(2)
    grid = arcpy.GetParameterAsText(3)
    idField = arcpy.GetParameterAsText(4)
    datPath = arcpy.GetParameterAsText(5)
    
    WriteFPXSEC(fpxs, case_field, dirField, grid, idField, datPath)

        
 
    
