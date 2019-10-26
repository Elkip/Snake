from pygame.locals import *
import pygame
import time
from tkinter import messagebox


class Player:
    x = 10
    y = 10
    speed = 10
    direction = 0
    score = 0

    def update(self):
        if self.direction == 0:
            self.x += self.speed
        if self.direction == 1:
            self.x -= self.speed
        if self.direction == 2:
            self.y -= self.speed
        if self.direction == 3:
            self.y += self.speed

    # set the direction of snake
    def move_right(self):
        self.direction = 0

    def move_left(self):
        self.direction = 1

    def move_up(self):
        self.direction = 2

    def move_down(self):
        self.direction = 3


class App:
    windowWidth = 800
    windowHeight = 800
    player = None

    def __init__(self):
        self._running = True    # The App is running
        self._display_surf = None   # Display surface
        self._image_surf = None     # image surface
        self.player = Player()

    def on_init(self):
        pygame.init()   # Start pygame module
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        pygame.display.set_caption('SNEK')
        self._running = True
        self._image_surf = pygame.image.load("green.png").convert()    # The "Snake"

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.player.update()
        time.sleep(100/1000)
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self._display_surf.blit(self._image_surf, (self.player.x, self.player.y)) # Place player at cordinates
        pygame.display.flip()

    def on_quit(self):
        print("quiting...")
        pygame.quit()

    def game_over(self):
        message = "Your score was " + str(self.player.score)
        messagebox.showinfo("Game Over", message)

    def on_execute(self):
        # If app did not initalize properly
        if self.on_init() == False:
            self._running = False

        while self._running:
            pygame.event.pump() # get next event
            keys = pygame.key.get_pressed()

            # print('x', self.player.x, 'y', self.player.y)

            maxed_rx = (self.player.x >= self.windowWidth - 100)
            maxed_lx = (self.player.x <= 0)
            maxed_uy = (self.player.y >= self.windowHeight - 100)
            maxed_dy = (self.player.y <= 0)

            if maxed_rx or maxed_lx or maxed_uy or maxed_dy:
                self.game_over()
                self._running = False
            if keys[K_RIGHT]:
                self.player.move_right()
            if keys[K_LEFT]:
                self.player.move_left()
            if keys[K_UP]:
                self.player.move_up()
            if keys[K_DOWN]:
                self.player.move_down()
            if keys[K_ESCAPE]:
                self._running = False

            self.on_loop()
            self.on_render()

        self.on_quit()


if __name__ == "__main__":
    game = App()
    game.on_execute()
