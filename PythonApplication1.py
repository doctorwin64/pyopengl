import os
os.environ["SDL_VIDEO_WINDOW_POS"] = "100, 100"

import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pygame
import numpy
import pyrr
from PIL import Image

vertex_shader = """
#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texture;

uniform mat4 rotation;

out vec2 o_texture;

void main()
{
    gl_Position = rotation * vec4(position, 1.0);
    o_texture = texture;
}
"""

fragment_shader = """
#version 330 core

out vec4 color;

in vec2 o_texture;
uniform sampler2D s_texture;

void main()
{
    color = texture(s_texture, o_texture);
}
"""

if not glfw.init():
    raise Exception("GLFW was not initialized")

window = glfw.create_window(1280, 720, "Jezricor's engine", None, None)
if not window:
    raise Exception("window was not created")
    glfw.terminate()

glfw.make_context_current(window)
glfw.set_window_pos(window, 100, 100)

vertices = [
    -0.5, -0.5,  0.5,  0.0, 0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
     
    -0.5, -0.5,  0.5,  0.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
    -0.5,  0.5,  0.5,  0.0, 1.0,
    
    -0.5, -0.5, -0.5,  0.0, 0.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5, -0.5, -0.5,  1.0, 0.0,
     
    -0.5, -0.5, -0.5,  0.0, 0.0,
    -0.5,  0.5, -0.5,  0.0, 1.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
    
    -0.5, -0.5, -0.5,  0.0, 0.0,
    -0.5, -0.5,  0.5,  1.0, 0.0,
    -0.5,  0.5,  0.5,  1.0, 1.0,
     
    -0.5, -0.5, -0.5,  0.0, 0.0,
    -0.5,  0.5,  0.5,  1.0, 1.0,
    -0.5,  0.5, -0.5,  0.0, 1.0,
    
     0.5, -0.5, -0.5,  0.0, 0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
     
     0.5, -0.5, -0.5,  0.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
     0.5,  0.5, -0.5,  0.0, 1.0,
    
    -0.5,  0.5, -0.5,  0.0, 0.0,
     0.5,  0.5, -0.5,  1.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
     
    -0.5,  0.5, -0.5,  0.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
    -0.5,  0.5,  0.5,  0.0, 1.0,
    
    -0.5, -0.5, -0.5,  0.0, 0.0,
     0.5, -0.5,  0.5,  1.0, 1.0,
     0.5, -0.5, -0.5,  1.0, 0.0,
     
    -0.5, -0.5, -0.5,  0.0, 0.0,
    -0.5, -0.5,  0.5,  0.0, 1.0,
     0.5, -0.5,  0.5,  1.0, 1.0,
]

def window_size_callback(window, width, height):
    glViewport(0, 0, width, height)

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        if key:
            print(f"Key {key} is pressed")

glfw.set_window_size_callback(window, window_size_callback)
glfw.set_key_callback(window, key_callback)

vertices = numpy.array(vertices, dtype=numpy.float32)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), 
                        compileShader(fragment_shader, GL_FRAGMENT_SHADER))
glUseProgram(shader)

rotation_location = glGetUniformLocation(shader, "rotation")

position = glGetAttribLocation(shader, "position")
glEnableVertexAttribArray(position)
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 5, ctypes.c_void_p(0))

texture = glGetAttribLocation(shader, "texture")
glEnableVertexAttribArray(texture)
glVertexAttribPointer(texture, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * 5, ctypes.c_void_p(12))

ourTexture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, ourTexture)

try:
    image = Image.open("texture.jpg")
    image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    image_data = image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)
except FileNotFoundError:
    print("Texture file not found, using white texture")
    white_pixel = numpy.array([255, 255, 255, 255], dtype=numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1, 1, 0, GL_RGBA, GL_UNSIGNED_BYTE, white_pixel)

glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(1.5 * glfw.get_time())
    glUniformMatrix4fv(rotation_location, 1, GL_FALSE, pyrr.matrix44.multiply(rot_x, rot_y))
    
    glDrawArrays(GL_TRIANGLES, 0, 36)
    
    glfw.swap_buffers(window)

glfw.terminate()