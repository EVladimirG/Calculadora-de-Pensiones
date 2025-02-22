# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import calendar
import os
from num2words import num2words
import csv

from db import *  #Ahí se encuentran los datos de salarios minimos y UMAS
 
#---------------------------------------------------------------------------Pensiones.pyw

iteraciones = 0 
Yeari=0
Yearf=0 
Monthi=0 
Monthf=0
Archivo = ""
dec = str("")

def cerrar_ventana():
    root.destroy()

def Recargar():
    tipo = 0
    global iteraciones, C_tipo
    if iteraciones == 0:
        tipo = C_tipo.get()
        L_tipo.destroy()
        C_tipo.destroy()
        B_Recargar.destroy()
        iteraciones +=1

    TipoDeuda(tipo)
    root.title(f"Calculadora de pensiones")

def Repetir():
    global iteraciones
    iteraciones = 0
    root.destroy()
    main()

def base():
    global E_nombre_archivo, E_yeari,C_mes_inicio,E_yearf,C_mes_final,C_tipo,B_repetir
    root.geometry("300x300")
    L_nombre_archivo = tk.Label(root, text="Nombre del archivo:",bg="#dedede")
    L_nombre_archivo.grid(row=0, column=0, padx=5, pady=5)
    E_nombre_archivo = tk.Entry(root)
    E_nombre_archivo.grid(row=0, column=1, padx=5, pady=5)

    L_yeari = tk.Label(root, text="Año de inicio:",bg="#dedede")
    L_yeari.grid(row=1, column=0, padx=5, pady=5)
    E_yeari = tk.Entry(root,validate="key",validatecommand=(root.register(validar_float), "%P", "%S"))
    E_yeari.grid(row=1, column=1, padx=5, pady=5)

    L_mes_inicio = tk.Label(root, text="Mes de inicio:",bg="#dedede")
    L_mes_inicio.grid(row=2, column=0, padx=5, pady=5)
    C_mes_inicio = ttk.Combobox(root, values=list(range(1, 13)),state='readonly')
    C_mes_inicio.grid(row=2, column=1, padx=5, pady=5)

    L_yearf = tk.Label(root, text="Año final:",bg="#dedede")
    L_yearf.grid(row=3, column=0, padx=5, pady=5)
    E_yearf = tk.Entry(root,validate="key",validatecommand=(root.register(validar_float), "%P", "%S"))
    E_yearf.grid(row=3, column=1, padx=5, pady=5)

    L_mes_final = tk.Label(root, text="Mes final:",bg="#dedede")
    L_mes_final.grid(row=4, column=0, padx=5, pady=5)
    C_mes_final = ttk.Combobox(root, values=list(range(1, 13)),state='readonly')
    C_mes_final.grid(row=4, column=1, padx=5, pady=5)

    B_repetir = tk.Button(root, text="Repetir", command= Repetir)
    B_repetir.grid(row=8,column=1, columnspan=1, padx=5, pady=5)

def numero_a_moneda(numero):
    entero = int(numero)
    decimales = round((numero - entero) * 100)

    texto_entero = num2words(entero, lang='es').capitalize()

    texto_decimales = num2words(decimales, lang='es').capitalize()

    if decimales > 0:
        resultado = f"{texto_entero} pesos y {texto_decimales} centavos"
    else:
        resultado = f"{texto_entero} pesos"

    return resultado

def strtf(string_value):                    #String a float
    try:
        float_value = float(string_value)
        return float_value
    except ValueError:
        print("Error: El string no contiene un valor numérico")
        return None
    
def strti(string_value):                    #String a int
    try:
        float_value = int(string_value)
        return float_value
    except ValueError:
        print("Error: El string no contiene un valor numérico")
        return None

def validar_float(input_string, event):     #Por si a caso
    if input_string.isdigit() or input_string == "." or (input_string[0] == "." and len(input_string) == 1):
        try:
            float(input_string)
            return True
        except ValueError:
            return False
    else:
        return False

def convertir_a_float(lista):               #Convierte toda una lista a float
    try:
        return [float(elemento) for elemento in lista]
    except ValueError:
        return "Error: No todos los elementos de la lista pueden convertirse a float."

def cant_dias(year, month):                
    return calendar.monthrange(year, month)[1]

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

