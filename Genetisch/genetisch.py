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
NUMERO_GENERACIONES = 15630
TAMANIO_GENOMA = 100
TAMANIO_POBLACION = 36
MEJORES_INDIVIDUOS = 5
PROBABILIDAD_MUTA = .01
PROBABILIDAD_CRUZA = .9
AGUILA = True
SOL = False



def intTObin(integer):
    binario = bin(integer).replace('0b','').replace('-','')
    if (integer < 0):
        return '1'+binario
    return '0'+binario


def binTOint(listGen):
    binario = ''.join(str(e) for e in listGen)

    if (int(binario[0]) == 1):
        binario = binario[:0] + binario[(0+1):]
        return int(binario, 2)*-1
    return int(binario,2)


def praxis_1(gen):
    ###################-----EJERCICIO_1-----########### 18 Cada X 18mil generaciones
    entero1 = gen[0:8]
    genoma1 =  ''.join(str(x) for x in entero1)
    decimal1 = gen[8:18]

    entero2 = gen[18:26]
    genoma2 =  ''.join(str(x) for x in entero2)
    decimal2 = gen[26:36]

    ent1 = binTOint(genoma1)
    dec1 = 0.0
    ent2 = binTOint(genoma2)
    dec2 = 0.0

    for i in range(1,11):
        if( decimal1[i-1] == 1 ):
            dec1 += 1.0/pow(2,i)

    for i in range(1,11):
        if( decimal2[i-1] == 1 ):
            dec2 += 1.0/pow(2,i)

    if( ent1<0 ):
        x1 = ent1-dec1
    else:
        x1 = ent1+dec1
    if( ent2<0 ):
        x2 = ent2-dec2
    else:
        x2 = ent2+dec2

    if((x1<-65.536) or (x1>65.536)):
        x1 = x1*99999999
    if((x2<-65.536) or (x2>65.536)):
        x2 = x2*99999999

    return x1,x2


def praxis_2_5(gen):
    ###################-----EJERCICIO_2_5-----########### 15 Cada x 12mil | de 15 Cada x 9 - 6
    entero1 = gen[0:10]
    genoma1 =  ''.join(str(x) for x in entero1)
    decimal1 = gen[10:11]

    entero2 = gen[11:21]
    genoma2 =  ''.join(str(x) for x in entero2)
    decimal2 = gen[21:22]

    entero3 = gen[22:32]
    genoma3 =  ''.join(str(x) for x in entero3)
    decimal3 = gen[32:33]

    entero4 = gen[33:43]
    genoma4 =  ''.join(str(x) for x in entero4)
    decimal4 = gen[43:44]

    ent1 = binTOint(genoma1)
    dec1 = 0.0
    ent2 = binTOint(genoma2)
    dec2 = 0.0
    ent3 = binTOint(genoma3)
    dec3 = 0.0
    ent4 = binTOint(genoma4)
    dec4 = 0.0

    for i in range(1,len(decimal1)):
        if( decimal1[i-1] == 1 ):
            dec1 += 1.0/pow(2,i)

    for i in range(1,len(decimal2)):
        if( decimal2[i-1] == 1 ):
            dec2 += 1.0/pow(2,i)

    for i in range(1,len(decimal3)):
        if( decimal3[i-1] == 1 ):
            dec3 += 1.0/pow(2,i)

    for i in range(1,len(decimal4)):
        if( decimal4[i-1] == 1 ):
            dec4 += 1.0/pow(2,i)

    if( ent1<0 ):
        x1 = ent1-dec1
    else:
        x1 = ent1+dec1
    if( ent2<0 ):
        x2 = ent2-dec2
    else:
        x2 = ent2+dec2
    if( ent3<0 ):
        x3 = ent3-dec3
    else:
        x3 = ent3+dec3
    if( ent4<0 ):
        x4 = ent4-dec4
    else:
        x4 = ent4+dec4

    if((x1<-500) or (x1>500)):
        x1 = x1%501
    if((x2<-500) or (x2>500)):
        x2 = x2%501
    if((x3<-500) or (x3>500)):
        x3 = x3%501
    if((x4<-500) or (x4>500)):
        x4 = x4%501

    return x1,x2,x3,x4


def praxis_3_4_7(gen):
    ###################-----EJERCICIO_3_y_4-----########### 18 Cada X
    entero1 = gen[0:5]
    genoma1 =  ''.join(str(x) for x in entero1)
    decimal1 = gen[5:10]

    entero2 = gen[10:15]
    genoma2 =  ''.join(str(x) for x in entero2)
    decimal2 = gen[15:20]

    ent1 = binTOint(genoma1)
    dec1 = 0.0
    ent2 = binTOint(genoma2)
    dec2 = 0.0

    for i in range(1,len(decimal1)):
        if( decimal1[i-1] == 1 ):
            dec1 += 1.0/pow(2,i)

    for i in range(1,len(decimal2)):
        if( decimal2[i-1] == 1 ):
            dec2 += 1.0/pow(2,i)

    if( ent1<0 ):
        x1 = ent1-dec1
    else:
        x1 = ent1+dec1
    if( ent2<0 ):
        x2 = ent2-dec2
    else:
        x2 = ent2+dec2

    if((x1<-10) or (x1>10)):
        x1 = x1*99
    if((x2<-10) or (x2>10)):
        x2 = x2*99

    return x1,x2


