import pygame, math
from pygame.locals import *
from basic import *

class Sprite(object):

	def __init__(self, pos, filepath, **kwargs):
		self.id = False
		self.z = kwargs['z'] if 'z' in kwargs else 4
		self.pos = pos
		self.filepath = filepath	
		self.state = 0
		self.hover = False
		self.active = False

	def load(self, alpha=255, **kwargs):

		if 'id' in kwargs: self.id = kwargs['id']

		if type(self.filepath) == str:
			if alpha == 'convert_alpha': self.image = pygame.image.load(self.filepath).convert_alpha()
			else: self.image = pygame.image.load(self.filepath).convert()
		elif type(self.filepath) == pygame.Surface:
			self.image = self.filepath

		if type(alpha) == int: self.image.set_alpha(alpha)
		if 'scale' in kwargs: self.image = pygame.transform.scale(self.image, multiply_tuple(kwargs['scale'], self.image.get_rect().size, int=True))

		self.rect = self.image.get_rect()

		if self.pos != None: self.rect.x, self.rect.y = self.pos
		
	def update_image(self, image, alpha=255):

		if type(image) == str:
			if alpha == 'convert_alpha': self.image = pygame.image.load(self.filepath).convert_alpha()
			else: self.image = pygame.image.load(self.filepath).convert()
		elif type(image) == pygame.Surface:
			self.image = image

		self.image.set_alpha(alpha)

		self.rect = self.image.get_rect()

		if self.pos != None: self.rect.x, self.rect.y = self.pos

	def set_pos(self, pos):

		if pos != None: self.rect.topleft = pos
		
		self.pos = pos

	def draw(self, display, **kwargs):

		pos = kwargs['pos'] if 'pos' in kwargs else self.rect.topleft 

		if 'clip' in kwargs:
			clip_surface = pygame.Surface(kwargs['clip'].size)
			clip_surface_rect = kwargs['clip']

			self.image.blit(clip_surface, subtract_tuple(pos, clip_surface_rect.topleft))
			
			display.blit(self.image, (pos[1] + (self.rect.height - clip_surface_rect.height), pos[0] + (self.rect.width - clip_surface_rect.width)))

		else:
			display.blit(self.image, pos)

class Button(Sprite):

	def __init__(self, pos, filepath, **kwargs):

		self.id = False
		self.z = kwargs['z'] if 'z' in kwargs else 6
		self.pos = list(pos)
		self.filepath = filepath
		self.state = 0
		self.type = kwargs['type'] if 'type' in kwargs else 'on_mouse_up'
		self.active = False
		self.hover = False
		self.mouse_pos = (0, 0)

	def check_active(self, mouse, **kwargs):

		self.hover = False
		self.clip_rect = self.rect.clip(kwargs['clip']) if 'clip' in kwargs else self.rect

		if self.clip_rect.collidepoint(mouse['pos']): 

			if not self.type == 'follow':
				self.hover = True

			if mouse['Lup']:

				if self.type == 'on_mouse_up':
					self.active = True
				elif self.type == 'tool':
					self.Lactive = True

			elif mouse['Rup']:

				if self.type == 'tool':
					self.Ractive = True

			elif mouse['Ldown']:

				if self.type == 'follow':
					self.active = True
					if type(self) == Button: self.mouse_pos = subtract_tuple(mouse['pos'], self.pos)
					elif type(self) == Slider: 
						if self.orientation == 0: self.mouse_pos = subtract_tuple(mouse['pos'], (self.pos[0], self.pos[1]+self.displace))
						else: self.mouse_pos = subtract_tuple(mouse['pos'], (self.pos[0]+self.displace, self.pos[1]))
						
				elif self.type == 'on_mouse_down':
					self.active = True

			elif mouse['Lactive'] or (self.type == 'tool' and mouse['Ractive']):

				self.state = 1

			else:

				self.state = 2
				self.active = False
				if self.type == 'tool':
					self.Ractive = False
					self.Lactive = False

		else:

			self.state = 0
			if not (self.type == 'follow' and self.active and mouse['Lactive']):	

				self.active = False
				self.mouse_pos = (0, 0)
				if self.type == 'tool':
					self.Ractive = False
					self.Lactive = False

		if self.active and self.type == 'follow':
				
			if self.orientation == 1: self.update(displace=-self.mouse_pos[0] + mouse['pos'][0] - self.bar_rect.left)
			else: self.update(displace=-self.mouse_pos[1] + mouse['pos'][1] - self.bar_rect.top)

	def get_hover(self):

		if self.id: return 'click'

	def get_action(self):

		if self.id: return self.id + '/click'

	def draw(self, display, **kwargs):
			
		if 'clip' in kwargs:

			clip_surface_rect = self.rect.clip(kwargs['clip'])

			clip_surface = pygame.Surface(clip_surface_rect.size)

			clip_surface.blit(self.image, subtract_tuple(self.rect.topleft, clip_surface_rect.topleft))
			
			display.blit(clip_surface, clip_surface_rect.topleft)

		else: 
			display.blit(self.image, self.rect.topleft)

		if self.state == 1:
			s = pygame.Surface(self.rect.size, pygame.SRCALPHA)
			s.fill((0, 0, 0, 120))
			display.blit(s, self.pos)
			pygame.draw.rect(display, (255, 255, 255), self.rect, 1)

		elif self.state == 2:
			pygame.draw.rect(display, (255, 255, 255), self.rect, 1)

