import pygame as pg
from settings import *
import random
import time


class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((TILESIZE, TILESIZE))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y

	def move(self, dx=0, dy=0):
		self.x += dx
		self.y += dy

	def check_collision(self):
		pass

	def update(self):
		self.rect.x = self.x * TILESIZE
		self.rect.y = self.y * TILESIZE

class Coin(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.all_coins
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.image.load('coin.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y

	def update(self):
		self.rect.x = self.x * TILESIZE+COINOFFSET
		self.rect.y = self.y * TILESIZE+COINOFFSET