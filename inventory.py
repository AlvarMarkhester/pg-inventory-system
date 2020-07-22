import pygame as pg
from settings import *
import random
import time

class Inventory:
	def __init__(self, player, totalSlots, cols, rows):
		self.totalSlots = totalSlots
		self.rows = rows
		self.cols = cols
		self.inventory_slots = []
		self.armor_slots = []
		self.weapon_slots = []
		self.display_inventory = False
		self.player = player
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
		self.armor_slots[0].slottype = 'head'
		self.armor_slots[1].slottype = 'chest'
		self.armor_slots[2].slottype = 'legs'
		self.armor_slots[3].slottype = 'feet'
		self.weapon_slots[0].slottype = 'weapon'

	def draw(self, screen):
		if self.display_inventory == True:
			for invslot in self.inventory_slots:
				invslot.draw(screen)
				invslot.drawItems(screen)
			for armorslot in self.armor_slots:
				armorslot.draw(screen)
				armorslot.drawItems(screen)
			for wepslot in self.weapon_slots:
				wepslot.draw(screen)
				wepslot.drawItems(screen)

	def toggleInventory(self):
		self.display_inventory = not self.display_inventory

	def addItemInv(self, item):
		for slot in self.inventory_slots:
			if slot.item == None:
				slot.item = item
				break
	def removeItemInv(self, item):
		for slot in self.inventory_slots:
			if slot.item == item:
				slot.item = None
				break

	def checkSlot(self, screen, mousepos):
		for slot in self.inventory_slots + self.armor_slots + self.weapon_slots:
			if isinstance(slot, InventorySlot):
				if slot.draw(screen).collidepoint(mousepos):
					if isinstance(slot.item, Equipable):
						self.equipItem(slot.item)
					if isinstance(slot.item, Consumable):
						self.useItem(slot.item)
			if isinstance(slot, EquipableSlot):
				if slot.draw(screen).collidepoint(mousepos):
					if slot.item != None:
						self.unequipItem(slot.item)

	def getEquipSlot(self, item):
		for slot in self.armor_slots + self.weapon_slots:
			if slot.slottype == item.slot:
				return slot

	def useItem(self, item):
		item.use(self, self.player)

	def equipItem(self, item):
		item.equip(self, self.player)

	def unequipItem(self, item):
		item.unequip(self)

class InventorySlot:
	def __init__(self, x, y, item=None):
		self.x = x
		self.y = y
		self.item = item

	def draw(self, screen):
		return pg.draw.rect(screen, WHITE, (self.x, self.y, INVTILESIZE, INVTILESIZE))
	
	def drawItems(self, screen):
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
		return pg.draw.rect(screen, WHITE, (self.x, self.y, INVTILESIZE, INVTILESIZE))
	
	def drawItems(self, screen):
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

	def use(self, inv, target):
		inv.removeItemInv(self)
		target.addHp(self.hp_gain)
		target.addProt(self.prot_gain)

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

	def equip(self, inv, target):
		if inv.getEquipSlot(self).item != None:
			inv.getEquipSlot(self).item.unequip(inv)
		Equipable.equip(self, target)
		target.equip_armor(self)
		inv.removeItemInv(self)
		inv.getEquipSlot(self).item = self

	def unequip(self, inv):
		self.equipped_to.unequip_armor(self.slot)
		Equipable.unequip(self)
		inv.addItemInv(self)
		inv.getEquipSlot(self).item = None

class Weapon(Equipable):
	def __init__(self, img, value, atk, slot, wpn_type):
		Equipable.__init__(self, img, value)
		self.atk = atk
		self.slot = slot
		self.wpn_type = wpn_type

	def equip(self, inv, target):
		if inv.getEquipSlot(self).item != None:
			inv.getEquipSlot(self).item.unequip(inv)
		Equipable.equip(self, target)
		target.equip_weapon(self)
		inv.removeItemInv(self)
		inv.getEquipSlot(self).item = self

	def unequip(self, inv):
		self.equipped_to.unequip_weapon()
		Equipable.unequip(self)
		inv.addItemInv(self)
		inv.getEquipSlot(self).item = None