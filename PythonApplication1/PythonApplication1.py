import glfw
from OpenGL.GL import *
import numpy
from OpenGL.GL.shaders import compileProgram, compileShader

vertex_shader = """
#version 330 core

in vec3 position;
in vec3 v_color;

out vec3 o_color;

void main()
{
	gl_Position = vec4(position, 1.0);
	o_color = v_color;
}
"""

fragment_shader = """
#version 330 core

in vec3 o_color;
out vec4 color;

void main()
{
	color = vec4(o_color, 1.0);
}
"""

if not glfw.init():
	raise Exception("GLFW was not initialized")
	glfw.terminate()

window = glfw.create_window(1280, 720, "Jezricor's engine", None, None)
if not window:
	raise Exception("window was not created")
	glfw.terminate()

glfw.make_context_current(window)

vertices = [
	-0.5, -0.5, 0.0,
	0.0, 0.5, 0.0,
	0.5, -0.5, 0.0,
	1.0,  0.0, 0.0,
    0.0,  1.0, 0.0,
    0.0,  0.0, 1.0
	]

vertices = numpy.array(vertices, dtype=numpy.float32)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), compileShader(fragment_shader, GL_FRAGMENT_SHADER))
glUseProgram(shader)

position = glGetAttribLocation(shader, "position")
glEnableVertexAttribArray(position)
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))

color = glGetAttribLocation(shader, "v_color")
glEnableVertexAttribArray(color)
glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(36))

glClearColor(0, 0.1, 0.1, 1)

while not glfw.window_should_close(window):
	glfw.poll_events()
	glClear(GL_COLOR_BUFFER_BIT)
	glDrawArrays(GL_TRIANGLES, 0, 3)
	glfw.swap_buffers(window)

glfw.terminate()