import pygame
from basic import *
from sprites import *

class Selection(object):

	def __init__(self, rect, scale, bounding_rect, filepath, **kwargs):

		self.z = kwargs['z'] if 'z' in kwargs else 8
		if 'id' in kwargs: self.id = kwargs['id']
		self.scale = scale
		self.bounding_rect = bounding_rect
		self.rect = rect
		self.hover = False
		self.active = False

		self.points = {'topleft' : Button(subtract_tuple(self.rect.topleft, (8, 8)), filepath + 'point.png'), 
					   'top' : Button(subtract_tuple(((self.rect.left+self.rect.right)/2, self.rect.top), (8, 8)), filepath + 'point.png'), 
					   'topright' : Button(subtract_tuple(self.rect.topright, (8, 8)), filepath + 'point.png'),
					   'left' : Button(subtract_tuple((self.rect.left, (self.rect.top+self.rect.bottom)/2), (8, 8)), filepath + 'point.png'), 
					   'right' : Button(subtract_tuple((self.rect.right, (self.rect.top+self.rect.bottom)/2), (8, 8)), filepath + 'point.png'),
					   'bottomleft' : Button(subtract_tuple(self.rect.bottomleft, (8, 8)), filepath + 'point.png'), 
					   'bottom' : Button(subtract_tuple(((self.rect.left+self.rect.right)/2, self.rect.bottom), (8, 8)), filepath + 'point.png'), 
					   'bottomright' : Button(subtract_tuple(self.rect.bottomright, (8, 8)), filepath + 'point.png')}

		for point in self.points:
			self.points[point].load('convert_alpha', id=point, scale=self.scale)

	def update(self, **kwargs):

		if 'rect' in kwargs: self.rect = kwargs['rect']
	
	def check_active(self, mouse):
		self.hover = False
		
		for point in self.points:
			self.points[point].check_active(mouse)
			if self.points[point].hover:
				self.hover = True

	def get_hover(self):
		for point in self.points:
			if self.points[point].hover:
				return 'horizontal'

	def draw(self, display):
		pygame.draw.rect(display, (255, 255, 255), self.rect, 1)
		for point in self.points:
			self.points[point].draw(display)

class Selector(object):

	def __init__(self, pos, scale, bounding_rect, **kwargs):

		self.z = kwargs['z'] if 'z' in kwargs else 8
		if 'id' in kwargs: self.id = kwargs['id']
		self.pos = pos
		self.bounding_rect = bounding_rect
		self.rect = Rect((pos), (0, 0))
		self.dash_size = 2 * scale

		self.hover = False
		self.active = False

	def update(self, **kwargs):

		if 'rect' in kwargs: self.rect = kwargs['rect']
		elif 'mouse' in kwargs:

			mouse = list(kwargs['mouse'])
			if mouse[0] > self.pos[0]:
				mouse[0] = min(self.bounding_rect.right, mouse[0])
				self.rect.width = mouse[0] - self.pos[0]
				self.rect.left = self.pos[0]
			else: 
				mouse[0] = max(self.bounding_rect.left, mouse[0])
				self.rect.width = self.pos[0] - mouse[0]
				self.rect.left = mouse[0]

			if mouse[1] > self.pos[1]:
				mouse[1] = min(self.bounding_rect.bottom, mouse[1])
				self.rect.height = mouse[1] - self.pos[1]
				self.rect.top = self.pos[1]
			else: 
				mouse[1] = max(self.bounding_rect.top, mouse[1])
				self.rect.height = self.pos[1] - mouse[1]
				self.rect.top = mouse[1]

		# else:
		# 	if 'topleft' in kwargs: self.rect.topleft = kwargs['topleft']
		# 	elif 'pos' in kwargs: self.rect.topleft = kwargs['pos']
		# 	if 'size' in kwargs: self.rect.size = kwargs['size']

	def check_active(self, mouse):
		pass

	def draw(self, display):

		if self.rect.height <= 0:
			self.rect.height = 1
		if self.rect.width <= 0:
			self.rect.width = 1
			
		self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

		end, overrun = divmod(self.rect.width, 3*self.dash_size)

		for i in range(0, int(end) + 1):
			pygame.draw.line(self.surface, (255, 255, 255), (3 * i * self.dash_size, 0), ((3 * i + 1) * self.dash_size, 0), 1)
		
		end = self.rect.height//3*self.dash_size

		for i in range(0, int(end) + 1):
		 	pygame.draw.line(self.surface, (255, 255, 255), (self.rect.width-1, 3 * i * self.dash_size - overrun), (self.rect.width-1, (3 * i + 1) * self.dash_size - overrun), 1)

		overrun = (self.rect.height + overrun) % (3*self.dash_size)

	 	end = self.rect.width//3*self.dash_size

		for i in range(0, int(end) + 1):
			pygame.draw.line(self.surface, (255, 255, 255), (self.rect.width-1 - (3 * i * self.dash_size - overrun), self.rect.height-1), (self.rect.width-1 - ((3 * i + 1) * self.dash_size - overrun), self.rect.height-1), 1)
	 	
		overrun = (self.rect.width + overrun) % (3*self.dash_size)

	 	end = self.rect.height//3*self.dash_size

		for i in range(0, int(end) + 1):
			pygame.draw.line(self.surface, (255, 255, 255), (0, self.rect.height-1 - (3 * i * self.dash_size - overrun)), (0, self.rect.height-1 - ((3 * i + 1) * self.dash_size - overrun)), 1)

		display.blit(self.surface, self.rect.topleft)

