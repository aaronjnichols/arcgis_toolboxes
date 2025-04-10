import arcpy
from _ExtractRasterValuesToField import ExtractRasterValuesToField
def main():
    grid = arcpy.GetParameterAsText(0)
    rain_raster = arcpy.GetParameterAsText(1)
    id_field = arcpy.GetParameterAsText(2)
    outpath = arcpy.GetParameterAsText(3)

    depth_field = 'rain_depth'
    arf_field = 'arf_field'
    rain_table = outpath + r'/rain_table'

    ExtractRasterValuesToField(grid, rain_raster, id_field, depth_field, rain_table)
    arcpy.AddField_management(rain_table, arf_field, 'FLOAT', '4', '3')
    
    with arcpy.da.SearchCursor(rain_table, depth_field) as cursor:
        depths = []
        for row in cursor:
            depths.append(float(row[0]))

    max_depth = max(depths)
    arcpy.AddMessage("\nCalculating rainfall depths and rainfall ARF's.")
    expression = '!{}!/{}'.format(depth_field, max_depth)
    arcpy.CalculateField_management(rain_table, arf_field, expression, 'PYTHON_9.3')

if __name__ == '__main__':
    main()
    
