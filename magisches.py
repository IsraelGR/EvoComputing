import sys
import numpy
import struct
import math

def creaHijo(tamanio):
    return [-1]*tamanio


def clonar(padre):
    clonPadre = padre
    return clonPadre


def seleccionarPosicionAleatoria(tamanio):
    return numpy.random.randint(tamanio)


def cruza1Punto(padre, madre):
    t = len(padre)
    i = seleccionarPosicionAleatoria(t)
    hijo1 = creaHijo(t)
    hijo2 = creaHijo(t)

    hijo1[0:i] = padre[0:i]
    hijo2[0:i] = madre[0:i]
    hijo1[i:t] = madre[i:t]
    hijo2[i:t] = padre[i:t]

    return hijo1, hijo2


def cruza2Punto(padre, madre):
    t = len(padre)
    i = seleccionarPosicionAleatoria(t)
    j= seleccionarPosicionAleatoria(t)
    hijo1 = creaHijo(t)
    hijo2 = creaHijo(t)

    if(i > j):
        i, j = j, i


    hijo1[0:i] = padre[0:i]
    hijo2[0:i] = madre[0:i]
    hijo1[i:j] = madre[i:j]
    hijo2[i:j] = padre[i:j]
    hijo1[j:t] = padre[j:t]
    hijo2[j:t] = madre[j:t]

    return hijo1, hijo2


def cruzaUniforme(padre, madre):
    t = len(padre)
    hijo1 = creaHijo(t)
    hijo2 = creaHijo(t)

    for i in xrange(t):
        a = numpy.random.uniform(0,1)
        if(a > 0.5):
            hijo1[i] = padre[i]
        else:
            hijo1[i] = madre[i]

        a = numpy.random.uniform(0,1)
        if(a > 0.5):
            hijo2[i] = padre[i]
        else:
            hijo2[i] = madre[i]

    return hijo1, hijo2


def cruzaAcentuada(padre, madre, d): #d es el numero de alelos a cambiar
    t = len(padre)
    hijo1 = clonar(padre)
    hijo2 = clonar(madre)

    for i in xrange(d):
        p = seleccionarPosicionAleatoria(t)
        hijo1[p] = madre[p]

        p = seleccionarPosicionAleatoria(t)
        hijo2[p] = padre[p]

    return hijo1, hijo2

###################################################################################
NUMERO_GENERACIONES = 156
TAMANIO_CUADRADO = 3
TAMANIO_POBLACION = 36
MEJORES_INDIVIDUOS = 5
PROBABILIDAD_MUTA = .01
PROBABILIDAD_CRUZA = .9
AGUILA = True
SOL = False


def funcionAptitud(gen):
    return


def creaGen(tamanio):
    cuadrado = pow(tamanio,2)
    genotipo = []
    option = numpy.random.randint(0,3)

    for i in xrange(cuadrado):
        if option == 0:
            genotipo.append(i+1)
        elif option == 1:
            genotipo.append(pow(tamanio,2)-i)
        elif option == 2:
            genotipo.append(i+1)
            numpy.random.shuffle(genotipo)

    return genotipo


def ordered_CrossOver(padre, madre):
    tamanioPadre = len(padre)

    comienza = seleccionarPosicionAleatoria(tamanioPadre)
    longitud = numpy.random.randint(0,tamanioPadre+1) + comienza
    hijo1 = creaHijo(tamanioPadre)
    for i in range(comienza,longitud):
        hijo1[i%tamanioPadre] = padre[i%tamanioPadre]

    comienza = seleccionarPosicionAleatoria(tamanioPadre)
    longitud = numpy.random.randint(0,tamanioPadre+1) + comienza
    hijo2 = creaHijo(tamanioPadre)
    for i in range(comienza,longitud):
        hijo2[i%tamanioPadre] = madre[i%tamanioPadre]

    for i in xrange(tamanioPadre):
        if( madre[i] not in hijo1 ):
            hijo1[hijo1.index(-1)] = madre[i]

        if( padre[i] not in hijo2 ):
            hijo2[hijo2.index(-1)] = padre[i]

    return hijo1,hijo2