def letzter(gen):
    ###################-----EJERCICIO_2_5-----########### 11 Cada x
    entero1 = gen[0:6]
    genoma1 =  ''.join(str(x) for x in entero1)
    decimal1 = gen[6:15]

    entero2 = gen[15:21]
    genoma2 =  ''.join(str(x) for x in entero2)
    decimal2 = gen[21:30]

    entero3 = gen[30:36]
    genoma3 =  ''.join(str(x) for x in entero3)
    decimal3 = gen[36:45]

    entero4 = gen[45:51]
    genoma4 =  ''.join(str(x) for x in entero4)
    decimal4 = gen[51:60]

    entero5 = gen[60:66]
    genoma5 =  ''.join(str(x) for x in entero4)
    decimal5 = gen[66:75]

    ent1 = binTOint(genoma1)
    dec1 = 0.0
    ent2 = binTOint(genoma2)
    dec2 = 0.0
    ent3 = binTOint(genoma3)
    dec3 = 0.0
    ent4 = binTOint(genoma4)
    dec4 = 0.0
    ent5 = binTOint(genoma4)
    dec5 = 0.0

    for i in range(1,len(decimal1)):
        if( decimal1[i-1] == 1 ):
            dec1 += 1.0/pow(2,i)

    for i in range(1,len(decimal2)):
        if( decimal2[i-1] == 1 ):
            dec2 += 1.0/pow(2,i)

    for i in range(1,len(decimal3)):
        if( decimal3[i-1] == 1 ):
            dec3 += 1.0/pow(2,i)

    for i in range(1,len(decimal4)):
        if( decimal4[i-1] == 1 ):
            dec4 += 1.0/pow(2,i)

    for i in range(1,len(decimal5)):
        if( decimal5[i-1] == 1 ):
            dec5 += 1.0/pow(2,i)

    if( ent1<0 ):
        x1 = ent1-dec1
    else:
        x1 = ent1+dec1
    if( ent2<0 ):
        x2 = ent2-dec2
    else:
        x2 = ent2+dec2
    if( ent3<0 ):
        x3 = ent3-dec3
    else:
        x3 = ent3+dec3
    if( ent4<0 ):
        x4 = ent4-dec4
    else:
        x4 = ent4+dec4
    if( ent4<0 ):
        x5 = ent5-dec5
    else:
        x5 = ent5+dec5

    if((x1<1) or (x1>60)):
        x1 = x1%61
    if((x2<1) or (x2>60)):
        x2 = x2%61
    if((x3<1) or (x3>60)):
        x3 = x3%61
    if((x4<1) or (x4>60)):
        x4 = x4%61
    if((x5<1) or (x5>60)):
        x5 = x5%61

    return x1,x2,x3,x4,x5


def praxis_6(gen):

    entero1 = gen[0:4]
    genoma1 =  ''.join(str(x) for x in entero1)
    decimal1 = gen[4:5]

    entero2 = gen[5:9]
    genoma2 =  ''.join(str(x) for x in entero2)
    decimal2 = gen[9:10]

    entero3 = gen[10:14]
    genoma3 =  ''.join(str(x) for x in entero3)
    decimal3 = gen[14:15]

    entero4 = gen[15:19]
    genoma4 =  ''.join(str(x) for x in entero4)
    decimal4 = gen[19:20]

    ent1 = binTOint(genoma1)
    dec1 = 0.0
    ent2 = binTOint(genoma2)
    dec2 = 0.0
    ent3 = binTOint(genoma3)
    dec3 = 0.0
    ent4 = binTOint(genoma4)
    dec4 = 0.0

    for i in range(1,len(decimal1)):
        if( decimal1[i-1] == 1 ):
            dec1 += 1.0/pow(2,i)

    for i in range(1,len(decimal2)):
        if( decimal2[i-1] == 1 ):
            dec2 += 1.0/pow(2,i)

    for i in range(1,len(decimal3)):
        if( decimal3[i-1] == 1 ):
            dec3 += 1.0/pow(2,i)

    for i in range(1,len(decimal4)):
        if( decimal4[i-1] == 1 ):
            dec4 += 1.0/pow(2,i)

    if( ent1<0 ):
        x1 = ent1-dec1
    else:
        x1 = ent1+dec1
    if( ent2<0 ):
        x2 = ent2-dec2
    else:
        x2 = ent2+dec2
    if( ent3<0 ):
        x3 = ent3-dec3
    else:
        x3 = ent3+dec3
    if( ent4<0 ):
        x4 = ent4-dec4
    else:
        x4 = ent4+dec4

    if((x1<0) or (x1>10)):
        x1 = x1%11
    if((x2<0) or (x2>10)):
        x2 = x2%11
    if((x3<0) or (x3>10)):
        x3 = x3%11
    if((x4<0) or (x4>10)):
        x4 = x4%11

    return x1,x2,x3,x4