class Cyclic_Button(Button):

	def __init__(self, pos, curr_image=0, *filepaths, **kwargs):

		self.id = False
		self.z = kwargs['z'] if 'z' in kwargs else 6
		self.pos = pos
		self.curr_image = curr_image
		self.filepaths = filepaths
		self.state = 0
		self.type = 'on_mouse_up'
		self.hover = False
		self.active = False
		self.mouse_pos = (0, 0)

	def load(self, alpha=255, **kwargs):

		if 'id' in kwargs: self.id = kwargs['id']

		self.images = []

		for filepath in self.filepaths:
			if type(filepath) == str:
				self.images.append(pygame.image.load(filepath).convert())
			elif type(filepath) == pygame.Surface:
				self.images.append(self.filepath)

		for image in self.images:
			image.set_alpha(alpha)
		if 'scale' in kwargs:
			for image in range(0, len(self.images)):
				self.images[image] = pygame.transform.scale(self.images[image], multiply_tuple(kwargs['scale'], self.images[image].get_rect().size, int=True))

		self.image = self.images[self.curr_image]
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = self.pos

	def cycle(self):
		self.curr_image = (self.curr_image + 1) % len(self.images)
		self.image = self.images[self.curr_image]
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = self.pos

class MultiSprite(object):

	def __init__(self, pos, *args):
		self.id = False
		self.pos = pos
		self.sprites = []
		self.hover = False
		self.active = False
		
		for sprite in args:
			self.sprites.append(sprite)
			sprite.pos = add_tuple(sprite.pos, self.pos)

	def load(self, **kwargs):
		if 'id' in kwargs: self.id = kwargs['id']

		for sprite in self.sprites: 
			sprite.load() 

	def draw(self, display):
		for sprite in self.sprites:
			sprite.draw(display)

	def update(self, **kwargs):
		for sprite in self.sprites:
			if 'zoom' in kwargs and type(sprite) == Slider:	
				sprite.update(length=sprite.range/kwargs['zoom'])
			
	def check_active(self, mouse):

		self.hover = False
		self.active = False

		for sprite in self.sprites:
			if type(sprite) == Button:
				sprite.check_active(mouse)
			elif type(sprite) == Slider:
				sprite.check_active(mouse)
			if sprite.active:
				self.active = True
			if sprite.hover:
				self.hover = True

	def get_hover(self):

		for sprite in self.sprites:
			if sprite.hover:
				return sprite.get_hover()

	def get_action(self):

		for sprite in self.sprites:
			if sprite.active:
				if self.id: return self.id + '/' + sprite.get_action()
				else: return sprite.get_action()
				
class Slider(Button):

	def __init__(self, bar_rect, orientation, **kwargs):

		self.id = False
		self.z = kwargs['z'] if 'z' in kwargs else 5
		self.type = kwargs['type'] if 'type' in kwargs else 'follow' 

		self.bar_rect = bar_rect
		self.orientation = orientation
		self.range = self.bar_rect.size[1-self.orientation]-4
		self.pos = add_tuple((2, 2), self.bar_rect.topleft)

		self.length = math.ceil(self.range/12.0)
		self.displace = 11.0*self.range / 12.0
		self.mouse_pos = (0, 0)

		self.update() 

		self.hover = False
		self.active = False
		self.state = 0

	def update(self, **kwargs):

		if 'displace' in kwargs: self.displace = kwargs['displace'] 
		elif 'add_displace' in kwargs: self.displace += kwargs['add_displace'] 
		if 'length' in kwargs: 
			length_dif = self.length - kwargs['length']
			self.length = kwargs['length']
			self.displace += length_dif/2.0
		if 'add' in kwargs: self.displace += kwargs['add']
		
		if self.displace > self.range - self.length or 'max' in kwargs: self.displace = self.range - self.length
		elif self.displace < 0: self.displace = 0
		
		if self.length >= self.range:
			self.percent = 0.0
		else:
			self.percent = 100.0 * self.displace / (self.range - self.length)
		
		if self.orientation == 0:
			self.rect = Rect((self.pos[0], self.pos[1] + self.displace), (self.bar_rect.width-4, self.length))

		else:
			self.rect = Rect((self.pos[0] + self.displace, self.pos[1]), (self.length, self.bar_rect.height-4))

	def load(self, **kwargs):
		if 'id' in kwargs: self.id = kwargs['id']

	def draw(self, display):
		pygame.draw.rect(display, (225, 225, 225), self.rect)
		pygame.draw.rect(display, (125, 125, 125), self.rect, 1)
		if self.state == 1:
			s = pygame.Surface(self.rect.size, pygame.SRCALPHA)
			s.fill((0, 0, 0, 100))
			display.blit(s, self.rect)

		elif self.state == 2:
			s = pygame.Surface(self.rect.size, pygame.SRCALPHA)
			s.fill((0, 0, 0, 50))
			display.blit(s, self.rect)

