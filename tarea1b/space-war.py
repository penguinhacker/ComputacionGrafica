import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
from math import *
import transformations as tr
import basic_shapes as bs
import easy_shaders as es
from random import *
#-----------------------------------------------
#Funciones que podrian ser utiles
#-----------------------------------------------
print("aaaaaaaaaaaa")
def listaN(N):
    l = []
    if N ==0:
        return l
    for i in range(0,N):
        l += [-1]
    return l

#lista llena con "valor" de un largo N
def listaPro(N,valor):
    l = []
    if N == 0:
        return l
    for i in range(0, N):
        l += [valor]
    return l

def listaAleatoria(N):
    l = []
    if N == 0:
        return l
    for i in range(0,N):
        a=randint(0,1)
        if a ==1:
            l += [random()]
        if a == 0:
            l += [- random()]
    return l

def consigueIndice(lista,valor):
    for i in range(0,len(lista)):
        if lista[i] == valor:
            return i


#-----------------------------------------------
#en enemigos se almacena la cantidad de enemigos asignada al ingresar en comando en anaconda prompt
#-----------------------------------------------
enemigos= int(sys.argv[1])




#-----------------------------------------------
#Nuestro controller
#-----------------------------------------------

class Controller:
    def __init__(self):
        self.fillPolygon = True

    x_nave = 0
    y_nave = -0.6
    disparo = False


controller = Controller()