def PMX(padre, madre):
    tamanioPadres = len(padre)

    #Mapea las posiciones elegidas de los padres a los hijos
    comienza = seleccionarPosicionAleatoria(tamanioPadres)
    longitud = numpy.random.randint(0,tamanioPadres+1)
    termina = longitud+comienza
    hijo1 = creaHijo(tamanioPadres)
    print comienza, longitud
    for i in range(comienza,termina):
        hijo1[i%tamanioPadres] = madre[i%tamanioPadres]

    hijo2 = creaHijo(tamanioPadres)
    comienza = seleccionarPosicionAleatoria(tamanioPadres)
    termina = longitud+comienza
    print comienza, longitud
    for i in range(comienza, termina):
        hijo2[i%tamanioPadres] = padre[i%tamanioPadres]

    print hijo1, hijo2

    for i in xrange(tamanioPadres):
        if((padre[i] not in hijo1)and(hijo1[i] == -1)):
            hijo1[i] = padre[i]
        if((madre[i] not in hijo2)and(hijo2[i] == -1)):
            hijo2[i] = madre[i]


    return hijo1, hijo2










def calcularPM(cromosoma):
    return 1.0/len(cromosoma)


def calcularMedia(poblacion):
    sumaAptitudes = 0

    for i in xrange(poblacion.tamanio):
        sumaAptitudes += poblacion.individuos[i].aptitud

    return (1.0/poblacion.tamanio)*sumaAptitudes


def calcularEsperanza(poblacion):
    poblacion.esperanzas = [] # Para limpiar esperanzas antes calculadas
    for i in xrange(poblacion.tamanio):
        poblacion.individuos[i].esperanza = (1- poblacion.individuos[i].aptitud)/poblacion.media #Agrega la esperanza a c/ Individuo
        #poblacion.individuos[i].esperanza = poblacion.individuos[i].aptitud/poblacion.media #Agrega la esperanza a c/ Individuo
        poblacion.esperanzas.append(poblacion.individuos[i].esperanza) #Agrega las esperanzas de los individuos a la lista de la poblacion


def calcularDatos(poblacion):
    poblacion.tamanio = len(poblacion.individuos)

    for i in xrange(poblacion.tamanio):
        poblacion.individuos[i].aptitud = funcionAptitud(poblacion.individuos[i].gen)
        poblacion.individuos[i].tamanio = len(poblacion.individuos[i].gen)

    poblacion.media = calcularMedia(poblacion)
    calcularEsperanza(poblacion)


class Individuo(): #Tiene tamanio,gen,aptitud,esperanza
    tamanio = 0
    gen = []
    aptitud = 0.0
    esperanza = 0.0


def creaIndividuo():
    nuevoIndividuo = Individuo()

    nuevoIndividuo.tamanio = TAMANIO_GENOMA
    nuevoIndividuo.gen = creaGen(nuevoIndividuo.tamanio)
    nuevoIndividuo.aptitud = funcionAptitud(nuevoIndividuo.gen)

    return nuevoIndividuo


def add_Individuo(lista_individuos, individuo):
    lista_individuos.append(individuo)


class Poblacion(): #Tiene individuos, tamanio, media, esperanzas
    individuos = []
    tamanio = 0
    media = 0.0
    esperanzas = []


def borraDatos(poblacion):
    poblacion.individuos = []
    tamanio = 0
    poblacion.media = 0.0
    poblacion.esperanzas = []


def creaPoblacion():
    nuevaPoblacion = Poblacion()
    borraDatos(nuevaPoblacion)

    for i in xrange(TAMANIO_POBLACION):
        add_Individuo(nuevaPoblacion.individuos, creaIndividuo())

    nuevaPoblacion.tamanio = TAMANIO_POBLACION
    nuevaPoblacion.media = calcularMedia(nuevaPoblacion)

    return nuevaPoblacion


#Agregar lista de aptitudes a la poblacion
def seleccionRuleta(poblacion):
    r = numpy.random.uniform(0, poblacion.tamanio)
    SumEsp = 0
    i = 0

    while i <= poblacion.tamanio:
        SumEsp += poblacion.esperanzas[i]

        if(SumEsp > r):
            return i
        i += 1

    return i-1


def mantiza(numero):
    return numero % 1


def mantizas(vector):
    for i in xrange(len(vector)):
        vector[i] = vector[i] % 1


def volado(numero):
    r = numpy.random.uniform(0,1)

    if(r < numero):
        return AGUILA
    return SOL


