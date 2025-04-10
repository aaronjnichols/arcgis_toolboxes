import arcpy

#get parameters from user
f_path = arcpy.GetParameterAsText(0) # path to folder where HEC-RAS model is
hecras_version = arcpy.GetParameterAsText(1) #version of HEC-RAS you are using
f_new_name = arcpy.GetParameterAsText(2) #what would you like the new unsteady flow file to be called
flow_title = arcpy.GetParameterAsText(3) #what would you like the flow title to be for the new unsteady flow file
rain_pnts = arcpy.GetParameterAsText(4) #point shapefile or feature class with the rainfall data in attribute table
name_field = arcpy.GetParameterAsText(5) #each point needs unqiue name. what is the name of the field with the names
x_field = arcpy.GetParameterAsText(6) #field with x coordinates of points
y_field = arcpy.GetParameterAsText(7) #field with y coordinates of points
long_field = arcpy.GetParameterAsText(8)#field with longitude of points
lat_field = arcpy.GetParameterAsText(9) #field with latitude of points
gageheight_field = arcpy.GetParameterAsText(10) #field with gage heights of points
depth_field = arcpy.GetParameterAsText(11) #field with rainfall depths of points
distribution_path = arcpy.GetParameterAsText(12) #path to rainfall distribution text file
time_interval = arcpy.GetParameterAsText(13) #time interval in minutes
duration = arcpy.GetParameterAsText(14) #rainfall duration in hours
units = arcpy.GetParameterAsText(15) #units for rainfall depths (in, mm)
data_type = arcpy.GetParameterAsText(16) #PER-CUM, INST-VAL, PER-AVER

#open files
f = open(r'{}\{}.u99'.format(f_path, f_new_name), 'w')
distribution = open(distribution_path)

# use rainfall point data to write gage location data to unsteady flow file (.u99)
f.write(
    '''Flow Title={}
Program Version={}
Use Restart= 0\n'''.format(flow_title, hecras_version)
)
rain_dict = {} #initialize empty dictionary to collect data from rain_pnts attribute table
with arcpy.da.SearchCursor(rain_pnts, [name_field, gageheight_field, long_field, lat_field, x_field, y_field, depth_field]) as cur:
    for row in cur:
        f.write('''Met Station Name={}
Met Station Gauge Height={}
Met Station LL={},{}
Met Station XY={},{}\n'''.format(row[0], row[1], row[2], row[3], row[4], row[5]))
        rain_dict[int(row[0])] = round(float(row[6]), 3)
   
f.write(
    '''Met Point Raster Parameters=,,,,
Precipitation Mode=Enable
Wind Mode=No Wind Forces
Air Density Mode=Specified
Met BC=Precipitation|Mode=Point
Met BC=Precipitation|Expanded View=-1'''
    )

#write rainfall distributions for each gage location to unsteady flow file
n=0
max_rain = max(rain_dict.values())
table_rows = float(duration)*60/float(time_interval) + 1
for r in rain_dict:
    depth_ratio = rain_dict[r]/max_rain
    if n==0:
        f.write('''\nMet BC=Precipitation|Constant Units=mm/hr
Met BC=Precipitation|Point Interpolation=Thiessen Polygon
Met BC=Precipitation|TS Name={}
Met BC=Precipitation|TS Used=-1
Met BC=Precipitation|TS Source=Table
Met BC=Precipitation|TS Table Mode=0
Met BC=Precipitation|TS Table Use Fixed Start=0
Met BC=Precipitation|TS Table StartDateTime=30Dec1899 00:00:00
Met BC=Precipitation|TS Table Interval={} Minute
Met BC=Precipitation|TS Table Data Units={}
Met BC=Precipitation|TS Table Data Type={}
Met BC=Precipitation|TS Table Data={}\n'''.format(r, time_interval, units, data_type, table_rows))
        n=1
    else:
        f.write('''\nMet BC=Precipitation|TS Constant Units=mm/hr
Met BC=Precipitation|TS Name={}
Met BC=Precipitation|TS Used=-1
Met BC=Precipitation|TS Source=Table
Met BC=Precipitation|TS Table Mode=0
Met BC=Precipitation|TS Table Use Fixed Start=0
Met BC=Precipitation|TS Table Interval={} Minute
Met BC=Precipitation|TS Table Data Units={}
Met BC=Precipitation|TS Table Data Type={}
Met BC=Precipitation|TS Table Data={}\n'''.format(r, time_interval, units, data_type, table_rows))
    i=0
    for line in distribution:
        splt = line.split()
        if i < 2:
            f.write('{:>16}{:>16}'.format(0, round(float(splt[0]) * depth_ratio, 6)))
            i+=1
        else:
            f.write('\n{:>16}{:>16}'.format(0, round(float(splt[0]) * depth_ratio, 6)))
            i=1

    distribution.seek(0)