class Scrollbar(MultiSprite):
	
	def __init__(self, pos, orientation, *args, **kwargs):

		self.id = False
		self.pos = pos
		self.sprites = []
		self.orientation = orientation
		self.hover = False
		self.active = False

		for sprite in args:
			self.sprites.append(sprite)
			sprite.pos = add_tuple(sprite.pos, self.pos)

		self.type = kwargs['type'] if 'type' in kwargs else 'normal'
		self.z = kwargs['z'] if 'z' in kwargs else 2

	def load(self, scale, **kwargs):
		if 'id' in kwargs: self.id = kwargs['id']

		for sprite in self.sprites: 
			sprite.pos = multiply_tuple(scale, sprite.pos)
			
		self.sprites[0].load(scale=scale, id='decrease') if self.orientation else self.sprites[0].load(scale=scale, id='increase')
		self.sprites[1].load(scale=scale)
		self.sprites[2].load(scale=scale, id='increase') if self.orientation else self.sprites[2].load(scale=scale, id='decrease')

		self.sprites.append(Slider(self.sprites[1].rect, self.orientation, type='follow'))
		self.sprites[-1].load(id='slider')

class Text(object):

 	def __init__(self, font, text, pos, **kwargs):

		self.id = False
 		self.z = kwargs['z'] if 'z' in kwargs else 9
 		self.font = font
 		self.text = text
 		self.pos = pos
		self.hover = False
 		self.active = False

 		self.length = kwargs['length'] if 'length' in kwargs else 0
 		self.background = kwargs['background'] if 'background' in kwargs else True
 		self.lifetime = kwargs['lifetime'] if 'lifetime' in kwargs else 50
 		self.align_right = kwargs['align_right'] if 'align_right' in kwargs else False
 		self.fit_rect = kwargs['fit_rect'] if 'fit_rect' in kwargs else False
 
 		self.expired = False

 		if self.length == 0:
 			self.length = 10000
 		self.height = font.get_height()

 		self.lines = []

		i = 0
		j = 0
		done = False
 		while not done:
 			j = i
 			last_space = j
	 		while j < len(self.text):
	 			if self.text[j] == ' ':
	 				last_space = j

	 			if self.font.size(self.text[i:j])[0] > self.length:
	 				self.lines.append(self.text[i:last_space])
	 				i = last_space + 1
	 				break

	 			elif j == len(self.text) - 1:
	 				self.lines.append(self.text[i:])
	 				done = True
	 				break
	 			j += 1

	 	if len(self.lines) > 1: 
	 		self.rect = Rect((0, 0), (self.length + self.height/1.5, (self.height + 1)*len(self.lines) + 4))
	 	else: 
	 		self.rect = Rect((0, 0), (self.font.size(self.text)[0] + self.height/1.5, self.height + 5))

	 	if self.background:
	 		self.fsurface = pygame.Surface(self.rect.size)
		 	self.fsurface.fill((255, 255, 255))
		 	pygame.draw.rect(self.fsurface, (130, 130, 130), self.rect, 1)
		else:
			self.fsurface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

	 	for line in range(0, len(self.lines)):
	 		line_surface = self.font.render(self.lines[line], True, (0, 0, 0))
	 		self.fsurface.blit(line_surface, (2, 2 + (self.height + 1)*line))

	def check_active(self, mouse):
		pass

	def age(self):
		if not self.lifetime == None:
			self.lifetime -= 1
			if self.lifetime <= 0: self.expired = True

 	def draw(self, display):

 		bounding_rect = display.get_rect() if self.fit_rect == False else self.fit_rect

 		self.draw_pos = self.pos

		if self.align_right:
 			self.draw_pos = (self.draw_pos[0]-self.rect.width, self.draw_pos[1])
 		
 		elif self.draw_pos[1] + self.rect.height > bounding_rect.bottom:
 			self.draw_pos = (self.draw_pos[0], bounding_rect.bottom-self.rect.height)
 		
 		if self.draw_pos[1] <= bounding_rect.top:
 			self.draw_pos = (self.draw_pos[0], bounding_rect.top)

 		if self.draw_pos[0] + self.rect.width > bounding_rect.right + int(self.rect.height/3.0):
 			self.draw_pos = (bounding_rect.right-self.rect.width + int(self.rect.height/3.0), self.draw_pos[1])

 		elif self.draw_pos[0] <= bounding_rect.left:
 			self.draw_pos = (bounding_rect.left, self.draw_pos[1])

		display.blit(self.fsurface, self.draw_pos)  