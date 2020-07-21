import pygame as pg
from settings import *
import random
import time

class Inventory:
	def __init__(self, totalSlots, cols, rows):
		self.totalSlots = totalSlots
		self.rows = rows
		self.cols = cols
		self.slots = []
		self.displayInventory = False

		while len(self.slots) != self.totalSlots:
			for x in range(WIDTH//2 - ((INVTILESIZE+2) * self.cols)//2, WIDTH//2 + ((INVTILESIZE+2) * self.cols) //2, INVTILESIZE+2):
				for y in range(650, 650+INVTILESIZE * self.rows, INVTILESIZE+2):
					self.slots.append(Slot(x, y, None))

	def draw(self, screen):
		if self.displayInventory == True:
			for slot in self.slots:
				slot.draw(screen)

	def toggleInventory(self):
		if self.displayInventory == False:
			self.displayInventory = True
		elif self.displayInventory == True:
			self.displayInventory = False

	def addItem(self, item):
		for slot in self.slots:
			if slot.item == None:
				slot.item = item
				break
			
class Slot:
	def __init__(self, x, y, item):
		self.x = x
		self.y = y
		self.item = item
	def draw(self, screen):
		pg.draw.rect(screen, WHITE, (self.x, self.y, INVTILESIZE, INVTILESIZE))
		if self.item != None:
			self.image = pg.image.load(self.item.img).convert_alpha()
			screen.blit(self.image, (self.x-7, self.y-7))

class InventoryItem:
	def __init__(self, img, value):
		self.img = img
		self.value = value

class Consumable(InventoryItem):
	def __init__(self, img, value, hp_gain=0, prot_gain=0):
		InventoryItem.__init__(self, img, value)
		self.hp_gain = hp_gain
		self.prot_gain = prot_gain

	def use(self, target):
		Inventory.remove(self)
		target.addHp(self.hp_gain)
		target.addDef(self.prot_gain)

class Equipable(InventoryItem):
	def __init__(self, img, value):
		InventoryItem.__init__(self, img, value)
		self.is_equipped = False
		self.equipped_to = None

		def equip(self, target):
			self.is_equipped = True
			self.equipped_to = target

		def unequip(self):
			self.is_equipped = False
			self.equipped_to = None

class Armor(Equipable):
	def __init__(self, img, value, prot, slot):
		Equipable.__init__(self, img, value)
		self.prot = prot
		self.slot = slot

	def equip(self, target):
		Equipable.equip(self, target)
		target.equip_armor(self, self.slot)

	def unequip(self):
		self.equipped_to.unequip_armor(self.slot)
		Equipable.unequip(self)

class Weapon(Equipable):
	def __init__(self, img, value, atk, wpn_type):
		Equipable.__init__(self, img, value)
		self.atk = atk
		self.wpn_type = wpn_type

	def equip(self, target):
		Equipable.equip(self, target)
		target.equip_weapon(self)

	def unequip(self):
		self.equipped_to.unequip_weapon()
		Equipable.unequip(self)