from sgengine import physics, start, utils
from sgengine.lifecycle import Node
import sgengine
import pygame
import math

from sgengine.screen import Camera


class Player(Node):
    def start(self) -> None:
        self.sprite = pygame.image.load("assets/simpleguy_small.bmp")
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.sprite.set_colorkey((0, 0, 0))
        self.rect = self.sprite.get_rect()
        self.movement_x = [False, False]
        self.movement_y = [False, False]
        self.movement_speed = 5
        self.camera_priority = -10
        self.solid = True
        self.camera = self.find_node_by_type(Camera)
        self.gravity_settings.enabled = True
        return super().start()

    def update(self) -> None:
        ev = sgengine.event_loop().get_current_events()

        for e in ev:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    self.movement_x[0] = True  # Sinistra
                if e.key == pygame.K_d:
                    self.movement_x[1] = True  # Destra
                if e.key == pygame.K_w:
                    self.movement_y[0] = True  # Su
                if e.key == pygame.K_s:
                    self.movement_y[1] = True  # Giu
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_a:
                    self.movement_x[0] = False  # Sinistra
                if e.key == pygame.K_d:
                    self.movement_x[1] = False  # Destra
                if e.key == pygame.K_w:
                    self.movement_y[0] = False  # Su
                if e.key == pygame.K_s:
                    self.movement_y[1] = False  # Giu

        x = 0
        y = 0

        if not self.movement_x == [True, True]:
            if self.movement_x[0]:
                x = -self.movement_speed
            if self.movement_x[1]:
                x = +self.movement_speed

        if not self.movement_y == [True, True]:
            if self.movement_y[0]:
                y = -self.movement_speed
            if self.movement_y[1]:
                y = +self.movement_speed

        last_pos = self.rect.copy()
        self.rect.move_ip(x, y)

        colliding, other = physics.is_colliding(self)

        if (colliding):
            self.rect.topleft = last_pos.topleft

        self.camera.rect.center = self.rect.center

        return super().update()

class Tree(Node):
    def start(self) -> None:
        self.sprite = pygame.image.load("assets/simpletree.bmp")
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.sprite.set_colorkey((0, 0, 0))
        self.rect = self.sprite.get_rect()
        self.solid = True
        return super().start()


class Wall(Node):
    def start(self) -> None:
        self.wall = True
        self.color = (128, 128, 128)
        self.rect = pygame.Rect(0, 0, 20, 20)
        return super().start()

class FPSCamera(Camera):
    def start(self) -> None:
        self.fov = 80
        self.render_distance = 100
        self.rotation = 0
        self.rect = pygame.Rect(0, 0, 0 ,0)
        self.scan_resolution = 100

        return super().start()

    def draw_on_screen(self) -> None:

        wm = self.find_window_manager()

        if wm == None or wm.window == None:
            return


        half_fov = self.fov/2
        start_angle = int(self.rotation - half_fov)
        finish_angle = int(self.rotation + half_fov)

        origin = self.rect.center

        frame = pygame.Surface(wm.window.get_size(), flags=pygame.HWSURFACE)

        step_size = frame.get_rect().width / self.fov

        alive_nodes = sgengine.event_loop().alive_nodes()

        for i in range(start_angle, finish_angle):
            line = utils.create_line(origin, self.render_distance, i)

            lenghts = []

            for node in alive_nodes:
                if hasattr(node, "wall") and node.wall and node.rect and hasattr(node, "color") and node.color:
                    #Render vertical line
                    result = node.rect.clipline(line)
                    if result:
                        start, end = result
                        lenght = utils.line_lenght(origin, start)

                        if lenght > 0:
                            lenghts.append((lenght, node.color))
                        

            if len(lenghts) > 0:
                lenghts.sort(key=lambda l: l[0])
                closer_lenght = lenghts[0][0]
                color = lenghts[0][1]

                ratio = (closer_lenght / self.render_distance) * 100

                screen_ratio = 100 - ratio

                height_to_screen = ((screen_ratio / 100) * 400) + 30

                rect_to_draw = pygame.Rect(0, 0, step_size, height_to_screen)
                rect_to_draw.centery = frame.get_rect().centery
                rect_to_draw.left = (i - start_angle) * step_size

                frame.fill(color, rect_to_draw)

        wm.window.blit(frame, (0, 0))

class FPSPlayer(Node):
    def start(self) -> None:
        self.movement_speed = 5
        self.movement_x = [False, False]
        self.movement_y = [False, False]
        self.camera = self.find_node_by_type(FPSCamera)
        return super().start()

    def update(self) -> None:
        ev = sgengine.event_loop().get_current_events()

        for e in ev:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    self.movement_x[0] = True  # Sinistra
                if e.key == pygame.K_d:
                    self.movement_x[1] = True  # Destra
                if e.key == pygame.K_w:
                    self.movement_y[0] = True  # Su
                if e.key == pygame.K_s:
                    self.movement_y[1] = True  # Giu
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_a:
                    self.movement_x[0] = False  # Sinistra
                if e.key == pygame.K_d:
                    self.movement_x[1] = False  # Destra
                if e.key == pygame.K_w:
                    self.movement_y[0] = False  # Su
                if e.key == pygame.K_s:
                    self.movement_y[1] = False  # Giu

        x = 0
        y = 0

        if not self.movement_x == [True, True]:
            if self.movement_x[0]:
                x = -self.movement_speed
            if self.movement_x[1]:
                x = +self.movement_speed

        if not self.movement_y == [True, True]:
            if self.movement_y[0]:
                y = -self.movement_speed
            if self.movement_y[1]:
                y = +self.movement_speed


        self.camera.rotation += x

        line = utils.create_line(self.camera.rect.center, -y, self.camera.rotation)

        mx, my = end_pos = line[1]

        self.camera.rect.center = end_pos
    

        return super().update()
  