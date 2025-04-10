import xlwt
import arcpy

# define function to write entire column of data from list
def WriteColumn(worksheet, strt_row, col, list_to_write, style):
    for row, item in enumerate(list_to_write, strt_row):
        worksheet.write(row, col, item, style)
        
# define function to write entire row of data from list
def WriteRow(worksheet, row, strt_col, list_to_write, style):
    for col, item in enumerate(list_to_write, strt_col):
        worksheet.write(row, col, item, style)
                
# extract outflow hydrographs from OUTNQ.DAT to a dictionary
def GetHydrographsOUTNQ(f):
    d = {}
    switch = 0
    for line in f:
        splitter = line.split()
        if len(splitter) > 0 and splitter[0] == "ELEMENT":
            switch = 1
        if switch == 1 and len(splitter) > 0 and splitter[0] != "ELEMENT":
            grid = str(splitter[0])
            d[grid] = [splitter[2]]
            switch = 2
        elif switch == 2 and len(splitter) > 0:
            d[grid].append(splitter[1])

    return(d)

# extract specified grids hydrographs from hydrograph dicitionary
def GetGridHydrographs(grid_list, d):
    d_new = {}
    for k in d.keys():
        if k in grid_list:
            d_new[k] = d[k]

    return(d_new)

def main():
    # get parameters
    grid = arcpy.GetParameterAsText(0)
    id_field = arcpy.GetParameterAsText(1)
    mdl_path =  arcpy.GetParameterAsText(2)

    # populate list with grid id's
    grid_list = []
    with arcpy.da.SearchCursor(grid, id_field) as cur:
        for row in cur:
            grid_list.append(str(row[0]))

    arcpy.AddMessage(grid_list[0])
    # open OUTNQ.OUT file 
    f = open(mdl_path + r'\OUTNQ.OUT', 'r')
    
    # create excel workbook
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Outflow Hydrographs', True)

    # define excel spreadsheet styles
    xlwt.add_palette_colour('light gray', 0X21)
    wb.set_colour_RGB(0x21, 236, 236, 236)
    style_headings = xlwt.easyxf('font: name Calibri, color white, bold on; align: wrap on, horiz center; pattern: pattern solid, fore_color black; borders: top_color gray40, bottom_color gray40, right_color gray40, left_color gray40, left thin, right thin, top thin, bottom thin; protection: cell_locked false')
    style = xlwt.easyxf('font: name Calibri; align: wrap off, horiz center; pattern: pattern solid, fore_color light gray; borders: top_color gray40, bottom_color gray40, right_color gray40, left_color gray40, left thin, right thin, top thin, bottom thin; protection: cell_locked false')

    # get hydrograph dictionary for all outflow nodes
    all_hydrographs_dict = GetHydrographsOUTNQ(f)
    arcpy.AddMessage(all_hydrographs_dict.keys()[0])
    # filtered hydrograph dictionary for selected outflow cells
    grid_hydrographs_dict = GetGridHydrographs(grid_list, all_hydrographs_dict)
    arcpy.AddMessage(grid_hydrographs_dict.keys()[0])
    # write data to excel
    WriteRow(ws, 0, 0, grid_hydrographs_dict.keys(), style_headings)
    for col, k in enumerate(grid_hydrographs_dict.keys()):
        lst = grid_hydrographs_dict[k]
        WriteColumn(ws, 1, col, lst, style)

    wb.save(mdl_path + r'/Outflow_Hydrographs.xls')
          
if __name__ == '__main__':
    main()
    
