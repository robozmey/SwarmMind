import random

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import pygame
import math


field_width = 1600 #3200
field_height = 900 #1800

screen_width = 1600
screen_height = 900


def to_screen_coordinates(x, y):
    return ((x + field_width/2) * field_width * 0.9 / screen_width, (y + field_height/2) * field_height * 0.9 / screen_height)


class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_alive = True

    def step(self):
        pass

    def see_around(self):
        pass

    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def direction_to(self, other):
        return math.atan2(other.y - self.y, other.x - self.x)

class Worker(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.distance_to_food = 0
        self.distance_to_queen = 0
        self.speed = 3 + 1 * (2 * random.random() - 1)
        self.is_holding_food = False
        self.direction = math.pi*2 * random.random()
        self.see_radius = 50
        self.life_time = 1000 * random.random()
        self.type = random.random() > 0.5

    def draw(self):
        if self.is_holding_food:
            pygame.draw.circle(screen, (255 * self.type, 0, 255 * (1 - self.type)), to_screen_coordinates(self.x, self.y), 2)
        else:
            pygame.draw.circle(screen, (0, 128, 0), to_screen_coordinates(self.x, self.y), 2)

    def step(self):
        self.x = self.x + self.speed * math.cos(self.direction)
        self.y = self.y + self.speed * math.sin(self.direction)
        self.distance_to_queen += 20
        self.distance_to_food += 20

        self.direction += 0.1 * (random.random() - 0.5)

        self.life_time -= 0

        if self.life_time < 0 or abs(self.x) >= screen_width * 0.45 or abs(self.y) >= screen_height * 0.45:
            self.is_alive = False

    def see_around(self):

        for object in objects:
            if type(object) is Queen and self.distance_to(object) <= object.size:
                self.distance_to_queen = 0
                if self.is_holding_food:
                    self.direction += math.pi
                    self.is_holding_food = False
                    object.add_food()

            if type(object) is Food and self.distance_to(object) <= object.size and self.type == object.type:
                self.distance_to_food = 0
                if not self.is_holding_food:
                    self.direction += math.pi
                    self.is_holding_food = True

            if type(object) is Worker and self.distance_to(object) <= self.see_radius:
                if self.distance_to_food > object.distance_to_food + self.see_radius and self.type == object.type:
                    self.distance_to_food = object.distance_to_food + self.see_radius
                    pygame.draw.line(screen, (128, 10, 0), to_screen_coordinates(self.x, self.y), to_screen_coordinates(object.x, object.y))
                    if not self.is_holding_food:
                        self.direction = self.direction_to(object)

                if self.distance_to_queen > object.distance_to_queen + self.see_radius:
                    self.distance_to_queen = object.distance_to_queen + self.see_radius
                    pygame.draw.line(screen, (10, 128, 0), to_screen_coordinates(self.x, self.y), to_screen_coordinates(object.x, object.y))
                    if self.is_holding_food:
                        self.direction = self.direction_to(object)

        if self.distance_to_queen > 1000 and random.random() < 0:

            objects.append(Queen(self.x, self.y))
            self.is_alive = False





class Queen(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.direction = random.random() * math.pi * 2
        self.speed = 0.5
        self.satiety = 30
        self.size = 3 + min(self.satiety, 120) / 10

    def draw(self):
        pygame.draw.circle(screen, (0, 255, 0), to_screen_coordinates(self.x, self.y), self.size)

    def add_food(self):
        self.satiety = min(self.satiety+3, 60)

        self.size = 3 + max(self.satiety, 120) / 10

        if self.satiety >= 60 and random.random() < 0.01:
            self.satiety -= 10
            objects.append(Worker(self.x, self.y + self.size))

    def step(self):
        if random.random() < 0.01:
            self.direction = random.random() * math.pi * 2

        self.satiety = max(self.satiety - 0.05, 0)
        self.size = 3 + max(self.satiety, 120) / 10

        self.x = self.x + self.speed * math.cos(self.direction)
        self.y = self.y + self.speed * math.sin(self.direction)

        if self.x < -screen_width/3:
            self.direction += math.pi

        if self.x > screen_width/3:
            self.direction += math.pi

        if self.y < -screen_height/3:
            self.direction += math.pi

        if self.y > screen_height/3:
            self.direction += math.pi

        if self.satiety == 0:
            self.is_alive = False


class Food(Unit):
    def __init__(self, x, y, type):
        super().__init__(x, y)
        self.size = 20
        self.type = type

    def draw(self):
        pygame.draw.circle(screen, (255 * self.type, 0, 255 * (1 - self.type)), to_screen_coordinates(self.x, self.y), self.size)


objects = []


def update():
    global objects


if __name__ == '__main__':

    objects += [Queen(0, 0), Food(-200, -200, 1), Food(200, 200, 1), Food(-200, 200, 0), Food(200, -200, 0)]

    objects += [Worker(random.random() * field_width * 0.8 - field_width / 2 * 0.8 , random.random() * field_height * 0.8 - field_height / 2 * 0.8 ) for i in range(400)]

    # Simple pygame program

    # Import and initialize the pygame library

    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([screen_width, screen_height])

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill((0, 0, 0))

        # Draw a solid blue circle in the center

        for object in objects:
            object.see_around()

        for object in objects:
            object.step()

        for object in objects:
            object.draw()

        for object in objects:
            if not object.is_alive:
                objects.remove(object)



        # Flip the display
        pygame.display.flip()

        time.sleep(0.002)

    # Done! Time to quit.
    pygame.quit()






