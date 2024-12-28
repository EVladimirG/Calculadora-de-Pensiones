# -*- coding: utf-8 -*-

import calendar
import os
from Cantidades import numero_a_letras, numero_a_moneda, NombreMes
from Salarios import SM
import time

def cant_dias(year, month):                
    return calendar.monthrange(year, month)[1]

def smm(smda, year, month):
    return round((smda * cant_dias(year, month)), 3)


doc = input("Ingresa el nombre del archivo: ")
doc = (doc+".txt")
arc = open(doc)

os.system('cls')

yeari = int(input("Ingresa el año de inicio: "))
monthi = int(input("Ingresa el mes de inicio: "))
yearf = int(input("Ingresa el año final: "))
monthf = int(input("Ingresa el mes final: "))
dec = input("Medio salario minimo? (s/n) ")
os.system('cls')

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

    #smda = float(input(f'Valor del salario mínimo diario en {year}? '))
    smda = SM[year]['diario']
    if dec == "s":
        smda /= 2
    print("\t\t--Año:", year, "--")
    if dec == "s":
        print(f"\t\tSalario mínimo: {smda*2}\n")
    else:
        print(f"\t\tSalario mínimo: {smda}\n")
    SumMensual = []
    
    for mes in range(MesI, MesF+1):
        salario_mes = smm(smda, year, mes)
        SumMensual.append(salario_mes)
        print(f"{NombreMes(mes)} - {year}\t: ${salario_mes} ({numero_a_moneda(salario_mes)} m.n)")

    SumAnual = sum(SumMensual)
    SumTotal += SumAnual
    print(f"\nSuma de los salarios mínimos mensuales en el año {year}: ${round(SumAnual,3)} ({numero_a_moneda(SumAnual)})")
    print(f"Suma total acumulada hasta el año {year}: ${round(SumTotal,3)} ({numero_a_moneda(SumTotal)})\n")
os.system('pause')
