# Obtain data from output file (cell ID, value)
grid = 'Grid_South'
id_field = 'fid_1'
outflow_path = r'B:\WP FLO-2D\205131_Eagle_Shadows\Regional\2020-07-30_South_Updated_Inflows'
outflow_cells = 'Outflow_Cells_South'
outflow_field = 'OUT_NUM'
outpath = r'B:\WP FLO-2D\093415_05_NSCW\Model_Input_Data.gdb\Inflow_Outflow'

outflow = open(outflow_path + r'\OUTFLOW.DAT', 'r')

# loop through outflow.dat and get grid id's and outflow type
d = {}
grid_list = []
for line in outflow:
    splt = line.split()
    if len(splt) > 0:
        d[splt[1]] = splt[0]
        grid_list.append(splt[1])
        

def CreateShapefile(grids_list, new_shp, dictionary, GRID, id_field, outPath, field_name):
    gridsString = ",".join("%s" % grid for grid in grids_list)
    arcpy.SelectLayerByAttribute_management(GRID, "NEW_SELECTION", '"{}" IN ({})'.format(id_field, gridsString))
    SHP = outPath+r'\{}'.format(new_shp)
    arcpy.CopyFeatures_management(GRID, SHP)
    arcpy.AddField_management(SHP, field_name, 'FLOAT', 12, 1)

CreateShapefile(grid_list, outflow_cells, d, grid,  id_field, outpath, outflow_field)