def sobranteEstocasticoSR(poblacion):
    listaPadres = []

    for i in xrange(poblacion.tamanio):
        if( poblacion.esperanzas[i] >= 1):
            listaPadres.append(i)

    i=0

    while (len(listaPadres) < poblacion.tamanio):
        if (volado(mantiza(poblacion.esperanzas[i%poblacion.tamanio])) == AGUILA):
            listaPadres.append(i%poblacion.tamanio)

        i += 1

    return listaPadres


def sobranteEstocasticoCR(poblacion, listaPadres):#NO se tiene que calcular esperanza antes de usar este
    if len(listaPadres) == poblacion.tamanio:
        return

    else:
        calcularEsperanza(poblacion)

        for i in xrange(poblacion.tamanio):
            if ( (poblacion.esperanzas[i] >= 1) and (len(listaPadres) < poblacion.tamanio) ):
                listaPadres.append(i)

        mantizas(poblacion.esperanzas)

        for i in xrange(poblacion.tamanio):
            poblacion.individuos[i].aptitud = poblacion.esperanzas[i]


        poblacion.media = calcularMedia(poblacion)
        sobranteEstocasticoCR(poblacion,listaPadres)

    #Se vuelven a calcular los datos ya que se modificaron al hacer uso de ellos anteriormente
    calcularDatos(poblacion)
    return


def creaIndividuoGen(genoma):
    nuevoIndividuo = Individuo()

    nuevoIndividuo.tamanio = len(genoma)
    nuevoIndividuo.gen = genoma
    nuevoIndividuo.aptitud = funcionAptitud(nuevoIndividuo.gen)

    return nuevoIndividuo


def cruzaPadres(poblacion, listaPadres, probabilidadCruza):
    nuevaPoblacion = Poblacion()
    borraDatos(nuevaPoblacion)

    for i in range(0,poblacion.tamanio,2):
        if volado( probabilidadCruza ) == AGUILA:
            genHijo1, genHijo2 = cruza1Punto(poblacion.individuos[listaPadres[i]].gen, poblacion.individuos[listaPadres[i+1]].gen)
            #curza1 punto, 2 puntos, uniforme y acentuada

            hijo1 = creaIndividuoGen(genHijo1)
            hijo2 = creaIndividuoGen(genHijo2)

        else:
            hijo1 = clonar(poblacion.individuos[listaPadres[i]])
            hijo2 = clonar(poblacion.individuos[listaPadres[i+1]])

        add_Individuo(nuevaPoblacion.individuos, hijo1)
        add_Individuo(nuevaPoblacion.individuos, hijo2)


    calcularDatos(nuevaPoblacion)

    return nuevaPoblacion


def seleccionarPadres(poblacion):
    listaPadres = []

    for i in xrange(poblacion.tamanio):
        add_Individuo(listaPadres, seleccionRuleta(poblacion))

    return listaPadres


def mutacionUniforme(individuo, porcentajeMutacion):

    for i in xrange(individuo.tamanio):
        r = numpy.random.uniform(0,1)

        if( r <= calcularPM(individuo.gen) ):
            individuo.gen[i] = int(not(individuo.gen[i]))


def mutarPoblacion(poblacion, probabilidadMuta):
    for i in xrange(poblacion.tamanio):
        mutacionUniforme(poblacion.individuos[i],probabilidadMuta)

    calcularDatos(poblacion)


def ordenar(poblacion):
    mejores = sorted(poblacion.esperanzas, reverse=True)
    listaMejores=[]

    for i in xrange(len(poblacion.esperanzas)):
        listaMejores.append(poblacion.esperanzas.index(mejores[i]))
        poblacion.esperanzas[poblacion.esperanzas.index(mejores[i])] = 0

    calcularEsperanza(poblacion)
    return listaMejores


def seleccionMejor(mejoresIndividuos, Elite=Poblacion()):
    if not len(Elite.individuos):
        ordenados = ordenar(mejoresIndividuos)
        borraDatos(Elite)
        for i in xrange(mejoresIndividuos.tamanio):
            add_Individuo(Elite.individuos, mejoresIndividuos.individuos[ordenados[i]])

    else:
        for i in xrange(mejoresIndividuos.tamanio):
            if( mejoresIndividuos.individuos[i].aptitud >= Elite.individuos[i].aptitud ):
                Elite.individuos[i] = mejoresIndividuos.individuos[i]

    return Elite


