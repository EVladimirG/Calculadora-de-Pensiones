# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import calendar
import os

#---------------------------------------------------------------------------DB.py

SM = {
    2000: {
        "diario": 37.9,
        "mensual": 1137,
        "anual": 13644
    },
    2001: {
        "diario": 40.35,
        "mensual": 1210.5,
        "anual": 14526
    },
    2002: {
        "diario": 42.15,
        "mensual": 1264.5,
        "anual": 15174
    },
    2003: {
        "diario": 43.65,
        "mensual": 1309.5,
        "anual": 15714
    },
    2004: {
        "diario": 45.24,
        "mensual": 1357.2,
        "anual": 16286.4
    },
    2005: {
        "diario": 46.8,
        "mensual": 1404,
        "anual": 16848
    },
    2006: {
        "diario": 47.16,
        "mensual": 1460.1,
        "anual": 17521.2
    },
    2007: {
        "diario": 50.57,
        "mensual": 1517.1,
        "anual": 18205.2
    },
    2008: {
        "diario": 52.59,
        "mensual": 1577.7,
        "anual": 18932.4
    },
    2009: {
        "diario": 54.8,
        "mensual": 1644,
        "anual": 19728
    },
    2010: {
        "diario": 57.46,
        "mensual": 1723.8,
        "anual": 20685.6
    },
    2011: {
        "diario": 59.82,
        "mensual": 1794.6,
        "anual": 21535.2
    },
    2012: {
        "diario": 62.33,
        "mensual": 1869.9,
        "anual": 22439.2
    },
    2013: {
        "diario": 64.76,
        "mensual": 1942.8,
        "anual": 23313.6
    },
    2014: {
        "diario": 67.29,
        "mensual": 2018.7,
        "anual": 24224.4
    },
    2015: {
        "diario": 70.1,
        "mensual": 2103,
        "anual": 25236
    },
    2016: {
        "diario": 73.04,
        "mensual": 2191.2,
        "anual": 26294.4,
        "UMAS": 73.04
    },
    2017: {
        "diario": 80.04,
        "mensual": 2401.2,
        "anual": 28814.4,
        "UMAS": 75.49
    },
    2018: {
        "diario": 88.36,
        "mensual": 2650.8,
        "anual": 31809.6,
        "UMAS": 80.60
    },
    2019: {
        "diario": 102.68,
        "mensual": 3080.4,
        "anual": 36964.8,
        "UMAS": 86.49
    },
    2020: {
        "diario": 123.22,
        "mensual": 3696.6,
        "anual": 44359.2,
        "UMAS": 86.88
    },
    2021: {
        "diario": 141.7,
        "mensual": 4251,
        "anual": 51012,
        "UMAS": 89.62
    },
    2022: {
        "diario": 172.87,
        "mensual": 5186.1,
        "anual": 62233.2,
        "UMAS": 96.22
    },
    2023: {
        "diario": 207.44,
        "mensual": 6223.2,
        "anual": 74678.4,
        "UMAS": 103.74
    },
    2024: {
        "diario": 248.93,
        "mensual": 7467.9,
        "anual": 89614.8,
        "UMAS": 108.57
    }
}

#---------------------------------------------------------------------------Util.py

MONEDA_SINGULAR = 'peso'
MONEDA_PLURAL = 'pesos'

CENTIMOS_SINGULAR = 'centavo'
CENTIMOS_PLURAL = 'centavos'

MAX_NUMERO = 999999999999

UNIDADES = (
    'cero',
    'uno',
    'dos',
    'tres',
    'cuatro',
    'cinco',
    'seis',
    'siete',
    'ocho',
    'nueve'
)

DECENAS = (
    'diez',
    'once',
    'doce',
    'trece',
    'catorce',
    'quince',
    'dieciseis',
    'diecisiete',
    'dieciocho',
    'diecinueve'
)

DIEZ_DIEZ = (
    'cero',
    'diez',
    'veinte',
    'treinta',
    'cuarenta',
    'cincuenta',
    'sesenta',
    'setenta',
    'ochenta',
    'noventa'
)

CIENTOS = (
    '_',
    'ciento',
    'doscientos',
    'trescientos',
    'cuatroscientos',
    'quinientos',
    'seiscientos',
    'setecientos',
    'ochocientos',
    'novecientos'
)

