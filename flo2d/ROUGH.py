import os

grid = 
grid_id = 'GRIDCODE'
f_path = r'Z:\2017\174766.04\Project Support\Outgoing\2020-10-06_1st_Model_Submittal\Models\South'
f = open(os.path.join(f_path, 'ROUGH.OUT'))
out_path = os.path.join(f_path, 'Model Review Shapefiles')

def CreateShapefile(grid_list, new_shp, dictionary, grid, out_path, field_name):
    grid_string = ",".join("%s" % grid for grid in grid_list)
    arcpy.SelectLayerByAttribute_management(grid, "NEW_SELECTION", '"{}" IN ({})'.format(grid_id, grid_string))
    shp = os.path.join(out_path, new_shp)
    arcpy.CopyFeatures_management(grid, shp)

    # Add fields
    arcpy.AddField_management(shp, field_name, 'FLOAT', 12, 3)
    arcpy.AddField_management(shp, 'Notes', 'TEXT', 200)

    with arcpy.da.UpdateCursor(shp, [grid_id, field_name]) as cursor:
        for row in cursor:
            grid = int(row[0])
            item = dictionary['{}'.format(grid)]
            row[1] = float(item)
            cursor.updateRow(row)

d = {}
switch = 0
for line in f:
    splt = line.split()
    if switch == 1:
        n = round(float(splt[2]), 3)
        d[splt[1]] = n
    if len(splt) > 0 and splt[0] == 'NODE':
        switch = 1

grid_list = [int(k) for k in d.keys()]
print(len(grid_list))
if len(grid_list) > 0:
    field_name = 'n_adjust'
    new_shp = 'Rough.shp'
    CreateShapefile(grid_list, new_shp, d, grid, out_path, field_name)
    