#-----------------------------------------------
#segmento donde aplico los inputs de mivimiento y disparo
#-----------------------------------------------
def on_key(window, key, scancode, action, mods):
    global controller
    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            controller.disparo = True

        if key == glfw.KEY_A:
            if controller.x_nave -0.04 >-1:
                controller.x_nave -= 0.04


        if key == glfw.KEY_D:
            if controller.x_nave + 0.04 < 1:
                controller.x_nave += 0.04

        if key == glfw.KEY_W:
            if controller.y_nave +0.04 < 1:
                controller.y_nave += 0.04

        if key == glfw.KEY_S:
            if controller.y_nave -0.04 > -1:
                controller.y_nave -= 0.04

        if key == glfw.KEY_ESCAPE:
            sys.exit()



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Space Penguins", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # A simple shader program with position and texture coordinates as inputs.
    pipeline = es.SimpleTextureTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    #-----------------------------------------------
    #Creacion de gpushapes
    # -----------------------------------------------

    fondo =es.toGPUShape(bs.seleccionarSegmentoFigura("espacio.png",1,2,0, 0, 1, 1), GL_REPEAT,GL_NEAREST)
    nave1 =es.toGPUShape(bs.seleccionarSegmento("nave.png",0,0,1/3,1), GL_REPEAT, GL_NEAREST)
    nave2 =es.toGPUShape(bs.seleccionarSegmento("nave.png",1/3,0,2/3,1), GL_REPEAT, GL_NEAREST)
    nave3 =es.toGPUShape(bs.seleccionarSegmento("nave.png",2/3,0,1,1), GL_REPEAT, GL_NEAREST)
    bala = es.toGPUShape(bs.seleccionarSegmento("bala.png",0,0,1,1), GL_REPEAT, GL_NEAREST)
    bala2 = es.toGPUShape(bs.seleccionarSegmento("bala2.png", 0, 0, 1, 1), GL_REPEAT, GL_NEAREST)
    enemigo = es.toGPUShape(bs.seleccionarSegmento("enemigo.png", 0, 0, 1, 1), GL_REPEAT, GL_NEAREST)
    vida = es.toGPUShape(bs.seleccionarSegmento("vida.png", 0, 0, 1, 1), GL_REPEAT, GL_NEAREST)
    vida2 = es.toGPUShape(bs.seleccionarSegmento("vida2.png", 0, 0, 1, 1), GL_REPEAT, GL_NEAREST)
    game = es.toGPUShape(bs.seleccionarSegmento("game.png", 0, 0, 1, 1), GL_REPEAT, GL_NEAREST)
    over = es.toGPUShape(bs.seleccionarSegmento("over.png", 0, 0, 1, 1), GL_REPEAT, GL_NEAREST)
    ganaste = es.toGPUShape(bs.seleccionarSegmento("ganaste.png", 0, 0, 1, 1), GL_REPEAT, GL_NEAREST)



    #Funcion disparo enemigo
    def disparo_enemy(shape,x_bala_enemigo,y_bala_enemigo,disparando,listax,i,y):
        if x_bala_enemigo[0] == None:
            x_bala_enemigo[0] = listax[i]
            y_bala_enemigo[0] = y
        if y_bala_enemigo[0] >-1:
            matriz = tr.matmul([tr.translate(x_bala_enemigo[0], y_bala_enemigo[0], 0.0), tr.scale(0.05,0.15,0.1)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(shape)
            y_bala_enemigo[0] -= 0.005
        if y_bala_enemigo[0] <-1:
            x_bala_enemigo[0]=None
            y_bala_enemigo[0]=None
            disparando[0] = None




    #movimiento enemigo
    def mover1(shape, t, l, i,y):
        b = t
        x = sin(t)
        l[i] = x
        matriz= tr.matmul([tr.translate(x, y, 0.0),tr.uniformScale(0.3)])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
        pipeline.drawShape(shape)

    #proceso de que un enemigo baje hasta su posicion
    def bajar(shape,x,y_actual,i,y,estado):
        if y_actual[i] > y:
            y_actual[i] -= 0.001
            matriz = tr.matmul([tr.translate(x, y_actual[i], 0.0), tr.uniformScale(0.3)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(shape)
        if y_actual[i] < y:
            estado[i]="abajo"

    #animacion para que las latras de victoria y derrota se muevan a la derecha
    def mov_Derecha(shape,lista,y,i,scale_x,scale_y):
        if lista[i]< 0:
            lista[i]+= 0.01
            matriz = tr.matmul([tr.translate(lista[i], y, 0.0), tr.scale(scale_x,scale_y,1)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(shape)
        else:
            matriz = tr.matmul([tr.translate(lista[i], y, 0.0), tr.scale(scale_x, scale_y, 1)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(shape)

    def mov_Izquierda(shape,lista):
        if lista[1]> 0:
            lista[1]-= 0.01
            matriz = tr.matmul([tr.translate(lista[1], -0.3, 0.0), tr.scale(2,0.5,1)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(shape)
        else:
            matriz = tr.matmul([tr.translate(lista[1], -0.3, 0.0), tr.scale(2, 0.5, 1)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(shape)



    #Listas de las coordenadas de nuestras 3 balas
    lista_balasy = [None, None, None]
    lista_balasx = [None, None, None]





    #Guardamos la cantidad de enmigos por lista dividiendola por 3
    cantidad_por_lista= enemigos//3

    #lista de estados para cada fila
    estados_arriba= listaPro(cantidad_por_lista+enemigos%3,"esperando")
    estados_medio= listaPro(cantidad_por_lista,"esperando")
    estados_abajo = listaPro(cantidad_por_lista, "esperando")


    #Cada lista tiene sus propias coordenadas, tanto para sus posiciones...
    x_arriba = listaPro(cantidad_por_lista + enemigos % 3, None)
    x_medio = listaPro(cantidad_por_lista, None)
    x_abajo = listaPro(cantidad_por_lista, None)

    y_actual_arriba = listaPro(cantidad_por_lista + enemigos % 3, 1.2)
    y_actual_medio = listaPro(cantidad_por_lista, 1.2)
    y_actual_abajo = listaPro(cantidad_por_lista, 1.2)

    #como para un tiempo donde empiecen a moverse horizontalmente
    t0_arriba=None
    t0_medio=None
    t0_abajo=None

    #Como para sus balas e informaciones
    y_bala_enemigo_arriba = [None]
    y_bala_enemigo_abajo = [None]
    y_bala_enemigo_medio = [None]

    x_bala_enemigo_arriba = [None]
    x_bala_enemigo_abajo = [None]
    x_bala_enemigo_medio = [None]

    disparando_arriba=[None]
    disparando_medio=[None]
    disparando_abajo=[None]


    #vidas del jugador
    vidas=3

    jugando="si"

    #posicion inicial de las letras de ganar o perder
    game_over=[-2,2,-2]

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()


        #Condiciones para llenar o no llenar las figuras
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # limpiar todo
        glClear(GL_COLOR_BUFFER_BIT)

        #agregamos un timer para establecer los tiempos
        t = glfw.get_time()


        #segmento para hacer la traslacion del fondo
        matrizTransformada = tr.matmul([
            tr.translate(0, 1-((t%4)/2), 0.0),tr.uniformScale(2)
        ])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matrizTransformada)
        pipeline.drawShape(fondo)







        #-------------------------------------------------------------------------------------
        #-----------------------------------SEGMENTO Enemigos---------------------------------
        #-------------------------------------------------------------------------------------


        #separado en 3 segmentos: arriba, medio y abajo
        for i in range(0,len(estados_arriba)):
            if estados_arriba[i] == "bajando":
                bajar(enemigo,0,y_actual_arriba,i,0.8,estados_arriba)
                break

            if estados_arriba[i] == "abajo":
                if t0_arriba==None:
                    t0_arriba = glfw.get_time()

                if disparando_arriba[0] ==None or disparando_arriba[0] >=50:
                    numero= randint(0,1000)
                    disparando_arriba[0] = numero

                if disparando_arriba[0] < 50:

                    a =disparo_enemy(bala,x_bala_enemigo_arriba,y_bala_enemigo_arriba,disparando_arriba,x_arriba,i,0.8)

                mover1(enemigo,t-t0_arriba,x_arriba,i,0.8)
                break

            if estados_arriba[i] == "esperando":
                estados_arriba[i]="bajando"
                break



        for i in range(0,len(estados_medio)):
            if estados_medio[i] == "bajando":
                bajar(enemigo,0,y_actual_medio,i,0.6,estados_medio)
                break

            if estados_medio[i] == "abajo":
                if t0_medio==None:
                    t0_medio = glfw.get_time()

                if disparando_medio[0] ==None or disparando_medio[0] >=50:
                    numero= randint(0,1000)
                    disparando_medio[0] = numero

                if disparando_medio[0] < 50:

                    a =disparo_enemy(bala,x_bala_enemigo_medio,y_bala_enemigo_medio,disparando_medio,x_medio,i,0.6)

                mover1(enemigo,t-t0_medio,x_medio,i,0.6)
                break

            if estados_medio[i] == "esperando":
                estados_medio[i]="bajando"
                break

        for i in range(0,len(estados_abajo)):
            if estados_abajo[i] == "bajando":
                bajar(enemigo,0,y_actual_abajo,i,0.4,estados_abajo)
                break

            if estados_abajo[i] == "abajo":
                if t0_abajo==None:
                    t0_abajo = glfw.get_time()

                if disparando_abajo[0] ==None or disparando_abajo[0] >=50:
                    numero= randint(0,1000)
                    disparando_abajo[0] = numero

                if disparando_abajo[0] < 50:

                    a =disparo_enemy(bala,x_bala_enemigo_abajo,y_bala_enemigo_abajo,disparando_abajo,x_abajo,i,0.4)

                mover1(enemigo,t-t0_abajo,x_abajo,i,0.4)
                break

            if estados_abajo[i] == "esperando":
                estados_abajo[i]="bajando"
                break

        #-------------------------------------------------------------------------------
        #---------------------------------SEGMENTO NAVE---------------------------------
        #-------------------------------------------------------------------------------
        a = t%1
        #Creacion de nave con sprites
        if vidas >0:
            matrizNave= np.matmul(tr.translate(controller.x_nave,controller.y_nave,0), tr.uniformScale(0.3))

            if a>0 and a<=0.3:
                glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matrizNave)
                pipeline.drawShape(nave1)

            if a>0.3 and a<=0.6:
                glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matrizNave)
                pipeline.drawShape(nave2)

            if a>0.6:
                glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matrizNave)
                pipeline.drawShape(nave3)


        #------------------------------------------------------------------------------------------
        #---------------------------segmento BALA amiga(que dispara el jugador)-------------------------------
        #------------------------------------------------------------------------------------------
        if vidas > 0:
            if controller.disparo == True:
                for i in range(0,len(lista_balasx)):
                    if lista_balasx[i] == None:
                        lista_balasx[i]= controller.x_nave
                        lista_balasy[i]= controller.y_nave
                        break
                controller.disparo = False


            def disparar(shape,lista_balasy,lista_balasx,i):

                a = lista_balasy[i]
                b = a + 0.02
                lista_balasy[i] = b

                matriz = tr.matmul([tr.translate(lista_balasx[i], b, 0.0),tr.scale(0.05,0.15,1)])
                glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
                pipeline.drawShape(shape)

            for i in range(0,3):
                if type(lista_balasy[i]) == float and lista_balasy[i] > 1:
                    lista_balasy[i] = None
                    lista_balasx[i] = None
                elif type(lista_balasy[i]) == float and lista_balasy[i] < 1:
                    disparar(bala2,lista_balasy,lista_balasx,i)

        # -------------------------------------------------------------------------------------
        # ------------------------------------SEGMENTO VIDAS-----------------------------------
        # -------------------------------------------------------------------------------------
        if vidas == 3:

            matriz = tr.matmul([tr.translate(-0.8, -0.8, 0.0), tr.uniformScale(1 / 8)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(vida)

            matriz = tr.matmul([tr.translate(-0.7, -0.8, 0.0), tr.uniformScale(1 / 8)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(vida)

            matriz = tr.matmul([tr.translate(-0.6, -0.8, 0.0), tr.uniformScale(1 / 8)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(vida)

        if vidas == 2:

            matriz = tr.matmul([tr.translate(-0.8, -0.8, 0.0), tr.uniformScale(1 / 8)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(vida)

            matriz = tr.matmul([tr.translate(-0.7, -0.8, 0.0), tr.uniformScale(1 / 8)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(vida)

            matriz = tr.matmul([tr.translate(-0.6, -0.8, 0.0), tr.uniformScale(1 / 8)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(vida2)

        if vidas == 1:

            matriz = tr.matmul([tr.translate(-0.8, -0.8, 0.0), tr.uniformScale(1 / 8)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(vida)

            matriz = tr.matmul([tr.translate(-0.7, -0.8, 0.0), tr.uniformScale(1 / 8)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(vida2)

            matriz = tr.matmul([tr.translate(-0.6, -0.8, 0.0), tr.uniformScale(1 / 8)])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, matriz)
            pipeline.drawShape(vida2)

        #----------------------------------------------------------------------------------
        #------------------------SEGMENTO COLISIONES---------------------------------------
        #----------------------------------------------------------------------------------
        #Tanto para balas enemigas como amigas.
        for i in range(0,3):
            ixa= consigueIndice(estados_arriba,"abajo")
            if ixa!=None and lista_balasx[i]!=None and x_arriba[ixa] != None:
                if lista_balasx[i] < x_arriba[ixa]+0.1 and lista_balasx[i] > x_arriba[ixa]-0.1:
                    if lista_balasy[i] < 0.8 + 0.05 and lista_balasy[i] > 0.8 - 0.05:
                        lista_balasx[i] = None
                        lista_balasy[i] = None
                        estados_arriba[ixa]="muerto"
                        t0_arriba=None

        for i in range(0,3):
            ixa= consigueIndice(estados_medio,"abajo")
            if ixa!=None and lista_balasx[i]!=None and x_medio[ixa] !=None:
                if lista_balasx[i] < x_medio[ixa]+0.1 and lista_balasx[i] > x_medio[ixa]-0.1:
                    if lista_balasy[i] < 0.6 + 0.05 and lista_balasy[i] > 0.6 - 0.05:
                        lista_balasx[i] = None
                        lista_balasy[i] = None
                        estados_medio[ixa]="muerto"
                        t0_medio=None

        for i in range(0,3):
            ixa= consigueIndice(estados_abajo,"abajo")
            if ixa!=None and lista_balasx[i]!=None and x_abajo[ixa] != None:
                if lista_balasx[i] < x_abajo[ixa]+0.1 and lista_balasx[i] > x_abajo[ixa]-0.1:
                    if lista_balasy[i] < 0.4 + 0.05 and lista_balasy[i] > 0.4 - 0.05:
                        lista_balasx[i] = None
                        lista_balasy[i] = None
                        estados_abajo[ixa]="muerto"
                        t0_abajo=None

        if y_bala_enemigo_arriba[0] != None and x_bala_enemigo_arriba[0] != None:
            if controller.x_nave-0.1 < x_bala_enemigo_arriba[0] and controller.x_nave+0.1 > x_bala_enemigo_arriba[0]:
                if controller.y_nave-0.05 < y_bala_enemigo_arriba[0] and controller.y_nave+0.05>y_bala_enemigo_arriba[0]:
                    vidas-=1
                    x_bala_enemigo_arriba[0]=None
                    y_bala_enemigo_arriba[0]=None
                    disparando_arriba[0]=None

        if y_bala_enemigo_medio[0] != None and x_bala_enemigo_medio[0] != None:
            if controller.x_nave-0.1 < x_bala_enemigo_medio[0] and controller.x_nave+0.1 > x_bala_enemigo_medio[0]:
                if controller.y_nave-0.05 < y_bala_enemigo_medio[0] and controller.y_nave+0.05>y_bala_enemigo_medio[0]:
                    vidas-=1
                    x_bala_enemigo_medio[0]=None
                    y_bala_enemigo_medio[0]=None
                    disparando_medio[0]=None


        if y_bala_enemigo_abajo[0] != None and x_bala_enemigo_abajo[0] != None:
            if controller.x_nave-0.1 < x_bala_enemigo_abajo[0] and controller.x_nave+0.1 > x_bala_enemigo_abajo[0]:
                if controller.y_nave-0.05 < y_bala_enemigo_abajo[0] and controller.y_nave+0.05>y_bala_enemigo_abajo[0]:
                    vidas-=1
                    x_bala_enemigo_abajo[0]=None
                    y_bala_enemigo_abajo[0]=None
                    disparando_abajo[0]=None

        if vidas ==0:
            jugando ="no"

        if estados_arriba== ["muerto"]*len(estados_arriba) and estados_medio ==["muerto"]*len(estados_medio) and estados_abajo==["muerto"]*len(estados_abajo):
            mov_Derecha(ganaste,game_over,0,2,2,2)
        

        if jugando =="no":
            mov_Derecha(game,game_over,0.3,0,2,0.5)
            mov_Izquierda(over,game_over)


        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()