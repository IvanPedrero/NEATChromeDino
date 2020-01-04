import pygame
import neat
import time
import os
import random
import time


DINO_IMGS = [	pygame.image.load(os.path.join("img", "run1.png")),
				pygame.image.load(os.path.join("img", "run2.png")),
				pygame.image.load(os.path.join("img", "run3.png")),
				pygame.image.load(os.path.join("img", "run4.png"))]

DINO_CROUCH_IMGS = [	pygame.image.load(os.path.join("img", "low1.png")),
						pygame.image.load(os.path.join("img", "low2.png")),
						pygame.image.load(os.path.join("img", "low3.png"))]

CACTUS_IMGS = [	pygame.image.load(os.path.join("img", "cactus1.png")),
				pygame.image.load(os.path.join("img", "cactus2.png")),
				pygame.image.load(os.path.join("img", "cactus3.png")),
				pygame.image.load(os.path.join("img", "cactus4.png")),
				pygame.image.load(os.path.join("img", "cactus5.png"))]

PTERO_IMGS = [	 pygame.transform.scale(pygame.image.load(os.path.join("img", "enemy1.png")), (50, 30)),
				 pygame.transform.scale(pygame.image.load(os.path.join("img", "enemy2.png")), (50, 30)),
				 pygame.transform.scale(pygame.image.load(os.path.join("img", "enemy3.png")), (50, 30)) ]

FLOOR_IMG = pygame.image.load(os.path.join("img", "floor.png"))

BUTTON_IMG = pygame.image.load(os.path.join("img", "restart.png"))

WIN_WIDTH = 591
WIN_HEIGHT = 500

GLOBAL_VEL = 7
GEN = 0
BEST_SCORE = 0

pygame.init()
pygame.font.init()
pygame.display.set_icon(DINO_IMGS[0])
pygame.display.set_caption('AI learns Chrome Dino Game')
STAT_FONT = pygame.font.Font(os.path.join("font", "pixelmix.ttf"), 15)


class Dino:

	IMGS = DINO_IMGS
	IMGS_CROUCH = DINO_CROUCH_IMGS
	MAX_ROTATION = 25
	ROT_VEL = 20
	ANIMATION_TIME = 5
	t_end = 0

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]
		self.isJump = False
		self.isCrouch = False
		self.jumpCount = 10

	def jump(self):
		self.isJump = True

	def crouch(self):		
		self.isCrouch = True

	def end_crouch(self):
		self.isCrouch = False

	def move(self):
		if self.isJump:
			if self.jumpCount >= -10:
				self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.3
				self.jumpCount -= 1
			else:
				self.jumpCount = 10
				self.isJump = False
				self.img = self.IMGS[2]
				self.img_count = self.ANIMATION_TIME*4

	def draw(self, win):
		self.img_count += 1

		if not self.isCrouch:
			if self.img_count < self.ANIMATION_TIME:
				self.img = self.IMGS[0]
			elif self.img_count < self.ANIMATION_TIME*2:
				self.img = self.IMGS[1]
			elif self.img_count < self.ANIMATION_TIME*3:
				self.img = self.IMGS[2]
			elif self.img_count < self.ANIMATION_TIME*4:
				self.img = self.IMGS[1]
			elif self.img_count == self.ANIMATION_TIME*4 + 1:
				self.img = self.IMGS[0]
				self.img_count = 0			

		else:
			if self.img_count < self.ANIMATION_TIME:
				self.img = self.IMGS_CROUCH[0]
			elif self.img_count < self.ANIMATION_TIME*2:
				self.img = self.IMGS_CROUCH[1]
			elif self.img_count < self.ANIMATION_TIME*3:
				self.img = self.IMGS_CROUCH[2]
			elif self.img_count < self.ANIMATION_TIME*4:
				self.img = self.IMGS_CROUCH[1]
			elif self.img_count == self.ANIMATION_TIME*4 + 1:
				self.img = self.IMGS_CROUCH[0]
				self.img_count = 0

		if self.isJump:
			self.img = self.IMGS[3]

		win.blit(self.img, (self.x ,self.y))

	def get_mask(self):
		return pygame.mask.from_surface(self.img)


class Cactus:

	VEL = GLOBAL_VEL
	GAP = 500

	def __init__(self, x, y):
		self.x = x
		self.y = y

		self.CACTUS = CACTUS_IMGS[random.randrange(0, 5)]
		self.alreadySpawnedCactus = False
		self.passed = False

	def move(self):
		self.x -= self.VEL

	def draw(self, win):
		win.blit(self.CACTUS, (self.x, self.y))

	def collide(self, dino):
		dino_mask = dino.get_mask()
		cactus_mask = pygame.mask.from_surface(self.CACTUS)

		offset = (self.x - dino.x, self.y - round(dino.y))

		b_point = dino_mask.overlap(cactus_mask, offset)

		if b_point:
			return True
		else:
			return False


