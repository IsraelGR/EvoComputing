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
TAMANIO_POBLACION = 350
MEJORES_INDIVIDUOS = 20
PROBABILIDAD_MUTA = .01
PROBABILIDAD_CRUZA = .9
TAMANIO_GEN = 7
MATERIAS = 15
COMBINACIONES = 16
AGUILA = True
SOL = False

frecuencia = [
[2,[1,0,1,0,0]],
[2,[1,0,0,1,0]],
[2,[0,1,0,1,0]],
[2,[0,1,0,0,1]],
[2,[0,0,1,0,1]],
[3,[1,0,1,1,0]],
[3,[1,0,1,0,1]],
[3,[0,1,1,0,1]],
[3,[1,0,0,1,1]],
[3,[0,1,0,1,1]],
[4,[0,1,1,1,1]],
[4,[1,0,1,1,1]],
[4,[1,1,0,1,1]],
[4,[1,1,1,0,1]],
[4,[1,1,1,1,0]],
[5,[1,1,1,1,1]]]

asignaturas = [
["Calculo",5,3,2],
["Analisis Vectorial",6,4,1],
["Algebra Lineal",6,3,1.5],
["Ecuaciones Diferenciales",5,2,2.5],
["Computo Evolutivo",2,3,3],
["Analisis de Algoritmos",4,3,2],
["Estructura de Datos",4,2,2],
["Metodos Numericos",3,4,1.5],
["Sistemas Operativos",5,5,2.5],
["Algebra",1,2,3],
####################NUevas asignaturas
["Matematicas Discretas",4,3,3],
["Seniales",4,3,1.5],
["Bioinformatics",3,2,2],
["Cryptography",3,2,3],
["Ciberseguridad",5,3,2],
["Computer Graphics",2,3,1]]

def calculaCastigo(gen):
    castigo = 0
    for i in xrange(TAMANIO_GEN):
        if (frecuencia[gen[i+TAMANIO_GEN]%COMBINACIONES][0] > asignaturas[gen[i]][2]):
            cont_frec = gen[i+TAMANIO_GEN]%COMBINACIONES
            while(frecuencia[cont_frec][0] != asignaturas[gen[i]][2]):
                cont_frec -= 1
                castigo += 1

        elif (frecuencia[gen[i+TAMANIO_GEN]%COMBINACIONES][0] < asignaturas[gen[i]][2]):
            cont_frec = gen[i+TAMANIO_GEN]%COMBINACIONES
            while(frecuencia[cont_frec][0] != asignaturas[gen[i]][2]):
                cont_frec += 1
                castigo += 2

    return castigo/2



def funcionAptitud(gen):
    aptitud = 0
    for i in xrange(TAMANIO_GEN):
        aptitud += asignaturas[gen[i]%7][1]%16
    castigo = calculaCastigo(gen)
    aptitud = aptitud - castigo
    return aptitud


def creaGen():
    genotipo = []

    while(len(genotipo) != TAMANIO_GEN):
        asignature = numpy.random.randint(0,MATERIAS+1)
        if(asignature not in genotipo):
            genotipo.append(asignature)

    while(len(genotipo) != TAMANIO_GEN*2):
        days = numpy.random.randint(MATERIAS+1,MATERIAS+COMBINACIONES+1)
        if(days not in genotipo):
            genotipo.append(days)

    return genotipo


def imprimir(list):
    print "\n"
    for i in xrange(len(list)):
        print list[i]


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

def mio(padre, madre):
    hijo1 = padre
    hijo2 = madre

    tamanioPadres = len(padre)
    comienza = seleccionarPosicionAleatoria(TAMANIO_GEN)
    longitud = numpy.random.randint(0,TAMANIO_GEN)
    termina = longitud+comienza
    for aux in xrange(comienza,termina%TAMANIO_GEN):
        hijo1[aux],hijo2[aux] = madre[aux], padre[aux]

    comienza = numpy.random.randint(TAMANIO_GEN,tamanioPadres)
    longitud = numpy.random.randint(0,TAMANIO_GEN)
    termina = longitud+comienza
    for i in xrange(comienza, termina):
        hijo1[(i%TAMANIO_GEN)+TAMANIO_GEN], hijo2[(i%TAMANIO_GEN)+TAMANIO_GEN] = madre[(i%TAMANIO_GEN)+TAMANIO_GEN], padre[(i%TAMANIO_GEN)+TAMANIO_GEN]

    return padre, madre








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
        print dato
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
        #poblacion.individuos[i].esperanza = poblacion.individuos[i].esperanza = (1- poblacion.individuos[i].aptitud)/poblacion.media#Agrega la esperanza a c/ Individuo
        poblacion.individuos[i].esperanza = poblacion.individuos[i].aptitud/poblacion.media #Agrega la esperanza a c/ Individuo
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

    nuevoIndividuo.tamanio = TAMANIO_GEN*2
    nuevoIndividuo.gen = creaGen()
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
            genHijo1, genHijo2 = mio(poblacion.individuos[listaPadres[i]].gen, poblacion.individuos[listaPadres[i+1]].gen)
            #ordered_CrossOver, PMX, positionBased_CO
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


def mutacionUniforme(individuo, probabilidadMuta):

    for i in xrange(individuo.tamanio):
        r = numpy.random.uniform(0,1)

        if( r <= probabilidadMuta ):
            MutaPermxInt(individuo.gen)#-------------------------------------------------------------------------------------------------------------------WARNINGWARNINGWARNINGWARNINGWARNINGWARNINGWARNINGWARNINGWARNINGWARNINGWARNINGWARNINGWARNINGWARNING


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
            print Elite.individuos[i].gen, Elite.individuos[i].aptitud



def main():
    #algoritmoGeneticoSimple(NUMERO_GENERACIONES, PROBABILIDAD_CRUZA, PROBABILIDAD_MUTA, MEJORES_INDIVIDUOS)
    gen = [6, 6, 8, 3, 9, 14, 15, 16, 19, 31, 29, 22, 30, 25]
    for i in xrange(7):
        print asignaturas[gen[i]]
        print frecuencia[gen[i+7]%7]#'''










main()