def numero_a_letras(numero):
    numero_entero = int(numero)
    if numero_entero > MAX_NUMERO:
        raise OverflowError('Número demasiado alto')
    if numero_entero < 0:
        return 'menos %s' % numero_a_letras(abs(numero))
    letras_decimal = ''
    parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
    if parte_decimal > 9:
        letras_decimal = f'punto {numero_a_letras(parte_decimal)} centavos'
    elif parte_decimal > 0:
        letras_decimal = f'punto cero {numero_a_letras(parte_decimal)} centavos'
    if (numero_entero <= 99):
        resultado = leer_decenas(numero_entero)
    elif (numero_entero <= 999):
        resultado = leer_centenas(numero_entero)
    elif (numero_entero <= 999999):
        resultado = leer_miles(numero_entero)
    elif (numero_entero <= 999999999):
        resultado = leer_millones(numero_entero)
    else:
        resultado = leer_millardos(numero_entero)
    resultado = resultado.replace('uno mil', 'un mil')
    resultado = resultado.strip()
    resultado = resultado.replace(' _ ', ' ')
    resultado = resultado.replace('  ', ' ')
    if parte_decimal > 0:
        resultado = '%s %s' % (resultado, letras_decimal)
    return resultado

def numero_a_moneda(numero):
    numero_entero = int(numero)
    parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
    centimos = ''
    if parte_decimal == 1:
        centimos = CENTIMOS_SINGULAR
    else:
        centimos = CENTIMOS_PLURAL
    moneda = ''
    if numero_entero == 1:
        moneda = MONEDA_SINGULAR
    else:
        moneda = MONEDA_PLURAL
    letras = numero_a_letras(numero_entero)
    letras = letras.replace('uno', 'un')
    letras_decimal = 'con %s %s' % (numero_a_letras(parte_decimal).replace('uno', 'un'), centimos)
    letras = '%s %s %s' % (letras, moneda, letras_decimal)
    return letras

def leer_decenas(numero):
    if numero < 10:
        return UNIDADES[numero]
    decena, unidad = divmod(numero, 10)
    if numero <= 19:
        resultado = DECENAS[unidad]
    elif numero <= 29:
        resultado = 'veinti%s' % UNIDADES[unidad]
    else:
        resultado = DIEZ_DIEZ[decena]
        if unidad > 0:
            resultado = '%s y %s' % (resultado, UNIDADES[unidad])
    return resultado

def leer_centenas(numero):
    centena, decena = divmod(numero, 100)
    if numero == 0:
        resultado = 'cien'
    else:
        resultado = CIENTOS[centena]
        if decena > 0:
            resultado = '%s %s' % (resultado, leer_decenas(decena))
    return resultado

def leer_miles(numero):
    millar, centena = divmod(numero, 1000)
    resultado = ''
    if (millar == 1):
        resultado = ''
    if (millar >= 2) and (millar <= 9):
        resultado = UNIDADES[millar]
    elif (millar >= 10) and (millar <= 99):
        resultado = leer_decenas(millar)
    elif (millar >= 100) and (millar <= 999):
        resultado = leer_centenas(millar)
    resultado = '%s mil' % resultado
    if centena > 0:
        resultado = '%s %s' % (resultado, leer_centenas(centena))
    return resultado

def leer_millones(numero):
    millon, millar = divmod(numero, 1000000)
    resultado = ''
    if (millon == 1):
        resultado = ' un millon '
    if (millon >= 2) and (millon <= 9):
        resultado = UNIDADES[millon]
    elif (millon >= 10) and (millon <= 99):
        resultado = leer_decenas(millon)
    elif (millon >= 100) and (millon <= 999):
        resultado = leer_centenas(millon)
    if millon > 1:
        resultado = '%s millones' % resultado
    if (millar > 0) and (millar <= 999):
        resultado = '%s %s' % (resultado, leer_centenas(millar))
    elif (millar >= 1000) and (millar <= 999999):
        resultado = '%s %s' % (resultado, leer_miles(millar))
    return resultado

def leer_millardos(numero):
    millardo, millon = divmod(numero, 1000000)
    return '%s millones %s' % (leer_miles(millardo), leer_millones(millon))

def NombreMes(numero_mes):
    meses = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }
    return meses.get(numero_mes, "Mes inválido")

Meses = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

#---------------------------------------------------------------------------Pensiones.pyw

def cant_dias(year, month):                
    return calendar.monthrange(year, month)[1]

def string_to_float(string_value):
    try:
        float_value = float(string_value)
        return float_value
    except ValueError:
        print("Error: The string contains a non-numeric value.")
        return None