class Ptero:

	VEL = GLOBAL_VEL
	GAP = 500
	ANIMATION_TIME = 5
	IMGS = PTERO_IMGS

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.img = self.IMGS[0]
		self.img_count = 0
		self.alreadySpawnedPtero = False
		self.passed = False

	def move(self):
		self.x -= self.VEL

	def draw(self, win):
		self.img_count += 1
		if self.img_count < self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*3:
			self.img = self.IMGS[2]
		elif self.img_count < self.ANIMATION_TIME*4:
			self.img = self.IMGS[1]
		elif self.img_count == self.ANIMATION_TIME*4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0
			
		win.blit(self.img, (self.x ,self.y))

	def collide(self, dino):
		dino_mask = dino.get_mask()
		cactus_mask = pygame.mask.from_surface(self.img)

		offset = (self.x - dino.x, self.y - round(dino.y))

		b_point = dino_mask.overlap(cactus_mask, offset)

		if dino.isCrouch:
			return False

		if b_point:
			return True
		else:
			return False


class Floor:

	VEL = GLOBAL_VEL
	WIDTH = FLOOR_IMG.get_width()
	IMG = FLOOR_IMG

	def __init__(self, y):
		self.y = y
		self.x1 = 1
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

	def draw(self, win):
		win.blit(self.IMG, (self.x1 ,self.y))
		win.blit(self.IMG, (self.x2 ,self.y))


class Button:

	IMG = BUTTON_IMG

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def collide(self, mouse_pos):
		return True

	def draw(self, win):
		win.blit(self.IMG, (self.x, self.y))


def draw_window(win, dinos, floor, cactuses, pteros, score, best_score, gen, alive, restart_button):

	# Display general information.
	text = STAT_FONT.render("Score : " + str(score), 1, (0, 0, 0))
	win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

	text = STAT_FONT.render("Best : " + str(best_score), 1, (0, 0, 0))
	win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 60))

	text = STAT_FONT.render("Generation : " + str(gen), 1, (0, 0, 0))
	win.blit(text, (10, 10))

	text = STAT_FONT.render("Alive : " + str(alive), 1, (0, 0, 0))
	win.blit(text, (10, 60))

	# Draw a restart button.
	restart_button.draw(win)

	# Draw the floor.
	floor.draw(win)

	# Draw all the catuses.
	for cactus in cactuses:
		cactus.draw(win)

	# Draw all the pteros.
	for ptero in pteros:
		ptero.draw(win)

	# Draw all the dinos.
	for dino in dinos:
		dino.draw(win)

	# Update the frames.
	pygame.display.update()


