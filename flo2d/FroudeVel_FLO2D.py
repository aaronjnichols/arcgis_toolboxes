import csv
import pandas as pd
import array
import numpy as np

Space = r"B:\WP FLO-2D\195022_Metro\1A\2020-08-19_SHALLOWN=0.1\CSVFILES"

Output = open('{}\Output_Data.csv'.format(Space),'rb')
Super = open('{}\Super.csv'.format(Space),'w')
Velocity = open('{}\VelocityTimeFP.csv'.format(Space),'w')

Super.close()
Velocity.close


my_csv = pd.read_csv(Output)
column_Vel = my_csv['MaxVel']
column_Fro = my_csv['QPFroude']
column_X = my_csv['X']
column_Y = my_csv['Y']
Ran = max(my_csv['GRIDCODE'])
print(Ran)
i = 0

print(column_Vel[1])

while i < (Ran-1):
    i = i+1
    if column_Vel[i] > 15:
        print(column_Vel[i])
        V = (i,column_X[i],column_Y[i],column_Vel[i])
        with open('{}\VelocityTimeFP.csv'.format(Space),'a') as VelocityA:
            writer = csv.writer(VelocityA)
            writer.writerow(V)
    else:
        pass
    if column_Fro[i] > 2:
        print(column_Fro[i])
        S = (i,column_X[i],column_Y[i],column_Fro[i])
        with open('{}\Super.csv'.format(Space),'a') as SuperA:
            writerS = csv.writer(SuperA)
            writerS.writerow(S)
    else:
        pass

print(i)
Output.close()
SuperA.close()
VelocityA.close()


Froude_Data = pd.read_csv(Space + "\Super.csv")
import arcpy
from arcpy import env
arcpy.env.workspace = Space
arcpy.MakeXYEventLayer_management("Super.csv","Field2" , "Field3", "Froude_Warning","P:\GIS Users\Coordinate Systems\NAD 1983 HARN StatePlane Arizona Central FIPS 0202 (Intl Feet).prj")
arcpy.MakeXYEventLayer_management("VelocityTimeFP.csv","Field2" , "Field3", "Velocity_Warning","P:\GIS Users\Coordinate Systems\NAD 1983 HARN StatePlane Arizona Central FIPS 0202 (Intl Feet).prj")
arcpy.FeatureClassToShapefile_conversion(["Velocity_Warning","Froude_Warning"],Space)
