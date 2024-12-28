import calendar
from Cantidades import numero_a_letras, numero_a_moneda, NombreMes
from Salarios import SM
import os

def cant_dias(year, month):                
    return calendar.monthrange(year, month)[1]

def smm(smda, year, month):
    return round((smda * cant_dias(year, month)), 3)

doc = input("Ingresa el nombre del archivo: ")
doc = (f"Salidas//{doc}.txt")
f = open(f"{doc}","x")

yeari = int(input("Ingresa el año de inicio: "))
monthi = int(input("Ingresa el mes de inicio: "))
yearf = int(input("Ingresa el año final: "))
monthf = int(input("Ingresa el mes final: "))
dec = input("Medio salario minimo? (s/n) ")

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
        if dec == "s":
            smda /= 2
        archivo.write(f"\t\t--Año: {year} --\n")
        if dec == "s":
            archivo.write(f"\t\tSalario mínimo: {smda*2}\n\n")
        else:
            archivo.write(f"\t\tSalario mínimo: {smda}\n\n")
        
        SumMensual = []
        for mes in range(MesI, MesF+1):
            salario_mes = smm(smda, year, mes)
            SumMensual.append(salario_mes)
            archivo.write(f"{NombreMes(mes)} - {year}\t: ${salario_mes} ({numero_a_moneda(salario_mes)} m.n)\n")

        SumAnual = sum(SumMensual)
        SumTotal += SumAnual
        archivo.write(f"\nSuma de los salarios mínimos mensuales en el año {year}: ${round(SumAnual,3)} ({numero_a_moneda(SumAnual)})\n")
        archivo.write(f"Suma total acumulada hasta el año {year}: ${round(SumTotal,3)} ({numero_a_moneda(SumTotal)})\n\n")
