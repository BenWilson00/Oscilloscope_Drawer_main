import csv
import pygame
import collections
from basic import *
from sprites import *
from selection import *

class Frame(object):

	def __init__(self, frame_num, points, split_points, frame_rect):
		self.z = 0
		self.frame_num = frame_num
		self.id = 'frame'

		self.points = points
		self.split_points = split_points
		self.selected_points = []

		self.sizes = {'normal' : (6, 4),
					  			'mini' : (2, 0.5)}

		self.colours = [[(0, 100, 0), (0, 200, 0)], 
										[(0, 150, 0), (0, 255, 0)], 
										[(60, 200, 60), (160, 255, 160)],
										[(60, 60, 200), (160, 160, 255)]]

		self.window_pos = frame_rect.topleft
		self.surface = pygame.Surface(frame_rect.size)
		self.rect = self.surface.get_rect()
		self.zoom = 1.0

		self.tools = {}

		self.mod_key = 'None'
		self.k_space = False
		self.req_action = False

		self.selection = False
		self.start_selecting = False
	#	self.resize_selection = False
		self.selected = False

		self.hover = False
		self.action = False
		self.active = False
		self.active_point = False
		self.mouse_pos = False
			
		self.change = False
		self.prev_changes = collections.deque()
		self.undo_dist = 0

		self.change_pos = [0, 0, 0]
		
		self.min_distance = {'dist' : 20/self.zoom,
										 		 'next_point' : None,
												 'pos' : None}
		self.load_points()

