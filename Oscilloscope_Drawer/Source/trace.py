import csv
import pygame
from basic import *
from sprites import *
from frame import *
from frame_selector import *

class Trace(object):

	def __init__(self, lines, **kwargs):

		self.id = 'trace'
		self.lines = [lines[line].split('/') for line in range(1, len(lines))]
		self.frames = []
		self.curr_frame_n = int(lines[0][14:])
		self.z = kwargs['z'] if 'z' in kwargs else 3
		self.hover = False
		self.active = False

	def get_cf(self):

		if len(self.frames) > self.curr_frame_n:
			return self.frames[self.curr_frame_n]
		else:
			return -1

	def load(self, frame_rect, grid_type):

		self.grid_type = grid_type
		self.frame_rect = frame_rect
		frame_lists = []

		for line in self.lines:
			temp_frame = []

			reader = list(csv.reader(line))
			for i in range(0, len(reader[0])):
				temp_frame.append([reader[0][i], reader[1][i]])
			
			frame_lists.append(temp_frame)

		frame_split_points = [{} for frame in frame_lists]
		frame_int_lists = [[] for frame in frame_lists]

		for frame in range(0, len(frame_lists)):
			for point in range(0, len(frame_lists[frame])):
				if frame_lists[frame][point] != ['~', '~'] and frame_lists[frame][point] != ['-', '-']:
					frame_int_lists[frame].append([int(value) for value in frame_lists[frame][point]])
				else:
					frame_split_points[frame][point - len(frame_split_points[frame])] = frame_lists[frame][point][0]

		for frame in range(0, len(frame_int_lists)):
			self.frames.append(Frame(frame, frame_int_lists[frame], frame_split_points[frame], self.frame_rect))

		self.frame_selector = Frame_selector(self.frames, CWD() + '\Images\\')

	def draw(self, display):
		self.get_cf().draw(display, self.grid_type)
		self.frame_selector.draw(display, self.curr_frame_n)

	def global_to_rel(self, mouse):
		return self.get_cf().global_to_rel(mouse)

	def update(self, **kwargs):
		
		self.get_cf().update(kwargs)
		
	def check_active(self, mouse):

		for frame in self.frames:
			if frame.change and not (mouse['Lactive'] or mouse['Ractive']):
				self.frame_selector.load(frame=frame)
				frame.change = False

		self.active = False
		self.hover = False
		
		self.get_cf().check_active(mouse)
		self.frame_selector.check_active(mouse)

		if self.frame_selector.active: self.active = True
		self.active |= self.get_cf().active
		if self.get_cf().hover: self.hover = True
		elif self.frame_selector.hover: self.hover = True

	def get_hover(self):

		if self.get_cf().hover:
			return self.get_cf().get_hover()

		if self.frame_selector.hover:
			return self.frame_selector.get_hover()

	def get_action(self):
		
		if self.get_cf().active:
			if self.id: return (self.id,) + self.get_cf().get_action()
		 	else: return self.get_cf().get_action()

		elif self.frame_selector.active:
			if self.id: return (self.id,) + self.frame_selector.get_action()
		 	else: return self.frame_selector.get_action()
		# for tool in self.tools:
		# 	if self.tools[tool].Lactive or self.tools[tool].Ractive:
		# 		if self.id: return self.id + '/' + self.tools[tool].get_action()
		# 		else: return self.tools[tool].get_action()

	def add_frame(self, points, pos='end'):
		if pos == 'end':
			self.frames.append(Frame(len(self.frames), points, {}, self.frame_rect))
			self.frame_selector.update(new_frame=[self.frames[-1], pos])
		else:
			self.frames.insert(Frame(pos, points, {}, self.frame_rect), pos)
			self.frame_selector.update(new_frame=[self.frames[pos], pos])

	def delete_frame(self, pos='end'):
		if pos == 'end':
			self.frames.pop()
		else:
			self.frames.pop(pos)
		self.frame_selector.update(delete_frame=pos)
		if self.curr_frame_n >= len(self.frames):
			self.curr_frame_n = len(self.frames) - 1

	def get_points(self):
		return self.get_cf().get_points()

	def save_file(self, filepath, name):
		to_write = 'curr_frame_n = ' + str(self.curr_frame_n) + '\n'
		for frame in self.frames:
			if len(frame.points) > 0:
				x_points, y_points = zip(*frame.points)
				x_points = map(lambda x: frame.split_points[x] + ',' + str(x_points[x]) if x in frame.split_points else str(x_points[x]), range(0, len(x_points)))
				y_points = map(lambda y: frame.split_points[y] + ',' + str(y_points[y]) if y in frame.split_points else str(y_points[y]), range(0, len(y_points)))
				to_write += ','.join(x_points) + '/' + ','.join(y_points) + '\n'
			else:
				to_write += '\n'

		trace_file = open(filepath, 'w')
		trace_file.write(to_write)
		trace_file.close()
		print 'Written successfully to', name

		time.sleep(0.5)
