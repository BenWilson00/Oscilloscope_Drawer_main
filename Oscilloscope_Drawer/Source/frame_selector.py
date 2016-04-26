import csv
import pygame
from basic import *
from sprites import *
from frame import *


class Frame_selector(object):

	def __init__(self, frames, directory, **kwargs):

		self.id = 'frame selector'
		self.z = kwargs['z'] if 'z' in kwargs else 3
		self.frames = frames
		self.frame_sprites = []
		self.delete_buttons = []
		self.hover = False
		self.active = False
		self.surface = pygame.Surface(scaleup(784, 134))
		self.surface_rect = self.surface.get_rect()
		self.pos = scaleup(58, 636)
		self.displace = 0.0
		self.update()
		self.directory = directory

	def scaleup(self, *values):
		if len(values) == 1 and type(values[0]) == tuple:
			return multiply_tuple(SCALE(), values[0])
		elif len(values) > 1:
			return multiply_tuple(SCALE(), values)
		else:
			return SCALE() * values[0]

	def load(self, **kwargs):

		if 'frame' in kwargs:
			self.frames[kwargs['frame'].frame_num] = kwargs['frame']
			self.frame_sprites[kwargs['frame'].frame_num].update_image(self.frames[kwargs['frame'].frame_num].get_mini(self.surface))

		else:
			for frame in range(0, len(self.frames)):
			  	self.frame_sprites.append(Button((SCALE()*frame*176+6, SCALE()*15), self.frames[frame].get_mini(self.surface)))
				self.delete_buttons.append(Button((SCALE()*(frame*176+153)+6, SCALE()*15), self.directory + 'remove_frame_button.png'))
				self.frame_sprites[frame].load(id='select frame '+str(frame))
				self.delete_buttons[frame].load(scale=SCALE(), id='delete frame '+str(frame))

			self.add_button = Button((SCALE()*len(self.frames)*176+6, SCALE()*15), self.directory + 'add_frame_button.png')
			self.add_button.load(150, scale=SCALE(), id='add empty frame')

	def update(self, **kwargs):

		self.range = SCALE()*((len(self.frames)+1)*(176)+4)

		if self.range > self.surface_rect.width:
			self.len_percent = float(self.range)/self.surface_rect.width
		else:
			self.len_percent = 1.0

		if 'displace' in kwargs: 
			self.displace = kwargs['displace']*(self.range - self.surface_rect.width)

			self.update_positions()

		if 'new_frame' in kwargs:

			if kwargs['new_frame'][1] == 'end':
				self.frame_sprites.append(Button((0, 0), self.frames[-1].get_mini(self.surface)))
				self.delete_buttons.append(Button((0, 0), self.directory + 'remove_frame_button.png'))
				self.frame_sprites[-1].load(id='select frame '+str(len(self.frame_sprites)))
				self.delete_buttons[-1].load(scale=SCALE(), id='delete frame '+str(len(self.frame_sprites)))

			else:
				self.frame_sprites.insert(Button((0, 0), self.frames[kwargs['new_frame'][1]].get_mini(self.surface)), kwargs['new_frame'][1])
				self.delete_buttons.insert(Button((0, 0), self.directory + 'remove_frame_button.png'), kwargs['new_frame'][1])
				self.frame_sprites[kwargs['new_frame'][1]].load(id='select frame '+str(kwargs['new_frame'][1]))
				self.delete_buttons[kwargs['new_frame'][1]].load(scale=SCALE(), id='delete frame '+str(kwargs['new_frame'][1]))

			self.update_positions()

		if 'delete_frame' in kwargs:
			if kwargs['delete_frame'] == 'end':
				self.frame_sprites.pop()
				self.delete_buttons.pop()
			else:
				self.frame_sprites.pop(kwargs['delete_frame'])
				self.delete_buttons.pop(kwargs['delete_frame'])
			
			self.update_positions()

	def update_positions(self):

		for frame in range(0, len(self.frames)):
		  	self.frame_sprites[frame].set_pos((SCALE()*(frame*176)+6-self.displace, SCALE()*15))
			self.delete_buttons[frame].set_pos((SCALE()*(frame*176+153)+6-self.displace, SCALE()*15))

		self.add_button.set_pos((SCALE()*(len(self.frames)*176)+6-self.displace, SCALE()*15))

	def check_active(self, mouse):

		self.hover = False
		self.active = False
		adjusted_mouse = mouse.copy()

		adjusted_mouse['pos'] = subtract_tuple(adjusted_mouse['pos'], self.pos)

		if len(self.delete_buttons) > 1:

			for i in range(0, len(self.frames)):

				if self.surface_rect.colliderect(self.frame_sprites[i].rect):
					self.frame_sprites[i].check_active(adjusted_mouse, clip=self.surface_rect)
					if self.frame_sprites[i].active: 
						self.active = str(i)
					if self.frame_sprites[i].hover:
						self.hover = True

				if self.surface_rect.colliderect(self.delete_buttons[i].rect):
					self.delete_buttons[i].check_active(adjusted_mouse, clip=self.surface_rect)
					if self.delete_buttons[i].active:
						self.active = str(i)
					if self.delete_buttons[i].hover:
						self.hover = True

	 	if self.surface_rect.colliderect(self.add_button.rect):
	 	 	self.add_button.check_active(adjusted_mouse, clip=self.surface_rect)

	 	if self.add_button.active: self.active = True
	 	if self.add_button.hover: self.hover = True

	def get_action(self):

		for i in range(0, len(self.frames)):

			if self.delete_buttons[i].active:
				return (self.id, "delete frame", i,)

			elif self.frame_sprites[i].active:
				return (self.id, "select frame", i,)

		if self.add_button.active:
			return (self.id,) + self.add_button.get_action()

	def get_hover(self):

		for i in range(0, len(self.frames)):

			if self.delete_buttons[i].hover or self.frame_sprites[i].hover: return 'click'

		if self.add_button.hover: return 'click'

	def draw(self, display, curr_frame):

		self.surface.fill((68, 68, 68))

		for frame in range(0, len(self.frames)):
			if self.surface_rect.colliderect(self.frame_sprites[frame].rect):
				if frame == curr_frame:
					pygame.draw.rect(self.surface, (0, 170, 0), ((SCALE()*frame*176+2-self.displace, SCALE()*15-4), (SCALE()*168 + 8, SCALE()*104 + 8)))
				pygame.draw.rect(self.surface, (68, 68, 68), ((SCALE()*frame*176+4-self.displace, SCALE()*15-2), (SCALE()*168 + 4, SCALE()*104 + 4)), 1)
				pygame.draw.rect(self.surface, (153, 153, 153), ((SCALE()*frame*176+5-self.displace, SCALE()*15-1), (SCALE()*168 + 2, SCALE()*104 + 2)), 1)
				self.frame_sprites[frame].draw(self.surface)
				if len(self.delete_buttons) > 1: self.delete_buttons[frame].draw(self.surface)

		if self.surface_rect.colliderect(self.frame_sprites[-1].rect):
			pygame.draw.rect(self.surface, (68, 68, 68), ((SCALE()*len(self.frames)*176+4-self.displace, SCALE()*15-2), scaleup(172, 108)), 1)
			pygame.draw.rect(self.surface, (153, 153, 153), ((SCALE()*len(self.frames)*176+5-self.displace, SCALE()*15-1), scaleup(170, 106)), 1)	
			self.add_button.draw(self.surface)

		display.blit(self.surface, self.pos)

	# def global_to_rel(self, point):

	# 	return subtract_tuple(point, self.pos)



