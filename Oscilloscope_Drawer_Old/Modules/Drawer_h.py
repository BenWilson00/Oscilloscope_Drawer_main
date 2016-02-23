import pygame

class Point(object):

	def __init__(self, pos, _id):
		self.pos = pos
		self._id = _id
		self.pressed = False


	def draw(self, tracing, display):
		if self.pressed:
			colours = [(200, 200, 200), (0, 255, 0)]
		else:
			colours = [(0, 100, 55), (0, 255, 55)]

		if tracing:
			sizes = [3, 2]
		else:
			sizes = [6, 4]

		pygame.draw.circle(display, colours[0], self.pos, sizes[0], 0)
		pygame.draw.circle(display, colours[1], self.pos, sizes[1], 0)

	def check_pressed(self, mouse, click, rightclick):
		if ((mouse[0] - self.pos[0])**2 + (mouse[1] - self.pos[1])**2) < 64:
			if click:
				self.pressed = True
				return 'click'
			elif rightclick:
				return 'pop'
		elif self.pressed and click:
			return 'click'
		else:
			self.pressed = False
			return 'no click'


class Button(object):

	def __init__(self, pos, icon, pressed):
		self.pos = pos
		self.icon = icon
		self.pressed = pressed

	def draw(self, display):
		if self.pressed:
			colours = [(50, 50, 50), (75, 75, 75), (200, 200, 200)]
		else:
			colours = [(100, 100, 100), (155, 155, 155), (200, 200, 200)]

		pygame.draw.polygon(display, colours[2], ((self.pos[0]-16, self.pos[1]-16), 
												  (self.pos[0]+16, self.pos[1]-16), 
												  (self.pos[0]+16, self.pos[1]+16), 
												  (self.pos[0]-16, self.pos[1]+16)), 0)
		pygame.draw.polygon(display, colours[0], ((self.pos[0]-14, self.pos[1]-14), 
												  (self.pos[0]+14, self.pos[1]-14), 
												  (self.pos[0]+14, self.pos[1]+14), 
												  (self.pos[0]-14, self.pos[1]+14)), 0)
		if self.icon == '+':
			pygame.draw.polygon(display, colours[1], ((self.pos[0]-10, self.pos[1]-2), 
													  (self.pos[0]+10, self.pos[1]-2), 
													  (self.pos[0]+10, self.pos[1]+2), 
													  (self.pos[0]-10, self.pos[1]+2)), 0)

			pygame.draw.polygon(display, colours[1], ((self.pos[0]-2, self.pos[1]-10), 
													  (self.pos[0]+2, self.pos[1]-10), 
													  (self.pos[0]+2, self.pos[1]+10), 
													  (self.pos[0]-2, self.pos[1]+10)), 0)

		elif self.icon == '-':
			pygame.draw.polygon(display, colours[1], ((self.pos[0]-10, self.pos[1]-2), 
													  (self.pos[0]+10, self.pos[1]-2), 
													  (self.pos[0]+10, self.pos[1]+2), 
													  (self.pos[0]-10, self.pos[1]+2)), 0)

		elif self.icon == '>':
			pygame.draw.polygon(display, colours[1], ((self.pos[0]-8, self.pos[1]-10), 
													  (self.pos[0]+8, self.pos[1]), 
													  (self.pos[0]-8, self.pos[1]+10)), 0)

		elif self.icon == '||':
			pygame.draw.polygon(display, colours[1], ((self.pos[0]-6, self.pos[1]-10), 
													  (self.pos[0]-2, self.pos[1]-10), 
													  (self.pos[0]-2, self.pos[1]+10), 
													  (self.pos[0]-6, self.pos[1]+10)), 0)
			pygame.draw.polygon(display, colours[1], ((self.pos[0]+6, self.pos[1]-10), 
													  (self.pos[0]+2, self.pos[1]-10), 
													  (self.pos[0]+2, self.pos[1]+10), 
													  (self.pos[0]+6, self.pos[1]+10)), 0)

		elif self.icon == 'save':
			pygame.draw.polygon(display, colours[1], ((self.pos[0]-10, self.pos[1]+2), 
													  (self.pos[0]+10, self.pos[1]+2), 
													  (self.pos[0]+10, self.pos[1]+12), 
													  (self.pos[0]-10, self.pos[1]+12)), 0)
			pygame.draw.polygon(display, colours[1], ((self.pos[0]-8, self.pos[1]-12), 
													  (self.pos[0]+8, self.pos[1]-12), 
													  (self.pos[0]+8, self.pos[1]-4), 
													  (self.pos[0]-8, self.pos[1]-4)), 0)
			pygame.draw.polygon(display, colours[2], ((self.pos[0]+14, self.pos[1]-14), 
													  (self.pos[0]+11, self.pos[1]-14), 
													  (self.pos[0]+14, self.pos[1]-11)), 0)
			pygame.draw.line(display, colours[0], (self.pos[0]+5, self.pos[1]-10),
												  (self.pos[0]+5, self.pos[1]-6), 3)
			pygame.draw.line(display, colours[0], (self.pos[0]-8, self.pos[1]+4),
												  (self.pos[0]+8, self.pos[1]+4), 1)
			pygame.draw.line(display, colours[0], (self.pos[0]-8, self.pos[1]+6),
												  (self.pos[0]+8, self.pos[1]+6), 1)
			pygame.draw.line(display, colours[0], (self.pos[0]-8, self.pos[1]+8),
												  (self.pos[0]+8, self.pos[1]+8), 1)
			pygame.draw.line(display, colours[0], (self.pos[0]-8, self.pos[1]+10),
												  (self.pos[0]+8, self.pos[1]+10), 1)


	def check_pressed(self, mouse, click):
		
		if mouse[0] >= self.pos[0]-14 and mouse[0] <= self.pos[0]+14 and mouse[1] >= self.pos[1]-14 and mouse[1] <= self.pos[1]+14:
			if click:
				self.pressed = True
				return False

			elif self.pressed:
				self.pressed = False
				return True
		else:
			self.pressed = False
			return False

