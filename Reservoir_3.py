from math import *
from random import *
from tkinter import *
from time import *

affVect = "hidden"
nbrPart = 2

def move(): #incrementation des particules, rebonds, contacts
    global d1, d2, d3, d4
    global part
    global boolPause
    global tempsTot, qTot
    

    mvTot = 0
    EcTot = 0
    librePPart = 0
    librePTot = 0

    c = 0
    
    
    #Mouvement de chaque particules de la liste :
    for p in part:
        

        #incrementation de la position :
        X = p[0]
        Y = p[1]
        dX = p[2]
        dY = p[3]
        m = p[4]
        
        p[0] = X + dX#x + dx
        p[1] = Y + dY#y + dy

        X = p[0]
        Y = p[1]
        
        #rebonds :
        if X <= 0:
            p[0] = 0
            p[2] = -dX
            libreParcours(c, -1)
            qTot = qTot+abs(2*dX)


        elif X >= 800-m:
            p[0] = 800-m
            p[2] = -dX
            libreParcours(c, -1)
            qTot = qTot+abs(2*dX)

    
        elif Y <= 0:
            p[1] = 0
            p[3] = -dY
            libreParcours(c, -1)
            qTot = qTot+abs(2*dY)


        elif Y >= 800-m:
            p[1] = 800-m
            p[3] = -dY
            libreParcours(c, -1)
            qTot = qTot+abs(2*dY)
            
            
        if p[10] != 0:
            librePPart = p[9]/p[10]
            librePTot = librePTot + librePPart
        #mise a jour graphique
        canv.coords(p[5], X, Y, X+m, Y+m)

        z = 15
        if boolVect:
            canv.coords(p[6], (X+(m/2)), (Y+(m/2)), (X+(z*dX)+(m/2)), (Y+(z*dY)+(m/2)))
        else:
            canv.coords(p[6], 0, 0, 0, 0)
        
        mvTot = mvTot + Qmvmnt(p)
        EcTot = EcTot + EnergieCin(p)
        


        c = c+1
        
    varEc.set("Energie cinetique (totale): " + str(int(EcTot)))
    varMvmnt.set("Quantite de mouvement (totale): " + str(int(mvTot)))

    librePTot = librePTot/nbrPart
    varLibreP.set("Libre parcours moyen (en pixels) : " + str(int(librePTot)))

    tempsTot = tempsTot+1
    pressionTot = (qTot/tempsTot)/3200
    varPression.set("Pression contre les parois : " + str(pressionTot))

    varGP.set("Pression x Surface = " + str(int(pressionTot*800*800)))

    collision()
    X = p[0]
    Y = p[1]

    

   
    #rappel :
    if boolPause:
        fen.after(5,move)

    
#___

def libreParcours(i,j):
    global part


    if j>=0:
        a = longueur2([part[i][0],part[i][1]],[part[i][7],part[i][8]])
        b = longueur2([part[j][0],part[j][1]],[part[j][7],part[j][8]])
        
        part[i][10] = part[i][10]+1
        part[j][10] = part[j][10]+1
        
        part[i][9] = part[i][9]+a
        part[j][9] = part[j][9]+b
                    
        part[i][7] = part[i][0]
        part[i][8] = part[i][1]
        part[j][7] = part[j][0]
        part[j][8] = part[j][1]
    else:
        a = longueur2([part[i][0],part[i][1]],[part[i][7],part[i][8]])
        
        part[i][10] = part[i][10]+1
        part[i][9] = part[i][9]+a

        part[i][7] = part[i][0]
        part[i][8] = part[i][1]
        
        

    

def pause():
    global boolPause
    if boolPause:
        boolPause = False
        varPause.set("Start")
    else:
        boolPause = True
        varPause.set("Stop")

    move()


def systemeDoubleEq(a, b, c, d, A, B):

    #résolution d'une matrice 2x2 
    x = ((A*d)-(B*c))/((a*d)-(b*c))
    y = ((a*B)-(b*A))/((a*d)-(b*c))

    return [x,y]

def calculRebond(i, j):
    #numero des particules en collision : i, j

    global part
    
    vecti = [part[i][2], part[i][3]]
    vectj = [part[j][2], part[j][3]]
    
    Xi = part[i][0]
    Yi = part[i][1]
    Xj = part[j][0]
    Yj = part[j][1]

    mi = part[i][4]
    mj = part[j][4]


    Et = [Xj-Xi, Yj-Yi]
    Et = [Et[0]/norme(Et), Et[1]/norme(Et)]
    
    En = [-Et[1], Et[0]]
    En = [En[0]/norme(En), En[1]/norme(En)]

    if produitScalaire(Et, vecti) <0: #test du sens du vecteur normal
        Et[0] = -Et[0]
        Et[1] = -Et[1]


    s1 = systemeDoubleEq(Et[0], Et[1], En[0], En[1], vecti[0], vecti[1])
    s2 = systemeDoubleEq(Et[0], Et[1], En[0], En[1], vectj[0], vectj[1])



    vectiF = (((mi-mj)/(mi+mj))*s1[0])+(((2*mj)/(mi+mj))*s2[0])
    vectjF = (((2*mi)/(mi+mj))*s1[0])+(((mj-mi)/(mi+mj))*s2[0])
    
    #vérif : 
    #vecti2 = [(Et[0]*s1[0])+En[0]*s1[1], (Et[1]*s1[0])+En[1]*s1[1]]
    #vectj2 = [(Et[0]*s2[0])+En[0]*s2[1], (Et[1]*s2[0])+En[1]*s2[1]]

    

    part[i][2] = (vectiF*En[0])+(s1[1]*Et[0])
    part[i][3] = (vectiF*En[1])+(s1[1]*Et[1])

    part[j][2] = (vectjF*En[0])+(s2[1]*Et[0])
    part[j][3] = (vectjF*En[1])+(s2[1]*Et[1])


