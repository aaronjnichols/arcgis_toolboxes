import arcpy

# Get grid points and output folder path from GIS
grid = arcpy.GetParameterAsText(0)
id_field = arcpy.GetParameterAsText(1)
n_field = arcpy.GetParameterAsText(2)
outpath = arcpy.GetParameterAsText(3)

# Create blank .dat files to write GIS data to.
MANNINGS_N = open(outpath+r'\MANNINGS_N.DAT', 'w')

# Loop through Grid Centroids shapefile and write data to .dat files 
with arcpy.da.SearchCursor(grid, [id_field, n_field]) as cursor:
    for row in cursor:
        grid_id = row[0]
        n = str(round(float(row[1]), 3))
        MANNINGS_N.write('%-12s %s\n' % (grid_id, n))

arcpy.AddMessage('DONE!')
                           

        
        
        