def main(genomes, config):

	# Keep track of generations.
	global GEN
	GEN += 1

	#Keep track of the best score.
	global BEST_SCORE

	# Neural network variables.
	nets = []
	ge = []
	dinos = []

	# Reset variables.
	global GLOBAL_VEL
	vel_multiplier = 1
	GLOBAL_VEL = 5

	# Create the network and birds for each genome. 
	for _, g in genomes:
		# Add the genome to the network.
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		# Create the dinos.
		dinos.append(Dino(40, 410 - DINO_IMGS[0].get_height()))
		# Set the fitness and add to the genome list.
		g.fitness = 0
		ge.append(g)

	# Create restart button.
	restart_button = Button(WIN_WIDTH/2, 10)

	# Create the first cactus.
	cactuses = [Cactus(WIN_WIDTH + 20, 410 - DINO_IMGS[0].get_height())]
	#Create the first ptero.
	pteros = [Ptero(WIN_WIDTH + 250, 390 - DINO_IMGS[0].get_height())]
	# Create the floor.
	floor = Floor(400)

	# Create the window.
	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	# Create the clock.
	clock = pygame.time.Clock()

	# Gameplay variables.
	score = 0
	vel_multiplier = 1
	run = True

	while run:
		# 30 fps.
		clock.tick(30)

		# Event handling.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				mouse = pygame.mouse.get_pos()
				if restart_button.collide(mouse):
					print("restart")


		# Move the dinos according the neural network if alive.
		cactus_ind = 0
		ptero_ind = 0
		# if there are dinos alive...
		if len(dinos) > 0:
			# If the dino passed the cactus...
			if len(cactuses) > 1 and dinos[0].x > cactuses[0].x + cactuses[0].CACTUS.get_width():
				#Let it be a secondary cactus...
				cactus_ind = 1
			# If the dino passed the pterodactyl...
			if len(pteros) > 1 and dinos[0].x > pteros[0].x + pteros[0].img.get_width():
				#Let it be a secondary pterodactyl..
				ptero_ind = 1
		else:
			run = False
			break

		for x, dino in enumerate(dinos):
			dino.move()
			# For each second, the dino will gain 30 fitness.
			ge[x].fitness += 0.1

			# If there are pterodactyls on the screen...
			if len(pteros) > 0:
				# Output of the nerual network. It will activate IF the dino is close to the cactus.
				output = nets[x].activate((dino.x, abs(dino.x - pteros[ptero_ind].x)))				
				# Two output neurons for pterodactyl decision.
				if output[0] > 0.2:
					dino.crouch()
				if output[1] > 0.5:
					dino.end_crouch()

			#If there are cactuses on the screen...
			if len(cactuses) > 0:
				# Output of the nerual network. It will activate IF the dino is close to the cactus.
				output = nets[x].activate((dino.x, abs(dino.x - cactuses[cactus_ind].x)))				
				# Output neuron to know if cactus is near.
				if output[0] > 0.5:
					dino.jump()

		# Generation of cactuses/pteros needs a flag to know if scored a point.
		add_cactus = False
		add_ptero = False

		# Lists to remove the cactus/ptero if passed.
		rem = []
		rem_ptero = []

		# Cactus management in-game.
		for cactus in cactuses:
			cactus.VEL = GLOBAL_VEL
			for x, dino in enumerate(dinos):
				# If a dino collided with a cactus...
				if cactus.collide(dino):
					# Remove the fitness for the one who died.
					ge[x].fitness -= 2
					# Remove from the list the ones who died.
					dinos.pop(x)
					nets.pop(x)
					ge.pop(x)

				if not cactus.passed and cactus.x < dino.x:
					cactus.passed = True
					add_cactus = True
			
			if cactus.x + cactus.CACTUS.get_width() < 0:
				rem.append(cactus)

			cactus.move()

		# Pterodactyl management in-game.
		for ptero in pteros:
			ptero.VEL = GLOBAL_VEL
			for x, dino in enumerate(dinos):
				# If a dino collided with a pterodactyl...
				if ptero.collide(dino):
					# Remove the fitness for the one who died.
					ge[x].fitness -= 2
					# Remove from the list the ones who died.
					dinos.pop(x)
					nets.pop(x)
					ge.pop(x)

				if not ptero.passed and ptero.x < dino.x:
					ptero.passed = True
					add_ptero = True
			
			if ptero.x + ptero.img.get_width() < 0:
				rem_ptero.append(ptero)

			ptero.move()

		
		if add_cactus or add_ptero:
			# Add to the score.
			score += 1

			# Save the best score.
			if score > BEST_SCORE:
				BEST_SCORE = score

			# The birds passed alive and safe.
			for g in ge:
				# Add fitness to the alive birds.
				g.fitness += 5

			# Add more velocity when got 5 or more points.
			if score > (5 * vel_multiplier) - 1:
				vel_multiplier += 1
				GLOBAL_VEL += 1
				floor.VEL = GLOBAL_VEL

			# 40% chance to spawn a pterodactyl.
			if random.random() < 0.4:
				pteros.append(Ptero(WIN_WIDTH + random.randrange(120, 150), 390 - DINO_IMGS[0].get_height()))
			else:
				cactuses.append(Cactus(WIN_WIDTH + random.randrange(120, 200), 410 - DINO_IMGS[0].get_height()))

		# Remove the passed obstacles from the lists.
		for r in rem:
			cactuses.remove(r)
		for r in rem_ptero:
			pteros.remove(r)

		# Move the floor.
		floor.move()

		# Set a white background
		win.fill((255,255,255))

		# Draw the game.
		draw_window(win, dinos, floor, cactuses, pteros, score, BEST_SCORE, GEN, len(dinos), restart_button)


# AI Functions:
def run(config_path):
	# Configure according to the file.
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

	# Set the population.
	p = neat.Population(config)

	# See the report of the network.
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	# Fitness function and how many generations will be created.
	# The fitness function will be main() and we want 50 generation.
	winner = p.run(main, 50)

if __name__ == '__main__':
	# Get the path we are in and load the config fil.
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config-feedforward.txt")
	run(config_path)
