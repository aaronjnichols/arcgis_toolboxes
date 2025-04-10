import arcpy

# inputs
grid = arcpy.GetParameterAsText(0)
id_field = arcpy.GetParameterAsText(1)
sfc = arcpy.GetParameterAsText(2)
n_field = arcpy.GetParameterAsText(3)
outpath = arcpy.GetParameterAsText(4)

arcpy.env.overwriteOutput = True

# add n field to grid attribute table
# arcpy.AddField_management(grid, 'N', 'FLOAT', 4, 3)

# intersect grid with surface feature characterization
if '.gdb' in outpath:
    grid_sfc = r'{}\grid_sfc'.format(outpath)
else:
    grid_sfc = r'{}\grid_sfc.shp'.format(outpath)
arcpy.Intersect_analysis([sfc, grid], grid_sfc)

# get total number of grid cells
result = arcpy.GetCount_management(grid)
grid_count = int(result[0])

# get grid cell area
with arcpy.da.SearchCursor(grid, ['SHAPE@AREA']) as cur:
    for row in cur:
        grid_area = row[0]
        break

# populate dictionary with area averaged n-values per grid cell
with arcpy.da.SearchCursor(grid_sfc, [id_field, n_field, 'SHAPE@AREA']) as cur:
    nDict = {i+1: [] for i in range(grid_count)}
    for row in cur:
        nDict[row[0]].append(row[1]*row[2]/grid_area)
arcpy.AddMessage('{}'.format(nDict[1]))
# add area averaged n-values to grid cell attribute table
with arcpy.da.UpdateCursor(grid, [id_field, 'N']) as cur:
    for row in cur:
        row[1] = sum(nDict[row[0]])
        cur.updateRow(row)
