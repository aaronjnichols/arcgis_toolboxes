import arcpy
import time

def AddElevation(grid, id_field, elev_raster, outpath):

    # Use Add Surface Information to determine elevations at grid cells
    arcpy.AddMessage('\nComputing interpolated elevations per grid cell.')
    if '.gdb' in outpath:
        out_table = outpath+r'/elevation_table'
    else:
        out_table = outpath+r'/elevation_table.dbf'

    # sample elevation raster with grid    
    arcpy.sa.ZonalStatisticsAsTable(grid, id_field, elev_raster, out_table, "DATA", "MEAN")

            
    arcpy.AddMessage('DONE!')
                           
# Run the script       
if __name__ == '__main__':
    # Get parameters
    grid = arcpy.GetParameterAsText(0)
    id_field = arcpy.GetParameterAsText(1)
    elev_field = arcpy.GetParameterAsText(2)
    elev_raster = arcpy.GetParameterAsText(3)
    outpath = arcpy.GetParameterAsText(4)

    # Run the main script
    AddElevation(grid, id_field, elev_raster, outpath)


  
        
