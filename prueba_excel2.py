import xlsxwriter

libro = xlsxwriter.Workbook("prueba_con_lista.xlsx")
hoja1 = libro.add_worksheet("prueba")

lista_datos = [
    ["valor 1", "valor 2", "valor 3", 500],
    [1,7,3,50],
    ["tercer fila", 8.3, "cincuenta 50", 80]
]

fila = -1
columna = 0
#primer for
for lista in lista_datos:
    #lista = ["valor 1", "valor 2", "valor 3"]
    fila += 1
    columna = 0
    for valor in lista:
        # valor = "valor 1"
        hoja1.write(fila, columna, valor)
        columna += 1

formula = "=sum(D1:D" + str((fila + 1)) + ")"
hoja1.write(fila +1, columna - 1, formula) # D4, "=sum(D1:D3)"

#hoja1.write ("A1", "EJEMPLO")

libro.close()


# Iterables
# () Tuplas
# [] Listas
# {} Diccionarios