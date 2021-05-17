import pygame
from Colors import *
import math

# initialize pygame
pygame.init()

# screen size
WIDTH, HEIGHT = 1920, 1080

# how many frames per second the game should run at
FPS = 60

# global variables
global WIN
global clock
global time

class Wave:
	def __init__(self, frequency, amplitude, center, radius):
		self.frequency = frequency
		self.amplitude = amplitude
		self.center = center
		self.radius = self.amplitude * radius
		self.node_pos = (self.center[0] + self.radius, self.center[1])

	def update(self):
		# polar to cartesian
		x = self.radius * math.cos(self.frequency * time)
		y = self.radius * math.sin(self.frequency * time)
		self.node_pos = (self.center[0] + x, self.center[1] + y)

	def draw_wave(self):
		# draw the circle at the circle center with a radius and don't fill it in
		pygame.draw.circle(WIN, WHITE, self.center, self.radius, width=1)

		# draw the radius from the center to the node_pos
		pygame.draw.line(WIN, GRAY, self.center, self.node_pos)

		# draw the node with a radius of 5 on the circle at the node position and fill it in
		pygame.draw.circle(WIN, WHITE, self.node_pos, radius=3, width=0)	

	def get_frequency(self):
		return self.frequency

	def get_amplitude(self):
		return self.amplitude	

	def get_center(self):
		return self.center

	def get_radius(self):
		return self.radius

	def get_node_pos(self):
		return self.node_pos

	def set_frequency(self, frequency):
		self.frequency = frequency

	def set_amplitude(self, amplitude):
		self.amplitude = amplitude		

	def set_center(self, center):
		self.center = center	

	def set_radius(self, radius):
		self.radius = radius	

	def set_node_pos(self, node_pos):
		self.node_pos = node_pos	

	def __repr__(self):
		return f"freq: {self.frequency}, amplitude: {self.amplitude}, radius: {self.radius}"


def draw(waves, fourier):
	# point width for the fourier
	point_width = 1

	# fill the screen with a white background to reset it
	WIN.fill(BLACK)

	# draw all of the waves and their points
	for w in waves:
		w.draw_wave()

	# draw line from last wave node to 
	last_npos = get_last_wave_node(waves)
	pygame.draw.line(WIN, RED, last_npos, (WIDTH // 2, last_npos[1]))

	# shift all the points over by point width so that the entire approximation moves
	for i in range(len(fourier)):
		point = fourier[i]
		fourier[i] = (point[0] + point_width, point[1])

	# draw all the point in the fourier approximation
	for i in range(len(fourier)):
		# when there is more than 1 point, and we aren't looking at the last point, and the point is on the screen, draw it
		if len(fourier) > 1 and i != len(fourier) - 1 and fourier[i][0] <= WIDTH:
			pygame.draw.line(WIN, GREEN, fourier[i], fourier[i+1])

	# update the screen to show changes
	pygame.display.update()


def get_last_wave_node(waves):
	return waves[-1].get_node_pos()


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
	n = 40

	# waves to be used in the fourier
	waves = []

	# approximate the fourier series as a string of points
	fourier = []
	fourier_num_points = 1400

	# radius for the circles to be multiplied against their amplitudes
	radius = 200

	# start frequency for the waves
	freq = 1

	# make all the waves
	for i in range(n):
		if i == 0:
			w = Wave(frequency=freq, amplitude=(4.0 / (math.pi * freq)), center=(WIDTH // 5,HEIGHT // 2), radius=radius)
		else:
			w = Wave(frequency=freq, amplitude=(4.0 / (math.pi * freq)), center=waves[i-1].get_node_pos(), radius=radius)
		
		# add the wave and print it
		waves.append(w)
		print(f"wave {i}: {w}")

		# update and frequency, and therefore the amplitude
		freq += 2

	# game loop
	while run:
		time += 1.0/FPS

		# caps the framerate at value of FPS to control how many times this while loop happens per second
		clock.tick(FPS)

		# loop through all game events
		for event in pygame.event.get():
			# stop the game loop
			if event.type == pygame.QUIT:
				run = False

		# update all the waves center points besides the first one
		for i in range(len(waves)):
			if i != 0:
				waves[i].set_center(waves[i-1].get_node_pos())
			waves[i].update()

		# get the last node position
		last_npos = get_last_wave_node(waves)

		# add the point to where it starts at the tip of the red line(3/8 of the screen from the left)
		last = (WIDTH // 2, last_npos[1])
		fourier.append(last)

		# if there are too many points in the wave, start removing them from the beginning(the right of the fourier)
		# since we are adding new ones to the end(the left of the fourier)
		if len(fourier) > fourier_num_points:
			fourier.pop(0)

		# draw all the waves and the fourier
		draw(waves, fourier)

	# quit the pygame
	pygame.quit()


if __name__ == "__main__":
	main()