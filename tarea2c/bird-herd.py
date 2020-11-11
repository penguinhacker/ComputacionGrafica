from bird import *
import numpy as np
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
import csv
from math import *
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#----------------------------SECTOR DE FUNCIONES UTILES---------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T

def catmullMatrix(P0, P1, P2, P3):
    # Generate a matrix concatenating the columns
    G = np.concatenate((P0, P1, P2, P3), axis=1)

    a = np.array([[0, -1, 2, -1], [2, 0, -5, 3], [0, 1, 4, -3], [0, 0, -1, 1]])
    return np.matmul(G, (1/2)*a)


def plotCurve(ax, curve, label, color=(0, 0, 1)):
    xs = curve[:, 0]
    ys = curve[:, 1]
    zs = curve[:, 2]

    ax.plot(xs, ys, zs, label=label, color=color)

def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)

    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)

    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T

    return curve

def unirPuntos(M,N):
    if len(M) ==0:
        return N
    curve = np.ndarray(shape=(len(M)+len(N)-1, 3), dtype=float)
    i =0
    a = 0
    for x in M:
        curve[i] = x
        i+=1
    for w in N:
        if a == 0:
            a = 1
        else:
            curve[i] = w
            i+=1
    return curve

def largo_archivo(file):
    filas=0
    with open(file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for h in spamreader:
            filas += 1
    return filas

def lee_y_entrega(file):
    matriz = np.ndarray(shape=(largo_archivo(file), 3), dtype=float)
    a = None
    b = None
    c = None
    with open(file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        contador = 0
        for row in spamreader:
            for x in row:

                if a == None:
                    a = x
                elif b == None:
                    b = x
                elif c == None:
                    c = x
                else:
                    fila = np.array([a,b,c])
                    matriz[contador] = fila
                    a = x
                    b = None
                    c = None
                    contador +=1
        fila = np.array([a, b, c])
        matriz[contador] = fila
    return matriz


#hacer que esta funcion evalue todos los puntos de un archivo y entregure un arreglo con todos los puntos finales :o
def evaluarArchivo(archivo,N):
    puntos_finales = np.ndarray(shape=(0, 3), dtype=float)
    puntos = lee_y_entrega(archivo)
    largo = largo_archivo(archivo)
    fin = largo - 2
    i = 1

    while i < fin:
        P1=np.array([puntos[i-1]]).T
        P2=np.array([puntos[i]]).T
        P3=np.array([puntos[i+1]]).T
        P4=np.array([puntos[i+2]]).T
        catmull= catmullMatrix(P1,P2,P3,P4)
        puntos_i = evalCurve(catmull,N)
        a = unirPuntos(puntos_finales,puntos_i)
        puntos_finales = a
        i+=1
    return puntos_finales


def rotacion_simple(v,angulo):
    return np.array([np.cos(angulo)*v[0]- np.sin(angulo)*v[1],np.sin(angulo)*v[0]+np.cos(angulo)*v[1]])

def modulo_simple(v):
    return sqrt(v[0]**2+v[1]**2)

def modulo(v):
    return sqrt(v[0]**2+v[1]**2+v[2]**2)

def vector_normalizado(v):
    hipotenusa = sqrt(v[0]**2+v[1]**2)
    return np.array([v[0]/hipotenusa,v[1]/hipotenusa])

def consigue_angulo(v):
    if v[0] >= 0 and v[1] >=0:
        return asin(v[1]/modulo_simple(v))
    if v[0] < 0 and v[1] >=0:
        return np.pi -asin(v[1]/modulo_simple(v))
    if v[0] < 0 and v[1] < 0:
        return np.pi + asin(-v[1]/modulo_simple(v))
    if v[0] >= 0 and v[1] < 0:
        return 2*np.pi- asin(-v[1]/modulo_simple(v))
    else:
        return None




def angulo_desde_Y(v):
    if v[0] >= 0 and v[1] >= 0:
        return 2*np.pi-atan(v[0] / v[1])
    if v[0] < 0 and v[1] >= 0:
        return atan(-v[0]/v[1])
    if v[0] < 0 and v[1] < 0:
        return np.pi/2 + atan(-v[1] / -v[0])
    if v[0] >= 0 and v[1] < 0:
        return np.pi + atan(v[0] / -v[1])
    else:
        return None



def anguloZ(va,vc):


    camino = np.array([vc[0], vc[1]])



    #----------------------------------
    angulo_camino = angulo_desde_Y(camino)

    return angulo_camino

def anguloX(va,vc):


    ave= np.array([va[1],va[2]])
    camino = np.array([vc[1], vc[2]])


    aveN= vector_normalizado(ave)
    caminoN= vector_normalizado(camino)

    #----------------------------------
    angulo_ave= consigue_angulo(aveN)

    angulo_camino = consigue_angulo(caminoN)

    if angulo_ave >= angulo_camino:
        #angulo del ave tiene mas
        op1= angulo_ave - angulo_camino
        op2= 2*np.pi - angulo_ave + angulo_camino
        if op1 >= op2:
            return op2
        else:
            return -op1
    else:
        #angulo del camino tiene mas
        op1= angulo_camino -angulo_ave
        op2= op2= 2*np.pi - angulo_camino + angulo_ave

        if op1 >= op2:
            return op2
        else:
            return -op1





#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#--------------------------SECTOR PARA MOSTRAR A LAS AVES --------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# coding=utf-8

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
from random import randint

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es
import lighting_shaders as ls





class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.mousePos = (0.0, 0.0)

controller = Controller()


def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        sys.exit()


def cursor_pos_callback(window, x, y):
    global controller
    controller.mousePos = (x,y)

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Observador", None, None)




    if not window:
        glfw.terminate()
        sys.exit()


    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    glfw.set_cursor_pos_callback(window, cursor_pos_callback)

    phongPipeline = ls.SimplePhongShaderProgram()

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleModelViewProjectionShaderProgram()


    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))

    pajaro1 = createBird(0.5,0.1,0)

    pajaro2 = createBird(0, 1, 0)
    pajaro3 = createBird(0.5, 0.1, 1)
    pajaro4 = createBird(0.2, 0.5, 0.4)
    pajaro5 = createBird(0.5, 0.1, 0.5)

    gpuFondo = es.toGPUShape(bs.createTextureCube("lateral.jpg"), GL_REPEAT, GL_LINEAR)
    gpuArriba= es.toGPUShape(bs.createTextureQuad("arriba.jpg"),GL_REPEAT,GL_LINEAR)
    gpuAbajo = es.toGPUShape(bs.createTextureQuad("abajo.jpg"), GL_REPEAT, GL_LINEAR)

    gpuAxis = es.toGPUShape(bs.createAxis(4))

    estado1=1 #1 ES PRENDER TODO Y 0 APAGAR
    estado2=0
    estado3=0
    estado4=0
    estado5=0


    t0 = glfw.get_time()
    camera_theta = np.pi / 4

    archivo = str(sys.argv[1])

    a = evaluarArchivo(archivo,150)
    b = len(a)-1
    contador1=1
    contador2=0
    contador3=0
    contador4=0
    contador5=0

    direc1=np.array([0,1,0])
    direc2 = np.array([1, 1, 1])
    direc3 = np.array([0, 0, 1])
    direc4 = np.array([0, 0, 1])
    direc5 = np.array([0, 0, 1])








    al1=randint(2,6)
    al2=randint(2,6)
    al3=randint(2,6)
    al4=randint(2,6)
    al5=randint(2,6)

    var1=randint(1,100)
    var2=randint(1,100)
    var3=randint(1,100)
    var4=randint(1,100)
    var5=randint(1,100)

    while not glfw.window_should_close(window):

        glfw.poll_events()

        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # -------------------------------------------------------------------
        #------------------------CAMBIOS DE ROTACION-------------------------
        # -------------------------------------------------------------------


        if contador1 >200 and estado2==0:
            estado2=1
        if contador1 >400 and estado3==0:
            estado3=1
        if contador1 >600 and estado4==0:
            estado4=1
        if contador1 >800 and estado5==0:
            estado5=1


        if estado1==1:

            nodo_rotacion_interno_derecha1 = sg.findNode(pajaro1, "interno_derecha2")
            nodo_rotacion_interno_derecha1.transform = tr.rotationY(np.pi/9 - np.pi/4 * (300- np.cos(t1*al1+var1)*300)/600)

            nodo_rotacion_interno_izquierda1 = sg.findNode(pajaro1, "interno_izquierda2")
            nodo_rotacion_interno_izquierda1.transform = tr.rotationY(-(np.pi / 9 - np.pi / 4 * (300- np.cos(t0*al1+var1)*300) / 600))

            nodo_cola_31 = sg.findNode(pajaro1, "cola3")
            nodo_cola_31.transform = tr.rotationX((300- np.cos(t0*4)*300) * np.pi / 10000)

            nodo_cara_cuello21 = sg.findNode(pajaro1, "cara_cuello2")
            nodo_cara_cuello21.transform = tr.rotationX(-(np.pi / 4 * (300- np.cos(t0*4)*300) / 1900))





            #----------------------------------------------------------------------------
            #ROTACION PAJARO 1
            #----------------------------------------------------------------------------


            vector_camino= np.array([a[contador1][0]-a[contador1-1][0],a[contador1][1]-a[contador1-1][1],a[contador1][2]-a[contador1-1][2]])
            angulo_vertical=acos(vector_camino[2]/modulo(vector_camino))
            nodo_cuerpo1 = sg.findNode(pajaro1,"total")

            nodo_cuerpo1.transform = np.matmul(
                np.matmul(tr.translate(a[contador1][0], a[contador1][1], a[contador1][2]),
                          tr.rotationZ(anguloZ(direc1,vector_camino))), tr.rotationX(np.pi/2-angulo_vertical))

            if contador1 < b:
                contador1+=1

        if estado2 == 1:

            nodo_rotacion_interno_derecha12 = sg.findNode(pajaro2, "interno_derecha2")
            nodo_rotacion_interno_derecha12.transform = tr.rotationY(
                np.pi / 9 - np.pi / 4 * (300 - np.cos(t1 * al2+var2) * 300) / 600)

            nodo_rotacion_interno_izquierda12 = sg.findNode(pajaro2, "interno_izquierda2")
            nodo_rotacion_interno_izquierda12.transform = tr.rotationY(
                -(np.pi / 9 - np.pi / 4 * (300 - np.cos(t0 * al2+var2) * 300) / 600))

            nodo_cola_32 = sg.findNode(pajaro2, "cola3")
            nodo_cola_32.transform = tr.rotationX((300 - np.cos(t0 * 4) * 300) * np.pi / 10000)

            nodo_cara_cuello22 = sg.findNode(pajaro2, "cara_cuello2")
            nodo_cara_cuello22.transform = tr.rotationX(-(np.pi / 4 * (300 - np.cos(t0 * 4) * 300) / 1900))

            # ----------------------------------------------------------------------------
            # ROTACION PAJARO 2
            # ----------------------------------------------------------------------------

            vector_camino2 = np.array([a[contador2][0] - a[contador2 - 1][0], a[contador2][1] - a[contador2 - 1][1],
                                      a[contador2][2] - a[contador2 - 1][2]])
            angulo_vertical2 = acos(vector_camino2[2] / modulo(vector_camino2))
            nodo_cuerpo2 = sg.findNode(pajaro2, "total")

            nodo_cuerpo2.transform = np.matmul(
                np.matmul(tr.translate(a[contador2][0], a[contador2][1], a[contador2][2]),
                          tr.rotationZ(anguloZ(direc2, vector_camino2))), tr.rotationX(np.pi / 2 - angulo_vertical2))

            if contador2 < b:
                contador2 += 1
        if estado3 == 1:

            nodo_rotacion_interno_derecha13 = sg.findNode(pajaro3, "interno_derecha2")
            nodo_rotacion_interno_derecha13.transform = tr.rotationY(
                np.pi / 9 - np.pi / 4 * (300 - np.cos(t1 * al3+var3) * 300) / 600)

            nodo_rotacion_interno_izquierda13 = sg.findNode(pajaro3, "interno_izquierda2")
            nodo_rotacion_interno_izquierda13.transform = tr.rotationY(
                -(np.pi / 9 - np.pi / 4 * (300 - np.cos(t0 * al3+var3) * 300) / 600))

            nodo_cola_33 = sg.findNode(pajaro3, "cola3")
            nodo_cola_33.transform = tr.rotationX((300 - np.cos(t0 * 4) * 300) * np.pi / 10000)

            nodo_cara_cuello23 = sg.findNode(pajaro3, "cara_cuello2")
            nodo_cara_cuello23.transform = tr.rotationX(-(np.pi / 4 * (300 - np.cos(t0 * 4) * 300) / 1900))

            # ----------------------------------------------------------------------------
            # ROTACION PAJARO 1
            # ----------------------------------------------------------------------------

            vector_camino3 = np.array([a[contador3][0] - a[contador3 - 1][0], a[contador3][1] - a[contador3 - 1][1],
                                      a[contador3][2] - a[contador3 - 1][2]])
            angulo_vertical3 = acos(vector_camino3[2] / modulo(vector_camino3))
            nodo_cuerpo3 = sg.findNode(pajaro3, "total")

            nodo_cuerpo3.transform = np.matmul(
                np.matmul(tr.translate(a[contador3][0], a[contador3][1], a[contador3][2]),
                          tr.rotationZ(anguloZ(direc3, vector_camino3))), tr.rotationX(np.pi / 2 - angulo_vertical3))

            if contador3 < b:
                contador3 += 1
        if estado4 == 1:

            nodo_rotacion_interno_derecha14 = sg.findNode(pajaro4, "interno_derecha2")
            nodo_rotacion_interno_derecha14.transform = tr.rotationY(
                np.pi / 9 - np.pi / 4 * (300 - np.cos(t1 * al4+var4) * 300) / 600)

            nodo_rotacion_interno_izquierda14 = sg.findNode(pajaro4, "interno_izquierda2")
            nodo_rotacion_interno_izquierda14.transform = tr.rotationY(
                -(np.pi / 9 - np.pi / 4 * (300 - np.cos(t0 * al4+var4) * 300) / 600))

            nodo_cola_34 = sg.findNode(pajaro4, "cola3")
            nodo_cola_34.transform = tr.rotationX((300 - np.cos(t0 *4)  * 300) * np.pi / 10000)

            nodo_cara_cuello24 = sg.findNode(pajaro4, "cara_cuello2")
            nodo_cara_cuello24.transform = tr.rotationX(-(np.pi / 4 * (300 - np.cos(t0 * 4) * 300) / 1900))

            # ----------------------------------------------------------------------------
            # ROTACION PAJARO 4
            # ----------------------------------------------------------------------------

            vector_camino4 = np.array([a[contador4][0] - a[contador4 - 1][0], a[contador4][1] - a[contador4 - 1][1],
                                      a[contador4][2] - a[contador4 - 1][2]])
            angulo_vertical4 = acos(vector_camino4[2] / modulo(vector_camino4))
            nodo_cuerpo4 = sg.findNode(pajaro4, "total")

            nodo_cuerpo4.transform = np.matmul(
                np.matmul(tr.translate(a[contador4][0], a[contador4][1], a[contador4][2]),
                          tr.rotationZ(anguloZ(direc4, vector_camino4))), tr.rotationX(np.pi / 2 - angulo_vertical4))

            if contador4 < b:
                contador4 += 1
        if estado5 == 1:

            nodo_rotacion_interno_derecha15 = sg.findNode(pajaro5, "interno_derecha2")
            nodo_rotacion_interno_derecha15.transform = tr.rotationY(
                np.pi / 9 - np.pi / 4 * (300 - np.cos(t1 * al5+var5) * 300) / 600)

            nodo_rotacion_interno_izquierda15 = sg.findNode(pajaro5, "interno_izquierda2")
            nodo_rotacion_interno_izquierda15.transform = tr.rotationY(
                -(np.pi / 9 - np.pi / 4 * (300 - np.cos(t0 * al5+var5) * 300) / 600))

            nodo_cola_35 = sg.findNode(pajaro5, "cola3")
            nodo_cola_35.transform = tr.rotationX((300 - np.cos(t0 * 4) * 300) * np.pi / 10000)

            nodo_cara_cuello25 = sg.findNode(pajaro5, "cara_cuello2")
            nodo_cara_cuello25.transform = tr.rotationX(-(np.pi / 4 * (300 - np.cos(t0 * 4) * 300) / 1900))

            # ----------------------------------------------------------------------------
            # ROTACION PAJARO 5
            # ----------------------------------------------------------------------------

            vector_camino5 = np.array([a[contador5][0] - a[contador5 - 1][0], a[contador5][1] - a[contador5 - 1][1],
                                      a[contador5][2] - a[contador5 - 1][2]])
            angulo_vertical5 = acos(vector_camino5[2] / modulo(vector_camino5))
            nodo_cuerpo5 = sg.findNode(pajaro5, "total")

            nodo_cuerpo5.transform = np.matmul(
                np.matmul(tr.translate(a[contador5][0], a[contador5][1], a[contador5][2]),
                          tr.rotationZ(anguloZ(direc1, vector_camino5))), tr.rotationX(np.pi / 2 - angulo_vertical5))

            if contador5 < b:
                contador5 += 1





        mousePosX= 2*(controller.mousePos[0]-width/2)/width
        mousePosY= 2*(height/2 - controller.mousePos[1])/height


        camX = 20 * np.sin(camera_theta)
        camY = 20 * np.cos(camera_theta)
        camZ = 5


        angulo_x= (np.pi + np.pi/4  -((controller.mousePos[0]-300)/300)*np.pi)
        angulo_y=  (np.pi/2+     ((controller.mousePos[1]-300)/300)*np.pi/2 + np.pi/8)

        #14,14,5
        viewPos = np.array([camX, camY, camZ])

        view = tr.lookAt(
            viewPos,
            np.array([3*np.sin(angulo_y)*np.cos(angulo_x)+camX, 3*np.sin(angulo_x)*np.sin(angulo_y)+camY, 3*np.cos(angulo_y)+camZ]),
            np.array([0, 0, 1])
        )

        model = tr.identity()





        projection = tr.perspective(45, float(width) / float(height), 0.1, 1000)



        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)



        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)





        lightingPipeline = phongPipeline
        glUseProgram(lightingPipeline.shaderProgram)

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.9, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), 0, 0, 10)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1],viewPos[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 10000)

        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE, model)

        glUseProgram(lightingPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        #lightingPipeline.drawShape(gpuAxis, GL_LINES)

        if estado1 == 1:
            sg.drawSceneGraphNode(pajaro1, lightingPipeline, "model")
        if estado2 == 1:
            sg.drawSceneGraphNode(pajaro2, lightingPipeline, "model")
        if estado3 == 1:
            sg.drawSceneGraphNode(pajaro3, lightingPipeline, "model")
        if estado4 == 1:
            sg.drawSceneGraphNode(pajaro4, lightingPipeline, "model")
        if estado5 == 1:
            sg.drawSceneGraphNode(pajaro5, lightingPipeline, "model")



        if contador1 == b:
            estado1 =-1
        if contador2 == b:
            estado2 =-1
        if contador3 == b:
            estado3 =-1
        if contador4 == b:
            estado4 =0-1
        if contador5 == b:
            estado5 =0-1


        #nodo_cuerpo1 = sg.findNode(pajaro1, "total")
        #nodo_cuerpo1.transform = np.matmul(
        #    np.matmul(tr.translate(7, -7, 0),
        #              tr.rotationZ(np.pi/4 * 7)), tr.rotationX(np.pi/4))
        #sg.drawSceneGraphNode(pajaro1, lightingPipeline, "model")


        escala = 100
        textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()

        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE,projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE,tr.uniformScale(escala))
        textureShaderProgram.drawShape(gpuFondo)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE,np.matmul(tr.uniformScale(escala),tr.translate(0,0,0.4888)))
        textureShaderProgram.drawShape(gpuArriba)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE,np.matmul(tr.uniformScale(escala), tr.translate(0, 0, -0.4888)))
        textureShaderProgram.drawShape(gpuAbajo)

        glfw.swap_buffers(window)

    glfw.terminate()