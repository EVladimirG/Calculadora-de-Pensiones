# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import calendar
import os
from num2words import num2words

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
    global iteraciones, combo_tipo
    if iteraciones == 0:
        tipo = combo_tipo.get()
        label_tipo.destroy()
        combo_tipo.destroy()
        boton_Recargar.destroy()
        iteraciones +=1

    TipoDeuda(tipo)
    root.title(f"Calculadora de pensiones")

def Repetir():
    global iteraciones
    iteraciones = 0
    root.destroy()
    main()

def base():
    global entry_nombre_archivo, entry_yeari,combo_mes_inicio,entry_yearf,combo_mes_final,combo_tipo,boton_repetir
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
    combo_mes_inicio = ttk.Combobox(root, values=list(range(1, 13)),state='readonly')
    combo_mes_inicio.grid(row=2, column=1, padx=5, pady=5)

    label_yearf = tk.Label(root, text="Año final:",bg="#dedede")
    label_yearf.grid(row=3, column=0, padx=5, pady=5)
    entry_yearf = tk.Entry(root,validate="key",validatecommand=(root.register(validate_float), "%P", "%S"))
    entry_yearf.grid(row=3, column=1, padx=5, pady=5)

    label_mes_final = tk.Label(root, text="Mes final:",bg="#dedede")
    label_mes_final.grid(row=4, column=0, padx=5, pady=5)
    combo_mes_final = ttk.Combobox(root, values=list(range(1, 13)),state='readonly')
    combo_mes_final.grid(row=4, column=1, padx=5, pady=5)

    boton_repetir = tk.Button(root, text="Repetir", command= Repetir)
    boton_repetir.grid(row=8,column=1, columnspan=1, padx=5, pady=5)
    # Ejecutar la ventana

def numero_a_moneda(numero):
    # Separar la parte entera y los decimales
    entero = int(numero)
    decimales = round((numero - entero) * 100)

    # Convertir la parte entera a texto
    texto_entero = num2words(entero, lang='es').capitalize()

    # Convertir los decimales a texto
    texto_decimales = num2words(decimales, lang='es').capitalize()

    # Crear la representación en texto
    if decimales > 0:
        resultado = f"{texto_entero} pesos y {texto_decimales} centavos"
    else:
        resultado = f"{texto_entero} pesos"

    return resultado

def strtf(string_value):
    try:
        float_value = float(string_value)
        return float_value
    except ValueError:
        print("Error: The string contains a non-numeric value.")
        return None
    
def strti(string_value):
    try:
        float_value = int(string_value)
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

def smm(smda, year, month):
    return round((smda * cant_dias(year, month)), 3)

def TipoDeuda(tipo):
    global entry_Porc, entry_Cant, entry_Cliq, combo_sm, combo_UMAS
    if tipo == "Salario Minimo":
        base()
        label_sm = tk.Label(root, text="Salario mínimo?",bg="#dedede")
        label_sm.grid(row=6, column=0, padx=5, pady=5)
        combo_sm = ttk.Combobox(root, values=["Completo", "Medio", "3/4", "Uno y medio","Doble"],state="readonly")
        combo_sm.grid(row=6, column=1, padx=5, pady=5)
        boton_SM = tk.Button(root, text="Generar Archivo", command=lambda: generar_archivoSM(dec))
        boton_SM.grid(row=8, columnspan=1, padx=5, pady=5)
    elif tipo == "UMAS":
        base()
        label_UMAS = tk.Label(root, text="Ingresa la UMA",bg="#dedede")
        label_UMAS.grid(row=6, column=0, padx=5, pady=5)
        combo_UMAS = ttk.Combobox(root, values=["Completa", "Media", "3/4", "Una y media","Doble"],state='readonly')
        combo_UMAS.grid(row=6, column=1, padx=5, pady=5)
        boton_UMAS = tk.Button(root, text="Generar Archivo", command=lambda: generar_archivoUMAS(dec))
        boton_UMAS.grid(row=8, columnspan=1, padx=5, pady=5)
    elif tipo == "C.Liquida":
        base()
        label_Cliq = tk.Label(root, text="Ingresa la cantidad",bg="#dedede")
        label_Cliq.grid(row=6, column=0, padx=5, pady=5)
        entry_Cliq = tk.Entry(root,validate="key",validatecommand=(root.register(validate_float), "%P", "%S"))
        entry_Cliq.grid(row=6, column=1, padx=5, pady=5)
        cant = entry_Cliq.get()
        boton_Cliq = tk.Button(root, text="Generar Archivo", command=lambda: generar_archivoCliq(cant))
        boton_Cliq.grid(row=8, columnspan=1, padx=5, pady=5)
    elif tipo == "Porcentaje":
        root.geometry("550x400")
        base()
        label_Cant = tk.Label(root, text="Ingresa la cantidad", bg="#dedede")
        label_Cant.grid(row=6, column=0, padx=5, pady=5)
        entry_Cant = tk.Entry(root, validate="key", validatecommand=(root.register(validate_float), "%P", "%S"))
        entry_Cant.grid(row=6, column=1, padx=5, pady=5)
        
        label_Porc = tk.Label(root, text="Ingresa el porcentaje", bg="#dedede")
        label_Porc.grid(row=7, column=0, padx=5, pady=5)
        entry_Porc = tk.Entry(root, validate="key", validatecommand=(root.register(validate_float), "%P", "%S"))
        entry_Porc.grid(row=7, column=1, padx=5, pady=5)
        boton_porc = tk.Button(root, text="Generar Archivo", command=lambda: generar_archivoPorc(entry_Cant.get(),entry_Porc.get()))
        boton_porc.grid(row=8, columnspan=1, padx=5, pady=5)