def Qmvmnt(p):
    mv = norme([p[2],p[3]])*p[4]
    return mv


def EnergieCin(p):
    Ec = 0.5*norme([p[2],p[3]])*norme([p[2],p[3]])*p[4]
    return Ec


def produitScalaire(v1, v2):
    #ne fonctionne qu'avec des unités, sinon sort de la range de arccos
    return (v1[0]*v2[0])+(v1[1]*v2[1])


def centre(l,masse):
    return((l+masse)/2)


def norme(V1):
    l = sqrt(pow(V1[0],2)+pow(V1[1], 2))
    #return(sqrt((V1[0]*V1[0])+(V1[1]*V1[1])))
    return l
    

def longueur(p1,p2): #p1, p2 tableaux de particules. A partir d'un vecteur
    
    resultat = sqrt(pow(p2[0]-p1[0],2)+pow(p2[1]-p1[1],2))
    return resultat


def longueur2(p1, p2): #a part de deux points
    return sqrt(((p2[0]-p1[0])**2)+((p2[1]-p1[1])**2))

def ballePlus():

    
    global part
    global nbrPart
    
    nbrPart = nbrPart+1
    i = [randint(50,750), randint(50,750), randint(-50,50)/25, randint(-50,50)/25, 20, "ovale", "vect", 0,0,0,0]
    part.append(i)

    part[nbrPart-1][5] = canv.create_oval(part[nbrPart-1][0], part[nbrPart-1][1], part[nbrPart-1][0]+part[nbrPart-1][4], part[nbrPart-1][1]+part[nbrPart-1][4], fill = "light green")
    part[nbrPart-1][6] = canv.create_line(part[nbrPart-1][0]+(part[nbrPart-1][4]/2), part[nbrPart-1][1]+(part[nbrPart-1][4]/2), part[nbrPart-1][2]+part[nbrPart-1][0], part[nbrPart-1][3]+part[nbrPart-1][1], arrow="last", fill = "blue", state = affVect)

    

    
def testCollision(x,y):
    global part

    i = 0
    while i<(len(part)-1):
        if x == part[i][0] and y == part[i][1]:
            return True

    return False
    

def collision():
    global part #on récupère toutes les particules
    global nbrPart
    global k    
    i = 0
    j = 0
    
    while i<nbrPart:
        
        j = i+1
        while j<nbrPart:
            
            if longueur(part[i],part[j]) <= (part[i][4]/2)+(part[j][4]/2): #si longueur entre deux balles inférieur a la sommes de leurs rayons (donc collision), alors :
                pass
                part[j][0] = part[j][0] - part[j][2]
                part[j][1] = part[j][1] - part[j][3]


                part[i][0] = part[i][0] - part[i][2]
                part[i][1] = part[i][1] - part[i][3]
                #(on remet les balles a la position d'avant la collision)

                libreParcours(i,j)

                calculRebond(i,j)
                
                

            j = j+1
        i = i+1
                      
    
    
#init :

i=0
k=0

tempsTot = 0
qTot = 0


part = [] #list des particules

boolPause = True
boolVect = True

#def des particules : 
while i < nbrPart:

    p1 = [randint(50,750), randint(50,750), randint(-50,50)/25, randint(-50,50)/25, 2, "ovale", "vect",0,0,0,0] #liste d'une particule donnée, coord, masse, vitesse, numéro
    #p1 = [posX, posY, dX, dY, masse, Forme, position X, Y (pour le libre parcours), longueur libreparcours]
    part.append(p1)
    #print("particules", i, " :", part[i])
    i = i+1
    



#Bordel de Tkinter :

fen=Tk()
fen.title("Reservoire a particules")
canv = Canvas(fen, bg = "pink", height = 800, width = 800)
canv.pack(side=LEFT ,padx = 5, pady = 5)


#Labels variables : 
varMvmnt = StringVar()
labelMvmnt = Label(fen, textvariable = varMvmnt)
labelMvmnt.pack(side=BOTTOM, padx = 10)

varEc = StringVar()
labelEc = Label(fen, textvariable = varEc)
labelEc.pack(side=BOTTOM, padx = 10)

varLibreP = StringVar()
varLibreP.set("0")
labelLibreP = Label(fen, textvariable = varLibreP)
labelLibreP.pack(side=BOTTOM, padx = 50)

varPression = StringVar()
varPression.set("0")
labelPression = Label(fen, textvariable = varPression)
labelPression.pack(side=BOTTOM, padx = 10)

varGP = StringVar()
varGP.set("0")
labelGP = Label(fen, textvariable = varGP)
labelGP.pack(side=BOTTOM, padx = 10)


#Bouttons et élémens interactifs : 
varPause = StringVar()
varPause.set("Stop")
bouttonPause = Button(fen, textvariable = varPause, command = pause)
bouttonPause.pack(side=TOP, padx = 10)

boutBalle = Button(fen, text = " balle + ", command = ballePlus)
boutBalle.pack(side = TOP, padx = 10)


#Formes géométriques :

i = 0
while i<nbrPart:

    part[i][5] = canv.create_oval(part[i][0], part[i][1], part[i][0]+part[i][4], part[i][1]+part[i][4], fill = "light green")
    part[i][6] = canv.create_line(part[i][0]+(part[i][4]/2), part[i][1]+(part[i][4]/2), part[i][2]+part[i][0], part[i][3]+part[i][1], arrow="last", fill = "blue", state = affVect)
    i = i+1

#Affichage :


move()
fen.mainloop()
