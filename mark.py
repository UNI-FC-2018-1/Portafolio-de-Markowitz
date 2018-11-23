import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import random
import math

print("\n\t\t\tPORTAFOLIO DE MARKOWITZ")
print("\nVeamos un programa el cual calcula las diferentes formas en las\nque una persona puede invertir su dinero en una cantidad 'n'\nde activos.")
print("Esta nos ayudará a entender como funciona la Teoría de Markowitz.")

#importando los datos de excel
lista_activos=pd.read_csv('listActivos.csv',header=0,sep=';')

#genero porcentajes aleatorios para invertir en el portafolio
def puntos_aleatorios(num):
      lista=[0]*num
      for i in range(num):
          lista[i]=random.random()
      return lista

#definimos la cantidad de activos del portafolio
cant_activos=12

#extrayendo los activos del archivo csv
def extraerDatos(cant_activos):
    def precio_de_activo(posicion):
        lista=lista_activos.iloc[:,posicion]
        return lista
    precios_de_activo=[0]*(cant_activos)
    for i in range(cant_activos):
        precios_de_activo[i]=precio_de_activo(i+1)
    return precios_de_activo
vector_de_precios=extraerDatos(cant_activos)

#usamos como referencia el tamaño del primer activo ya que todos tienen el mismo
activo_1=vector_de_precios[0]
longitud=len(activo_1)
empresas=['Caterpillar','QUALCOMM Incorporated','Starbucks Corporation',"Domino's Pizza",'LATAM Airlines Group S.A.','VMware','Oracle Corporation','Microsoft Corporation','Adobe','Sony Corporation','Toyota Motor Corporation','Canon']


print("\nTomemos como ejemplo las siguientes empresas:\n\n1) Caterpillar\n2) QUALCOMM Incorporated\n3) Starbucks Corporation\n4) Domino's Pizza\n5) LATAM Airlines Group S.A.\n6) VMware\n7) Oracle Corporation\n8) Microsoft Corporation\n9) Adobe\n10) Sony Corporation\n11) Toyota Motor Corporation\n12) Canon\n")
cant_invertir=int(input("¿En cuántas empresas deseas invertir?: "))
print("\n¿En cuáles deseas invertir?\n")
vector_elegidos=[0]*cant_invertir
nombres=[0]*cant_invertir
for a in range(cant_invertir):
    num_empresa=int(input("Activo #"+str(a+1)+": "))
    nombres[a]=empresas[num_empresa-1]
    vector_elegidos[a]=vector_de_precios[num_empresa-1]

#calculamos los retornos de los activos
def retornosActivos(longitud,vector_elegidos):
    retornos_de_activo=[]
    for vector in vector_elegidos:
        retorno=[0]*(longitud-1)
        for i in range(longitud-1):
            retorno[i]=((vector[i+1]-vector[i])/vector[i])
        retornos_de_activo.append(retorno)
    return retornos_de_activo
vector_de_retornos=retornosActivos(longitud,vector_elegidos)
vector_de_retornos=np.asarray(vector_de_retornos)

#calculamos las esperanzas de los activos
def esperanzaActivos(vector_de_retornos):
    esperanza_de_activo=[]
    for i in range(cant_invertir):
        esperanza=vector_de_retornos[i].mean()
        esperanza_de_activo.append(esperanza)
    return esperanza_de_activo
vector_de_esperanzas=esperanzaActivos(vector_de_retornos)
vector_de_esperanzas=np.asarray(vector_de_esperanzas)

#calculamos las varianzas y covarianzas entre los activos
def covarianzaActivos(vector_de_retornos):
    covarianza_de_activo=[]
    for i in range(cant_invertir):
        fila=[0]*cant_invertir
        for j in range(cant_invertir):
            fila[j]=np.cov(vector_de_retornos[i],vector_de_retornos[j],ddof=0)[0][1]
        covarianza_de_activo.append(fila)
    return covarianza_de_activo
matriz_de_var_covar=covarianzaActivos(vector_de_retornos)
matriz_de_var_covar=np.asarray(matriz_de_var_covar)

tabla_1={}
for i in range(cant_invertir):
    tabla_1['Activo #'+str(i+1)+' elegido(%)']=vector_de_retornos[i]
tabla_retornos=pd.DataFrame(tabla_1)

tabla_2={'':['Esperanza','Varianza','D. Estándar']}
for i in range(cant_invertir):
    tabla_2['Activo #'+str(i+1)+' elegido(%)']=[vector_de_retornos[i].mean()*100,np.var(vector_de_retornos[i])*100,np.std(vector_de_retornos[i])*100]
tabla_info_activos=pd.DataFrame(tabla_2)

print("\n","\t"*cant_invertir,"DATOS ACERCA DE LOS ACTIVOS ELEGIDOS\n\n",lista_activos[nombres])
input("\nPulse enter para continuar...")

print("\n","\t"*cant_invertir,"RETORNOS DE LOS ACTIVOS\n\n",tabla_retornos*100)
input("\nPulse enter para continuar...")

print("\n","\t"*cant_invertir,"VARIABLES DE LOS ACTIVOS\n\n",tabla_info_activos)
print("\n","\t"*cant_invertir,"MATRIZ DE VARIANZA Y COVARIANZA (%)\n")
print(matriz_de_var_covar*100)

#funcion para generar n numeros aleatorios que suman 1
def puntos_aleatorios(cant_invertir):
    suma_num=1
    lista=[0]*cant_invertir
    for i in range(0,cant_invertir-1):
         lista[i]=random.uniform(0,suma_num)
         suma_num-=lista[i]
    lista[-1]=suma_num
    return lista

cant_puntos=int(input("\nIngrese la cantidad de puntos de la gráfica: "))

#lista de combinaciones de los n numeros aleatorios
def puntos(cant_puntos):
    porc_aleat=[0]*cant_puntos
    for i in range(0,cant_puntos):
         porc_aleat[i]=puntos_aleatorios(cant_invertir)
    return porc_aleat
puntos_grafica=puntos(cant_puntos)
puntos_grafica=np.asarray(puntos_grafica)

#esperanzas aletorias del portafolio
def esperanzas(cant_puntos,vector_prob_aleatorio):
    esperanza_aleat=[0]*cant_puntos
    for i in range(0,cant_puntos):
        esperanza_aleat[i]=vector_de_esperanzas.dot(vector_prob_aleatorio[i])
    return esperanza_aleat
esperanza_portafolio=esperanzas(cant_puntos,puntos_grafica)

#desviaciones aletorias del portafolio
def desviaciones(cant_puntos,vector_prob_aleatorio):
    desv_aleatoria=[0]*cant_puntos
    for i in range(0,cant_puntos):
        desv_aleatoria[i]=math.sqrt(vector_prob_aleatorio[i].transpose().dot(matriz_de_var_covar.dot(vector_prob_aleatorio[i])))
    return desv_aleatoria
desv_portafolio=desviaciones(cant_puntos,puntos_grafica)

#graficamente
plt.title("PORTAFOLIO DE MARKOWITZ")
plt.plot(desv_portafolio,esperanza_portafolio,'g.')
plt.xlabel("RIESGO")
plt.ylabel("RENTABILIDAD")
plt.grid(True)
plt.show()
