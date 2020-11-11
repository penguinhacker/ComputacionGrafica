# coding=utf-8
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
from random import randint
import json
import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es
import lighting_shaders as ls

archivo = sys.argv[1]

Data= None
with open(archivo) as file:
    data =json.load(file)
    Data = data

#casos iniciales
t_a = Data["t_a"]
t_b = Data["t_b"]
t_c = Data["t_c"]
n_a = Data["n_a"]
n_b = Data["n_b"]
n_c = Data["n_c"]
archivo = Data["filename"]



class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.sector = None

controller = Controller()

def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_A:
        if controller.sector == "a":
            controller.sector = None
        else:
            controller.sector = "a"

    elif key == glfw.KEY_B:
        if controller.sector == "b":
            controller.sector = None
        else:
            controller.sector = "b"

    elif key == glfw.KEY_C:
        if controller.sector == "c":
            controller.sector = None
        else:
            controller.sector = "c"

    elif key == glfw.KEY_ESCAPE:
        sys.exit()


def createColorCube(i, j, k, X, Y, Z):
    l_x = X[i, j, k]
    r_x = X[i+1, j, k]
    b_y = Y[i, j, k]
    f_y = Y[i, j+1, k]
    b_z = Z[i, j, k]
    t_z = Z[i, j, k+1]



    #   positions    colors
    vertices = [
    # Z+: number 1
        l_x, b_y,  t_z, 0,0,1,
         r_x, b_y,  t_z, 0,0,1,
         r_x,  f_y,  t_z, 0,0,1,
        l_x,  f_y,  t_z, 0,0,1,
    # Z-: number 6
        l_x, b_y, b_z, 0,0,1,
         r_x, b_y, b_z, 0,0,1,
         r_x,  f_y, b_z, 0,0,1,
        l_x,  f_y, b_z, 0,0,1,
    # X+: number 5
         r_x, b_y, b_z, 0,0,1,
         r_x,  f_y, b_z, 0,0,1,
         r_x,  f_y,  t_z, 0,0,1,
         r_x, b_y,  t_z, 0,0,1,
    # X-: number 2
        l_x, b_y, b_z, 0,0,1,
        l_x,  f_y, b_z, 0,0,1,
        l_x,  f_y,  t_z, 0,0,1,
        l_x, b_y,  t_z, 0,0,1,
    # Y+: number 4
        l_x,  f_y, b_z, 0,0,1,
        r_x,  f_y, b_z, 0,0,1,
        r_x,  f_y, t_z, 0,0,1,
        l_x,  f_y, t_z, 0,0,1,
    # Y-: number 3
        l_x, b_y, b_z, 0,0,1,
        r_x, b_y, b_z, 0,0,1,
        r_x, b_y, t_z, 0,0,1,
        l_x, b_y, t_z, 0,0,1,
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return bs.Shape(vertices, indices)

def merge(destinationShape, strideSize, sourceShape):

    # current vertices are an offset for indices refering to vertices of the new shape
    offset = len(destinationShape.vertices)
    destinationShape.vertices += sourceShape.vertices
    destinationShape.indices += [(offset/strideSize) + index for index in sourceShape.indices]

def createFish1(r,g,b):
    gpuColorCube = es.toGPUShape(bs.createColorNormalsCube(r,g,b))
    gpuBlackCube = es.toGPUShape(bs.createColorNormalsCube(0, 0, 0))
    gpuTriangulo = es.toGPUShape(bs.createTriangulo3D(r, g, b))

    cuerpo = sg.SceneGraphNode("cuerpo")
    cuerpo.transform = tr.scale(0.4,2,1)
    cuerpo.childs += [gpuColorCube]
    
    ojo_izq = sg.SceneGraphNode("ojo_izq")
    ojo_izq.transform =tr.matmul([tr.translate(0.25,0.5,0.25),tr.scale(0.1,0.1,0.1)])
    ojo_izq.childs += [gpuBlackCube]

    ojo_der = sg.SceneGraphNode("ojo_der")
    ojo_der.transform = tr.matmul([tr.translate(-0.25,0.5,0.25), tr.scale(0.1,0.1,0.1)])
    ojo_der.childs += [gpuBlackCube]

    cola = sg.SceneGraphNode("cola")
    cola.transform = tr.matmul([tr.translate(0,0,0.75),tr.rotationX(np.pi/4),tr.scale(0.2,1,2),tr.translate(0,-1.5,0)])
    cola.childs += [gpuTriangulo]

    casi = sg.SceneGraphNode("casi")
    casi.childs += [cola]

    total = sg.SceneGraphNode("total")
    total.childs += [cuerpo]
    total.childs += [ojo_izq]
    total.childs += [ojo_der]
    total.childs += [casi]

    return total

def createFish2(r,g,b):
    gpuColorCube = es.toGPUShape(bs.createColorNormalsCube(r, g, b))
    gpuBlackCube = es.toGPUShape(bs.createColorNormalsCube(0, 0, 0))
    gpuTriangulo = es.toGPUShape(bs.createTriangulo3D(r, g, b))
    gpuWhiteCube = es.toGPUShape(bs.createColorNormalsCube(1, 1, 1))

    cuerpo = sg.SceneGraphNode("cuerpo")
    cuerpo.transform = tr.scale(0.6, 2.5, 1.3)
    cuerpo.childs += [gpuColorCube]

    ojo_blanco = sg.SceneGraphNode("ojo_blanco")
    ojo_blanco.transform = tr.matmul([tr.scale(1,0.5,0.5),tr.translate(0,1.3,0.3)])
    ojo_blanco.childs += [gpuWhiteCube]

    ojo_negro = sg.SceneGraphNode("ojo_negro")
    ojo_negro.transform = tr.matmul([tr.scale(1.1, 0.1, 0.1), tr.translate(0, 6, 1.6)])
    ojo_negro.childs += [gpuBlackCube]
    
    escama1 = sg.SceneGraphNode("escama1")
    escama1.transform = tr.matmul([tr.scale(0.2,1,1.5),tr.translate(0,0.3,0.2)])
    escama1.childs += [gpuTriangulo]

    escama2 = sg.SceneGraphNode("escama2")
    escama2.transform = tr.matmul([tr.scale(0.2, 1, 1.5), tr.translate(0, -0.7, 0.1)])
    escama2.childs += [gpuTriangulo]

    cola = sg.SceneGraphNode("cola")
    cola.transform = tr.matmul([tr.translate(0, -0.3, 0.75), tr.rotationX(np.pi / 4), tr.scale(0.2, 1, 2), tr.translate(0, -1.5, 0)])
    cola.childs += [gpuTriangulo]

    casi = sg.SceneGraphNode("casi")
    casi.childs += [cola]

    total = sg.SceneGraphNode("total")
    total.childs += [cuerpo]
    total.childs += [ojo_blanco]
    total.childs += [ojo_negro]
    total.childs += [escama1]
    total.childs += [escama2]
    total.childs += [casi]

    return total

def createFish3(r,g,b):
    gpuColorCube = es.toGPUShape(bs.createColorNormalsCube(r, g, b))
    gpuBlackCube = es.toGPUShape(bs.createColorNormalsCube(0, 0, 0))
    gpuTriangulo = es.toGPUShape(bs.createTriangulo3D(r, g, b))
    gpuWhiteCube = es.toGPUShape(bs.createColorNormalsCube(1, 1, 1))
    gpuOjo = es.toGPUShape(bs.createTriangulo3D(0, 0, 0))

    cuerpo = sg.SceneGraphNode("cuerpo")
    cuerpo.transform = tr.scale(1, 2.5, 1.3)
    cuerpo.childs += [gpuColorCube]

    frente1 = sg.SceneGraphNode("frente1")
    frente1.transform = tr.matmul([tr.translate(0,1.4,1),tr.rotationX(np.pi/6),tr.scale(0.1,1.5,0.1)])
    frente1.childs += [gpuColorCube]

    frente2 = sg.SceneGraphNode("frente2")
    frente2.transform = tr.matmul([tr.translate(0,2,0.9),tr.scale(0.1,0.1,1)])
    frente2.childs += [gpuColorCube]

    luz = sg.SceneGraphNode("luz")
    luz.transform = tr.matmul([tr.translate(0,2,0.3),tr.scale(0.3,0.3,0.3)])
    luz.childs += [gpuWhiteCube]

    escama1 = sg.SceneGraphNode("escama1")
    escama1.transform = tr.matmul([tr.scale(0.2, 1, 1.5), tr.translate(0, 0, 0.2)])
    escama1.childs += [gpuTriangulo]

    cola = sg.SceneGraphNode("cola")
    cola.transform = tr.matmul(
        [tr.translate(0, -0.3, 0.75), tr.rotationX(np.pi / 4), tr.scale(0.2, 1, 2), tr.translate(0, -1.5, 0)])
    cola.childs += [gpuTriangulo]

    ojo1 = sg.SceneGraphNode("ojo1")
    ojo1.transform = tr.matmul([tr.translate(-0.4,1.2,0),tr.rotationZ(np.pi/2),tr.scale(0.25,0.4,0.5)])
    ojo1.childs += [gpuOjo]

    ojo2 = sg.SceneGraphNode("ojo2")
    ojo2.transform = tr.matmul([tr.translate(0.4, 1.2, 0), tr.rotationZ(-np.pi / 2), tr.scale(0.25, 0.4, 0.5)])
    ojo2.childs += [gpuOjo]

    casi = sg.SceneGraphNode("casi")
    casi.transform = tr.rotationZ(0.3)
    casi.childs += [cola]

    total = sg.SceneGraphNode("total")
    total.childs += [cuerpo]
    total.childs += [frente1]
    total.childs += [frente2]
    total.childs += [luz]
    total.childs += [escama1]
    total.childs += [casi]
    total.childs += [ojo1]
    total.childs += [ojo2]

    return total

def createPecera(L,W,H,s):
    gpuGrayCube = es.toGPUShape(bs.createColorNormalsCube(128, 128, 128))

    palo_horizontal1= sg.SceneGraphNode("palo_horizontal1")
    palo_horizontal1.transform = tr.scale(0.1,1*s,0.1)
    palo_horizontal1.childs += [gpuGrayCube]

    palo_horizontal2 = sg.SceneGraphNode("palo_horizontal2")
    palo_horizontal2.transform = tr.scale((W/L)*s, 0.1, 0.1)
    palo_horizontal2.childs += [gpuGrayCube]

    palo_vertical = sg.SceneGraphNode("palo_vertical")
    palo_vertical.transform = tr.scale(0.1,0.1,(H/L)*s)
    palo_vertical.childs += [gpuGrayCube]

    uno= sg.SceneGraphNode("uno")
    uno.transform = tr.translate((W/L)*(s/2),0,-(H/L)*(s/2))
    uno.childs += [palo_horizontal1]

    dos = sg.SceneGraphNode("dos")
    dos.transform = tr.translate((W/L)*(s/2),0,(H/L)*(s/2))
    dos.childs += [palo_horizontal1]

    tres = sg.SceneGraphNode("tres")
    tres.transform = tr.translate(-(W/L)*(s/2),0,-(H/L)*(s/2))
    tres.childs += [palo_horizontal1]

    cuatro = sg.SceneGraphNode("cuatro")
    cuatro.transform = tr.translate(-(W/L)*(s/2),0,(H/L)*(s/2))
    cuatro.childs += [palo_horizontal1]

    cinco = sg.SceneGraphNode("cinco")
    cinco.transform = tr.translate(0,-s/2,-(H/L)*(s/2))
    cinco.childs += [palo_horizontal2]

    seis = sg.SceneGraphNode("seis")
    seis.transform = tr.translate(0,s/2,-(H/L)*(s/2))
    seis.childs += [palo_horizontal2]

    siete = sg.SceneGraphNode("siete")
    siete.transform = tr.translate(0,-s/2,(H/L)*(s/2))
    siete.childs += [palo_horizontal2]

    ocho = sg.SceneGraphNode("ocho")
    ocho.transform = tr.translate(0,s/2,(H/L)*(s/2))
    ocho.childs += [palo_horizontal2]

    nueve = sg.SceneGraphNode("nueve")
    nueve.transform = tr.translate(-(W/L)*(s/2),s/2,0)
    nueve.childs += [palo_vertical]

    diez = sg.SceneGraphNode("diez")
    diez.transform = tr.translate((W/L)*(s/2),-s/2,0)
    diez.childs += [palo_vertical]

    once = sg.SceneGraphNode("once")
    once.transform = tr.translate(-(W/L)*(s/2),-s/2,0)
    once.childs += [palo_vertical]

    doce = sg.SceneGraphNode("doce")
    doce.transform = tr.translate((W/L)*(s/2),s/2,0)
    doce.childs += [palo_vertical]

    total = sg.SceneGraphNode("total")
    total.transform = tr.scale(1,1,1)
    total.childs += [uno,dos,tres,cuatro,cinco,seis,siete,ocho,nueve,diez,once,doce]

    return total



def asignarPosiciones(lista_listas,k):
    lista = []
    for i in range(0,k):
        a = randint(0,len(lista_listas)-1)
        lista += [lista_listas[a]]

    return lista

def NGPUs(gpu, n):
    lista = []
    for i in range(0,n):
        lista += [gpu]
    return lista















if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "acuario", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)



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
    glEnable(GL_BLEND)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))




    loaded = np.load(archivo)
    W = loaded.shape[0]
    L = loaded.shape[1]
    H = loaded.shape[2]

    pecera = createPecera(L,W,H,6)



    Y,X,Z = np.meshgrid(np.linspace(0,L,L),np.linspace(0,W,W),np.linspace(0,H,H))

    isosurfacea = bs.Shape([], [])
    isosurfaceb = bs.Shape([], [])
    isosurfacec = bs.Shape([], [])

    coordenadasa = []
    coordenadasb = []
    coordenadasc = []


    for i in range(X.shape[0] - 1):
        for j in range(X.shape[1] - 1):
            for k in range(X.shape[2] - 1):
                if loaded[i, j, k] <t_a+2 and loaded[i,j,k] >t_a-2:
                    coordenadasa += [[i,j,k]]
                    temp_shape = createColorCube(i, j, k, X, Y, Z)
                    merge(destinationShape=isosurfacea, strideSize=6, sourceShape=temp_shape)

    for i in range(X.shape[0] - 1):
        for j in range(X.shape[1] - 1):
            for k in range(X.shape[2] - 1):
                if loaded[i, j, k] <t_b+2 and loaded[i,j,k] >t_b-2:
                    coordenadasb += [[i,j,k]]
                    temp_shape = createColorCube(i, j, k, X, Y, Z)
                    merge(destinationShape=isosurfaceb, strideSize=6, sourceShape=temp_shape)

    for i in range(X.shape[0] - 1):
        for j in range(X.shape[1] - 1):
            for k in range(X.shape[2] - 1):
                if loaded[i, j, k] <t_c+2 and loaded[i,j,k] >t_c-2:
                    coordenadasc += [[i,j,k]]
                    temp_shape = createColorCube(i, j, k, X, Y, Z)
                    merge(destinationShape=isosurfacec, strideSize=6, sourceShape=temp_shape)


    gpu_surfacea = es.toGPUShape(isosurfacea)
    gpu_surfaceb = es.toGPUShape(isosurfaceb)
    gpu_surfacec = es.toGPUShape(isosurfacec)

    #posicionesa = asignarPosiciones(coordenadasa,n_a)
    posicionesa= asignarPosiciones(coordenadasa,n_a)
    posicionesb = asignarPosiciones(coordenadasb,n_b)
    posicionesc = asignarPosiciones(coordenadasc,n_c)

    lista_pecesa = NGPUs(createFish1(82/255,219/255,1),n_a)
    lista_pecesb = NGPUs(createFish3(128/255, 0, 128/255), n_b)
    lista_pecesc = NGPUs(createFish2(253/255, 106/255, 2/255), n_c)




    gpu_Pared = es.toGPUShape(bs.createColorQuad(0,0,1))

    t0 = glfw.get_time()
    camera_theta = np.pi / 4
    acercamiento = 1

    while not glfw.window_should_close(window):

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glfw.poll_events()

        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera_theta -= 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera_theta += 2* dt

        if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):
            acercamiento -= 2* dt

        if (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS):
            acercamiento += 2* dt

        camX = 10 *acercamiento* np.sin(camera_theta)
        camY = 10 *acercamiento* np.cos(camera_theta)

        viewPos = np.array([camX, camY, 3])

        view = tr.lookAt(
            viewPos,
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )

        model = tr.identity()

        projection = tr.perspective(45, float(width) / float(height), 0.1, 100)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        lightingPipeline = phongPipeline
        glUseProgram(lightingPipeline.shaderProgram)





        #TEMAS DE LUZ------------------------------------------------------------------------------------------------
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.9, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), -5, -5, 5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1],viewPos[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)

        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01)
        #-----------------------------------------------------------------------------------------------------------

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)


        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE, model)

        sg.drawSceneGraphNode(pecera, lightingPipeline, "model")

        #para mostrar ahora los pescados de a
        for i in range(0,n_a):
            a = lista_pecesa[i]
            mov_cola = sg.findNode(a,"casi")
            mov_cola.transform = tr.rotationZ(np.sin(t0)*0.15)
            transformacion = sg.findNode(a, "total")
            transformacion.transform = tr.matmul([tr.uniformScale(6/L),tr.translate(posicionesa[i][0]-W / 2,posicionesa[i][1]-L / 2,posicionesa[i][2]-H / 2)])

            sg.drawSceneGraphNode(a, lightingPipeline, "model")

        for i in range(0,n_b):
            a = lista_pecesb[i]
            mov_cola = sg.findNode(a, "casi")
            mov_cola.transform = tr.rotationZ(np.sin(t0+2) * 0.15)
            transformacion = sg.findNode(a, "total")
            transformacion.transform = tr.matmul([tr.uniformScale(6/L),tr.translate(posicionesb[i][0]-W / 2,posicionesb[i][1]-L / 2,posicionesb[i][2]-H / 2)])

            sg.drawSceneGraphNode(a, lightingPipeline, "model")

        for i in range(0,n_c):
            a = lista_pecesc[i]
            mov_cola = sg.findNode(a, "casi")
            mov_cola.transform = tr.rotationZ(np.sin(t0+3) * 0.15)
            transformacion = sg.findNode(a, "total")
            transformacion.transform = tr.matmul([tr.uniformScale(6/L),tr.translate(posicionesc[i][0]-W / 2,posicionesc[i][1]-L / 2,posicionesc[i][2]-H / 2)])

            sg.drawSceneGraphNode(a, lightingPipeline, "model")





        glUseProgram(pipeline.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        movimiento = tr.matmul(
            [tr.scale(6 / L, 6 / L, 6 / L),tr.translate(-W/2,-L/2,-H/2) ])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, movimiento)



        if controller.sector == "a":
            pipeline.drawShape(gpu_surfacea,GL_LINES)

        if controller.sector == "b":
            pipeline.drawShape(gpu_surfaceb,GL_LINES)

        if controller.sector == "c":
            pipeline.drawShape(gpu_surfacec,GL_LINES)


        glBlendFunc(GL_ONE, GL_ONE)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(3))
        #pipeline.drawShape(gpu_Pared)

        glfw.swap_buffers(window)

    glfw.terminate()