def funcionAptitud(gen):
    """unos = 0
    for i in xrange(len(gen)):
        if gen[i] == 1:
            unos += 1
    return unos"""
    """a1 = [-32,-16,0,16,32,-32,-16,0,16,32,-32,-16,0,16,32,-32,-16,0,16,32,-32,-16,0,16,32]
    a2 = [-32,-32,-32,-32,-32,-16,-16,-16,-16,-16,0,0,0,0,0,16,16,16,16,16,32,32,32,32,32]

    a = a1,a2
    x1,x2 = praxis_1(gen)

    fx =0.002
    for i in range(1,26):
        fx += 1/(i + pow((x1 - a[0][i-1]),6) + pow((x2 - a[1][i-1]),6))
    fx = 1/fx
    return fx*(-1)"""

    """x1,x2,x3,x4 = praxis_2_5(gen)
    x = x1,x2,x3,x4
    fx = 10.0*4
    for i in range(1,5):
        fx += (pow(x[i-1],2) - 10*math.cos(2*math.pi*x[i-1]))
    return fx*(-1.0)"""

    """x1,x2 = praxis_3_4_7(gen)
    fx = 0.5 + ( (pow( math.sin(pow(x1,2)-pow(x2,2)),2 ) - 0.5)/( pow( 1 + (0.001*(pow(x1,2)+pow(x2,2))) ,2) ) )
    return fx*(-1)"""

    """x1,x2 = praxis_3_4_7(gen)
    fx = (  0.5 + ((math.cos( math.sin( abs( pow(x1,2)-pow(x2,2) ))) - 0.5)/(pow( (1 + 0.001*(pow(x1,2)+pow(x2,2)) ) ,2))  ))
    return fx*(-1)"""
    x1,x2,x3,x4 = praxis_2_5(gen)
    x = x1,x2,x3,x4
    fx = 418.9829*4
    for i in range(1,5):
        fx -= x[i-1]*math.sin(math.sqrt(abs(x[i-1])))
    return fx*(-1)
    """#praxis_6
    b = [1,1,2,2,4,4,6,3,7,5,5]
    c_1 = [4.0, 1.0, 8.0, 6.0, 3.0, 2.0, 5.0, 8.0, 6.0, 7.0]
    c_2 = [4.0, 1.0, 8.0, 6.0, 7.0, 9.0, 3.0, 1.0, 2.0, 3.0]
    c_3 = [4.0, 1.0, 8.0, 6.0, 3.0, 2.0, 5.0, 8.0, 6.0, 7.0]
    c_4 = [4.0, 1.0, 8.0, 6.0, 7.0, 9.0, 3.0, 1.0, 2.0, 3.0]
    c = c_1,c_2,c_3,c_4

    sum1 = 0
    sum2 = 0
    x1,x2,x3,x4 = praxis_6(gen)
    x = x1,x2,x3,x4
    for i in range(1,11):
        for j in range(1,5):
            sum1 += pow( x[j-1]-c[j-1][i-1] ,2) + (1.0/10)*b[i]
        sum2 += pow(sum1, -1)

    return sum2"""
    """x1,x2 = praxis_3_4_7(gen)
    fx = 0.0
    fx1 = 0.0
    fx2 = 0.0
    for i in range(1,6):
        fx1 += ( i*math.cos(((i+1)*x1)+i) )
        fx2 += ( i*math.cos(((i+1)*x2)+i) )
    fx = fx1*fx2
    return fx*(-1)"""
    """t = []
    y = []
    fx = 0.0
    x1,x2,x3,x4,x5 = letzter(gen)
    for i in range(1,25):
        t.append((0.1)*(i-1))
        y.append( 53.81*(pow(1.27,t[i-1]))*math.tanh(math.degrees((3.012*t[i-1])) + (math.sin(math.degrees(2.13*t[i-1]))))*math.cos(math.degrees(math.exp(0.507)*t[i-1])) )
        #Transformar de grados a radianes si la solucion no se acerca a 0
    for i in range(1,25):
        fx += pow(((x1*pow(x2,t[i-1]))*math.tanh( math.degrees((x3*t[i-1])+math.sin(x4*t[i-1])) )*math.cos(math.degrees(t[i-1]*math.exp(x5))) - y[i-1]), 2 )

    return fx*(-1)"""


def creaGen(tamanio):
    genotipo = [-1]*tamanio

    for i in xrange(tamanio):
        genotipo[i] = numpy.random.randint(0,2)%2

    return genotipo


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
    algoritmoGeneticoSimple(NUMERO_GENERACIONES, PROBABILIDAD_CRUZA, PROBABILIDAD_MUTA, MEJORES_INDIVIDUOS)


main()