class Trace_Particle(object):

	def __init__(self, pos):

		self.pos = pos
		self.starttime = 0
		self.killtime = 0

	def draw(self, trace_iteration, t_length, display, rainbow_lst, rainbow, iteration):
		
		if rainbow:
			if self.killtime > trace_iteration and (self.killtime - trace_iteration)/float(self.lifetime) <= 1:
				fraction = (self.killtime - trace_iteration)/float(self.lifetime)
				pygame.draw.circle(display, rainbow_lst[int(fraction*254)], self.pos, 3, 0)

			elif trace_iteration + t_length < self.killtime and trace_iteration < self.lifetime: 
				fraction = (self.killtime - trace_iteration - t_length)/float(self.lifetime)
				pygame.draw.circle(display, rainbow_lst[int(fraction*254)], self.pos, 3, 0)
		else:
			if self.killtime > trace_iteration and (self.killtime - trace_iteration)/float(self.lifetime) <= 1:
				fraction = (self.killtime - trace_iteration)/float(self.lifetime)
				pygame.draw.circle(display, [0, int(fraction*254), 0], self.pos, 3, 0)

			elif trace_iteration + t_length < self.killtime and trace_iteration < self.lifetime: 
				fraction = (self.killtime - trace_iteration - t_length)/float(self.lifetime)
				pygame.draw.circle(display, [0, int(fraction*254), 0], self.pos, 3, 0)

	def set_life(self, iteration, lifetime):

		self.starttime = iteration
		self.lifetime = lifetime
		self.killtime = iteration + lifetime

def trace_path(points, trace_particles, iteration, length, n_trace_particles, trail_length):

	
	for p in range(0, len(points)):

		jump = length / float(n_trace_particles)

		x_dif = points[p].pos[0] - points[p-1].pos[0]
		y_dif = points[p].pos[1] - points[p-1].pos[1]
		dif = int((x_dif**2 + y_dif**2)**0.5)

		for i in range(0, int(dif/jump)):

			trace_particles.append(Trace_Particle((int(points[p-1].pos[0] + x_dif*i*jump/dif), int(points[p-1].pos[1] + y_dif*i*jump/dif))))


	for t in range(0, len(trace_particles)):
		trace_particles[t].set_life(iteration+t, int((len(trace_particles) - 10)*trail_length/12))

class RainbowSpark(object):

	def __init__(self, pos, v, colour, size, iteration, lifetime):
		self.pos = pos
		self.v = v
		self.colour = colour
		self.size = int(size)
		self.starttime = iteration
		self.lifetime = lifetime
		self.killtime = self.starttime + self.lifetime 

	def update(self, iteration):

		self.pos[0] += self.v[0]
		self.pos[1] += self.v[1]

		self.v[0] *= (self.killtime - iteration)/float(self.lifetime)
		self.v[1] *= (self.killtime - iteration)/float(self.lifetime)

	def draw(self, display):

		pygame.draw.circle(display, self.colour, [int(self.pos[0]), int(self.pos[1])], self.size, 0)


def calc_trace_length(points):

	trace_length = 0
	for p in range(0, len(points)):

		x_dif = points[p].pos[0] - points[p-1].pos[0]
		y_dif = points[p].pos[1] - points[p-1].pos[1]
		dif = int((x_dif**2 + y_dif**2)**0.5)
		trace_length += dif

	return trace_length