def generar_archivoSM(dec):
    global entry_yeari, entry_yearf, combo_mes_final, combo_mes_inicio, entry_nombre_archivo,combo_sm
    Archivo = entry_nombre_archivo.get()
    doc = Archivo
    doc = f"{doc}.txt"
    dec = ""
    try:
        dec = combo_sm.get()
        Yeari = int(entry_yeari.get())
        Yearf = int(entry_yearf.get())
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
    Monthi = combo_mes_inicio.current()+1
    Monthf = combo_mes_final.current()+1
    
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
    global entry_yeari, entry_yearf, combo_mes_final, combo_mes_inicio, entry_nombre_archivo,combo_UMAS
    Archivo = entry_nombre_archivo.get()
    doc = Archivo
    doc = f"{doc}.txt"
    dec = ""
    try:
        dec = combo_UMAS.get()
        Yeari = int(entry_yeari.get())
        Yearf = int(entry_yearf.get())
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
    Monthi = combo_mes_inicio.current()+1
    Monthf = combo_mes_final.current()+1
    
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
    global entry_yeari, entry_yearf, combo_mes_final, combo_mes_inicio, entry_nombre_archivo, entry_Cliq
    Archivo = entry_nombre_archivo.get()
    doc = Archivo
    doc = f"{doc}.txt"
    try:
        Yeari = int(entry_yeari.get())
        Yearf = int(entry_yearf.get())
        cantidad = strtf(entry_Cliq.get())
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
    Monthi = combo_mes_inicio.current()+1
    Monthf = combo_mes_final.current()+1
    
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
    global entry_Porc, entry_Cant, entry_yeari, entry_yearf, combo_mes_final, combo_mes_inicio, entry_nombre_archivo
    Archivo = entry_nombre_archivo.get()
    doc = Archivo
    doc = f"{doc}.txt"
    try:
        Yeari = strti(entry_yeari.get())
        Yearf = strti(entry_yearf.get())
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
    Monthi = combo_mes_inicio.current()+1
    Monthf = combo_mes_final.current()+1
    
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

def main():

    global combo_tipo, root, label_tipo, boton_Recargar

    root = tk.Tk()
    root.title("Calculadora de pensiones")
    root.config(bg="#dedede")
    root.resizable(0,0)

    root.geometry("230x100")
    label_tipo = tk.Label(root, text="Tipo",bg="#dedede")
    label_tipo.grid(row=5, column=0, padx=5, pady=5)
    combo_tipo = ttk.Combobox(root, values=["Salario Minimo", "UMAS", "C.Liquida","Porcentaje"],state="readonly")
    combo_tipo.grid(row=5, column=1, padx=5, pady=5)

    boton_Recargar = tk.Button(root, text="Continuar", command= Recargar)
    boton_Recargar.grid(row=7,column=1, columnspan=2, padx=5, pady=5)

    root.mainloop()

main()