def validate_float(input_string, event):
    """Validate input as a floating-point number."""
    if input_string.isdigit() or input_string == "." or (input_string[0] == "." and len(input_string) == 1):
        try:
            float(input_string)
            return True
        except ValueError:
            return False
    else:
        return False

def smm(smda, year, month):
    return round((smda * cant_dias(year, month)), 3)

def cerrar_ventana():
    root.destroy()

def Recargar():
    global combo_tipo
    tipo = combo_tipo.get()
    label_tipo.destroy()
    combo_tipo.destroy()
    base()

def base():
    global entry_nombre_archivo, entry_yeari,combo_mes_inicio,entry_yearf,combo_mes_final,combo_tipo
    root.geometry("300x300")
    label_nombre_archivo = tk.Label(root, text="Nombre del archivo:",bg="#dedede")
    label_nombre_archivo.grid(row=0, column=0, padx=5, pady=5)
    entry_nombre_archivo = tk.Entry(root)
    entry_nombre_archivo.grid(row=0, column=1, padx=5, pady=5)

    label_yeari = tk.Label(root, text="Año de inicio:",bg="#dedede")
    label_yeari.grid(row=1, column=0, padx=5, pady=5)
    entry_yeari = tk.Entry(root,validate="key",validatecommand=(root.register(validate_float), "%P", "%S"))
    entry_yeari.grid(row=1, column=1, padx=5, pady=5)

    label_mes_inicio = tk.Label(root, text="Mes de inicio:",bg="#dedede")
    label_mes_inicio.grid(row=2, column=0, padx=5, pady=5)
    combo_mes_inicio = ttk.Combobox(root, values=list(range(1, 13)))
    combo_mes_inicio.grid(row=2, column=1, padx=5, pady=5)

    label_yearf = tk.Label(root, text="Año final:",bg="#dedede")
    label_yearf.grid(row=3, column=0, padx=5, pady=5)
    entry_yearf = tk.Entry(root,validate="key",validatecommand=(root.register(validate_float), "%P", "%S"))
    entry_yearf.grid(row=3, column=1, padx=5, pady=5)

    label_mes_final = tk.Label(root, text="Mes final:",bg="#dedede")
    label_mes_final.grid(row=4, column=0, padx=5, pady=5)
    combo_mes_final = ttk.Combobox(root, values=list(range(1, 13)))
    combo_mes_final.grid(row=4, column=1, padx=5, pady=5)

    boton_Recargar = tk.Button(root, text="Recargar", command=Recargar)
    boton_Recargar.grid(row=7, columnspan=1, padx=5, pady=5)

    boton_cerrar = tk.Button(root, text="Cerrar", command=cerrar_ventana)
    boton_cerrar.grid(row=7,column=1, columnspan=1, padx=5, pady=5)
    # Ejecutar la ventana


def generar_archivoSM(dec):
    global entry_nombre_archivo, entry_yeari,combo_mes_inicio,entry_yearf,combo_mes_final
    doc = entry_nombre_archivo.get()
    doc = f"{doc}.txt"
    yeari = int(entry_yeari.get())
    monthi = combo_mes_inicio.current()
    yearf = int(entry_yearf.get())
    monthf = combo_mes_final.current()

    with open(doc, "w") as archivo:
        SumTotal = 0
        for year in range(yeari, yearf+1):
            if year == yeari:
                MesI = monthi
            else:
                MesI = 1
            if year == yearf:
                MesF = monthf
            else:
                MesF = 12
            smda = SM[year]['diario']
            if dec == "Medio":
                smda /= 0.5
            elif dec == "Uno y medio":
                smda *= 1.5
            elif dec == "Doble":
                smda *= 2
            elif dec == "Completo":
                smda * 1
            archivo.write(f"\t\t--Año: {year} --\n")
            if dec == "Medio":
                archivo.write(f"\t\tSalario mínimo: {smda*2}\n\n")
            elif dec == "Uno y medio":
                archivo.write(f"\t\tSalario mínimo: {smda/1.5}\n\n")
            elif dec == "Doble":
                archivo.write(f"\t\tSalario mínimo: {smda/2}\n\n")
            else:
                archivo.write(f"\t\tSalario mínimo: {smda}\n\n")
            
            SumMensual = []
            for mes in range(MesI, MesF+1):
                salario_mes = smm(smda, year, mes)
                SumMensual.append(salario_mes)
                archivo.write(f"{NombreMes(mes)} - {year}\t: ${salario_mes} ({numero_a_moneda(salario_mes)} m.n)\n")

            SumAnual = sum(SumMensual)
            SumTotal += SumAnual
            archivo.write(f"\nSuma de los salarios mínimos mensuales en el año {year}: ${round(SumAnual,3)} ({numero_a_moneda(SumAnual)} m.n)\n")
            archivo.write(f"Suma total acumulada hasta el año {year}: ${round(SumTotal,3)} ({numero_a_moneda(SumTotal)} m.n)\n\n")
    
    messagebox.showinfo("Archivo Creado", "El archivo se generó exitosamente")

