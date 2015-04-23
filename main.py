import pygame
from Player import Player
from enemy import Enemy
from star import Star
import random
import math

if False:
	# a hint for cx_freeze
	import pygame._view

def pygame_default_font(size):
	"""Emulate the output of pygame.font.SysFont("", size), but in a way that doesn't crash if run through cx_Freeze"""

	# reduce the size to match what pygame's font.c:font_init() does
	# reportedly, this is to keep the modern pygame default font roughly the same size as that of older pygame versions.
	size = int(size * 0.6875)
	if size < 1:
		size = 1

	return pygame.font.Font("media/freesansbold.ttf", size)


print "Hello"

black = 0, 0, 0
white = 255, 255, 255
blue = 0, 0, 255

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
background = pygame.Surface(screen.get_size())
backgroundImage = pygame.image.load("media/background.png").convert()
myFont = pygame_default_font(15)

def createNewEnemy():
	r = 400*random.random() + 100
	theta = math.pi * 2 * random.random()
	return Enemy(screen, r*math.cos(theta)+width/2., r*math.sin(theta)+height/2.)

def spawnEnemy(times, index):
	now = pygame.time.get_ticks()
	if now - times[index]>= 3000:
		return createNewEnemy()
	
def createNewStar(ii):
	return Star(screen, width/4+ii*width/2, (height/2)*random.random()+(height/4))
	
def displayScore(score):
	font = pygame_default_font(30)
	scoretext = font.render("Score: "+str(score), 1, white)
	screen.blit(scoretext, (10, 10))

def displayTime(time):
	font = pygame_default_font(30)
	timetext = font.render("Time Left: "+str(time), 1, white)
	screen.blit(timetext, (650, 10))

player = Player(screen, width/2., height/2.)
nEnemies = 5
enemy = []
times = []
for ii in range(nEnemies):
	enemy.append(createNewEnemy())
	times.append(pygame.time.get_ticks())

stars = []
for ii in range(2):
	stars.append(createNewStar(ii))
	
	
spriteGroup = pygame.sprite.Group()

spriteGroup.add(player)

clock = pygame.time.Clock()
running = True
nframes = 0
while running:

	direction = ''

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pressedKey = pygame.key.get_pressed()
	if pressedKey[pygame.K_UP]:
		direction += 'U'
	if pressedKey[pygame.K_DOWN]:
		direction += 'D'
	if pressedKey[pygame.K_LEFT]:
		direction += 'L'
	if pressedKey[pygame.K_RIGHT]:
		direction += 'R'
		
	pygame.event.pump()
	screen.blit(backgroundImage, [0,0])
	
	#spriteGroup.clear(screen, background)
	player.blit()
	player.update(direction)
	for ii in range(2):
		stars[ii].blit()
		
	for ii in range(nEnemies):
		if enemy[ii]:
			enemy[ii].blit()
			enemy[ii].update(player.x, player.y)
			colBH = pygame.sprite.collide_rect(enemy[ii], player)
			if colBH == True:
				player.score += 1
				times[ii] = pygame.time.get_ticks()
				enemy[ii] = None
			
				break
			for jj in range(2):
				colStar = pygame.sprite.collide_rect(enemy[ii], stars[jj])
				if colStar == True:
					player.score += 10
					enemy[ii] = createNewEnemy()
		else:
			enemy[ii] = spawnEnemy(times, ii)
	displayScore(player.score)
	displayTime(60-int(nframes/60.))
	clock.tick(60)
	if nframes/60 > 60:
		fontGO = pygame_default_font(60)
		fontScore = pygame_default_font(40)
		gameOverText = fontGO.render("Game Over", 1, white)
		screen.blit(gameOverText, (285, 300))
		scoretext = fontScore.render("Final Score: "+str(player.score), 1, white)
		screen.blit(scoretext, (303, 340))
		pygame.display.flip()
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
						
	pygame.display.flip()
	nframes += 1

			
			
sys.exit()
