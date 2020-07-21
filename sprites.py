import pygame as pg
from settings import *
import random
import time


class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y, hp, prot, atk):
		#PYGAME
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((TILESIZE, TILESIZE))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y

		#Player attr
		self.hp = hp
		self.prot = prot
		self.hp_max = hp
		self.prot_max = prot
		self.atk = atk
		self.armor = {'head': None, 'chest': None, 'legs': None, 'feet': None}
		self.weapon = None
		self.p_coins = 0
		

	def move(self, dx=0, dy=0):
		if self.game.inventory.display_inventory != True:
			self.x += dx
			self.y += dy
			self.check_collision()

	def addHp(self, hp_gain):
		self.hp += hp_gain
		if self.hp > self.hp_max:
			self.hp = self.hp_max

	def addProt(self, prot_gain):
		self.prot += prot_gain
		if self.prot > self.prot_max:
			self.prot = self.prot_max

	def equip_armor(armor, slot):
		if self.armor[slot] != None:
			self.unequip_armor(slot)
		self.armor[slot] = armor
		self.prot += armor.prot

	def unequip_armor(slot):
		if self.armor[slot] != None:
			self.prot -= self.armor[slot].prot
			self.armor[slot] = None

	def equip_weapon(weapon):
		if self.weapon != None:
			self.unequip_weapon()
		self.weapon = weapon
		self.atk += weapon.atk

	def unequip_weapon():
		if self.weapon != None:
			self.atk -= self.weapon.atk
			self.weapon = None

	def check_collision(self):
		self.check_coin()

	def check_coin(self):
		if self.x == self.game.coin.x and self.y == self.game.coin.y:
			self.add_coin()
			self.game.new_coin()

	def add_coin(self):
		self.p_coins += 10

	def update(self):
		self.rect.x = self.x * TILESIZE
		self.rect.y = self.y * TILESIZE


class Coin(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.all_coins
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.image.load('img/coin.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y

	def update(self):
		self.rect.x = self.x * TILESIZE+COINOFFSET
		self.rect.y = self.y * TILESIZE+COINOFFSET