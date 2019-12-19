from pygame.locals import *
import pygame
import time
from tkinter import messagebox
from random import randint


class Apple:
    x = 0
    y = 0
    step = 10

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class Player:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3

    updateCountMax = 2  # Max number of times for growth
    updateCount = 0  # How many times snake has updated

    def __init__(self, length):
        self.length = length
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)

        # initial position no collision
        self.x[1] = 1 * 44
        self.x[2] = 2 * 44

    def update(self):
        self.updateCount = self.updateCount + 1

        if self.updateCount > self.updateCountMax:
            # update previous position
            for i in range(self.length - 1, 0, -1):
                # print("self.x[" + str(i) + "] = self.x[" + str(i - 1) + "]")
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            # Update head of snake
            if self.direction == 0:
                self.x[0] += self.step
            if self.direction == 1:
                self.x[0] -= self.step
            if self.direction == 2:
                self.y[0] -= self.step
            if self.direction == 3:
                self.y[0] += self.step

            self.updateCount = 0

    # set the direction of snake
    def move_right(self):
        self.direction = 0

    def move_left(self):
        self.direction = 1

    def move_up(self):
        self.direction = 2

    def move_down(self):
        self.direction = 3

    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))


class Game:
    # Check to see if block matches another block pos. bsize is block size
    def isCollision(self, x1, x2, y1, y2, bsize):
        if x2 <= x1 <= x2 + bsize:
            if y2 <= y1 <= y2 + bsize:
                return True
        return False


class App:
    windowWidth = 800
    windowHeight = 600
    player = None
    apple = None

    def __init__(self):
        self._running = True  # The App is running
        self._display_surf = None  # Display surface
        self._image_surf = None  # image surface
        self._apple_surf = None
        self.player = Player(10)
        self.apple = Apple(5, 5)
        self.game = Game()

    def on_init(self):
        pygame.init()  # Start pygame module
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('SNEK')
        self._running = True
        self._image_surf = pygame.image.load("green.png").convert()  # The "Snake"
        self._apple_surf = pygame.image.load("red.png").convert()  # The "Apple"

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.player.update()
        # If the snake eats the apple
        for i in range(0, self.player.length):
            if self.game.isCollision(self.apple.x, self.player.x[i], self.apple.y, self.player.y[i], 44):
                self.apple.x = randint(2, 9) * 44
                self.apple.y = randint(2, 9) * 44
                print("Hungry for apples?")
                self.player.length += 1
        # If the snake collides with itself
        for i in range(2, self.player.length):
            if self.game.isCollision(self.player.x[0], self.player.x[i], self.player.y[0], self.player.y[i], 40):
                print("YOU LOSE")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                self.game_over()
        time.sleep(100 / 1000)
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.player.draw(self._display_surf, self._image_surf)  # Place player
        self.apple.draw(self._display_surf, self._apple_surf)  # Place apple
        pygame.display.flip()

    def on_quit(self):
        print("quiting...")
        pygame.quit()

    def game_over(self):
        message = "Your score was " + str(self.player.length)
        messagebox.showinfo("Game Over", message)
        exit(0)

    def on_execute(self):
        # If app did not initalize properly
        if self.on_init() == False:
            self._running = False

        while self._running:
            pygame.event.pump()  # get next event
            keys = pygame.key.get_pressed()

            # print('x', self.player.x[0], 'y', self.player.y[0])

            maxed_rx = (self.player.x[0] > self.windowWidth)
            maxed_lx = (self.player.x[0] < 0)
            maxed_uy = (self.player.y[0] > self.windowHeight)
            maxed_dy = (self.player.y[0] < 0)

            if maxed_rx or maxed_lx or maxed_uy or maxed_dy:
                self.game_over()

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
