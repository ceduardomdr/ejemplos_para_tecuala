import xlsxwriter

libro = xlsxwriter.Workbook("prueba.xlsx")
hoja = libro.add_worksheet()

hoja.write("A1", "Bienvenidos a Python")

libro.close()

print("Generamos el archivo excel")