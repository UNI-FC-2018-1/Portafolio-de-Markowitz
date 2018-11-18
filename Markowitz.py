import matplotlib.pyplot as plt
import pandas as pd # importando pandas
import numpy as np
import math
import random
import csv
from matplotlib.ticker import NullFormatter

print("\n\t\t\tPORTAFOLIO DE MARKOWITZ")
print("\nRealizaremos a modo de ejemplo un portafolio que posee solo dos activos,\npero este puede tener muchos más. Depende del inversionista.")
print("\nEsta nos ayudará a entender como funciona la teoría de Markowitz.")
input("\nPulse enter para continuar...")

#importando desde excel los precios de los activos
datos_activos_csv= pd.read_csv('datos_activos.csv', header=0, sep=';')

#array de activos del portafolio
activo_1=np.asarray(datos_activos_csv['Precios del primer activo'])
activo_2=np.asarray(datos_activos_csv['Precios del segundo activo'])

#cantidad de precios de los activos
cant_1=len(activo_1)
cant_2=len(activo_2)

#funcion para convertir la lista a arreglo
def retornos_por_activo(activo,cant):
    resultado=[]
    for i in range(0,cant-1):
        retorno = ((activo[i+1]-activo[i])/activo[i])
        resultado.append(retorno)
    return resultado

#retornos de los activos
retorno_1=retornos_por_activo(activo_1,cant_1)
retorno_2=retornos_por_activo(activo_2,cant_2)

#convertir retornos a vectores
retorno_1=np.asarray(retorno_1)
retorno_2=np.asarray(retorno_2)

#media de cada activo
esperanza_1=retorno_1.mean()
esperanza_2=retorno_2.mean()

#desviacion estandar de cada activo
riesgo_1=np.std(retorno_1)
riesgo_2=np.std(retorno_2)

#varianza de cada activo
varianza_1=np.var(retorno_1)
varianza_2=np.var(retorno_2)
#covarianza de los activos
covarianza=np.cov(retorno_1, retorno_2, ddof=0)[0][1]

#esperanza del portafolio
suma_1=np.sum(retorno_1)
suma_2=np.sum(retorno_2)

#genero porcentajes aleatorios para invertir en el portafolio
def puntos_aleatorios(num):
      lista=[0]*num
      for i in range(num):
          lista[i]=random.random()
      return lista

#genero esperanzas aleatorias a partir de los porcentajes anteriores
def esperanzas_aleatorias(num,aleatorios):
      lista=[0]*num
      for i in range(num):
          lista[i]=(aleatorios[i]*suma_1)+suma_2*((1-aleatorios[i]))
      return lista

#genero riesgos aleatorias a partir de los porcentajes anteriores
def riesgos_aleatorios(num,aleatorios):
      lista = [0]  * num
      for i in range(num):
          lista[i] = math.sqrt((pow(aleatorios[i],2)*varianza_1)+(2*aleatorios[i]*(1-aleatorios[i])*covarianza)+(pow(1-aleatorios[i],2)*varianza_2))
      return lista

#creando una tabla para los retornos de los activos
retornos_de_activos={'Activo #1 (%)':retorno_1,'Activo #2 (%)':retorno_2}
tabla_rendimientos=pd.DataFrame(retornos_de_activos)

#creando una tabla para la informacion de los activos
info_activos={'':['Esperanza','Varianza','D. Estándar','Covarianza'],'Activo #1 (%)':[esperanza_1*100,varianza_1*100,riesgo_1*100,covarianza*100],'Activo #2 (%)':[esperanza_2*100,varianza_2*100,riesgo_2*100,covarianza*100]}
tabla_info_activos=pd.DataFrame(info_activos)

print("\n","\t"*3,"DATOS ACERCA DE LOS ACTIVOS\n\n",datos_activos_csv)
input("\nPulse enter para continuar...")

print("\n\tRETORNOS DE LOS ACTIVOS\n\n",tabla_rendimientos*100)
input("\nPulse enter para continuar...")

print("\n\t\tVARIABLES DE LOS ACTIVOS\n\n",tabla_info_activos)
num=int(input("\nIngrese cuantos puntos de la grafica desea obtener: "))

#lista de porcentajes aleatorios
porc_aleatorios=puntos_aleatorios(num)

#lista de esperanzas aleatorias del portafolio
lista_esperanzas=esperanzas_aleatorias(num,porc_aleatorios)

#lista de riesgos aleatorios del portafolio
lista_riesgos=riesgos_aleatorios(num,porc_aleatorios)

#graficamente
riesgo=np.array(lista_riesgos)
rentabilidad = np.array(lista_esperanzas)
plt.title("FRONTERA EFICIENTE")
plt.plot(riesgo,rentabilidad,'g.')
plt.xlabel("RIESGO")
plt.ylabel("RENTABILIDAD")
plt.grid(True)
plt.show()
