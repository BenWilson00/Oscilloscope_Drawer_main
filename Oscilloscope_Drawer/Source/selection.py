import pygame
from basic import *
from sprites import *

class Selection(object):

	def __init__(self, pos, bounding_rect, filepath, **kwargs):

		self.z = kwargs['z'] if 'z' in kwargs else 8
		if 'id' in kwargs: self.id = kwargs['id']
		self.filepath = filepath

		self.bounding_rect = bounding_rect
		self.pos = pos

		self.dash_size = 2 * SCALE()
		
		self.hover = False
		self.active = False

		if not 'copy' in kwargs:

			self.rect = Rect((pos), (0, 0))
			
			self.selecting = True
			self.start_selecting = True

			self.points_in_rect = False
			self.split_points = False

		else:

			self.rect, self.selecting, self.points_in_rect, self.split_points, self.id = kwargs['copy']

			self.start_selecting = False

		self.points = { key : Button((0, 0), filepath + 'point.png', type = "follow") 
										 for key in ("mover", "topleft",     "top",     "topright", 
																					"left",                      "right",
																					"bottomleft", "bottom", "bottomright") }

		for point in self.points:
			self.points[point].load('convert_alpha', id=point, scale=SCALE())

		self.align_points()

	def copy(self, topleft = "bounding rect"):

		if topleft == "bounding rect":
			return Selection(self.rect.topleft, self.bounding_rect, self.filepath, copy=(Rect(self.bounding_rect.topleft, self.rect.size), self.selecting, self.points_in_rect, self.split_points, self.id))
		elif topleft == "current":
			return Selection(self.rect.topleft, self.bounding_rect, self.filepath, copy=(self.rect.copy(), self.selecting, self.points_in_rect, self.split_points, self.id))
		elif type(topleft) != str:
			return Selection(self.rect.topleft, self.bounding_rect, self.filepath, copy=(Rect(topleft, self.rect.size), self.selecting, self.points_in_rect, self.split_points, self.id))
		else:
			print topleft

	def align_points(self):

		self.points['mover'].set_pos( (self.rect.left+self.rect.right)/2 - SCALE()*4, self.rect.top - SCALE()*18) 
		self.points['topleft'].set_pos( subtract_tuple(self.rect.topleft, (SCALE()*4, SCALE()*4) ) )
		self.points['top'].set_pos( (self.rect.left+self.rect.right)/2 - SCALE()*4, self.rect.top - SCALE()*4) 
		self.points['topright'].set_pos( subtract_tuple(self.rect.topright, (SCALE()*4, SCALE()*4)) )
		self.points['left'].set_pos( self.rect.left - SCALE()*4, (self.rect.top+self.rect.bottom)/2 - SCALE()*4 )
		self.points['right'].set_pos( self.rect.right - SCALE()*4, (self.rect.top+self.rect.bottom)/2 - SCALE()*4 )
		self.points['bottomleft'].set_pos( subtract_tuple(self.rect.bottomleft, (SCALE()*4, SCALE()*4)) )
		self.points['bottom'].set_pos( (self.rect.left+self.rect.right)/2 - SCALE()*4, self.rect.bottom - SCALE()*4)
		self.points['bottomright'].set_pos( subtract_tuple(self.rect.bottomright, (SCALE()*4, SCALE()*4)) )

	def update(self, **kwargs):

		if 'rect' in kwargs: self.rect = kwargs['rect']
		if 'selecting' in kwargs: self.selecting = kwargs['selecting']	
		if 'points_in_rect' in kwargs:
			if self.points_in_rect:
				del_lst = []

				for point in self.points_in_rect:
					if point in kwargs['points_in_rect']:
						self.points_in_rect[point] = kwargs['points_in_rect'][point]
					else:
						del_lst.append(point)

				for point in del_lst:
					del self.points_in_rect[point]

			else:
				self.points_in_rect = kwargs['points_in_rect']

		if 'split_points' in kwargs:
			self.split_points = kwargs['split_points']
	
	def check_active(self, mouse):

		self.hover = False
		self.active = False

		for point in self.points:
			self.points[point].check_active(mouse)
			if self.points[point].hover:
				self.hover = True

			if self.points[point].active:
				self.active = True
				
	def get_action(self):

		for point in self.points:
			if self.points[point].active:
				if self.selecting:
					return (self.id, point, 'change selection')
				else:
					return (self.id, point, 'mutate')

	def set_start_size(self, mouse_pos):
		
		mouse = list(mouse_pos)
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

	def mutate(self, change_point, mouse):

		old_rect_size = self.rect.size
		if self.rect.height > 0:
			
			if "right" in change_point:
				self.rect.width = max(3, min(mouse['pos'][0], self.bounding_rect.right) - self.rect.left)

			if "bottom" in change_point:
				self.rect.height = max(3, min(mouse['pos'][1], self.bounding_rect.bottom) - self.rect.top)

			if "left" in change_point:
				if mouse['pos'][0] < self.rect.right:
					self.rect.width = self.rect.right - max(mouse['pos'][0], self.bounding_rect.left)
					self.rect.left = max(mouse['pos'][0], self.bounding_rect.left)
				else:
					self.rect.left = self.rect.right - 3
					self.rect.width = 3

			if "top" in change_point:
				if mouse['pos'][1] < self.rect.bottom:
					self.rect.height = max(3, self.rect.bottom - max(mouse['pos'][1], self.bounding_rect.top))
					self.rect.top = max(mouse['pos'][1], self.bounding_rect.top)
				else:
					self.rect.top = self.rect.bottom - 3
					self.rect.height = 3

			if "mover" in change_point:
				if mouse['pos'][0] - self.rect.width/2 < self.bounding_rect.left:
					self.rect.left = self.bounding_rect.left
				elif mouse['pos'][0] + self.rect.width/2 > self.bounding_rect.right:
					self.rect.right = self.bounding_rect.right
				else:
					self.rect.left = mouse['pos'][0] - self.rect.width/2

				if mouse['pos'][1] + 18*SCALE() < self.bounding_rect.top:
					self.rect.top = self.bounding_rect.top
				elif mouse['pos'][1] + self.rect.height + 18*SCALE() > self.bounding_rect.bottom:
					self.rect.bottom = self.bounding_rect.bottom
				else:
					self.rect.top = mouse['pos'][1] + 18*SCALE()
				
		self.align_points()

		if not self.selecting:
			for point in self.points_in_rect:
				self.points_in_rect[point] = multiply_tuple(self.points_in_rect[point], divide_tuple(self.rect.size, old_rect_size))

			return self.points_in_rect

	def get_hover(self):
		for point in self.points:
			if self.points[point].hover:
				if point == 'left' or point == 'right':
					return 'horizontal'
				elif point == 'top' or point == 'bottom':
					return 'vertical'
				elif point == 'topright' or point == 'bottomleft':
					return 'diag1'	
				elif point == 'topleft' or point == 'bottomright':
					return 'diag2'
				elif point == 'mover':
					return 'cardinal'

	def draw(self, display):

		if self.selecting:
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

		else:	
			pygame.draw.rect(display, (255, 255, 255), self.rect, 1)
			pygame.draw.line(display, (255, 255, 255), add_tuple(self.points["mover"].pos, (SCALE()*4, SCALE()*4)), add_tuple(self.points["top"].pos, (SCALE()*4, SCALE()*4)), 1)
		
		if not self.start_selecting:	
			for point in self.points:
				self.points[point].draw(display)

