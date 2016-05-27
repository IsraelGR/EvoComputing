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

###################################################################################
NUMERO_GENERACIONES = 9600
TAMANIO_CUADRADO = 5
TAMANIO_POBLACION = 350
MEJORES_INDIVIDUOS = 20
PROBABILIDAD_MUTA = .01
PROBABILIDAD_CRUZA = .9
AGUILA = True
SOL = False


def funcionAptitud(gen):
    Sn = (TAMANIO_CUADRADO*(pow(TAMANIO_CUADRADO,2)+1))/2
    Matriz = calculaVectores(gen)
    aptitud = 0
    for vectores in xrange(2*(TAMANIO_CUADRADO+1)):
        aptitud += pow( (Sn - Matriz[vectores]) ,2)
        #aptitud += abs(Sn - Matriz[vectores])*2
    return aptitud


def calculaVectores(gen):
    #Variables que guardaran la suma de cada vecto
    Horizontal = [0]*TAMANIO_CUADRADO
    Vertical = [0]*TAMANIO_CUADRADO
    Diagonal_D = [0]
    Diagonal_I = [0]

    #Suma de los vectores
    for linea in xrange(TAMANIO_CUADRADO):
        Diagonal_I[0] += gen[linea * (TAMANIO_CUADRADO+1)]
        Diagonal_D[0] += gen[(linea+1) * (TAMANIO_CUADRADO-1)]
        for contador in xrange(TAMANIO_CUADRADO):
            Horizontal[linea] += gen[contador + (linea*TAMANIO_CUADRADO)]
            Vertical[linea] += gen[linea + (contador*TAMANIO_CUADRADO)]

    return Horizontal+Vertical+Diagonal_I+Diagonal_D


def creaGen():
    genotipo = []

    while(len(genotipo) != 7):
        asignature = numpy.random.randint(1,16)
        if(asignature not in genotipo):
            genotipo.append(asignature)

    while(len(genotipo) != 14):
        days = numpy.random.randint(16,33)
        if(days not in genotipo):
            genotipo.append(days)

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
    for i in range(comienza,termina):
        hijo1[i%tamanioPadres] = madre[i%tamanioPadres]

    hijo2 = creaHijo(tamanioPadres)
    comienza = seleccionarPosicionAleatoria(tamanioPadres)
    termina = longitud+comienza
    for i in range(comienza, termina):
        hijo2[i%tamanioPadres] = padre[i%tamanioPadres]

    #Mapea los datos de los padres a los hijos excepto los valores del mapeo anterior
    noEstadoH1 = []
    noEstadoH2 = []
    for i in xrange(tamanioPadres):
        if((padre[i] not in hijo1)and(hijo1[i] == -1)):
            hijo1[i] = padre[i]
        if((madre[i] not in hijo2)and(hijo2[i] == -1)):
            hijo2[i] = madre[i]
        #Guardamos el indice para despues hacer un shuffle y poner los valores en estos lugares
        if( hijo1[i] == -1 ):
            noEstadoH1.append(i)
        if( hijo2[i] == -1 ):
            noEstadoH2.append(i)

    #Acomodamos los numeros restantes en las posiciones vacias y de manera aleatoria
    numpy.random.shuffle(noEstadoH1)
    numpy.random.shuffle(noEstadoH2)
    posi1 = 0
    posi2 = 0

    for dato in range(1,tamanioPadres+1):
        if(dato not in hijo1)and(posi1 <= len(noEstadoH1)):
            hijo1[noEstadoH1[posi1]] = dato
            posi1 += 1
        if(dato not in hijo2)and(posi2 <= len(noEstadoH2)):
            hijo2[noEstadoH2[posi2]] = dato
            posi2 += 1

    return hijo1, hijo2