#write text at the end of the unsteady flow file
end_text = '''Met BC=Precipitation|TS Constant Units=mm/hr
Met BC=Precipitation|Gridded Source=DSS
Met BC=Evapotranspiration|Mode=None
Met BC=Evapotranspiration|Expanded View=0
Met BC=Evapotranspiration|Constant Units=mm/hr
Met BC=Evapotranspiration|Point Interpolation=Nearest
Met BC=Evapotranspiration|Gridded Source=DSS
Met BC=Wind Speed|Expanded View=0
Met BC=Wind Speed|Point Interpolation=Nearest
Met BC=Wind Speed|Gridded Source=DSS
Met BC=Wind Direction|Expanded View=0
Met BC=Wind Direction|Point Interpolation=Nearest
Met BC=Wind Direction|Gridded Source=DSS
Met BC=Wind Velocity X|Expanded View=0
Met BC=Wind Velocity X|Point Interpolation=Nearest
Met BC=Wind Velocity X|Gridded Source=DSS
Met BC=Wind Velocity Y|Expanded View=0
Met BC=Wind Velocity Y|Point Interpolation=Nearest
Met BC=Wind Velocity Y|Gridded Source=DSS
Met BC=Air Density|Mode=Constant
Met BC=Air Density|Expanded View=0
Met BC=Air Density|Constant Value=1.225
Met BC=Air Density|Constant Units=kg/m3
Met BC=Air Density|Point Interpolation=Nearest
Met BC=Air Density|Gridded Source=DSS
Met BC=Air Temperature|Expanded View=0
Met BC=Air Temperature|Point Interpolation=Nearest
Met BC=Air Temperature|Gridded Source=DSS
Met BC=Humidity|Expanded View=0
Met BC=Humidity|Point Interpolation=Nearest
Met BC=Humidity|Gridded Source=DSS
Met BC=Air Pressure|Expanded View=0
Met BC=Air Pressure|Point Interpolation=Nearest
Met BC=Air Pressure|Gridded Source=DSS
Non-Newtonian Method= 0 , 
Non-Newtonian Constant Vol Conc=0
Non-Newtonian Yield Method= 0 , 
Non-Newtonian Yield Coef=0, 0
User Yeild=   0
Non-Newtonian Sed Visc= 0 , 
Non-Newtonian Obrian B=0
User Viscosity=0
User Viscosity Ratio=0
Herschel-Bulkley Coef=0, 0
Clastic Method= 0 , 
Coulomb Phi=0
Voellmy X=0
Non-Newtonian Hindered FV= 0 
Non-Newtonian FV K=0
Non-Newtonian ds=0
Non-Newtonian Max Cv=0
Non-Newtonian Bulking Method= 0 , 
Non-Newtonian High C Transport= 0 , 
Lava Activation= 0 
Temperature=1300,15,,15,14,980
Heat Ballance=1,1200,0.5,1,70,0.95
Viscosity=1000,,,
Yield Strength=,,,
Consistency Factor=,,,
Profile Coefficient=4,1.3,
Lava Param=,2500,\n'''

f.write(end_text)
f.close()
distribution.close()
