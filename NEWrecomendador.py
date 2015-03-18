import Pycluster as pc
import random
#import psycopg2


def buscarElemento(lista, elemento, largo):
    for i in range(0,largo):
                if(lista[i] == elemento):
                        return i


def imprimirMatriz(matriz, columnas, filas):
        for j in range(filas):
                print matriz[j]
                print "\n"


#MATRIZ_USER_VS_ITEM=[[ 0 for i in range(10) ] for j in range(5)] #MATRIZ LLENA DE 0 DE 20X42
MATRIZ_USER_VS_ITEM=[[ random.randint(0,5) for i in range(200) ] for j in range(100)]

#------NO ES ESTATICO---------
UserReco=MATRIZ_USER_VS_ITEM[1]
id_acompanante=1
#-----------------------------


##--------------------CONEXION BDD----------------

#try:
#    con = psycopg2.connect("dbname='planapp_db' user='planapp' host='127.0.0.1' password='nolase.1'")
#
#except:
#    print "I am unable to connect to the database"

#cur = con.cursor()

#----------------------LLENAR MATRIZ DE VOTOS-----

#cur.execute("SELECT count(*) from usuario")
#row0 = cur.fetchall()
#numerousuarios=row0[0]

#cur.execute("SELECT count(*) from lugar")
#row1 = cur.fetchall()
#numerolugares=row1[0]

#for i in range(numerousuarios):
#	for j in range(numerolugares):
#		cur.execute("SELECT voto_lugar from votos where id_acompanante=%s and id_usuario=%s and id_lugar=%s", (id_acompanante,i,j,))
#		rows = cur.fetchall()
#		if len(rows)!=0:
#			MATRIZ_USER_VS_ITEM[i][j]=rows[0]
			
	
print MATRIZ_USER_VS_ITEM


##---------------------BORRAR---------------------

lugares=[]

for i in range(len(MATRIZ_USER_VS_ITEM[1])):
        lugares.append(i)


#-------------------------------------------RECOMENDADOR-------------------------------------------

#print "MATRIZ_USER_VS_ITEMEGLO", MATRIZ_USER_VS_ITEM           

clusterid, error, nfound = pc.kcluster(MATRIZ_USER_VS_ITEM, nclusters=2, transpose=0, npass=1, method='a', dist='e')
centroids, algo = pc.clustercentroids(MATRIZ_USER_VS_ITEM, clusterid=clusterid)

#print "clusterid", clusterid #A que cluster pertence cada vector

buscar=clusterid[MATRIZ_USER_VS_ITEM.index(UserReco)] #BUSCAR = EL ID DEL CLUSTER AL QUE PERTENECE EL USER A RECOMENDAR

# Crear una lista para almacenar solo los usuarios que sirvan para la recomendacion (los que estan en el cluster)
var=[]

for i in range(len(clusterid)):
        if clusterid[i]==buscar:
                var.append(i) ### USUARIOS QUE ESTAN EN EL CLUSTER PARA RECOMENDAR

print "Elementos del cluster:", var

POS_ITEMR=[] #POSICION/NUMERO DEL LUGAR A RECOMENDAR (I1)
promedios=[]

# Lista para sacar los lugares posibles a recomendar (o sea no evaluados)

for i in range(len(UserReco)):
        if UserReco[i]==0:
                POS_ITEMR.append(i) #POSICION DE LOS LUGARES A RECOMENDAR

print "Pos items a recomendar" , POS_ITEMR

# Crear matriz auxiliar que solo contiene los usuarios que sirven (los del mismo cluster)

MATRIZ_AUX=[]

for i in range(len(var)):
        if MATRIZ_USER_VS_ITEM[var[i]]==UserReco:
                continue
        else :
                MATRIZ_AUX.append(MATRIZ_USER_VS_ITEM[var[i]]) #MATRIZ QUE CONTIENE SOLO LOS USUARIOS QUE SON REFERENCIA PARA LA RECOMENDACION

#Sacas promedio de notas del lugar      

for i in range(len(UserReco)):
        sum=0
        for j in range(len(var)-1):
                sum=sum+MATRIZ_AUX[j][i]
        promedios.append(float(sum/(len(var)-1))) #NOTA FINAL DE LOS LUGARES A RECOMENDAR

notas=[]
notas1=[]

# En notas se guarda lo mismo que promedios y la posicion de la nota corresponde a la posicion del lugar

for i in range(len(POS_ITEMR)):
        notas.append(promedios[POS_ITEMR[i]])

notas1=sorted(notas, reverse = True)
recomendados=[]

#print notas
#print notas1

#Notas 1 es notas pero ordenado descendente, luego se recorre ordenadamente notas1 y se ve a que lugar corresponde en notas (ya que posicion de notas equivale al lugar)

for i in range(len(notas1)):
        print i+1,"- item", POS_ITEMR[notas.index(notas1[i])], "nota:", notas1[i]
        recomendados.append(POS_ITEMR[notas.index(notas1[i])])
        notas[notas.index(notas1[i])]=1000  #Para evitar las repeteciones 

TopN=9

# Lista de los lugares recomendados

idrecomendados=[]

print "lugares ", len(lugares)
print "recomendados ", len(recomendados)

for i in range(len(recomendados)):
        print recomendados[i]
        idrecomendados.append(lugares[recomendados[i]])

print idrecomendados

panorama1=[]
actpanorama1=[]

panorama2=[]
actpanorama2=[]

panorama3=[]
actpanorama3=[]

r=0
s=0
t=0

#for i in range(len(idrecomendados)):
        #cur.execute("SELECT id_categoria from tipo_categoria where tipo_categoria.id_lugar=%s", (idrecomendados[i],))
        #rows2 = cur.fetchall()

        #if (actpanorama1.count(rows2[0])==0) and (r<3):
         #       panorama1.append(idrecomendados[i])
          #      actpanorama1.append(rows2[0])
           #     r=r+1
        #else:
         #       if (actpanorama2.count(rows2[0])==0 and s<3):
          #              panorama2.append(idrecomendados[i])
           #             actpanorama2.append(rows2[0])
            #            s=s+1
             #   else:
              #          if (actpanorama3.count(rows2[0])==0) and t<3:
               #                 panorama3.append(idrecomendados[i])
                #                actpanorama3.append(rows2[0])
                 #               t=t+1


print "PANORAMA1: "
for i in range(len(panorama1)):
        print "id: ", panorama1[i]
        print "act: ", actpanorama1[i]


print "PANORAMA2: "
for i in range(len(panorama2)):
        print "id: ", panorama2[i]
        print "act: ", actpanorama2[i]


print "PANORAMA3: "
for i in range(len(panorama3)):
        print "id: ", panorama3[i]
        print "act: ", actpanorama3[i]
