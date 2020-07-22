import pygame as pg
import sys
import random
from settings import *
from sprites import *
from inventory import *

class Game():
	def __init__(self):
		pg.init()
		pg.font.init()
		self.myfont = pg.font.SysFont('Calibri', 25)
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()

	def new(self):
		# start a new game
		self.all_sprites = pg.sprite.Group()
		self.all_coins = pg.sprite.Group()
		self.player = Player(self, 15, 15, DEFUALT_HP, DEFUALT_PROT, DEFUALT_ATK)
		self.coin = Coin(self, random.randrange(0, GRIDWIDTH), random.randrange(0, GRIDHEIGHT))
		self.inventory = Inventory(self.player, 10, 5, 2)
		sword_steel = Weapon('img/sword.png', 20, 20, 'weapon', 'sword')
		sword_wood = Weapon('img/swordWood.png', 10, 10, 'weapon', 'sword')
		hp_potion = Consumable('img/potionRed.png', 2, 30)
		helmet_armor = Armor('img/helmet.png', 10, 20, 'head')
		chest_armor = Armor('img/chest.png', 10, 40, 'chest')
		upg_helmet_armor = Armor('img/upg_helmet.png', 10, 40, 'head')
		upg_chest_armor = Armor('img/upg_chest.png', 10, 80, 'chest')
		self.inventory.addItemInv(helmet_armor)
		self.inventory.addItemInv(hp_potion)
		self.inventory.addItemInv(sword_steel)
		self.inventory.addItemInv(sword_wood)
		self.inventory.addItemInv(chest_armor)
		self.inventory.addItemInv(upg_helmet_armor)
		self.inventory.addItemInv(upg_chest_armor)
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
				if event.key == pg.K_b:
					self.inventory.toggleInventory()
			if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
				mouse_pos = pg.mouse.get_pos()
				self.inventory.checkSlot(self.screen, mouse_pos)

	def new_coin(self):
		self.coin.x = random.randrange(0, GRIDWIDTH)
		self.coin.y = random.randrange(0, GRIDHEIGHT)

	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):
			pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):
			pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

	def draw_player_stats(self):
		self.hp = self.myfont.render(f"{self.player.hp}" , False, RED)
		self.prot = self.myfont.render(f"{self.player.prot}" , False, WHITE)
		self.atk = self.myfont.render(f"{self.player.atk}" , False, WHITE)
		self.coins = self.myfont.render(f"{self.player.p_coins}" , False, GOLD)
		self.hpimg = pg.image.load('img/heart.png').convert_alpha()
		self.protimg = pg.image.load('img/upg_shieldSmall.png').convert_alpha()
		self.atkimg = pg.image.load('img/upg_dagger.png').convert_alpha()
		self.coinimg = pg.image.load('img/coin1.png').convert_alpha()
		self.screen.blit(self.hp,(STATPOSX,25))
		self.screen.blit(self.prot,(STATPOSX,75))
		self.screen.blit(self.atk,(STATPOSX,125))
		self.screen.blit(self.coins,(STATPOSX,175))
		self.screen.blit(self.hpimg,(STATPOSX-50,5))
		self.screen.blit(self.protimg,(STATPOSX-50,55))
		self.screen.blit(self.atkimg,(STATPOSX-50,105))
		self.screen.blit(self.coinimg,(STATPOSX-55,155))


	def draw(self):
		# game loop draw
		self.screen.fill(BGCOLOR)
		self.draw_grid()
		self.all_sprites.draw(self.screen)
		self.inventory.draw(self.screen)
		self.draw_player_stats()
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