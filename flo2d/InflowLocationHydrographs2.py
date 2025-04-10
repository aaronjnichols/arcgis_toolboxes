import arcpy
import os
import xlsxwriter as xl
from xlsxwriter.utility import xl_rowcol_to_cell
from xlsxwriter.utility import xl_col_to_name

# Inputs
outflow_lines = arcpy.GetParameterAsText(0)
field = arcpy.GetParameterAsText(1)
GRID = arcpy.GetParameterAsText(2)
outflow = arcpy.GetParameterAsText(3)
outPath = arcpy.GetParameterAsText(4)

# Create excel spreadsheet and styles
wb = xl.Workbook(outPath+r'\Location Hydrographs.xlsx')
style1 = wb.add_format({'bold': True, 'bg_color': 'black', 'font_color': 'white', 'align': 'center', 'border': 1})
style2 = wb.add_format({'bold': True, 'font_color': 'black', 'align': 'center', 'border': 1})
style3 = wb.add_format({'bold': True, 'align': 'center', 'border': 1})
style4 = wb.add_format({'align': 'center', 'border': 1})

# Add sheet to Excel workbook
def AddWorksheet(ws_name, ws2_name, chartsheet_name):
    ws = wb.add_worksheet(ws_name)
    ws2 = wb.add_worksheet(ws2_name)
    chartsheet = wb.add_chartsheet(chartsheet_name)

# Function to create chart
def createChart(name, categories, values, location, workbook, worksheet, chartsheet):
    chart1 = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'smooth'})

    # Configure  series.
    chart1.add_series({
        'name':       name,
        'categories': categories,
        'values':     values,
        'line': {'color': '#4682B4'}
    })

    # Add a chart title and some axis labels.
    chart1.set_title ({'name': name,
                       'name_font': {'bold': True, 'font_name': 'Century Gothic'}})
    chart1.set_x_axis({'name': 'Time (hrs)'})
    chart1.set_y_axis({'name': 'Q (cfs)'})

    # Set an Excel chart style.
    chart1.set_style(1)
    chart1.set_x_axis({
        'min': 0,
        'name': 'Time (hrs)'
        })
    chart1.set_y_axis({
        'min': 0,
        'name': 'Q (cfs)'
        })
    # Insert the chart into the worksheet (with an offset).
    chartsheet.set_chart(chart1)

# Count number of location lines    
result = arcpy.GetCount_management(outflow_lines)
num_locations = int(result[0])

# Open INFLOW.DAT and create dictionary of grids and hydrographs
f = open(outflow, 'r')
grid_dict = {}

t_switch = 0
t = []
for line in f:
    splitter = line.split()
    if len(splitter) == 3 and t_switch == 0:
        t.append(round(float(splitter[1]), 2))
	t_switch = 1
    elif len(splitter) == 2:
	t.append(round(float(splitter[0]),2))
    elif len(splitter) == 3 and t_switch == 1:
	break
f.seek(1)
   
for line in f:
    splitter = line.split()
    if len(splitter) == 3 and splitter[0] == 'F':
        grid = str(splitter[2])
        grid_dict[grid] = []
    elif len(splitter) == 3 and splitter[0] == 'H':
        grid_dict[grid].append(round(float(splitter[2]),2))

f.close()

# Select grid cells with location lines and add grid id's to list
for loc in range(num_locations):
    arcpy.SelectLayerByAttribute_management(outflow_lines, "NEW_SELECTION", '"{}" = {}'.format(field, loc+1))
    arcpy.SelectLayerByLocation_management(GRID, 'INTERSECT', outflow_lines)
    grid_list = []
    with arcpy.da.SearchCursor(GRID, 'FLO2D_ID') as cursor:
        for row in cursor:
            grid_list.append(str(int(row[0])))
            
# Select location specific grids and hydrographs from overall dictionary        
    loc_dict = {}
    for grid in grid_list:
        if grid in grid_dict.keys():
            loc_dict[grid] = grid_dict[grid]
            
# Write hydrographs to excel
    t_col = 2
    ws = wb.add_worksheet('Location {}'.format(loc+1))
    ws.write(0, t_col, 'Time (hrs)', style3)
    ws.write_column(1, t_col, t, style4)
    lst_keys = [k for k in loc_dict.keys()]

    col = 5
    for k in lst_keys:
        ws.write(0, col, k, style3)
        ws.write_column(1, col, loc_dict[k], style4)
        col += 1
    Qtot_col = 3
    
    for row in range(10000):
        start_formula = xl_rowcol_to_cell(row, 5)
        end_formula = xl_rowcol_to_cell(row, col)
        ws.write_formula(row, Qtot_col, '=SUM('+start_formula+':'+end_formula+')', style4)
        ws.write(0, Qtot_col, 'Q Total (cfs)', style3)
    
    ws.write_formula(0, 1, '{=MAX(D2:D10000)}', style2)
    ws.write(0,0,'Qmax (cfs)', style1)
    ws.write_formula(1, 1, '{=INDEX(C2:C10000,MATCH(B1,D2:D1000,0))}', style2)
    ws.write(1,0,'Time (hrs)', style1)
                     
 # Create plots for each location   
    row = 1
    col = 2
    name = 'Location-' + str(loc+1)
    categories = ['Location '+str(loc+1), row, col, 10000, col]
    values = ['Location '+str(loc+1), row, Qtot_col, 10000, Qtot_col]
    location = 'C2'
    chartsheet = wb.add_chartsheet('Location {} Hydrograph'.format(loc+1))
    createChart(name, categories, values, location, wb, ws, chartsheet)

    col += 3
    
wb.close()
    
    

           
    

        
    