def NumeroMes(nombre_mes):
    meses = {
        "Enero": 1,
        "Febrero": 2, 
        "Marzo": 3, 
        "Abril": 4,
        "Mayo": 5, 
        "Junio": 6, 
        "Julio": 7, 
        "Agosto": 8,
        "Septiembre": 9, 
        "Octubre": 10, 
        "Noviembre": 11, 
        "Diciembre": 12
    }
    return meses.get(nombre_mes.capitalize(), None)  

def smm(smda, year, month):
    return round((smda * cant_dias(year, month)), 3)

def Template(YearI, YearF, MesI, MesF):
    filename = 'Rango.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        for Year in range(YearI, YearF + 1):
            writer.writerow([f'{Year}']) 

            start_month = MesI if Year == YearI else 1
            end_month = MesF if Year == YearF else 12

            for Mes in range(start_month, end_month + 1):
                writer.writerow([f'{NombreMes(Mes)}', '']) 
            
    print(f"Archivo '{filename}' generado exitosamente.")

def obtener_valor(año, mes, archivo='Rango.csv'):
    with open(archivo, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        año_actual = None

        for row in reader:
            row = [campo.strip() for campo in row if campo.strip()] 
            if len(row) == 1:  
                try:
                    año_actual = int(row[0])
                except ValueError:
                    continue 
            elif len(row) == 2 and año_actual is not None: 
                nombre_mes, valor = row[0].strip(), row[1].strip()
                num_mes = NumeroMes(nombre_mes)

                if año_actual == año and num_mes == mes:
                    return int(valor)

def TipoDeuda(tipo):
    global E_Porc, E_Cant, E_Cliq, C_sm, C_UMAS, L_GenTemplate, B_GenTemplate  
    if tipo == "Salario Minimo":
        base()
        L_sm = tk.Label(root, text="Salario mínimo?",bg="#dedede")
        L_sm.grid(row=6, column=0, padx=5, pady=5)
        C_sm = ttk.Combobox(root, values=["Completo", "Medio", "3/4", "Uno y medio","Doble"],state="readonly")
        C_sm.grid(row=6, column=1, padx=5, pady=5)
        B_SM = tk.Button(root, text="Generar Archivo", command=lambda: generar_archivoSM(dec))
        B_SM.grid(row=8, columnspan=1, padx=5, pady=5)
    elif tipo == "UMAS":
        base()
        L_UMAS = tk.Label(root, text="Ingresa la UMA",bg="#dedede")
        L_UMAS.grid(row=6, column=0, padx=5, pady=5)
        C_UMAS = ttk.Combobox(root, values=["Completa", "Media", "3/4", "Una y media","Doble"],state='readonly')
        C_UMAS.grid(row=6, column=1, padx=5, pady=5)
        B_UMAS = tk.Button(root, text="Generar Archivo", command=lambda: generar_archivoUMAS(dec))
        B_UMAS.grid(row=8, columnspan=1, padx=5, pady=5)
    elif tipo == "C.Liquida":
        base()
        L_Cliq = tk.Label(root, text="Ingresa la cantidad",bg="#dedede")
        L_Cliq.grid(row=6, column=0, padx=5, pady=5)
        E_Cliq = tk.Entry(root,validate="key",validatecommand=(root.register(validar_float), "%P", "%S"))
        E_Cliq.grid(row=6, column=1, padx=5, pady=5)
        cant = E_Cliq.get()
        B_Cliq = tk.Button(root, text="Generar Archivo", command=lambda: generar_archivoCliq(cant))
        B_Cliq.grid(row=8, columnspan=1, padx=5, pady=5)
    elif tipo == "Porcentaje":
        root.geometry("550x400")
        base()
        L_Cant = tk.Label(root, text="Ingresa la cantidad", bg="#dedede")
        L_Cant.grid(row=6, column=0, padx=5, pady=5)
        E_Cant = tk.Entry(root, validate="key", validatecommand=(root.register(validar_float), "%P", "%S"))
        E_Cant.grid(row=6, column=1, padx=5, pady=5)
        
        L_Porc = tk.Label(root, text="Ingresa el porcentaje", bg="#dedede")
        L_Porc.grid(row=7, column=0, padx=5, pady=5)
        E_Porc = tk.Entry(root, validate="key", validatecommand=(root.register(validar_float), "%P", "%S"))
        E_Porc.grid(row=7, column=1, padx=5, pady=5)
        B_porc = tk.Button(root, text="Generar Archivo", command=lambda: generar_archivoPorc(E_Cant.get(),E_Porc.get()))
        B_porc.grid(row=8, columnspan=1, padx=5, pady=5)
    elif tipo == "Rango":
        base()
        L_GenTemplate = tk.Label(root, text="Generar Plantilla", bg="#dedede")
        L_GenTemplate.grid(row=5, column=0, padx=5, pady=5)
        B_GenTemplate = tk.Button(root, text="Generar", command=GenerarPlantilla)
        B_GenTemplate.grid(row=5,column=1, columnspan=2, padx=5, pady=5) 

        L_GenArchivo = tk.Label(root, text="Cargar Plantilla", bg="#dedede")
        L_GenArchivo.grid(row=6, column=0, padx=5, pady=5)
        B_GenArchivo = tk.Button(root, text="Cargar", command=lambda: generar_archivoCustom())
        B_GenArchivo.grid(row=6, column=1, columnspan=2, padx=5, pady=5) 

def GenerarPlantilla():
    global E_yeari, E_yearf, C_mes_final, C_mes_inicio, E_nombre_archivo, L_GenTemplate, B_GenTemplate 
    
    try:
        Y0=int(E_yeari.get())
        Y1=int(E_yearf.get())
        if Yearf < Yeari:
            messagebox.showwarning("Error","El año final es menor que el año de inicio")
            return
        if Yeari > 2025 or Yearf > 2025:
            messagebox.showwarning("Error","Ingresa un año igual o menor al actual")
            return
    except ValueError as er:
        if str(er) == "invalid literal for int() with base 10: ''":
            pass
        else: 
            messagebox.showwarning("Error","Verifica escribir bien tus datos")
    M0=int(C_mes_inicio.current())+1
    M1=int(C_mes_final.current())+1


    Template(Y0,Y1,M0,M1)
    os.system("Rango.csv")

def generar_archivoSM(dec):
    global E_yeari, E_yearf, C_mes_final, C_mes_inicio, E_nombre_archivo,C_sm
    Archivo = E_nombre_archivo.get()
    doc = Archivo
    doc = f"{doc}.txt"
    dec = ""
    try:
        dec = C_sm.get()
        Yeari = int(E_yeari.get())
        Yearf = int(E_yearf.get())
        if Yearf < Yeari:
            messagebox.showwarning("Error","El año final es menor que el año de inicio")
            return
        if Yeari > 2025 or Yearf > 2025:
            messagebox.showwarning("Error","Ingresa un año igual o menor al actual")
            return
    except ValueError as er:
        if str(er) == "invalid literal for int() with base 10: ''":
            pass
        else: 
            messagebox.showwarning("Error","Verifica escribir bien tus datos")
    Monthi = C_mes_inicio.current()+1
    Monthf = C_mes_final.current()+1
    
    with open(doc, "w") as archivo:
        SumTotal = 0
        for year in range(Yeari, Yearf+1):
            if year == Yeari:
                MesI = Monthi
            else:
                MesI = 1
            if year == Yearf:
                MesF = Monthf
            else:
                MesF = 12
            smda = 0
            smda = SM[year]['diario']
            if dec == "Medio":
                smda *= 0.5
            elif dec == "Uno y medio":
                smda *= 1.5
            elif dec == "Doble":
                smda *= 2
            elif dec == "Completo":
                smda * 1
            elif dec == "3/4":
                smda *= 3/4
            archivo.write(f"\t\t--Año: {year} --\n")            
            archivo.write(f"\t\tSalario mínimo: ${SM[year]['diario']}\n\n")            
            
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
    os.system(doc)

def generar_archivoUMAS(dec):
    global E_yeari, E_yearf, C_mes_final, C_mes_inicio, E_nombre_archivo,C_UMAS
    Archivo = E_nombre_archivo.get()
    doc = Archivo
    doc = f"{doc}.txt"
    dec = ""
    try:
        dec = C_UMAS.get()
        Yeari = int(E_yeari.get())
        Yearf = int(E_yearf.get())
        if Yearf < Yeari:
            messagebox.showwarning("Error","El año final es menor que el año de inicio")
            return
        if Yeari > 2025 or Yearf > 2025:
            messagebox.showwarning("Error","Ingresa un año igual o menor al actual")
            return
    except ValueError as er:
        if str(er) == "invalid literal for int() with base 10: ''":
            pass
        else: 
            messagebox.showwarning("Error","Verifica escribir bien tus datos")
    Monthi = C_mes_inicio.current()+1
    Monthf = C_mes_final.current()+1
    
    with open(doc, "w") as archivo:
        SumTotal = 0
        for year in range(Yeari, Yearf+1):
            if year == Yeari:
                MesI = Monthi
            else:
                MesI = 1
            if year == Yearf:
                MesF = Monthf
            else:
                MesF = 12
            umas = 0
            umas = SM[year]['UMA']
            if dec == "Media":
                umas *= 0.5
            elif dec == "Una y media":
                umas *= 1.5
            elif dec == "Doble":
                umas *= 2
            elif dec == "Completa":
                umas * 1
            elif dec == "3/4":
                umas *= 3/4
            archivo.write(f"\t\t--Año: {year} --\n")
            archivo.write(f"\t\tSalario mínimo: ${SM[year]['UMA']}\n\n")
            
            SumMensual = []
            for mes in range(MesI, MesF+1):
                salario_mes = smm(umas, year, mes)
                SumMensual.append(salario_mes)
                archivo.write(f"{NombreMes(mes)} - {year}\t: ${salario_mes} ({numero_a_moneda(salario_mes)} m.n)\n")

            SumAnual = sum(SumMensual)
            SumTotal += SumAnual
            archivo.write(f"\nSuma de los pagos en UMAS, mensualmente en el año {year}: ${round(SumAnual,3)} ({numero_a_moneda(SumAnual)} m.n)\n")
            archivo.write(f"Suma total acumulada hasta el año {year}: ${round(SumTotal,3)} ({numero_a_moneda(SumTotal)} m.n)\n\n")

    messagebox.showinfo("Archivo Creado", "El archivo se generó exitosamente")
    os.system(doc)

def generar_archivoCliq(cant):
    global E_yeari, E_yearf, C_mes_final, C_mes_inicio, E_nombre_archivo, E_Cliq
    Archivo = E_nombre_archivo.get()
    doc = Archivo
    doc = f"{doc}.txt"
    try:
        Yeari = int(E_yeari.get())
        Yearf = int(E_yearf.get())
        cantidad = strtf(E_Cliq.get())
        if Yearf < Yeari:
            messagebox.showwarning("Error","El año final es menor que el año de inicio")
            return
        if cantidad <= 0:
            messagebox.showwarning("Error","Ingresa un valor válido")
            return
        if Yeari > 2025 or Yearf > 2025:
            messagebox.showwarning("Error","Ingresa un año igual o menor al actual")
            return
    except ValueError as er:
        if str(er) == "invalid literal for int() with base 10: ''":
            pass
        else: 
            messagebox.showwarning("Error","Verifica escribir bien tus datos")
    Monthi = C_mes_inicio.current()+1
    Monthf = C_mes_final.current()+1
    
    with open(doc, "w") as archivo:
        SumTotal = 0
        for year in range(Yeari, Yearf+1):
            if year == Yeari:
                MesI = Monthi
            else:
                MesI = 1
            if year == Yearf:
                MesF = Monthf
            else:
                MesF = 12

            archivo.write(f"\t\t--Año: {year} --\n")
            archivo.write(f"\t\tSalario : ${cant}\n\n")
            
            SumMensual = []
            for mes in range(MesI, MesF+1):
                salario_mes = cantidad
                SumMensual.append(salario_mes)
                archivo.write(f"{NombreMes(mes)} - {year}\t: ${salario_mes} ({numero_a_moneda(salario_mes)} m.n)\n")

            SumAnual = sum(SumMensual)
            SumTotal += SumAnual
            archivo.write(f"\nSuma del salario mensualmente en el año {year}: ${round(SumAnual,3)} ({numero_a_moneda(SumAnual)} m.n)\n")
            archivo.write(f"Suma total acumulada hasta el año {year}: ${round(SumTotal,3)} ({numero_a_moneda(SumTotal)} m.n)\n\n")

    messagebox.showinfo("Archivo Creado", "El archivo se generó exitosamente")
    os.system(doc)

def generar_archivoPorc(cant, porc):
    global E_Porc, E_Cant, E_yeari, E_yearf, C_mes_final, C_mes_inicio, E_nombre_archivo
    Archivo = E_nombre_archivo.get()
    doc = Archivo
    doc = f"{doc}.txt"
    try:
        Yeari = strti(E_yeari.get())
        Yearf = strti(E_yearf.get())
        cantidad = (int(cant))*((int(porc))/100)
        if Yearf < Yeari:
            messagebox.showwarning("Error","El año final es menor que el año de inicio")
            return
        if cantidad <= 0:
            messagebox.showwarning("Error","Ingresa un valor válido")
            return
        if Yeari > 2025 or Yearf > 2025:
            messagebox.showwarning("Error","Ingresa un año igual o menor al actual")
            return
    except ValueError as er:
        if str(er) == "invalid literal for int() with base 10: ''":
            pass
        else: 
            messagebox.showwarning("Error","Verifica escribir bien tus datos")
    Monthi = C_mes_inicio.current()+1
    Monthf = C_mes_final.current()+1
    
    with open(doc, "w") as archivo:
        SumTotal = 0
        for year in range(Yeari, Yearf+1):
            if year == Yeari:
                MesI = Monthi
            else:
                MesI = 1
            if year == Yearf:
                MesF = Monthf
            else:
                MesF = 12

            archivo.write(f"\t\t--Año: {year} --\n")
            archivo.write(f"\t\tSalario : ${cant}\n\t\tPorcentaje: {porc}%\n\n")
            
            SumMensual = []
            for mes in range(MesI, MesF+1):
                salario_mes = cantidad
                SumMensual.append(salario_mes)
                archivo.write(f"{NombreMes(mes)} - {year}\t: ${salario_mes} ({numero_a_moneda(salario_mes)} m.n)\n")

            SumAnual = sum(SumMensual)
            SumTotal += SumAnual
            archivo.write(f"\nSuma del salario mensualmente en el año {year}: ${round(SumAnual,3)} ({numero_a_moneda(SumAnual)} m.n)\n")
            archivo.write(f"Suma total acumulada hasta el año {year}: ${round(SumTotal,3)} ({numero_a_moneda(SumTotal)} m.n)\n\n")

    messagebox.showinfo("Archivo Creado", "El archivo se generó exitosamente")
    os.system(doc)

def generar_archivoCustom():
    global E_yeari, E_yearf, C_mes_final, C_mes_inicio, E_nombre_archivo
    Archivo = E_nombre_archivo.get()
    doc = Archivo
    doc = f"{doc}.txt"
    
    try:
        Yeari = int(E_yeari.get())
        Yearf = int(E_yearf.get())
        if Yearf < Yeari:
            messagebox.showwarning("Error","El año final es menor que el año de inicio")
            return
        if Yeari > 2025 or Yearf > 2025:
            messagebox.showwarning("Error","Ingresa un año igual o menor al actual")
            return
    except ValueError as er:
        if str(er) == "invalid literal for int() with base 10: ''":
            pass
        else: 
            messagebox.showwarning("Error","Verifica escribir bien tus datos")
    Monthi = C_mes_inicio.current()+1
    Monthf = C_mes_final.current()+1


    with open(doc, "w") as archivo:
        SumTotal = 0
        for year in range(Yeari, Yearf+1):                      #Primer for (años)
            if year == Yeari:
                MesI = Monthi
            else:
                MesI = 1
            if year == Yearf:
                MesF = Monthf
            else:
                MesF = 12

            archivo.write(f"\t\t--Año: {year} --\n")
            
            SumMensual = []
            for mes in range(MesI, MesF+1):                     #Segundo for (meses)
                salario_mes = obtener_valor(year, mes)
                SumMensual.append(salario_mes)
                archivo.write(f"{NombreMes(mes)} - {year}\t: ${salario_mes} ({numero_a_moneda(salario_mes)} m.n)\n")

            SumAnual = sum(convertir_a_float(SumMensual))
            SumTotal += SumAnual
            archivo.write(f"\nSuma pagos mensuales en el año {year}: ${round(SumAnual,3)} ({numero_a_moneda(SumAnual)} m.n)\n")
            archivo.write(f"Suma total acumulada hasta el año {year}: ${round(SumTotal,3)} ({numero_a_moneda(SumTotal)} m.n)\n\n")

    os.system(doc)

def main():

    global C_tipo, root, L_tipo, B_Recargar

    root = tk.Tk()
    root.title("Calculadora de pensiones")
    root.config(bg="#dedede")
    root.resizable(0,0)

    root.geometry("230x100")
    L_tipo = tk.Label(root, text="Tipo",bg="#dedede")
    L_tipo.grid(row=5, column=0, padx=5, pady=5)
    C_tipo = ttk.Combobox(root, values=["Salario Minimo", "UMAS", "C.Liquida","Porcentaje","Rango"],state="readonly")
    C_tipo.grid(row=5, column=1, padx=5, pady=5)

    B_Recargar = tk.Button(root, text="Continuar", command= Recargar)
    B_Recargar.grid(row=7,column=1, columnspan=2, padx=5, pady=5)

    root.mainloop()

main()