#last_point = reduce(lambda x, y: max(x, y) if y < pos and x < pos else x, self.split_points)



	def global_to_rel(self, point, **kwargs):
		
		if type(point) == Rect:
			return Rect(self.global_to_rel(point.topleft), multiply_tuple(1/(self.zoom*SCALE()), point.size))

		return add_tuple(self.rect.topleft, multiply_tuple(1/(self.zoom*SCALE()), subtract_tuple(point, scaleup(30, 80)), int=True)) if 'int' in kwargs else add_tuple(self.rect.topleft, multiply_tuple(1/(self.zoom*SCALE()), subtract_tuple(point, scaleup(30, 80)), int=True))

	def rel_to_zoomed(self, point, **kwargs):

		point = multiply_tuple(self.zoom, subtract_tuple(point, self.rect.topleft))
		
		point = scaleup(point) if 'scale' in kwargs else point 

		return tuple([int(round(value)) for value in point]) if 'int' in kwargs else point

	def toggle_line(self, point):

		if len(self.points) > 0:
			if point not in self.split_points:

				if len(self.split_points) == 0:
					self.split_points[point] = '-'
				elif not ((point-1)%len(self.points) in self.split_points or (point+1)%len(self.points) in self.split_points):
					self.split_points[point] = '-'

				elif (point+1)%len(self.points) in self.split_points:
					self.split_points[point+1] = '~'

			elif self.split_points[point] == '-':

				if len(self.split_points) > 1:
					self.split_points[point] = '~'

				else:
					self.split_points.pop(point)

			elif self.split_points[point] == '~':
				self.split_points.pop(point)

			if len(self.split_points) == 1:
				for point in self.split_points:
					self.split_points[point] = '-'

			self.active = False
			self.action = False


	def add_point(self, start_pos, point_lst, set_active = False, **kwargs):


		if "split_points" in kwargs:
			get_split_points = True
			new_splits = kwargs["split_points"]
		else:
			get_split_points = False

		if type(point_lst[0]) != list and type(point_lst[0]) != tuple:
			point_lst = [point_lst]

		# adjust original split point positions

		to_update = []
		
		for split in self.split_points:
			if split > start_pos:
				to_update.append(split)
		for split in to_update:
			self.split_points[split + len(point_lst)] = self.split_points.pop(split)

		if start_pos in self.split_points:
			if self.split_points[start_pos] == '-':
				self.split_points[start_pos + len(point_lst)] = self.split_points.pop(start_pos)


		# add points and new split points
		for i in range(0, len(point_lst)):
			self.points.insert(start_pos + i, point_lst[i])

			if get_split_points:
				if new_splits[i]:
					self.split_points[start_pos + i] = new_splits[i]


		if set_active:
			self.load_points(active=start_pos)
		else:
			self.load_points()

	def delete_point(self, points):

		if type(points) != list and type(points) != tuple:
			points = [points]

		for point in points:

			if point == 'active':
				found = False
				for i in range(0, len(self.points)):
					if self.states[i] == 1:
						found = True
						point = i
						del self.points[i]
						break
				if not found:
					continue

			else:
				del self.points[point]

			to_update = []
			to_del = False

			for split in self.split_points:
				if split == point + 1:
					to_del = split

			if to_del != False:
				del self.split_points[to_del]

			for split in self.split_points:
				if split > point:
					to_update.append(split)
					continue

			for split in to_update:
				self.split_points[split - 1] = self.split_points.pop(split)

			if len(self.points) in self.split_points:
				self.split_points[0] = self.split_points.pop(len(self.points))

			del_dict = {}

			for split in self.split_points:
				for split2 in self.split_points:
					if split == split2 + 1:
						del_dict[split] = True

			for split in del_dict:
				del self.split_points[split]

			self.active_point = False
			self.active = False
			self.action = False

			for other_point in range(0, len(points)):
				if points[other_point] != "active":
					if int(points[other_point]) > int(point):
						points[other_point] -= 1


		self.load_points()

	def load_points(self, **kwargs):

		self.states = [0 for point in self.points]
		self.active_point = False
		if 'active' in kwargs:
			self.states[kwargs['active']] = 2
			self.active_point = str(kwargs['active'])

	def set_points(self, change_dict):
		for point in change_dict:
			self.points[point] = change_dict[point]

 	def get_points(self, **kwargs):

 		bound_rect = self.global_to_rel(kwargs["rect"]) if "rect" in kwargs else False
 		get_split_points = kwargs["split_points"] if "split_points" in kwargs else False

		return_points = {}
		if get_split_points: split_points = {}

		if bound_rect:
			for point in range(0, len(self.points)):
				if bound_rect.collidepoint(self.points[point]):
					return_points[point] = subtract_tuple(self.points[point], bound_rect.topleft)

			if get_split_points:
				for i in self.split_points:
					if (bound_rect.collidepoint(self.points[i]) and bound_rect.collidepoint(self.points[i-1])):
						split_points[i] = self.split_points[i]

		else:
			for point in range(0, len(self.points)):
				return_points[point] = [self.points[point], self.rel_to_zoomed(self.points[point], scale=True)]
			
			if get_split_points:
				split_points = self.split_points

		if get_split_points:
			return return_points, split_points
		else:
			return return_points
	
	def get_hover(self):
		
		if self.hover: return self.hover

	def get_action(self):

		if self.active_point:
			return (self.id, self.frame_num, 'move point', self.active_point)
		if self.action:
			return (self.id, self.frame_num, self.action)
		if self.selection:
			if self.selection.active: return (self.id, self.frame_num,) + self.selection.get_action()

	def check_active(self, mouse):

		mouse_rel = Point(self.global_to_rel(mouse['pos']))

		if not self.req_action:

			if not (mouse['Lactive'] or mouse['Ractive']):
				if self.start_selecting:
					self.start_selecting = False
					self.selection.start_selecting = False
					self.selection.selecting = False
					self.selection.align_points()

					self.active = True
					self.action = "toggle select type"
					return

				self.hover = False

			if self.selection:

				if not self.selection.selecting and not (mouse['Lactive'] or mouse['Ractive']):
					points_in_rect, split_points = self.get_points(rect = self.selection.rect, split_points=True)


					self.selection.update(points_in_rect = points_in_rect, split_points=split_points)

				self.selection.check_active(mouse)

				if self.selection.active: 
					self.active = True
					self.action = False
					return

				if self.selection.hover: 
					self.hover = self.selection.get_hover()
			

			if self.k_space and self.rect.collidepoint(mouse_rel.tup()) and mouse['Ldown']:
				if not self.hover: self.hover = 'grab'
				self.active = True
				self.action = 'grab & move'
				self.mouse_pos = mouse_rel.tup()

			if self.action == 'grab & move' and not (self.k_space and mouse['Lactive']):
				self.mouse_pos = False
				self.active = False
				self.action = False

			elif self.action == 'grab & move':
				self.change_pos = subtract_tuple(self.mouse_pos, mouse_rel.tup()) + (0,)
				return
		
			if mouse['Scrollup']:
				if self.mod_key == 'None':
					self.action = 'scroll up'
					self.change_pos = (0, -32, 0)
				elif self.mod_key == 'ctrl':
					self.action = 'zoom in'
					self.change_pos = (0, 0, -32)
				elif self.mod_key == 'shift':
					self.action = 'scroll right'
					self.change_pos = (32, 0, 0)

				self.active = True
				return
			else:
				self.change_pos = False

			if mouse['Scrolldown']:
				if self.mod_key == 'None':
					self.action = 'scroll down'
					self.change_pos = (0, 32, 0)
				elif self.mod_key == 'ctrl':
					self.action = 'zoom out'
					self.change_pos = (0, 0, 32)
				elif self.mod_key == 'shift':
					self.action = 'scroll left'
					self.change_pos = (-32, 0, 0)
				
				self.active = True
				return
			else:
				self.change_pos = False

			if not self.active_point:

				for point in range(0, len(self.points)):
					zoompoint = Point(self.points[point])

					if len(mouse_rel - zoompoint) <= self.sizes['normal'][0] / self.zoom: 

						if self.check_tool_active('move point', mouse) and self.rect.collidepoint(mouse_rel.tup()):
						  	self.active_point = str(point)
							self.states[point] = 2
						  	self.active = True
						
						if 'move point' in self.tools or 'delete point' in self.tools:
							if not self.hover: self.hover = 'click'
							self.states[point] = 1

					else:
						self.states[point] = 0

			if not (self.active_point or 1 in self.states) and (self.rect.collidepoint(mouse_rel.tup())  and ('add point' in self.tools or 'toggle line' in self.tools)):
				
				self.update_min_dist(mouse, mouse_rel.i_tup())
				if self.min_distance['pos']: 
					if not self.hover: self.hover = 'click'
			
			else:
				self.min_distance = {'dist' : 15/self.zoom,
													 	 'next_point' : None,
														 'pos' : None}

			for tool in set(['add point', 'delete point', 'toggle line', 'make selection', 'mutate selection']).intersection(self.tools):
				if self.check_tool_active(tool, mouse):
					self.action = tool
					self.active = True

			if not (mouse['Lactive'] or mouse['Ractive']):
				self.active_point = False
				self.active = False


		elif self.req_action == "paste":

			self.update_min_dist(mouse, mouse_rel.i_tup())

			if self.min_distance['pos']:
				if not self.hover: self.hover = 'click'

				if mouse["Ldown"]:
					self.active = True
					self.action = "end paste"
					self.req_action = False
				
 
		# if self.selector_rect:
		# 	for point in range(0, len(self.points)):
		# 		if self.selector_rect.collidepoint(self.points[point]):
		# 			self.states[point] = 1
				
	def update(self, kwargs):

		if 'tools' in kwargs: 
			self.tools = kwargs['tools']
			if self.selection:
				if 'make selection' in self.tools:
					self.selection.selecting = True
				if 'mutate selection' in self.tools:
					self.selection.selecting = False

		if 'pos' in kwargs and 'zoom' in kwargs: 
			self.update_pos(zoom=kwargs['zoom'], pos=kwargs['pos'])
		if 'selector_rect' in kwargs:
			self.selector_rect = Rect(self.global_to_rel(kwargs['selector_rect'].topleft), multiply_tuple(1/(self.zoom*SCALE()), kwargs['selector_rect'].size))
		if 'space' in kwargs:
			self.k_space = kwargs['space']
		if 'mod' in kwargs:
			self.mod_key = kwargs['mod']
		if "input_req" in kwargs:
			self.req_action = kwargs["input_req"]

	def update_pos(self, **kwargs):

		if 'zoom' in kwargs and 'pos' in kwargs:
			self.zoom = kwargs['zoom']
			self.pos_percent = kwargs['pos']
		elif 'displace' in kwargs:
			self.pos_percent = add_tuple(self.pos_percent, divide_tuple(kwargs['displace'], self.rect.size))

		self.rect = self.surface.get_rect()
		self.rect.width = round(self.rect.width/(self.zoom*SCALE()))
		self.rect.height = round(self.rect.height/(self.zoom*SCALE()))
		self.rect.topleft = multiply_tuple(multiply_tuple(0.01, self.pos_percent), subtract_tuple(multiply_tuple(1.0/SCALE(), self.surface.get_rect().bottomright), self.rect.bottomright))

	def update_min_dist(self, mouse, mouse_rel):

		if type(mouse_rel) != Point: mouse_rel = Point(mouse_rel)

		if len(self.points) <= 2:
			self.min_distance = {'dist' : 0,
													 'next_point' : len(self.points),
													 'pos' : mouse_rel.i_tup()}

		else:
			self.min_distance = {'dist' : 20/self.zoom,
													 'next_point' : None,
													 'pos' : None}

			last_split = max(self.split_points.keys(), key=int) if len(self.split_points) > 0 else 0

			for point in range(0, len(self.points)):
				
				valid = False

				if point in self.split_points:
					
					if self.split_points[point] == '-':
						
						p0 = Point(self.points[point-1])
						p1 = Point(self.points[last_split])

						last_split = point

					elif self.split_points[point] == '~':

						p0 = Point(self.points[point-1])
						p1 = Point(self.points[point])

						last_split = point

				else:
					p0 = Point(self.points[point-1])
					p1 = Point(self.points[point])

				d01 = p1 - p0

	 			x_acceptable = d01.y / 25.0 + 2 + int(SCALE()/3.0)

				if (d01.x >= x_acceptable or -x_acceptable >= d01.x) and d01.y != 0:

					if d01.x == 0: d01.x = 0.00001

					line_m = d01.y/d01.x
					line_c = p1.y + d01.y - line_m * (p1.x + d01.x)

					norm_m = -1/line_m
					norm_c = mouse_rel.y - norm_m * mouse_rel.x

					intercept = Point((round((line_c - norm_c) / (norm_m - line_m)), 0))
					intercept.y = round(line_m * intercept.x + line_c)

					if intercept.x_between(p0.x, p1.x) and intercept.y_between(p0.y, p1.y):
						valid = True
						dist = len(intercept - mouse_rel)

				elif x_acceptable >= d01.x >= -x_acceptable:

					intercept = Point((p0.x, mouse_rel.y))

					if intercept.y_between(p0.y, p1.y):
						valid = True
						dist0 = abs(mouse_rel.x - p0.x)
						dist1 = abs(mouse_rel.x - p1.x)
						dist2 = abs(mouse_rel.x - (p0.x+p1.x)/2.0)
						dist = min(dist0, dist1, dist2)

				elif d01.y == 0:

					intercept = Point((mouse_rel.x, p0.y))

					if intercept.x_between(p0.x, p1.x):
						valid = True
						dist0 = abs(mouse_rel.y - p0.y)
						dist1 = abs(mouse_rel.y - p1.y)
						dist2 = abs(mouse_rel.y - (p0.y+p1.y)/2.0)
						dist = min(dist0, dist1, dist2)

				if valid and dist <= self.min_distance['dist'] and not ('toggle line' in self.tools and ((point-1)%len(self.points) in self.split_points or (point+1)%len(self.points) in self.split_points)):
					
					self.min_distance = {'dist' : dist,
															 'next_point' : point,
															 'pos' : mouse_rel.i_tup()}

	def move_point(self, mouse):
		
		mouse_rel = list(self.global_to_rel(mouse['pos'], int=True))

		self.change_pos = [0, 0, 0]
		
		if self.active_point:

			if mouse_rel[1] < self.rect.top:
				mouse_rel[1] = self.rect.top+1
				self.change_pos[1] = -1

			if mouse_rel[1] > self.rect.bottom:
				mouse_rel[1] = self.rect.bottom-1
				self.change_pos[1] = 1

			if mouse_rel[0] < self.rect.left:
				mouse_rel[0] = self.rect.left+1
				self.change_pos[0] = -1

			elif mouse_rel[0] > self.rect.right:
				mouse_rel[0] = self.rect.right-1
				self.change_pos[0] = 1

			self.points[int(self.active_point)] = mouse_rel

	def draw_arrow_line(self, colour, p0, p1, **kwargs):

		if type(p0) != Point: p0 = Point(p0)
		if type(p1) != Point: p1 = Point(p1)

		d01 = p1 - p0

		x_acceptable = abs(d01.y) / 20.0

		if (d01.x >= x_acceptable or -x_acceptable >= d01.x) and d01.y != 0:

			line_m = d01.y/d01.x
			line_c = p1.y + d01.y - line_m * (p1.x + d01.x)
			norm_m = -1/line_m

			dx = math.sqrt((6*SCALE())**2 / (1 + line_m**2))

			if sign(dx) == sign(p1.x - p0.x):
				dx = -dx

			intercept = Point((p1.x + 2 * dx, p1.y + 2 * dx * line_m))

			dx2 = math.sqrt((6*SCALE())**2 / (1 + norm_m**2))
			dy2 = dx2 * norm_m

			pygame.draw.aaline(self.surface, colour, (intercept.x + dx2, intercept.y + dy2), (p1.x + dx, p1.y + dx * line_m))
			pygame.draw.aaline(self.surface, colour, (intercept.x - dx2, intercept.y - dy2), (p1.x + dx, p1.y + dx * line_m))
			
			if 'cross' in kwargs:
				midpoint = Point((p0.x + d01.x/2, p0.y + d01.y/2))
				pygame.draw.aaline(self.surface, colour, (midpoint.x + (dx - dx2)*0.6, midpoint.y + (dx * line_m - dy2)*0.6), (midpoint.x - (dx - dx2)*0.6, midpoint.y - (dx * line_m - dy2)*0.6))
				pygame.draw.aaline(self.surface, colour, (midpoint.x + (dx + dx2)*0.6, midpoint.y + (dx * line_m + dy2)*0.6), (midpoint.x - (dx + dx2)*0.6, midpoint.y - (dx * line_m + dy2)*0.6))

		elif x_acceptable >= d01.x >= -x_acceptable:
			pygame.draw.aaline(self.surface, colour, (p1.x - 6*SCALE(), p1.y - 14*sign(d01.y)*SCALE()), (p1.x, p1.y - 7*sign(d01.y)*SCALE()))
			pygame.draw.aaline(self.surface, colour, (p1.x + 6*SCALE(), p1.y - 14*sign(d01.y)*SCALE()), (p1.x, p1.y - 7*sign(d01.y)*SCALE()))
			if 'cross' in kwargs:
				midpoint = Point((p0.x, p0.y + d01.y/2))
				pygame.draw.aaline(self.surface, colour, (midpoint.x - 7*0.6, midpoint.y - 7*0.6), (midpoint.x + 7*0.6, midpoint.y + 7*0.6))
				pygame.draw.aaline(self.surface, colour, (midpoint.x - 7*0.6, midpoint.y + 7*0.6), (midpoint.x + 7*0.6, midpoint.y - 7*0.6))

		else:
			pygame.draw.aaline(self.surface, colour, (p1.x - 14*sign(d01.x), p1.y - 6), (p1.x - 7*sign(d01.x), p1.y))
			pygame.draw.aaline(self.surface, colour, (p1.x - 14*sign(d01.x), p1.y + 6), (p1.x - 7*sign(d01.x), p1.y))
			if 'cross' in kwargs:
				midpoint = Point((p0.x + d01.x/2, p0.y))
				pygame.draw.aaline(self.surface, colour, (midpoint.x - 7*0.6, midpoint.y - 7*0.6), (midpoint.x + 7*0.6, midpoint.y + 7*0.6))
				pygame.draw.aaline(self.surface, colour, (midpoint.x - 7*0.6, midpoint.y + 7*0.6), (midpoint.x + 7*0.6, midpoint.y - 7*0.6))

		if not 'head_only' in kwargs: pygame.draw.aaline(self.surface, colour, p0.tup(), p1.tup()) 

	def draw_lines(self, mini=False):

		last_split = max(self.split_points.keys(), key=int) if len(self.split_points) > 0 else 0

		for point in range(0, len(self.points)):

			if point in self.split_points:
				if self.split_points[point] == '-':
					if not mini:
						self.draw_arrow_line((180, 0, 0), self.rel_to_zoomed(self.points[point-1], scale=True), self.rel_to_zoomed(self.points[point], scale=True))
						if len(self.split_points) > 1:
							self.draw_arrow_line((40, 40, 120), self.rel_to_zoomed(self.points[point-1], scale=True), self.rel_to_zoomed(self.points[last_split], scale=True))
							self.draw_arrow_line((80, 80, 255), self.rel_to_zoomed(self.points[point-1], scale=True), self.rel_to_zoomed(self.points[last_split], scale=True), head_only=True, cross=True)
					
					if self.min_distance['next_point'] == point and 'toggle line' in self.tools:
						self.draw_arrow_line((255, 255, 255), self.rel_to_zoomed(self.points[point-1], scale=True), self.rel_to_zoomed(self.points[last_split], scale=True))
					
					last_split = point

				elif self.split_points[point] == '~':
					if not mini:
						self.draw_arrow_line((180, 0, 0), self.rel_to_zoomed(self.points[last_split], scale=True), self.rel_to_zoomed(self.points[point], scale=True))
						self.draw_arrow_line((0, 255, 0), self.rel_to_zoomed(self.points[point-1], scale=True), self.rel_to_zoomed(self.points[last_split], scale=True))
						if len(self.split_points) > 1:
							self.draw_arrow_line(scaleup(40, 40, 120), self.rel_to_zoomed(self.points[point-1], scale=True), self.rel_to_zoomed(self.points[point], scale=True))
							self.draw_arrow_line((80, 80, 255), self.rel_to_zoomed(self.points[point-1], scale=True), self.rel_to_zoomed(self.points[point], scale=True), head_only=True, cross=True)
					else:
						pygame.draw.aaline(mini, (0, 255, 0), multiply_tuple(0.2*SCALE(), self.points[point-1]), multiply_tuple(0.2*SCALE(), self.points[last_split]))
					
					if self.min_distance['next_point'] == point and 'toggle line' in self.tools:
						self.draw_arrow_line((255, 255, 255), self.rel_to_zoomed(self.points[point-1], scale=True), self.rel_to_zoomed(self.points[last_split], scale=True))
						self.draw_arrow_line((255, 255, 255), self.rel_to_zoomed(self.points[last_split], scale=True), self.rel_to_zoomed(self.points[point], scale=True))
					
					last_split = point

		last_split = max(self.split_points.keys(), key=int) if len(self.split_points) > 0 else 0

		for point in range(0, len(self.points)):
			
			if not mini:
				if self.min_distance['next_point'] == point:
					pygame.draw.aaline(self.surface, (255, 255, 255), self.rel_to_zoomed(self.points[point-1], scale=True), self.rel_to_zoomed(self.points[point], scale=True))
					
					if 'toggle line' in self.tools:
						if point in self.split_points:
							if self.split_points[point] == '-': self.draw_arrow_line((80, 80, 255), self.rel_to_zoomed(self.points[point-1], scale=True), self.rel_to_zoomed(self.points[point], scale=True), head_only=True)
							elif self.split_points[point] == '~': self.draw_arrow_line((0, 255, 0), self.rel_to_zoomed(self.points[point-1], scale=True), self.rel_to_zoomed(self.points[point], scale=True), head_only=True)
						else: self.draw_arrow_line((180, 0, 0), self.rel_to_zoomed(self.points[point-1], scale=True), self.rel_to_zoomed(self.points[point], scale=True), head_only=True)
				
				elif not point in self.split_points: 
					
					self.draw_arrow_line((0, 255, 0), self.rel_to_zoomed(self.points[point-1], scale=True), self.rel_to_zoomed(self.points[point], scale=True))
			
			elif not point in self.split_points:
				pygame.draw.aaline(mini, (0, 255, 0), multiply_tuple(0.2*SCALE(), self.points[point-1]), multiply_tuple(0.2*SCALE(), self.points[point]))
						
	def draw(self, display, grid_type):

		if self.selection:
			if self.selection.points_in_rect:
				for point in self.selection.points_in_rect:
					if point in range(len(self.states)):
						self.states[point] = 3
		
		self.surface.fill((0, 0, 0))

		if grid_type != 'None' and self.zoom > 6.0:
			
		 	if grid_type == 'Lined':
		 		grid_colour = multiply_tuple((self.zoom - 4.0)/10.0, (100, 100, 100), int=True)

		 		for i in range(0, self.rect.width):
		 			pygame.draw.line(self.surface, grid_colour, scaleup(i*self.zoom, 0), scaleup(i*self.zoom, self.rect.height*self.zoom))

		 		for i in range(0, self.rect.height):
		 			pygame.draw.line(self.surface, grid_colour, scaleup(0, i*self.zoom), scaleup(self.rect.width*self.zoom, i*self.zoom))

			elif grid_type == 'Dotted':
				grid_colour = multiply_tuple((self.zoom - 4.0)/5.0, (100, 100, 100), int=True)
				for i in range(0, self.rect.width):
					for j in range(0, self.rect.height):
						self.surface.set_at(map(int, scaleup(i*self.zoom, j*(self.zoom))), grid_colour)

		if len(self.points) > 0: self.draw_lines()

	 	for point in range(0, len(self.points)):
	 		if self.rect.collidepoint(self.points[point]):
				pygame.draw.circle(self.surface, self.colours[self.states[point]][0], self.rel_to_zoomed(self.points[point], int=True, scale=True), int(self.sizes['normal'][0]*SCALE()))
				pygame.draw.circle(self.surface, self.colours[self.states[point]][1], self.rel_to_zoomed(self.points[point], int=True, scale=True), int(self.sizes['normal'][1]*SCALE()))

		display.blit(self.surface, self.window_pos)

		if self.selection:
			self.selection.draw(display)

	def get_mini(self, display):

		mini = pygame.Surface(scaleup(168, 104))
		for point in self.points:
			pygame.draw.circle(mini, self.colours[0][0], multiply_tuple(0.2*SCALE(), tuple(point), int=True), int(self.sizes['mini'][0]*SCALE()))
			pygame.draw.circle(mini, self.colours[0][1], multiply_tuple(0.2*SCALE(), tuple(point), int=True), int(self.sizes['mini'][1]*SCALE()))
	
		self.draw_lines(mini)
		return mini

	def make_selection(self, mouse):

		if self.start_selecting:
			self.selection.set_start_size(mouse['pos'])

		else:
			self.start_selecting = True
			self.selection = Selection(mouse['pos'], Rect(self.window_pos, self.surface.get_rect().size), CWD() + '\Images\Selection\\', z=8, id='selection')

	def update_selection(self, update_type, **kwargs):

		if update_type == "change selection":
			self.selection.mutate(kwargs["point"], kwargs["mouse"], {})

		if update_type == "mutate":

			new_points_in_rect = self.selection.mutate(kwargs["point"], kwargs["mouse"])

			self.set_points( { key : map(int, add_tuple(new_points_in_rect[key], self.global_to_rel(self.selection.rect.topleft))) for key in new_points_in_rect})


		if update_type == "cut":

			for key in self.selection.split_points:
				if key in self.split_points:
					del self.split_points[key]
			self.delete_point(self.selection.points_in_rect.keys())

			new = self.selection.copy()
			self.selection = False
			return new


	def recalc_selection_rect(self):

		if self.selection:
			self.selection.points_in_rect = False


	def check_tool_active(self, tool, mouse):

		if not tool in self.tools:
			return False

		mouse_active = False
		mouse_down = False
		mouse_up = False

		if 'Lmouse' in self.tools[tool]: 
			mouse_active |= mouse['Lactive']
			mouse_down |= mouse['Ldown']
			mouse_up |= mouse['Lup']

		if 'Rmouse' in self.tools[tool]: 
			mouse_active |= mouse['Ractive']
			mouse_down |= mouse['Rdown']
			mouse_up |= mouse['Rup']

		if tool == 'add point' and mouse_down and self.min_distance['pos']:
			return True

		elif tool == 'move point' and mouse_down:
			return True

		elif tool == 'delete point' and mouse_active and 1 in self.states:
			return True

		elif tool == 'toggle line' and mouse_down and self.min_distance['pos']:
			return True

		elif tool == 'make selection' and mouse_active and self.rect.collidepoint(self.global_to_rel(mouse['pos'])):
			return True

		elif tool == 'mutate selection' and mouse_active:
			return True


			

	def record_change(self, reset_list = True):

		new_selection = self.selection.copy("current") if self.selection else False

		self.prev_changes.append({"points" : list(self.points),
															"split points" : dict(self.split_points),
															"selection" : new_selection})

		while len(self.prev_changes) > 100:
			self.prev_changes.popleft()

		if reset_list:

			if self.undo_dist != 0:
				for i in range(self.undo_dist, 0):
					self.prev_changes.pop()
				self.undo_dist = 0

		self.change = True

	def restore_change(self, displace = -1):

		n = self.undo_dist + displace

		if 0 < - n <= len(self.prev_changes): 

			if n == -1 and displace < 0: 
				self.record_change(False)
				n -= 1

			last_state = self.prev_changes[n]

			self.points = list(last_state["points"])
			self.split_points = dict(last_state["split points"])
			self.selection = last_state["selection"].copy("current") if last_state["selection"] else False

			self.undo_dist = n
			self.change = True

			self.load_points()