def elitismo(poblacion, numeroMejoresIndividuos, mejoresIndividuos=Poblacion()):
    if numeroMejoresIndividuos > poblacion.tamanio:
        print "No se pueden elegir mas mejores individuos que la poblacion"
        exit(1)

    ordenados = ordenar(poblacion)

    if not len(mejoresIndividuos.individuos):
        borraDatos(mejoresIndividuos)
        for i in xrange(numeroMejoresIndividuos):
            add_Individuo(mejoresIndividuos.individuos, poblacion.individuos[ordenados[i]])

        calcularDatos(mejoresIndividuos)
        return mejoresIndividuos

    else:
        dataEsperanzas = poblacion.esperanzas + mejoresIndividuos.esperanzas

        nuevosMejores = Poblacion()
        borraDatos(nuevosMejores)

        nuevosMejores.esperanzas = dataEsperanzas
        mejoresOrdenados =  ordenar(nuevosMejores)
        nuevosMejores.esperanzas = poblacion.esperanzas + mejoresIndividuos.esperanzas

        for j in xrange(numeroMejoresIndividuos): #Cuantos mejores individuos quiero tomar, cuantos guardare
            for i in xrange(poblacion.tamanio): #Cuantos individuos quiero comparar  si solo los primeros 3 o 2, etc
                if nuevosMejores.esperanzas[mejoresOrdenados[j]] == poblacion.esperanzas[i]:
                    add_Individuo(nuevosMejores.individuos, poblacion.individuos[i])
                    break

            for i in xrange(mejoresIndividuos.tamanio):
                if nuevosMejores.esperanzas[mejoresOrdenados[j]] == mejoresIndividuos.esperanzas[i]:
                    add_Individuo(nuevosMejores.individuos, mejoresIndividuos.individuos[i])
                    break

        if( len(nuevosMejores.individuos) > numeroMejoresIndividuos ):
            for i in xrange(len(nuevosMejores.individuos)-numeroMejoresIndividuos):
                nuevosMejores.individuos.pop()

        calcularDatos(nuevosMejores)

        return nuevosMejores



def algoritmoGeneticoSimple(numeroGeneraciones, porcentajeCruza, porcentajeMutacion, numeroMejoresIndividuos):
    generacionActual = 0
    poblacion = creaPoblacion()
    calcularEsperanza(poblacion)
    Elite = Individuo()

    mejoresIndividuos = elitismo(poblacion, numeroMejoresIndividuos)
    calcularDatos(mejoresIndividuos)
    listaPadres = []
    while( generacionActual < numeroGeneraciones ):
        print "\nGeneracion Actual: ", generacionActual

        #listaPadres = seleccionarPadres(poblacion)
        listaPadres = sobranteEstocasticoSR(poblacion)
        #sobranteEstocasticoCR(poblacion,listaPadres)
        nuevaPoblacion = cruzaPadres(poblacion, listaPadres, porcentajeCruza)
        mutarPoblacion(nuevaPoblacion, porcentajeMutacion)
        calcularDatos(nuevaPoblacion)

        mejoresIndividuos = elitismo(nuevaPoblacion, numeroMejoresIndividuos, mejoresIndividuos)

        Elite = seleccionMejor(mejoresIndividuos)

        poblacion = creaPoblacion()
        calcularEsperanza(poblacion)

        poblacion = seleccionMejor(poblacion,nuevaPoblacion)#elitismo(poblacion, TAMANIO_POBLACION ,nuevaPoblacion)
        generacionActual += 1


        #for i in xrange(mejoresIndividuos.tamanio):
        #    print "Genoma = ",Elite.individuos[i].gen, "| Aptitud = ",Elite.individuos[i].aptitud
    for i in xrange(MEJORES_INDIVIDUOS):
        x1, x2, x3, x4 = praxis_2_5(Elite.individuos[i].gen)
        print Elite.individuos[i].aptitud*(-1), "\t|",x1,"\t\t|",x2,"\t\t|",x3,"\t\t|",x4
    """for i in xrange(MEJORES_INDIVIDUOS):
        x1,x2 = praxis_3_4_7(Elite.individuos[i].gen)
        print Elite.individuos[i].aptitud*(-1), "\t|",x1,"\t\t|",x2"""



def main():
    #algoritmoGeneticoSimple(NUMERO_GENERACIONES, PROBABILIDAD_CRUZA, PROBABILIDAD_MUTA, MEJORES_INDIVIDUOS)
    padre = [1,3,5,7,9,2,4,6,8]
    madre = [1,2,3,4,5,6,7,8,9]
    print padre, madre
    print PMX(padre, madre)

main()
