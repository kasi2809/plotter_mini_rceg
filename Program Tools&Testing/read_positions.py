import xlrd
# import os
# my_file = 'test_board.csv'
# base = os.path.splitext(my_file)[0]
# os.rename(my_file, base + '.xls')
coordinates = []

wb = xlrd.open_workbook("test_board.xls")
sheet = wb.sheet_by_index(0)

pts = {}

for i in range(len(sheet.col_values(2))):
    coordinates = []
    if sheet.cell_value(i,2) == 1:
        rad = sheet.cell_value(i,7)
        co_ord = sheet.cell_value(i,10)
        co_ord=(co_ord[1:len(co_ord)-1]).split(')(')
        for co_str in co_ord:
            co_str=co_str.replace(' ',',')
            coordinates.append(co_str)
        pts[rad]=coordinates

print(pts)