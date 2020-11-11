# coding=utf-8

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

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

def createBird(r,g,b):

    gpuWhiteCube= es.toGPUShape(bs.createColorNormalsCube(1,1,1))
    gpuColorBird= es.toGPUShape(bs.createColorNormalsCube(r,g,b))
    gpuBlackCube= es.toGPUShape(bs.createColorNormalsCube(0,0,0))
    gpuOrangeCube = es.toGPUShape(bs.createColorNormalsCube(1,0.5,0))

    ala = sg.SceneGraphNode("ala")
    ala.transform = tr.scale(1, 1, 0.2)
    ala.childs += [gpuColorBird]

    cuerpo = sg.SceneGraphNode("cuerpo")
    cuerpo.transform = tr.matmul([tr.scale(1, 1.8, 0.4),tr.translate(0,-0.1,0)])
    cuerpo.childs += [gpuColorBird]

    cola = sg.SceneGraphNode("cola")
    cola.transform = tr.scale(0.3, 0.1, 0.3)
    cola.childs += [gpuBlackCube]

    pico = sg.SceneGraphNode("pico")
    pico.transform = tr.scale(0.5, 0.5, 0.2)
    pico.childs += [gpuOrangeCube]

    cuello = sg.SceneGraphNode("cuello")
    cuello.transform = tr.scale(0.2, 0.2, 0.5)
    cuello.childs += [gpuColorBird]

    cabeza = sg.SceneGraphNode("cabeza")
    cabeza.transform = tr.scale(1, 1, 1)
    cabeza.childs += [gpuColorBird]

    ojo = sg.SceneGraphNode("ojo")
    ojo.transform = tr.scale(0.1, 0.1, 0.1)
    ojo.childs += [gpuBlackCube]

    #--------------------------------------

    ojo_izq = sg.SceneGraphNode("ojo_izq")
    ojo_izq.transform = tr.translate(0.3,0.5,0.3)
    ojo_izq.childs += [ojo]

    ojo_der = sg.SceneGraphNode("ojo_der")
    ojo_der.transform = tr.translate(-0.3, 0.5,0.3)
    ojo_der.childs += [ojo]

    pico2 = sg.SceneGraphNode("pico2")
    pico2.transform = tr.translate(0, 0.5, 0)
    pico2.childs += [pico]

    cuello2 = sg.SceneGraphNode("cuello2")
    cuello2.transform = tr.rotationX(-3.14/3)
    cuello2.childs += [cuello]

    cara= sg.SceneGraphNode("cara")
    cara.childs += [ojo_izq]
    cara.childs += [ojo_der]
    cara.childs += [pico2]
    cara.childs += [cabeza]

    cara2 = sg.SceneGraphNode("cara2")
    cara2.transform = tr.translate(0,0.5,0.3)
    cara2.childs += [cara]

    cara_cuello = sg.SceneGraphNode("cara_cuello")
    cara_cuello.transform =tr.translate(0, 0.8, 0.3)
    cara_cuello.childs += [cara2]
    cara_cuello.childs += [cuello2]

    cara_cuello2 = sg.SceneGraphNode("cara_cuello2")
    cara_cuello2.childs += [cara_cuello]


    cola2= sg.SceneGraphNode("cola2")
    cola2.transform = tr.matmul([tr.translate(0,-1.15,0.3),tr.rotationX(3.14/3)])
    cola2.childs += [cola]

    cola3 = sg.SceneGraphNode("cola3")
    cola3.childs += [cola2]

    #ALAS

    externo_derecha = sg.SceneGraphNode("externo_derecha")
    externo_derecha.transform = tr.translate(1.4, 0, 0)
    externo_derecha.childs += [ala]

    externo_derecha2 = sg.SceneGraphNode("externo_derecha2")
    externo_derecha2.childs += [externo_derecha]

    externo_derecha3 = sg.SceneGraphNode("externo_derecha3")
    externo_derecha3.transform = tr.translate(0.5, 0,0)
    externo_derecha3.childs += [externo_derecha2]

    interno_derecha = sg.SceneGraphNode("interno_derecha")
    interno_derecha.transform = tr.translate(0.9,0,0)
    interno_derecha.childs += [ala]

    interno_derecha2 = sg.SceneGraphNode("interno_derecha2")
    interno_derecha2.childs += [interno_derecha]
    #interno_derecha2.childs += [externo_derecha3]

    interno_derecha3 = sg.SceneGraphNode("interno_derecha3")
    interno_derecha3.transform = tr.translate(0.1,0,0)
    interno_derecha3.childs += [interno_derecha2]

    externo_izquierda = sg.SceneGraphNode("externo_izquierda")
    externo_izquierda.transform = tr.translate(-1.4, 0, 0)
    externo_izquierda.childs += [ala]

    externo_izquierda2 = sg.SceneGraphNode("externo_izquierda2")
    externo_izquierda2.childs += [externo_izquierda]

    externo_izquierda3 = sg.SceneGraphNode("externo_izquierda3")
    externo_izquierda3.transform = tr.translate(-0.5, 0, 0)
    externo_izquierda3.childs += [externo_izquierda2]

    interno_izquierda = sg.SceneGraphNode("interno_izquierda")
    interno_izquierda.transform = tr.translate(-0.9, 0, 0)
    interno_izquierda.childs += [ala]

    interno_izquierda2 = sg.SceneGraphNode("interno_izquierda2")
    interno_izquierda2.childs += [interno_izquierda]
    #interno_izquierda2.childs += [externo_izquierda3]

    interno_izquierda3 = sg.SceneGraphNode("interno_izquierda3")
    interno_izquierda3.transform = tr.translate(-0.1, 0, 0)
    interno_izquierda3.childs += [interno_izquierda2]







    total = sg.SceneGraphNode("total")
    total.childs += [cara_cuello2]
    total.childs += [cuerpo]
    total.childs += [cola3]
    total.childs += [interno_derecha3]
    total.childs += [interno_izquierda3]

    #redWheelRotationNode = sg.findNode(redCarNode, "wheelRotation")

    return total


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "3D cars via scene graph", None, None)

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

    pajaro = createBird(0.5,0.1,0)

    t0 = glfw.get_time()
    camera_theta = np.pi / 4

    while not glfw.window_should_close(window):

        glfw.poll_events()

        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera_theta -= 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera_theta += 2* dt

        #------------------------CAMBIOS DE ROTACION-------------------------

        nodo_rotacion_interno_derecha = sg.findNode(pajaro, "interno_derecha2")
        nodo_rotacion_interno_derecha.transform = tr.rotationY(np.pi/9 - np.pi/4 * controller.mousePos[1]/600)

        nodo_rotacion_interno_izquierda = sg.findNode(pajaro, "interno_izquierda2")
        nodo_rotacion_interno_izquierda.transform = tr.rotationY(-(np.pi / 9 - np.pi / 4 * controller.mousePos[1] / 600))

        nodo_cola_3 = sg.findNode(pajaro, "cola3")
        nodo_cola_3.transform = tr.rotationX(controller.mousePos[1] * np.pi / 10000)

        nodo_cara_cuello2 = sg.findNode(pajaro, "cara_cuello2")
        nodo_cara_cuello2.transform = tr.rotationX(-(np.pi / 4 * controller.mousePos[1] / 1900))



        camX = 10 * np.sin(camera_theta)
        camY = 10 * np.cos(camera_theta)

        viewPos = np.array([camX, camY, 3])

        view = tr.lookAt(
            viewPos,
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )

        #axis = np.array([1, -1, 1])
        # axis = np.array([0,0,1])
        #axis = axis / np.linalg.norm(axis)
        model = tr.identity()





        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        #projection = tr.frustum(-5, 5, -5, 5, 9, 100)
        #projection = tr.ortho(-1, 1, -1, 1, 0.1, 100)
        projection = tr.perspective(45, float(width) / float(height), 0.1, 100)

        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)



        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())



        lightingPipeline = phongPipeline
        glUseProgram(lightingPipeline.shaderProgram)

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

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE, model)

        #pipeline.drawShape(gpuAxis, GL_LINES)
        sg.drawSceneGraphNode(pajaro, lightingPipeline, "model")

        glfw.swap_buffers(window)

    glfw.terminate()