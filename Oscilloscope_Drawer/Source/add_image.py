import pygame
import numpy as np
import cv2
import PIL
from PIL import Image
import menu
from basic import *
from sprites import *

accepted_filetypes = ("jpg", "png")


class ImageHandler(object):

	def __init__(self, dir_path, h, w, fonts):

		self.id = "image handler"
		self.z = 9

		self.fonts = fonts

		self.phase = "edge"

		self.success = True
		self.hover = False
		self.action = False
		self.active = False
		self.was_active = False
		self.dir_path = dir_path
		self.line_drawing = False

		# from 1 to 15
		self.START_R = 3
		self.END_R = 5
		
		self.max_jump = 15
		self.JUMP_LENGTH = 3
		self.MAX_STRAIGHT_SKIP = 3

		dir_files = [item for item in menu.listdir(dir_path) if item.split(".")[-1] in accepted_filetypes]

		selected = menu.options_run(dir_files, 0, [['d', 'to select'] , ['a', 'to exit']], "Please select an image to insert.")
		
		if selected[1] == "a":
			self.success = False
			return
		else:
			selected = selected[0]

		self.filename = dir_files[selected].split(".")[0]

		filepath = dir_path + dir_files[selected]

		clear()

		print "preparing..."
		#prepare image
		#resize

		max_dim = 300*SCALE()

		with PIL.Image.open(filepath) as image:

			biggest = max(image.size)

			#if biggest > max_dim:

			scale = max_dim / float(biggest)

			image = image.resize((int(i*scale) for i in image.size), PIL.Image.ANTIALIAS)

			image.save(filepath)

			self.image_size = image.size

		
		self.blur_r = 3
		self.max_blur = 19.0

		# read, apply single-channel colour
		image = cv2.imread(filepath)
		
		self.grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# save new file and create sprite object
		self.edged_path = self.dir_path + "line_versions\\" + self.filename + ".png"

		# get auto line tolerances for edge detect
		self.blurred = cv2.GaussianBlur(self.grey, (self.blur_r, self.blur_r), 0)

		mid_bright = np.median(self.blurred)

		self.detect_range = [int(max(0, 0.8*mid_bright)), int(min(255, 1.2*mid_bright))]

		# blur, apply Canny edge detect
		self.edge_detect(self.line_drawing)

		self.img = Sprite((0.6*w - 15*SCALE() - self.image_size[0], 15*SCALE()), self.edged_path)

		self.img.load()

		self.rect = Rect((0.2*w, 0.2*h), (0.6*w, 0.5*h))
		self.surface = pygame.Surface((0.6*w, 0.5*h))

		self.slider1_pos = ((50*SCALE(), 20*SCALE()), (50*SCALE(), self.rect.height - 120*SCALE()))
		self.s1_r = self.slider1_pos[1][1] - self.slider1_pos[0][1]

		self.slider2_pos = ((140*SCALE(), 20*SCALE()), (140*SCALE(), self.rect.height - 120*SCALE()))
		self.s2_r = self.slider2_pos[1][1] - self.slider2_pos[0][1]

		self.sliders = {"max1" : Slider( Rect(add_tuple(self.slider1_pos[0], (-5*SCALE(), 2)), (10*SCALE(), self.slider1_pos[1][1] - self.slider1_pos[0][1])), 0, image = CWD() + "\Images\slider.png", img_displace=(-12, -1), type="follow"),
										"min1" : Slider( Rect(add_tuple(self.slider1_pos[0], (-5*SCALE(), 2)), (10*SCALE(), self.slider1_pos[1][1] - self.slider1_pos[0][1])), 0, image = CWD() + "\Images\slider.png", img_displace=(-12, -1), type="follow"),
										"max2" : Slider( Rect(add_tuple(self.slider2_pos[0], (-5*SCALE(), 2)), (10*SCALE(), self.slider2_pos[1][1] - self.slider2_pos[0][1])), 0, image = CWD() + "\Images\slider.png", img_displace=(-12, -1), type="follow")}
										
		for slider in self.sliders:
			self.sliders[slider].load()

		self.sliders["min1"].update(percent = self.detect_range[1]/2.55, set_min=self.detect_range[0]) 
		self.sliders["max1"].update(percent = self.detect_range[0]/2.55, set_max=self.detect_range[1]) 
		self.sliders["max2"].update(percent = 100 - (self.blur_r/self.max_blur)*100)

		self.button_data = [("auto", "AUTOSET LINE TOLERANCE", (20*SCALE(), self.rect.height - 70*SCALE())),
												("prev", " < PREV", (200*SCALE(), self.rect.height - 70*SCALE())),
												("next", "NEXT > ", (280*SCALE(), self.rect.height - 70*SCALE())),
												("cancel", "CANCEL", (self.rect.width - 80*SCALE(), self.rect.height - 70*SCALE())),
												("toggle line drawing", "TOGGLE LINE/NORMAL DRAWING", (20*SCALE(), self.rect.height - 40*SCALE()))]

		self.get_text()

		self.buttons = {}
		for i in self.button_data:
			self.buttons[i[0]] = Button(subtract_tuple(self.texts[i[0]].rect.topleft, (2*SCALE(), SCALE())), self.texts[i[0]].rect.size)
			self.buttons[i[0]].load()

	def get_text(self):

		if self.phase == "edge":
			self.texts = {i[0] : Text(self.fonts[0], i[1], i[2], lifetime=None, **i[3])
										for i in (("s1 name", "LINE TOLERANCE", self.slider1_pos[1], {"background" : False, "align" : "centre"}),
															("s1 max", "max", (self.slider1_pos[0][0]-40*SCALE(), 17*SCALE()), {"background" : False}),
															("s1 min", "min", (self.slider1_pos[0][0]-40*SCALE(), self.rect.height - 130*SCALE()), {"background" : False}),
															("s2 name", "BLUR RADIUS", self.slider2_pos[1], {"background" : False, "align" : "centre"}),
															("s2 max", "max", (self.slider2_pos[0][0]-40*SCALE(), 17*SCALE()), {"background" : False}),
															("s2 min", "min", (self.slider2_pos[0][0]-40*SCALE(), self.rect.height - 130*SCALE()), {"background" : False}))}
		else:
			self.texts = {i[0] : Text(self.fonts[0], i[1], i[2], lifetime=None, **i[3])
										for i in (("s1 name", "SEARCH RADIUS", self.slider1_pos[1], {"background" : False, "align" : "centre"}),
															("s1 max", "max", (self.slider1_pos[0][0]-40*SCALE(), 17*SCALE()), {"background" : False}),
															("s1 min", "min", (self.slider1_pos[0][0]-40*SCALE(), self.rect.height - 130*SCALE()), {"background" : False}),
															("s2 name", "NODE JUMP NUMBER", self.slider2_pos[1], {"background" : False, "align" : "centre"}),
															("s2 max", "max", (self.slider2_pos[0][0]-40*SCALE(), 17*SCALE()), {"background" : False}),
															("s2 min", "min", (self.slider2_pos[0][0]-40*SCALE(), self.rect.height - 130*SCALE()), {"background" : False}))}

		for i in self.button_data:
			self.texts[i[0]] = Text(self.fonts[1], i[1], i[2],  lifetime=None, background=False)

	def auto_range(self):

		mid_bright = np.median(self.blurred)

		self.detect_range = [int(max(0, 0.8*mid_bright)), int(min(255, 1.2*mid_bright))]

		self.sliders["min1"].update(percent = self.detect_range[1]/2.55, set_min=self.detect_range[0]) 
		self.sliders["max1"].update(percent = self.detect_range[0]/2.55, set_max=self.detect_range[1]) 

		self.action = (self.id, "refresh image")
		self.active = True
		self.edge_detect(self.line_drawing)
		self.img.load()

	def check_active(self, mouse):

		self.active = False
		self.action = False

		adjusted_mouse = mouse.copy()

		adjusted_mouse['pos'] = subtract_tuple(mouse['pos'], self.rect.topleft)

		for slider in self.sliders:
			self.sliders[slider].check_active(adjusted_mouse)

			if self.sliders[slider].active:
				self.active = True
				self.was_active = True
				self.action = (self.id, slider)

				if self.phase == "edge":

					self.detect_range = [int(self.sliders["max1"].percent * 2.55), int(self.sliders["min1"].percent * 2.55)]
					self.sliders["min1"].update(set_min=(self.detect_range[0] / 2.55) + 2*SCALE())
					self.sliders["max1"].update(set_max=(self.detect_range[1] / 2.55) - 2*SCALE())

					self.blur_r = 2*int((self.max_blur - (self.sliders["max2"].percent * self.max_blur)/100.0)/2.0) + 1


				else:

					self.END_R, self.START_R = 1 + rnd(14 * (100 - self.sliders["max1"].percent) / 100), 1 + rnd(14 * (100 - self.sliders["min1"].percent) / 100)
					self.sliders["min1"].update(set_min=min(100, (( 100 - (self.END_R - 1) * 100.0 / 14))))
					self.sliders["max1"].update(set_max=max(0, (( 100 - (self.START_R - 1) * 100.0 / 14))))

					self.JUMP_LENGTH = rnd(self.max_jump * (100 - self.sliders["max2"].percent) / 100)


		for button in self.buttons:
			if not ((button == "auto" and self.phase != "edge") or (button == "prev" and self.phase == "edge")):
				self.buttons[button].check_active(adjusted_mouse)

		if self.buttons["auto"].active:
			self.auto_range()

		elif self.buttons["next"].active:
			if self.phase == "edge":

				self.action = (self.id, "refresh image")
				self.active = True

				self.phase = "trail"
				self.get_text()

				self.render_trails()

				self.sliders["min1"].update(percent = 100 - (self.START_R - 1) * 100.0 / 14.0) 
				self.sliders["max1"].update(percent = 100 - (self.END_R - 1) * 100.0 / 14.0) 
				self.sliders["max2"].update(percent = 100 - self.JUMP_LENGTH * 100.0 / self.max_jump)

			else:
				self.action = (self.id, "generate image point data")
				self.active = True
				points = {}
				split_points = {}

				i = 0
				curr_end_pos = (0, 0)
				while len(self.trails) > 0:

					if i != 0:
						split_points[i] = "-"

					next_start = min((trail for trail in range(len(self.trails))), key=lambda trail:(self.trails[trail][0][0] - curr_end_pos[0]) ** 2 + (self.trails[trail][0][1] - curr_end_pos[1]) ** 2) 

					for point in self.trails.pop(next_start):

						points[i] = point
						i += 1

					curr_end_pos = points[i-1]

				split_points[len(points)-1] = "-"

				size = list(scaleup(self.img.rect.size))


				self.image_data = (points, split_points, size)

		elif self.buttons["prev"].active:

			self.action = (self.id, "refresh image")
			self.active = True

			self.phase = "edge"

			self.get_text()

			self.edge_detect(self.line_drawing)
			self.img.load()

		elif self.buttons["cancel"].active:

			self.action = (self.id, "exit window")
			self.active = True
			return

		elif self.buttons["toggle line drawing"].active:

			self.action = (self.id, "toggle line drawing")
			self.active = True
			self.line_drawing = not self.line_drawing
			self.phase = "edge"
			self.edge_detect(self.line_drawing)
			self.img.load()

		if self.was_active and not self.active:
			self.was_active = False
			self.action = (self.id, "refresh image")
			self.active = True

			if self.phase == "edge":
				self.edge_detect(self.line_drawing)
				self.img.load()
			else:
				self.render_trails()


	def edge_detect(self, line_drawing = False):

		if line_drawing:

			self.blurred = cv2.GaussianBlur(self.grey, (self.blur_r, self.blur_r), 0)

			cv2.imwrite(self.edged_path, self.blurred)

			with PIL.Image.open(self.edged_path) as img:

				pxl_map = img.load()

				a = [[0 for i in range(img.size[0])] for j in range(img.size[1])]

				b = [[0 for i in range(img.size[0])] for j in range(img.size[1])]

				for j in range(img.size[0]):
					for i in range(img.size[1]):
						a[i][j] = pxl_map[j,i]

				for i in range(len(a)):
					for j in range(len(a[i])):
						if a[i][j] < 127: a[i][j] = 255
						else: a[i][j] = 0

				for i in range(1, len(a)):

					for j in range(1, len(a[i])):

						if (a[i][j-1] == 0 and a[i][j] == 255):
							b[i][j] = 255
						elif (a[i-1][j] == 0 and a[i][j] == 255):
							b[i][j] = 255

				img = Image.fromarray(np.uint8(b))

				img.save(self.edged_path)

		else:

			self.blurred = cv2.GaussianBlur(self.grey, (self.blur_r, self.blur_r), 0)
			self.edged_file = cv2.Canny(self.blurred, *self.detect_range)
			cv2.imwrite(self.edged_path, self.edged_file)

	def get_action(self):
		return self.action

	def get_hover(self):
		return self.hover


	def draw(self, display):

		self.surface.fill((225, 225, 225))

		pygame.draw.line(self.surface, (130, 130, 130), self.slider1_pos[0], self.slider1_pos[1], 10*SCALE())
		pygame.draw.line(self.surface, (180, 180, 180), self.slider1_pos[0], self.slider1_pos[1], 8*SCALE())
		pygame.draw.line(self.surface, (0, 0, 0), add_tuple(self.slider1_pos[0], (-10*SCALE(), 0)), add_tuple(self.slider1_pos[0], (5*SCALE(), 0)), 1*SCALE())
		pygame.draw.line(self.surface, (0, 0, 0), add_tuple(self.slider1_pos[1], (-10*SCALE(), 0)), add_tuple(self.slider1_pos[1], (5*SCALE(), 0)), 1*SCALE())

		pygame.draw.line(self.surface, (120, 120, 120), add_tuple(self.sliders["max1"].rect.topleft, (4*SCALE(), 4)), add_tuple(self.sliders["min1"].rect.topleft, (4*SCALE(), 4)), 7*SCALE())
		pygame.draw.line(self.surface, (80, 80, 80), add_tuple(self.sliders["max1"].rect.topleft, (4*SCALE(), 4)), add_tuple(self.sliders["min1"].rect.topleft, (4*SCALE(), 4)), 3*SCALE())


		pygame.draw.line(self.surface, (130, 130, 130), self.slider2_pos[0], self.slider2_pos[1], 10*SCALE())
		pygame.draw.line(self.surface, (180, 180, 180), self.slider2_pos[0], self.slider2_pos[1], 8*SCALE())
		pygame.draw.line(self.surface, (0, 0, 0), add_tuple(self.slider2_pos[0], (-10*SCALE(), 0)), add_tuple(self.slider2_pos[0], (5*SCALE(), 0)), 1*SCALE())
		pygame.draw.line(self.surface, (0, 0, 0), add_tuple(self.slider2_pos[1], (-10*SCALE(), 0)), add_tuple(self.slider2_pos[1], (5*SCALE(), 0)), 1*SCALE())
		
		pygame.draw.line(self.surface, (120, 120, 120), add_tuple(self.sliders["max2"].rect.topleft, (4*SCALE(), 4)), (self.sliders["max2"].rect.left + 4*SCALE(), self.slider2_pos[1][1]), 7*SCALE())
		pygame.draw.line(self.surface, (80, 80, 80), add_tuple(self.sliders["max2"].rect.topleft, (4*SCALE(), 4)), (self.sliders["max2"].rect.left + 4*SCALE(), self.slider2_pos[1][1]), 3*SCALE())


		for slider in self.sliders:
			self.sliders[slider].draw(self.surface)

		for button in self.buttons:
			if not ((button == "auto" and self.phase != "edge") or (button == "prev" and self.phase == "edge")):
				self.buttons[button].draw(self.surface)

		for text in self.texts:
			if not ((text == "auto" and self.phase != "edge") or (text in ("prev", "nodes") and self.phase == "edge")):
				self.texts[text].draw(self.surface)

		pygame.draw.rect(self.surface, (153, 153, 153), ((0, 0), self.rect.size), 4*SCALE())
		pygame.draw.rect(self.surface, (68, 68, 68), ((0, 0), self.rect.size), 2*SCALE())
		self.img.draw(self.surface)

		display.blit(self.surface, self.rect.topleft)




	def render_trails(self):

		self.img.image.fill((0, 0, 0))

		self.trails = self.find_trails()

		for trail in self.trails:

			for i in range(0, len(trail)):

				pygame.draw.circle(self.img.image, (100, 100, 100), trail[i], 2)

				if i > 0: pygame.draw.aaline(self.img.image, (80, 255, 80), trail[i-1], trail[i], 1)

		total_nodes = sum(len(i) for i in self.trails)
		self.texts["nodes"] = Text(self.fonts[0], "total nodes: " + str(total_nodes), (0.4*self.rect.width + 8*SCALE(), 3*SCALE()), background=False, lifetime=None)



	def find_trails(self):
		with PIL.Image.open(self.edged_path) as img:

			pxl_map = img.load()

			# convert to array form
			a = [[0 for j in range(img.size[1])] for i in range(img.size[0])]

			for i in range(img.size[0]):
					for j in range(img.size[1]):
							a[i][j] = pxl_map[i,j]

			# find a white pixel
			first_edge = find_edge(a)

			last_x, last_y = -1, -1
			trails = []

			# follow path of nearby white pixels, building an array of points visited
			while first_edge != -1:

				x, y = first_edge
				prev_dir = 30
				skips = 0
				one_end_found = False

				curr_trail = []
				curr_trail.append((x, y))

				# if it's stuck in a loop, set the pixels it's stuck on to black
				if last_x == x and last_y == y:
					a[x][y] = 0

				newstart = find_direction(a, x, y, self.START_R, 0)

				first_start = x, y, 30
				
				# if no white pixel is found, increase leniency up to a maximum radius and minimum number of pixels threshold
				while newstart != -1:

					x, y, new_dir = newstart
					
					# Skip out new point if it's in the same direction, to a maximum of MAX_STRAIGHT_SKIP
					if new_dir - prev_dir == 0:
						skips += 1

					if skips == self.MAX_STRAIGHT_SKIP or new_dir - prev_dir != 0:
						curr_trail.append((x, y))

						skips = 0

						# Don't change recorded prev direction unless there's been a direction change - prevent circles being one point
						prev_dir = new_dir



					i = 0
					while True:

						newstart = find_direction(a, x, y, self.START_R + i, int(self.END_R * i/max(1, float(self.END_R - self.START_R))))

						if newstart == -1:
							i += 1

							if self.START_R + i > self.END_R:

								curr_trail.append((x, y))

								if not one_end_found:
									# Can't go any further this way, try going the other direction from where we started
									one_end_found = True
									newstart = first_start
									curr_trail = [i for i in reversed(curr_trail)]

								# If gone the other way already, end the loop, start new trail
								break

						else:
							i = 0
							break

				# Trail finished, record and start a new one
				trails.append(curr_trail)
				last_x, last_y = x, y
			 
				first_edge = find_edge(a, first_edge[0])

			# Remove shortest trails
			i = 0
			while i < len(trails):
				if len(trails[i]) <= 3:
					trails.pop(i)
				else:
					i += 1

			# Reduce point number according to JUMP_LENGTH, but preserve end points
			for trail in trails:

				i = 0
				j = 1
				while j < len(trail):

					i += 1

					if self.JUMP_LENGTH == 0:
						j += 1
					elif i % self.JUMP_LENGTH == 0:
						j += 1
					else:
						trail.pop(j) 

					if j > len(trail) - self.JUMP_LENGTH/2 - 1:
						for k in range(j, len(trail)-1):
							trail.pop(j)
						break

		return trails



