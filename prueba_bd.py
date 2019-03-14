import psycopg2
import psycopg2.extras
import xlsxwriter

def conexion():
    con = psycopg2.connect(host="localhost", database="o_tecuala", user="admon_tecuala", password="ctteic")
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
select 
	ht.clave_suc
	, ht.caja_opca 
	, ht.fecha_trca
	, ht.folio_opca
	, ht.folio_trca
	, ht.clave_tins -- CLAVE TIPO DE INSTRUMENTO (1:Parte Social, 3:Depósito a la Vista, 4:Inversiones, 6:Aportaciones)
	, ht.clave_inst -- CLAVE (DEPOSITO A LA VISTA (1:DepositoALaVista, 2:AhorroJuvenil, 3:GarantíaLíquida)(INVERSIONES(2:30DIAS,3:60DIAS,4:90DIAS)
	, ht.importe_tcaj
	, ht.clave_ocap
	, hf.tipo_mov_fpca -- MOVIMIENTO (I:Ingreso, E:Egreso, C:Cambio)
	, hf.tipo_pago_fpca -- FORMA PAGO (E:Efectivo, C:Cheque, A:Abono a Cuenta de Cheque, P: Depósito en efectivo a Cuenta de Cheque)
	, so.clave_tper -- TIPO DE PERSONA (2:PersonaFísica, 4:PersonaFísicaExentaIVA, 6:PersonaMoralExentaIDE, 7:PersonaMoral)
	, est.nombre -- Nombre del Estado
	, hf.proceden_fpca -- Número de Referencia
	, hf.num_cheque_fpca -- Número de Cheque
	, ht.usuario -- Usuario que Realiza la Operación
	, ht.clave_soc
	, case when so.califica_pld = 'A' then 'ALTO RIESGO' when so.califica_pld ='M' then 'RIESGO MEDIO' else 'BAJO RIESGO' end as nivel_riesgo
	, so.funcionario_pub
--	, tipo_oper_trca -- MODULO (1:Captacón, 2:Crédito, 3:Caja, 4:Servicios)
from 
	htranca ht
	inner join hfpagca hf on hf.clave_suc = ht.clave_suc and hf.caja_opca = ht.caja_opca and hf.fecha_opca = ht.fecha_trca and hf.folio_opca = ht.folio_opca and hf.tipo_mov_fpca in ('I')
	inner join socio so on so.clave_suc = ht.clave_suc_soc and so.clave_soc = ht.clave_soc
	inner join domicil dom on dom.clave_suc = ht.clave_suc_soc and dom.clave_soc = ht.clave_soc and dom.tipo_dom = '1'
	inner join estados est on est.clave_edo = dom.clave_edo
where 
	extract('year' from ht.fecha_trca) = 2017  -- solo del año 2017
	and tipo_oper_trca = 1 -- solo movimientos captacion
	and clave_tins in (3,4) -- Solamente cuentas de ahorro e inversiones
order by
	fecha_trca
	, clave_suc
	, caja_opca
	, folio_opca
	, folio_trca
    """)  # triples comillas dobles para adherir una consulta multilinea 
    data = cur.fetchall()
    columnas = [ desc[0] for desc in cur.description ]
    #print(columnas)
    return (data, columnas)
    # info = data [1]
    # dato = info["clave_soc"]
    # print (data[0]["clave_soc"]) 

def crear_excel(datos, columnas):
    libro = xlsxwriter.Workbook("listado_socios.xlsx")
    hoja = libro.add_worksheet("socios")

    fila = 1
    col = 0
    for nomcol in columnas:
        hoja.write(0, col, nomcol )
        col +=1

    for dato in datos:
            col = 0
            for nombre_campo in columnas:
                hoja.write( fila, col, dato [nombre_campo])
                col +=1
            fila +=1


        #hoja.write(fila, 0,  dato ["clave_suc"])
        #hoja.write(fila, 1,  dato ["clave_soc"])
        #hoja.write(fila, 2,  dato ["nombre_socio"])
        #fila +=1
        #print(dato["clave_soc"], "-", dato["nombre_soc"])
    libro.close()
    print("Hemos generado exitosamente el listado de socios")



if __name__=="__main__":
    datos_socios, columnas = conexion()
    crear_excel(datos_socios, columnas)