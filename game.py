import pygame as pg
import sys
import random
from settings import *
from sprites import *

class Game():
	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()

	def new(self):
		# start a new game
		self.all_sprites = pg.sprite.Group()
		self.all_coins = pg.sprite.Group()
		self.player = Player(self, 15, 15)
		self.coin = Coin(self, 5, 2)
		g.run()

	def run(self):
		# game loop
		while True:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()

	def quit(self):
		sys.exit()

	def update(self):
		# game loop update
		self.all_sprites.update()
		self.player.update()
		self.all_coins.update()

	def events(self):
		# game loop events
		for event in pg.event.get():
        # check for closing window
			if event.type == pg.QUIT:
				self.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_UP or event.key == pg.K_w:
					self.player.move(0, -1)
				if event.key == pg.K_DOWN or event.key == pg.K_s:
					self.player.move(0, 1)
				if event.key == pg.K_LEFT or event.key == pg.K_a:
					self.player.move(-1)
				if event.key == pg.K_RIGHT or event.key == pg.K_d:
					self.player.move(1)
	
	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):
			pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):
			pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

	def draw(self):
		# game loop draw
		self.screen.fill(BGCOLOR)
		self.draw_grid()
		self.all_sprites.draw(self.screen)
		# flipping display after drawing
		pg.display.flip()

	def show_start_screen(self):
		pass

	def show_go_screen(self):
		pass

g = Game()
while True:
	g.new()

pg.quit()