def find_edge(a, start=0):
	for i in range(start, len(a)):
		for j in range(len(a[i])):
			if a[i][j] == 255:
				return i, j

	return -1


def clip(a, b):
	return min(len(a) - 1, max(0, b))

rnd = lambda x: int(x + 0.5)

_RT2 = 0.707
RT2_3 = 0.866
C22_5 = 0.924
S22_5 = 0.383

def find_direction(a, x, y, r, threshold):

	d = 2*r - 1


	x1 = max(0, x - (r-1))
	y1 = max(0, y - (r-1))


	cellstarts = [[x1, y1-d],
								[x1+rnd(d*S22_5), y1-rnd(d*C22_5)],
								[x1+rnd(d*_RT2),   y1-rnd(d*_RT2)],
								[x1+rnd(d*C22_5), y1-rnd(d*S22_5)], 

								[x1+d, y1],
								[x1+rnd(d*C22_5), y1+rnd(d*S22_5)],
								[x1+rnd(d*_RT2),   y1+rnd(d*_RT2)],
								[x1+rnd(d*S22_5), y1+rnd(d*C22_5)],

								[x1, y1+d], 
								[x1-rnd(d*S22_5), y1+rnd(d*C22_5)],
								[x1-rnd(d*_RT2),   y1+rnd(d*_RT2)],	
								[x1-rnd(d*C22_5), y1+rnd(d*S22_5)],

								[x1-d, y1],
								[x1-rnd(d*C22_5), y1-rnd(d*S22_5)],
								[x1-rnd(d*_RT2),   y1-rnd(d*_RT2)], 
								[x1-rnd(d*S22_5), y1-rnd(d*C22_5)]]


	max_total = 0
	direction = -1
	for k in range(len(cellstarts)):
		start = cellstarts[k]

		total = 0

		for i in range(clip(a, start[0]-r), clip(a, start[0]+r)):
			for j in range(clip(a[0], start[1]-r), clip(a[0], start[1]+r)):
				total += a[i][j]
				a[i][j] = 0


		#print start, total/255

		if total > max_total:
			max_total = total
			direction = k

	#print direction

	#erase lines
	if direction != -1:

		for i in range(clip(a, x1), clip(a, x1+d)):
			for j in range(clip(a[0], y1), clip(a[0], y1+d)):
				a[i][j] = 0


	if max_total > threshold and direction != -1:
		return (clip(a, cellstarts[direction][0] + r - 1), clip(a[0], cellstarts[direction][1] + r - 1), direction)
	else:
		return -1