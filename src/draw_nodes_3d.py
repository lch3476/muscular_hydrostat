import OpenGL.GL as gl
import OpenGL.GLU as glu
import pygame
import sys


class NodeDrawer3D:
    def __init__(self, structure, dt=0.02):
        self.structure = structure
        self.dt = dt

        pygame.init()

        display = (800, 600)
        self.screen = pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
        self.fps = 1 / self.dt
        self.clock = pygame.time.Clock()
        self.running = True

        glu.gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
        gl.glTranslatef(0.0, 0.0, -10)
        gl.glRotatef(20, 1, 0, 0)

        # pygame control parameters
        self.orbiting = False

    def main_loop(self, simulating=True):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # gl.glRotatef(1, 0, 1, 0)  # orbit view
                        _, _, _ = self.structure.calc_next_states(0.03)
                        print(self.structure.constraints())
                        # print(self.structure.jacobian())
                        # print(self.structure.jacobian_derivative())

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:
                        self.orbiting = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 2:
                        self.orbiting = False
                if event.type == pygame.MOUSEMOTION:
                    if self.orbiting:
                        gl.glRotatef(event.rel[0], 0, 1, 0)
                        # gl.glRotatef(event.rel[1], 1, 0, 0)
                if event.type == pygame.MOUSEWHEEL:
                    gl.glTranslatef(0.0, 0.0, event.y)

            # gl.glRotatef(1, 0, 1, 0)  # orbit view
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

            if simulating:
                _, _, _ = self.structure.calc_next_states(self.dt)
            self.draw_structure()

            actual_fps = self.clock.get_fps()
            # print("Actual FPS:", actual_fps)
            # print("positions:", self.structure.positions)

            pygame.display.flip()
            self.clock.tick(self.fps)

    def draw_structure(self):
        gl.glBegin(gl.GL_LINES)
        for edge in self.structure.edges:
            for vertex in edge:
                gl.glVertex3fv(self.structure.positions[vertex])
        gl.glEnd()