import sys
import numpy
import math

SOLUCION = [137,76,53]
C = 0.83
NUMERO_GENERACIONES = 1000
NUMERO_VARIABLES = 3
GEN_AUTO = 10
limites = 255


def generarSolucionAleatorio(n_variables, limites):
    genoma = []
    for i in xrange(n_variables):
        genoma.append(numpy.random.randint(0,limites+1))
    return genoma

def calcularAptitud(gen):
    aptitud = []
    total = 0
    for i in xrange(len(gen)):
        aptitud.append(math.sqrt(pow((SOLUCION[i]-gen[i]),2)))
        #total += aptitud[i]
    #aptitud.append(total)
    return aptitud

def crearPerturbacion(n_variables, media, varianza):
    #(loc=0.0, scale=1.0, size=None) # loc es la media, scale la desviacion estandar # size es un un valor entero deseado de valores a regresar
    perturbacion = numpy.random.normal(media, varianza, n_variables)
    return perturbacion

def validarRestricciones(gen):
    x_prima = []
    for i in xrange(len(gen)):
        if (gen[i] > 256):
            x_prima.append(gen[i]%256)
        else:
            x_prima.append(0)

    return x_prima

def suma(gen, perturbacion):
    newGen = []
    for i in xrange(len(perturbacion)):
        newGen.append(gen[i]+perturbacion[i])
    return newGen


def estrategiaEvolutiva1_1(generaciones, gene_auto, n_variables):
    media = 0
    varianza = 1
    exito = 0.0
    generacion = 0

    x = generarSolucionAleatorio(n_variables,limites)
    fx = calcularAptitud(x)

    while(generacion<generaciones ):#and fx[n_variables]!=0):

        Dx = crearPerturbacion(n_variables, media, varianza)
        x_1 = suma(x,Dx)
        penalizar = validarRestricciones(x_1)
        fx_1 = suma(calcularAptitud(x_1),penalizar)

        for i in xrange(n_variables):
            if(fx_1[i] < fx[i]):
                x[i] = x_1[i]
                fx[i] = fx_1[i]
                exito = exito + (1.0/n_variables)

        if((generacion % gene_auto) == 0):
            if((exito/gene_auto) < (1.0/5)):
                varianza = varianza*C

            elif((exito/gene_auto) > (1.0/5)):
                varianza = varianza/C

            print "\nGeneracion Actual", generacion
            print [round(elem) for elem in x]
            print [round(elem) for elem in fx]      
            exito = 0.0

        generacion = generacion + 1

estrategiaEvolutiva1_1(NUMERO_GENERACIONES,GEN_AUTO, NUMERO_VARIABLES)
# I took a pill in ibiza
