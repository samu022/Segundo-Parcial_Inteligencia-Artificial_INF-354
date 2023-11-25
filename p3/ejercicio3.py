# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 10:47:08 2023

@author: Samuel
Ejercicio 3 segundo parcial ia inf-354
Agente Viajero sin DEAP
"""
from __future__ import division

import random

import numpy as np
import copy


matriz=np.loadtxt("agente.csv", delimiter=";")

print(matriz)

#generamos la ruta empezando desde 0
#0=A, 1=B, 2=C, 3=D, 4=E

#definimos  poblacion
def Poblacion(Ptam):
    nPob=[]
    for i in range(Ptam):
        nPob.append(Permutacion())
    return nPob

def Permutacion():
    permutacion=[]
    permutacion.append(0)
    i=0
    while i<4:
        #random entre 1 y 4 
        au=random.randint(1,4)
        if au not in permutacion:
            #no se repite
            permutacion.append(au)
            i+=1
    return permutacion




#para hacer cruce
def hacer_cruce(individuo, distancia, Pcru):
    nPob=[]
    exac=[]
    for i in range(len(distancia)):
        exac.append(100/(distancia[i]))
    for j in range(len(individuo)//2):
        ind1, ind2 = elegir_dos_dif_padres(exac)
        hijos=CrucePadres(individuo[ind1], individuo[ind2], Pcru)
        nPob.append(hijos[0])
        nPob.append(hijos[1])
        
    return nPob

#cruce
def CrucePadres(ind1, ind2, Pcru):
    hijo=[]
    hijo1=[]
    hijo2=[]
    
    padre1=copy.deepcopy(ind1)
    padre2=copy.deepcopy(ind2)
    
    aux1=random.random()
    #es menor que la probabilidad de cruce se realiza op
    if(aux1<Pcru):
        #metodo 1
        longitud=len(padre1)
        #cruce seleccionar num 
        csec=random.randint(1,longitud-1)
        hijo1.append(padre1[0])
        hijo2.append(padre2[0])
        
        for i in range(csec):
            hijo1.append(padre1[i+1])
            hijo2.append(padre2[i+1])
        index=csec
        #cruce
        while len(hijo1)<longitud:
            if index==longitud:
                index=1
            aux=padre2[index]
            if aux not in hijo1:
                hijo1.append(aux)
            else:
                index+=1
        index=csec
        
        #segundo hijo
        while len(hijo2)<longitud:
            if index==longitud:
                index=1
            aux=padre1[index]
            if aux not in hijo2:
                hijo2.append(aux)
            else:
                index=index+1
        #devolvemos hijos
        hijo.append(hijo1)
        hijo.append(hijo2)
    else:
        #padres pasan a la siguiente generacion
        hijo.append(padre1)
        hijo.append(padre2)
    return hijo

#baja la probabilidad de mutacion

def elegir_un_padre(Exactitud):
    cont=len(Exactitud)
    idx1=int(np.floor(np.random.random()*cont))
    idx2=int(np.floor(np.random.random()*cont))
    while idx2 == idx1:
        idx2 = int(np.floor(np.random.random()*cont))
        
    if Exactitud[idx1]>Exactitud[idx2]:
        return idx1
    else:
        return idx2

def elegir_dos_dif_padres(Exactitud):
    idx1=elegir_un_padre(Exactitud)
    idx2=elegir_un_padre(Exactitud)
    while idx2==idx1:
        idx2 = elegir_un_padre(Exactitud)
    
    assert idx1<len(Exactitud)
    assert idx2 < len(Exactitud)
    return idx1, idx2

#creamos la clase de Seleccion
class Selection(object):
    def RuletaSeleccion(self, _a, k):
        a=np.asarray(_a)
        idx=np.argsort(a)
        idx=idx[::-1]
        sort_a=a[idx]
        sum_a=np.sum(a).astype(np.float)
        selected_index=[]
        j=0
        while j<k:
            u=np.random.rand()*sum_a
            sum_=0
            for i in range(sort_a.shape[0]):
                sum_ +=sort_a[i]
                if sum_ > u:
                    if idx[i] not in selected_index:
                        selected_index.append(idx[i])
                        j+=1
                    break
                
        return selected_index
        
#mutacion
def Mutacion(individuo, Pmut):
    aux=random.random()
    if aux<Pmut:
        pos1, pos2=elegir_dos_dif_padres(individuo)
        auxi=individuo[pos1]
        individuo[pos1]=individuo[pos2]
        individuo[pos2]=auxi
    return individuo

def hacer_mutacion(gente, Pmut):
    pMutada=[]
    for i in range(len(gente)):
        pMutada.append(Mutacion(gente[i], Pmut))
        
    return pMutada

#para evaluar
def Evaluar(individuo):
    suma=0
    #print(individuo)
    for i in range(0,len(individuo)-1):
        suma=suma+matriz[individuo[i],individuo[i+1]]
    suma=suma+matriz[individuo[len(individuo)-1],individuo[0]]
    return suma

#main
Pmax=10
Gmax=40
Pcruc=0.9
Pmut=0.1
poblacion=Poblacion(Pmax)

Totalpob=[]
Totaldis=[]
cuenta=0
pastelite=poblacion[0]
dato=[]

#evaluacion 0
viajeld=[]
for i in range(len(poblacion)):
    viajeld.append(Evaluar(poblacion[i]))

for i in range(len(poblacion)):
    Totalpob.append(poblacion[i])
    Totaldis.append(viajeld[i])

#generacionex
for i in range(Gmax):
    PobCompleta=[]
    DisCompleta=[]
    
    for j in range(len(poblacion)):
        PobCompleta.append(poblacion[j])
        DisCompleta.append(viajeld[j])
    
    #reproduccion
    pobcruc=hacer_cruce(poblacion, viajeld, Pcruc)
    #mutacion
    popmut=hacer_mutacion(pobcruc,Pmut)
    
    viajemut=[]
    
    for j in range(len(popmut)):
        if popmut[j] not in Totalpob:
            axd=Evaluar(popmut[j])
            viajemut.append(axd)
            Totalpob.append(popmut[j])
            Totaldis.append(axd)
        else:
            indice=Totalpob.index(popmut[j])
            viajemut.append(Totaldis[indice])
    for j in range(len(popmut)):
        if popmut[j] not in PobCompleta:
            PobCompleta.append(popmut[j])
            DisCompleta.append(viajemut[j])
    
    #hof
    bestindx=DisCompleta.index(min(DisCompleta))
    hof=PobCompleta[bestindx]
    
    s=Selection()
    selecindex=[]
    
    selecindex=s.RuletaSeleccion(DisCompleta, k=Pmax)
    poblacion=[]
    viajeld=[]
    
    for y in range(len(selecindex)):
        abcd=selecindex[y]
        poblacion.append(PobCompleta[abcd])
        viajeld.append(DisCompleta[abcd])
    
    if hof not in poblacion:
        ind50=random.randint(0, len(poblacion)-1)
        poblacion[ind50]=hof
        viajeld[ind50]=DisCompleta[bestindx]
      
    if pastelite==hof:
        cuenta+=1
    else:
        cuenta=0
        pastelite=copy.deepcopy(hof);
        print("ELITE ",hof)
        print(DisCompleta[bestindx])
    
    dato.append(DisCompleta[bestindx])
    
    print("Generacion: ",i," Mejor distancia:", min(DisCompleta), " Peor distancia:", max(DisCompleta))
    
    #para parar cuando no hay mejoras
    if cuenta==40:
        break
           
            

