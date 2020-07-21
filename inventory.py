import pygame as pg
from settings import *
import random
import time

class Inventory:
	def __init__(self, totalSlots, cols, rows):
		self.totalSlots = totalSlots
		self.rows = rows
		self.cols = cols
		self.inventory_slots = []
		self.armor_slots = []
		self.weapon_slots = []
		self.display_inventory = False
		self.appendSlots()
		self.setSlotTypes()
		
	def appendSlots(self):
		while len(self.inventory_slots) != self.totalSlots:
			for x in range(WIDTH//2 - ((INVTILESIZE+2) * self.cols)//2, WIDTH//2 + ((INVTILESIZE+2) * self.cols) //2, INVTILESIZE+2):
				for y in range(UIHEIGTH, UIHEIGTH+INVTILESIZE * self.rows, INVTILESIZE+2):
					self.inventory_slots.append(InventorySlot(x, y))

		while len(self.armor_slots) != 4:
			for y in range(UIHEIGTH-100, UIHEIGTH-100+(INVTILESIZE+1) * 4, INVTILESIZE+2):
				self.armor_slots.append(EquipableSlot(self.inventory_slots[0].x - 100, y))

		while len(self.weapon_slots) != 1:
			self.weapon_slots.append(EquipableSlot(self.armor_slots[3].x - 50, self.armor_slots[3].y))

	def setSlotTypes(self):
		for slot in self.armor_slots:
			if self.armor_slots[0] == slot:
				slot.slottype = 'head'
			if self.armor_slots[1] == slot:
				slot.slottype = 'chest'
			if self.armor_slots[2] == slot:
				slot.slottype = 'legs'
			if self.armor_slots[3] == slot:
				slot.slottype = 'feet'
		self.weapon_slots[0].slottype = 'weapon'


	def draw(self, screen):
		if self.display_inventory == True:
			for invslot in self.inventory_slots:
				invslot.draw(screen)
			for armorslot in self.armor_slots:
				armorslot.draw(screen)
			for wepslot in self.weapon_slots:
				wepslot.draw(screen)

	def toggleInventory(self):
		if self.display_inventory == False:
			self.display_inventory = True
		elif self.display_inventory == True:
			self.display_inventory = False

	def addItem(self, item):
		for slot in self.inventory_slots:
			if slot.item == None:
				slot.item = item
				break
	def removeItem(self, item):
		for slot in self.inventory_slots:
			if slot.item == item:
				slot.item = None
				break
			
class InventorySlot:
	def __init__(self, x, y, item=None):
		self.x = x
		self.y = y
		self.item = item
	def draw(self, screen):
		pg.draw.rect(screen, WHITE, (self.x, self.y, INVTILESIZE, INVTILESIZE))
		if self.item != None:
			self.image = pg.image.load(self.item.img).convert_alpha()
			screen.blit(self.image, (self.x-7, self.y-7))

class EquipableSlot:
	def __init__(self, x, y, slottype=None, item=None):
		self.x = x
		self.y = y
		self.slottype = slottype
		self.item = item
	def draw(self, screen):
		pg.draw.rect(screen, WHITE, (self.x, self.y, INVTILESIZE, INVTILESIZE))

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
	def __init__(self, img, value, atk, slot, wpn_type):
		Equipable.__init__(self, img, value)
		self.atk = atk
		self.wpn_type = wpn_type

	def equip(self, target):
		Equipable.equip(self, target)
		target.equip_weapon(self)

	def unequip(self):
		self.equipped_to.unequip_weapon()
		Equipable.unequip(self)