def generar_archivoUMAS(dec):
    pass

def generar_archivoCliqPorc(Cant):
    pass

def TipoDeuda(tipo):
    if tipo == "Salario Minimo":
        label_sm = tk.Label(root, text="Salario mínimo?",bg="#dedede")
        label_sm.grid(row=6, column=0, padx=5, pady=5)
        combo_sm = ttk.Combobox(root, values=["Completo", "Medio", "Uno y medio","Doble"])
        combo_sm.grid(row=6, column=1, padx=5, pady=5)
        dec = combo_sm.get()
        boton_SM = tk.Button(root, text="Generar Archivo", command=generar_archivoSM(dec))
        boton_SM.grid(row=8, columnspan=4, padx=5, pady=5)
    elif tipo == "UMAS":
        label_UMAS = tk.Label(root, text="Ingresa las UMAS",bg="#dedede")
        label_UMAS.grid(row=6, column=0, padx=5, pady=5)
        combo_UMAS = ttk.Combobox(root, values=["Completas", "Medias", "Una y media","Doble"])
        combo_UMAS.grid(row=6, column=1, padx=5, pady=5)
        dec = combo_UMAS.get()
        boton_UMAS = tk.Button(root, text="Generar Archivo", command=generar_archivoUMAS(dec))
        boton_UMAS.grid(row=8, columnspan=4, padx=5, pady=5)
    elif tipo == "C.Liquida":
        label_Cliq = tk.Label(root, text="Ingresa la cantidad",bg="#dedede")
        label_Cliq.grid(row=6, column=0, padx=5, pady=5)
        entry_Cliq = tk.Entry(root,validate="key",validatecommand=(root.register(validate_float), "%P", "%S"))
        entry_Cliq.grid(row=6, column=1, padx=5, pady=5)
        Cant = entry_Cliq.get()
        boton_Cliq = tk.Button(root, text="Generar Archivo", command=generar_archivoCliqPorc(Cant))
        boton_Cliq.grid(row=8, columnspan=4, padx=5, pady=5)
    elif tipo == "Porcentaje":
        root.geometry("550x300")
        label_Cant = tk.Label(root, text="Ingresa la cantidad",bg="#dedede")
        label_Cant.grid(row=6, column=0, padx=5, pady=5)
        entry_Cant = tk.Entry(root,validate="key",validatecommand=(root.register(validate_float), "%P", "%S"))
        entry_Cant.grid(row=6, column=1, padx=5, pady=5)
        label_Porc = tk.Label(root, text="Ingresa el porcentaje",bg="#dedede")
        label_Porc.grid(row=6, column=3, padx=5, pady=5)
        entry_Porc = tk.Entry(root,validate="key",validatecommand=(root.register(validate_float), "%P", "%S"))
        entry_Porc.grid(row=6, column=4, padx=5, pady=5)
        Porc = string_to_float(entry_Porc.get())
        Cant = entry_Cant.get()-(entry_Cant.get()*((Porc/100)))
        boton_porc = tk.Button(root, text="Generar Archivo", command=generar_archivoCliqPorc(Cant))
        boton_porc.grid(row=7,column=1, columnspan=1, padx=5, pady=5)

# Crear ventana
root = tk.Tk()
root.title("Calculadora de pensiones")
root.config(bg="#dedede")
root.resizable(0,0)
# Crear y posicionar los elementos en la ventana
root.geometry("300x100")
label_tipo = tk.Label(root, text="Tipo",bg="#dedede")
label_tipo.grid(row=5, column=0, padx=5, pady=5)
combo_tipo = ttk.Combobox(root, values=["Salario Minimo", "UMAS", "C.Liquida","Porcentaje"],state="readonly")
combo_tipo.grid(row=5, column=1, padx=5, pady=5)

boton_Recargar = tk.Button(root, text="Recargar", command=Recargar)
boton_Recargar.grid(row=7, columnspan=1, padx=5, pady=5)

root.mainloop()