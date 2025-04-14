from sympy import *
import sympy

def calcul_inverse_mod93(m ,n):
    M = Matrix(m)
    det_M = int(M.det()) % 93
    if sympy.gcd(det_M, 93) != 1:
        return "non inversible"
    else :
        det_inv = sympy.mod_inverse(det_M, 93)
        com_MT = M.adjugate()
        inv_M = (det_inv * com_MT) % 93
    #verification :
    I = eye(n)
    V = (inv_M * M) % 93
    if I == V :
        return inv_M.tolist()
    else :
        return "non inversible"

#etape 1 : conversion ascii

secret = "_!q7-8\!_/})!Z#XcPb'*3m,|>`<;ZB#>+`_CE?E"

tab1 = []
for i in secret:
    equivalent_i= ord(i) - 33
    tab1.append(equivalent_i)

#etape 2 : effectuer Hill avec keyA
n= len(tab1)
keyA = [[60,131,101,179,76],[1,134,179,127,115],[28,123,215,204,98],[157,22,28,219,15],[44,27,125,145,223]]

M5 = calcul_inverse_mod93(keyA, 5)
tab2 = []

for i in range(0,n, 5):
    C=[]
    P = []
    C.append([tab1[i]])
    C.append([tab1[i+1]])
    C.append([tab1[i+2]])
    C.append([tab1[i+3]])
    C.append([tab1[i+4]])
    P_mat= (Matrix(M5) * Matrix(C)) % 93
    P = P_mat.tolist()
    tab2.append(P[0][0])
    tab2.append(P[1][0])
    tab2.append(P[2][0])
    tab2.append(P[3][0])
    tab2.append(P[4][0])

#print(tab2)
    
#etape 3 : effectuer Hill avec keyC
keyC = [[89,52,162,39],[91,30,50,30],[222,183,124,41],[2,101,137,191]]

M4 = calcul_inverse_mod93(keyC, 4)
tab3 = []

for i in range(0,n, 4):
    C=[]
    P = []
    C.append([tab2[i]])
    C.append([tab2[i+1]])
    C.append([tab2[i+2]])
    C.append([tab2[i+3]])
    P_mat= (Matrix(M4) * Matrix(C)) % 93
    P = P_mat.tolist()
    tab3.append(P[0][0])
    tab3.append(P[1][0])
    tab3.append(P[2][0])
    tab3.append(P[3][0])

#print(tab3)

#etape 4 : effectuer Hill avec keyB

keyB = [[53,17],[5,46]]

M2 = calcul_inverse_mod93(keyB, 2)
tab4 = []

for i in range(0,n, 2):
    C=[]
    P = []
    C.append([tab3[i]])
    C.append([tab3[i+1]])
    P_mat= (Matrix(M2) * Matrix(C)) % 93
    P = P_mat.tolist()
    tab4.append(P[0][0])
    tab4.append(P[1][0])

#print(tab4)

#etape 5 : reconvertir en caractère :

message=""
for i in range(n):
    message = message + chr(tab4[i] + 33)

print('message =',message)
