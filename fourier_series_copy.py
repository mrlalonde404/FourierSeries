import pygame
from Colors import *
import random
import math

pygame.init()

# screen size
WIDTH, HEIGHT = 1000, 1000


# how many frames per second the game should run at
FPS = 60

# global variables
global WIN
global clock
global time


def draw(n_waves):
	# fill the screen with a white background to reset it
	WIN.fill(BLACK)

	x = WIDTH // 4
	y = HEIGHT // 2
	center = (x, y)
	node_pos = None
	radius = 200
	freq = 1

	# draw all of the waves and their points
	for w in range(n_waves):
		if w == 0:
			node_pos = (center[0] + (radius * math.cos(freq * time)), center[1] + (radius * math.sin(freq * time)))
		else:
			center = node_pos
			node_pos = (center[0] + (radius * math.cos(freq * time)), center[1] + (radius * math.sin(freq * time)))
		# draw the circle at the circle center with a radius and don't fill it in
		pygame.draw.circle(WIN, WHITE, center, radius, width=1)

		# draw the radius from the center to the node_pos
		pygame.draw.line(WIN, GRAY, center, node_pos)

		# draw the node with a radius of 5 on the circle at the node position and fill it in
		if w != n_waves-1:
			pygame.draw.circle(WIN, WHITE, node_pos, radius=3, width=0)
		else:
			pygame.draw.circle(WIN, BLUE, node_pos, radius=3, width=0)

		radius = radius // 2	

		freq += 2

	# update the screen to show changes
	pygame.display.update()


def main():
	global clock
	global WIN
	global FPS
	global time

	time = 0.0

	# make a clock object to control FPS
	clock = pygame.time.Clock()

	# bool to keep track of when the game loop should stop running
	run = True

	# make the pygame display
	WIN = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Fourier series")

	# number of waves to approximate
	n = 5

	# game loop
	while run:
		# caps the framerate at value of FPS to control how many times this while loop happens per second
		clock.tick(FPS)
		time += 1.0/FPS

		# loop through all game events
		for event in pygame.event.get():
			# stop the game loop
			if event.type == pygame.QUIT:
				run = False

		# draw the windows and the waves
		draw(n)

	pygame.quit()


if __name__ == "__main__":
	main()