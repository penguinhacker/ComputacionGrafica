import numpy as np
import sys
import json
import scipy.sparse as sparse
import scipy.sparse.linalg as linalg
import matplotlib.pyplot as plt


archivo = sys.argv[1]

Data= None
with open(archivo) as file:
    Data = json.load(file)

#casos iniciales
height = Data["height"]
width = Data["width"]
lenght = Data["lenght"]
windows_loss= Data["window_loss"]
heater_a= Data["heater_a"]
heater_b= Data["heater_b"]
bottom=0
ambient_temperature= Data["ambient_temperature"]

filename = Data["filename"]

h= 0.2

nx= int(width/h)+1
ny= int(lenght/h)+1
nz= int(height/h)

N = nx*ny*nz

def getK(i,j,l):
    return l*ny*nx+j*nx+i


def getIJL(k):
    i = k%nx
    j = (k%(nx*ny))//nx
    l = k//(nx*ny)
    return (i,j,l)

A = sparse.lil_matrix((N,N))
#A=np.zeros((N,N))
b = np.zeros((N,))

for i in range(0, nx):
    for j in range(0, ny):
        for l in range(0, nz):

            k = getK(i, j, l)
            k_up = getK(i, j, l + 1)
            k_down = getK(i, j, l - 1)
            k_left = getK(i, j - 1, l)
            k_right = getK(i, j + 1, l)
            k_bottom = getK(i - 1, j, l)
            k_top = getK(i + 1, j, l)

            # caso interior:
            if 1 <= i and i < nx - 1 and j < ny - 1 and l < nz - 1 and 1 <= j and 1 <= l:
                A[k, k_up] = 1
                A[k, k_down] = 1
                A[k, k_left] = 1
                A[k, k_right] = 1
                A[k, k_bottom] = 1
                A[k, k_top] = 1
                A[k, k] = -6
                b[k] = 0

            # CASOS CARAS (solamente con un choque)

            # superior
            elif 1 <= i and 1 <= j and i < nx - 1 and j < ny - 1 and l == nz - 1:
                # condicion tipo dirichlet
                A[k, k_top] = 1
                A[k, k_down] = 1
                A[k, k_left] = 1
                A[k, k_right] = 1
                A[k, k_bottom] = 1
                A[k, k] = -6
                b[k] = - ambient_temperature

            # lado1 (izquierda)
            elif 1 <= i and 1 <= l and i < nx - 1 and j == 0 and l < nz - 1:
                # condicion neumann
                A[k, k_up] = 1
                A[k, k_down] = 1
                A[k, k_top] = 1
                A[k, k_right] = 2
                A[k, k_bottom] = 1
                A[k, k] = -6
                b[k] = - 2 * h * windows_loss

            # lado2 (ventana mas al frente)
            elif i == nx - 1 and 1 <= j and j < ny - 1 and 1 <= l and l < nz - 1:
                # condicion neumann
                A[k, k_up] = 1
                A[k, k_down] = 1
                A[k, k_left] = 1
                A[k, k_right] = 1
                A[k, k_bottom] = 2
                A[k, k] = -6
                b[k] = - 2 * h * windows_loss

            # lado3 (derecha)
            elif 1 <= i and i < nx - 1 and 1 <= l and j == ny - 1 and l < nz - 1:
                # condicion neumann
                A[k, k_up] = 1
                A[k, k_down] = 1
                A[k, k_left] = 2
                A[k, k_top] = 1
                A[k, k_bottom] = 1
                A[k, k] = -6
                b[k] = - windows_loss * 2 * h

            # lado4 (fondo)
            elif i == 0 and 1 <= j and j < ny - 1 and 1 <= l and l < nz - 1:
                # condicion neumann
                A[k, k_up] = 1
                A[k, k_down] = 1
                A[k, k_left] = 1
                A[k, k_top] = 2
                A[k, k_right] = 1
                A[k, k] = -6
                b[k] = - windows_loss * 2 * h

            # CASOS DEL SUELO (3)

            # caso 1 (suelo normal)

            elif (nx // 3 <= i) and (i <= 2 * nx // 3) and (ny - (2 * ny // 5) <= j) and (
                    j <= ny - (ny // 5)) and l == 0:  # caso calefactor a (dirichlet)
                A[k, k_up] = 1
                A[k, k_bottom] = 1
                A[k, k_left] = 1
                A[k, k_top] = 1
                A[k, k_right] = 1
                A[k, k] = -6
                b[k] = - heater_a


            elif (nx // 3 <= i) and (i <= 2 * nx // 3) and (ny // 5 <= j) and (j <= 2 * ny // 5) and l == 0:
                # caso calefactor b (dirichlet)
                A[k, k_up] = 1
                A[k, k_bottom] = 1
                A[k, k_left] = 1
                A[k, k_top] = 1
                A[k, k_right] = 1
                A[k, k] = -6
                b[k] = - heater_b

            elif (1 <= i) and (i <= nx - 2) and (1 <= j) and (j <= ny - 2) and l == 0:
                # caso otros suelos (neumann)
                A[k, k_up] = 2
                A[k, k_bottom] = 1
                A[k, k_left] = 1
                A[k, k_top] = 1
                A[k, k_right] = 1
                A[k, k] = -6
                b[k] = 0
            # TERMINAMOS LOS CASOS DE LAS CARAS

            # ARISTAS

            # superior izquierda
            elif j == 0 and l == nz - 1 and 1 <= i and i < nx - 1:
                # caso neumann dirichlet
                A[k, k_down] = 1
                A[k, k_bottom] = 1
                A[k, k_top] = 1
                A[k, k_right] = 2
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - ambient_temperature

            # inferior izquierda
            elif j == 0 and l == 0 and 1 <= i and i < nx - 1:
                # caso neumann neumann
                A[k, k_up] = 2
                A[k, k_bottom] = 1
                A[k, k_top] = 1
                A[k, k_right] = 2
                A[k, k] = -6
                b[k] = -2 * h * windows_loss

            # superior derecha
            elif j == ny - 1 and l == nz - 1 and 1 <= i and i < nx - 1:
                # caso direcht neumann
                A[k, k_down] = 1
                A[k, k_bottom] = 1
                A[k, k_top] = 1
                A[k, k_left] = 2
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - ambient_temperature

            # inferior derecha
            elif j == ny - 1 and l == 0 and 1 <= i and i < nx - 1:
                # caso neumann neumann
                A[k, k_up] = 2
                A[k, k_bottom] = 1
                A[k, k_top] = 1
                A[k, k_left] = 2
                A[k, k] = -6
                b[k] = -2 * h * windows_loss


            # lateral fondo izquierda
            elif i == 0 and j == 0 and 1 <= l and l < nz - 1:
                # neumann neumann
                A[k, k_up] = 1
                A[k, k_right] = 2
                A[k, k_top] = 2
                A[k, k_down] = 1
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - 2 * h * windows_loss
            # lateral frente izquierda
            elif i == nx - 1 and j == 0 and 1 <= l and l < nz - 1:
                # neumann neumann
                A[k, k_up] = 1
                A[k, k_right] = 2
                A[k, k_bottom] = 2
                A[k, k_down] = 1
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - 2 * h * windows_loss

            # lateral fondo derecha
            elif i == 0 and j == ny - 1 and 1 <= l and l < nz - 1:
                # neumann neumann
                A[k, k_up] = 1
                A[k, k_left] = 2
                A[k, k_top] = 2
                A[k, k_down] = 1
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - 2 * h * windows_loss
            # lateral frente derecha
            elif i == nx - 1 and j == ny - 1 and 1 <= l and l < nz - 1:
                # neumann neumann
                A[k, k_up] = 1
                A[k, k_left] = 2
                A[k, k_bottom] = 2
                A[k, k_down] = 1
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - 2 * h * windows_loss


            # superior centro fondo
            elif i == 0 and l == nz - 1 and 1 <= j and j < ny - 1:
                # neumann dirichlet
                A[k, k_down] = 1
                A[k, k_left] = 1
                A[k, k_top] = 2
                A[k, k_right] = 1
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - ambient_temperature


            elif i == 0 and l == 0 and 1 <= j and j < ny - 1:
                # neumann dirichlet
                A[k, k_up] = 2
                A[k, k_left] = 1
                A[k, k_top] = 2
                A[k, k_right] = 1
                A[k, k] = -6
                b[k] = -2 * h * windows_loss

                # inferior centro fondo
            elif i == 0 and l == nz - 1 and 1 <= j and j < ny - 1:
                # neumann neumann
                A[k, k_down] = 2
                A[k, k_left] = 1
                A[k, k_top] = 2
                A[k, k_right] = 1
                A[k, k] = -6
                b[k] = -2 * h * windows_loss
            # superior centro frente
            elif i == nx - 1 and l == nz - 1 and 1 <= j and j < ny - 1:
                # neumann dirichlet
                A[k, k_down] = 1
                A[k, k_left] = 1
                A[k, k_bottom] = 2
                A[k, k_right] = 1
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - ambient_temperature
            # inferior centro frente
            elif i == nx - 1 and l == 0 and 1 <= j and j < ny - 1:
                # naumann neumann
                A[k, k_up] = 2
                A[k, k_left] = 1
                A[k, k_bottom] = 2
                A[k, k_right] = 1
                A[k, k] = -6
                b[k] = -2 * h * windows_loss


            # ESQUINAS
            # esquina 1 (izquierda atras abajo)
            elif i == 0 and j == 0 and l == 0:
                # 3 neumann
                A[k, k_up] = 2
                A[k, k_top] = 2
                A[k, k_right] = 2
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - 2 * h * windows_loss

            # esquina 2(izquierda atras arriba)
            elif i == 0 and j == 0 and l == nz - 1:
                # 2 neumann y dirchlet
                A[k, k_down] = 1
                A[k, k_top] = 2
                A[k, k_right] = 2
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - 2 * h * windows_loss - ambient_temperature

            # esquina 3(izquierda adelante abajo)
            elif i == nx - 1 and j == 0 and l == 0:
                # 3 neumann
                A[k, k_up] = 2
                A[k, k_bottom] = 2
                A[k, k_right] = 2
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - 2 * h * windows_loss

            # esquina 4(izquierda adelante arriba)
            elif i == nx - 1 and j == 0 and l == nz - 1:
                # 2 neumann y 1 D
                A[k, k_down] = 1
                A[k, k_bottom] = 2
                A[k, k_right] = 2
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - 2 * h * windows_loss - ambient_temperature

            # esquina 5(derecha atras abajo)
            elif i == 0 and j == ny - 1 and l == 0:
                # 3 neumann
                A[k, k_up] = 2
                A[k, k_top] = 2
                A[k, k_left] = 2
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - 2 * h * windows_loss

            # esquina6(derecha atras arriba)
            elif i == 0 and j == ny - 1 and l == nz - 1:
                # 2 neumann y 1 D
                A[k, k_down] = 1
                A[k, k_top] = 2
                A[k, k_left] = 2
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - 2 * h * windows_loss - ambient_temperature

            # esquina7 (derecha adelante abajo)
            elif i == nx - 1 and j == ny - 1 and l == 0:
                # 3 neumann
                A[k, k_up] = 2
                A[k, k_bottom] = 2
                A[k, k_left] = 2
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - 2 * h * windows_loss

            # esquina8 (derecha adelante arriba)
            elif i == nx - 1 and j == ny - 1 and l == nz - 1:
                # 2 neumann y 1 D
                A[k, k_down] = 1
                A[k, k_bottom] = 2
                A[k, k_left] = 2
                A[k, k] = -6
                b[k] = -2 * h * windows_loss - 2 * h * windows_loss - ambient_temperature

            else:
                print("Point (" + str(i) + ", " + str(j) + ", " + str(l) + ") missed!")
                print("Associated point index is " + str(k))
                raise Exception()



x = linalg.spsolve(A, b)

# Now we return our solution to the 3d discrete domain
# In this matrix we will store the solution in the 3d domain
u = np.zeros((nx,ny,nz))

for g in range(0, N):
    i,j,l = getIJL(g)
    u[i,j,l] = x[g]

#u tiene las temperaturas en forma de matriz cubica

# Adding the borders, as they have known values
ub = np.zeros((nx,ny,nz+1))
ub[0:nx, 0:ny, 0:nz] = u[:,:,:]

# Dirichlet boundary condition on the top side
ub[0:nx, 0:ny, nz] = ambient_temperature

print(ub)
#print(ub[3,0,0])

# Saving results for temperatures
np.save(filename,ub)

X, Y, Z = np.mgrid[0:width:16j, 0:lenght:31j, 0:height:21j]

fig = plt.figure()
ax = fig.gca(projection='3d')

scat = ax.scatter(X,Y,Z, c=ub, alpha=0.5, s=100, marker='s')

fig.colorbar(scat, shrink=0.5, aspect=5) # This is the colorbar at the side

# Showing the result
ax.set_title('Laplace equation solution from aquarium')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# Note:
# imshow is also valid but it uses another coordinate system,
# a data transformation is required
#ax.imshow(ub.T)

plt.show()