def positionBased_CO(padre, madre):
    tamanioPadres = len(padre)
    tam_conjunto = numpy.random.randint(1,tamanioPadres+1) #Tamanio del conjunto a agarrar
    posiciones1 = []
    posiciones2 = []
    hijo1 = creaHijo(tamanioPadres)
    hijo2 = creaHijo(tamanioPadres)

    #Guardo las posiciones en las que se va a mapear los datos
    for i in range(0,tam_conjunto):
        dato1 = seleccionarPosicionAleatoria(tam_conjunto)
        dato2 = seleccionarPosicionAleatoria(tam_conjunto)
        if( dato1 not in posiciones1 ):
            posiciones1.append(dato1)
        if( dato2 not in posiciones2 ):
            posiciones2.append(dato2)
    #Se mapean los datos del arreglo posiciones de padre
    for i in xrange(len(posiciones1)):
        hijo1[posiciones1[i]] = padre[posiciones1[i]]
    for i in xrange(len(posiciones2)):
        hijo2[posiciones2[i]] = madre[posiciones2[i]]


    #Se llena el gen con los datos faltantes de madre
    for i in xrange(tamanioPadres):
        if( madre[i] not in hijo1 ):
            hijo1[hijo1.index(-1)] = madre[i]
        if( padre[i] not in hijo2 ):
            hijo2[hijo2.index(-1)] = padre[i]


    return hijo1, hijo2


def MutaPermxInt(genoma):
    if(volado(PROBABILIDAD_MUTA)):
        posocion1 = numpy.random.randint(0,len(genoma))
        posocion2 = numpy.random.randint(0,len(genoma))
        genoma[posocion1], genoma[posocion2] = genoma[posocion2], genoma[posocion1]


def calcularPM(cromosoma):
    return 1.0/len(cromosoma)


def calcularMedia(poblacion):
    sumaAptitudes = 0

    for i in xrange(poblacion.tamanio):
        sumaAptitudes += poblacion.individuos[i].aptitud

    return (1.0/poblacion.tamanio)*sumaAptitudes


def calcularEsperanza(poblacion): #Para maximizacion poblacion.individuos[i].esperanza = (poblacion.individuos[i].aptitud)/poblacion.media
    poblacion.esperanzas = [] # Para limpiar esperanzas antes calculadas
    for i in xrange(poblacion.tamanio):
        poblacion.individuos[i].esperanza = poblacion.individuos[i].esperanza = (1- poblacion.individuos[i].aptitud)/poblacion.media#Agrega la esperanza a c/ Individuo
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
    aptitud = 0
    esperanza = 0.0


def creaIndividuo():
    nuevoIndividuo = Individuo()

    nuevoIndividuo.tamanio = pow(TAMANIO_CUADRADO,2)
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

    while i < poblacion.tamanio:
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

#Seleccion de padres
def sobranteEstocasticoSR(poblacion):
    listaPadres = []

    for i in xrange(poblacion.tamanio):
        if( poblacion.esperanzas[i] >= 1 ):
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
            genHijo1, genHijo2 = ordered_CrossOver(poblacion.individuos[listaPadres[i]].gen, poblacion.individuos[listaPadres[i+1]].gen)
            #ordered_CrossOver, PMX, positionBased_CO
            hijo1 = creaIndividuoGen(genHijo1)
            hijo2 = creaIndividuoGen(genHijo2)

        else:
            #hijo1 = clonar(poblacion.individuos[listaPadres[i]])
            #hijo2 = clonar(poblacion.individuos[listaPadres[i+1]])
            genHijo1, genHijo2 = PMX(poblacion.individuos[listaPadres[i]].gen, poblacion.individuos[listaPadres[i+1]].gen)
            hijo1 = creaIndividuoGen(genHijo1)
            hijo2 = creaIndividuoGen(genHijo2)


        add_Individuo(nuevaPoblacion.individuos, hijo1)
        add_Individuo(nuevaPoblacion.individuos, hijo2)


    calcularDatos(nuevaPoblacion)

    return nuevaPoblacion


def seleccionarPadres(poblacion):
    listaPadres = []

    for i in xrange(poblacion.tamanio):
        add_Individuo(listaPadres, seleccionRuleta(poblacion))

    return listaPadres


def mutacionUniforme(individuo, probabilidadMuta):

    for i in xrange(individuo.tamanio):
        r = numpy.random.uniform(0,1)

        if( r <= probabilidadMuta ):
            MutaPermxInt(individuo.gen)


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
            if( mejoresIndividuos.individuos[i].aptitud <= Elite.individuos[i].aptitud ):
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
    while( 1 ):
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
            print Elite.individuos[i].gen, Elite.individuos[i].aptitud, calculaVectores(Elite.individuos[i].gen)
        if( Elite.individuos[0].aptitud == 0):
            break



def main():
    #algoritmoGeneticoSimple(NUMERO_GENERACIONES, PROBABILIDAD_CRUZA, PROBABILIDAD_MUTA, MEJORES_INDIVIDUOS)
    print creaGen()




main()
