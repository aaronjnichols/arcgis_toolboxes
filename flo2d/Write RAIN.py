import arcpy
import time

# Get input parameters
RAIN_PNTS = arcpy.GetParameterAsText(0)
idField = arcpy.GetParameterAsText(1)             
Rain_Depth_Field = arcpy.GetParameterAsText(2)	    
RAIN_ARF_Field = arcpy.GetParameterAsText(3)        
Rain_File = arcpy.GetParameterAsText(4)             
Rainfall_Distribution = arcpy.GetParameterAsText(5)         
RAINABS = arcpy.GetParameterAsText(6)               
IRAINARF = arcpy.GetParameterAsText(7)                     
RAINSPEED = arcpy.GetParameterAsText(8)             
IRAINDIR = arcpy.GetParameterAsText(9)
IRAINREAL = arcpy.GetParameterAsText(10)             
IRAINBUILDING = arcpy.GetParameterAsText(11)
MOVINGSTORM = arcpy.GetParameterAsText(12)               
DAT_path = arcpy.GetParameterAsText(13)             

def IsTrue(booleanValue):
	if booleanValue.lower() == 'true':
		return 1
	else:
		return 0
IRAINREAL = IsTrue(IRAINREAL)
IRAINBUILDING = IsTrue(IRAINBUILDING)
MOVINGSTORM = IsTrue(MOVINGSTORM)

if Rainfall_Distribution == '24-Hour':
	distributionType = 1
else:
	distributionType = int(Rainfall_Distribution[12])	

depths = []
with arcpy.da.SearchCursor(RAIN_PNTS, Rain_Depth_Field) as cursor:
    for row in cursor:
        depths.append(float(row[0]))

RTT = round(max(depths),3)

# Create a timer function
def TellTime(t0, tf):
    if tf - t0 < 60:
        arcpy.AddMessage('Run Time = {} seconds.'.format(round(tf-t0,3)))
    else:
        arcpy.AddMessage('Run Time = {} minutes.'.format(round((tf-t0)/60,3)))

# Write RAIN.DAT
t0 = time.time()
arcpy.AddMessage('\nWriting RAIN.DAT file.')
RAIN_DAT = open(DAT_path+r'/RAIN.DAT', 'w')
f = open(Rain_File, 'r')
RAIN_DAT.write('%-5s %-5s\n' % (IRAINREAL, IRAINBUILDING))
RAIN_DAT.write('%-9s %-9s %-9s %-5s\n' % (RTT, RAINABS, IRAINARF, MOVINGSTORM))

# Loop through rainfall distribution txt file and write distribution
for line in f:
    splitter = line.split()
    t = splitter[0]
    P = splitter[distributionType]
    RAIN_DAT.write('%-5s %-9s %-9s\n' % ('R', t, P))

if RAINSPEED == '0' and IRAINDIR == '0':
	pass
else:
	RAIN_DAT.write('%-9s %-5s\n' % (RAINSPEED, IRAINDIR))

with arcpy.da.SearchCursor(RAIN_PNTS, [idField, RAIN_ARF_Field]) as cursor:
    for row in cursor:
        RAIN_DAT.write('%-13s %-9s\n' % (int(row[0]), round(float(row[1]),3)))

f.close()
RAIN_DAT.close()




