import pygame
import xbm_generator
from pygame.locals import *
from sprites import *
from basic import *
from tools_window import *










###############
# Undo & Redo
###############










class Editor(object):

	def __init__(self, trace, name):

		self.name = name
		self.trace = trace

		pygame.font.init()

		self.get_local_settings()
		
		SETSCALE(int(float(self.settings['window size'][:-1])))
		self.width = int(900*SCALE())
		self.height = int(800*SCALE())
		self.trace_rect = Rect((int(30)*SCALE(), int(80*SCALE())), (int(840*SCALE()), int(520*SCALE())))
		self.zoom = 1.0
		self.screen_pos = 0
		self.display = pygame.display.set_mode((self.width, self.height))

		self.whitewash = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.whitewash.fill((255, 255, 255, 120))
		
		self.large_font = pygame.font.Font('C:\Windows\Fonts\\calibri.ttf', int(18*SCALE()))
		self.med_font = pygame.font.Font('C:\Windows\Fonts\\calibri.ttf', int(14*SCALE()))
		self.small_font = pygame.font.Font('C:\Windows\Fonts\\calibri.ttf', int(10*SCALE()))
		
		self.grid_types = ['Lined',
										   'Dotted',
										   'None']

		xbm_generator.generate()

		self.cm = xbm_generator.Cursor_Manager("arrow")

		pygame.mouse.set_visible(1)

		self.trace.load(self.trace_rect, self.settings['grid type'])

		self.tools_window_init(CWD() + '\Images\\')
		self.scrollbars_init(CWD() + '\Images\\')
		self.buttons_init(CWD() + '\Images\\')
		self.trace.frame_selector.load()

		self.mouse = {'Ldown' : False, 'Lup' : False, 'Lactive' : False, 
								  'Rdown' : False, 'Rup' : False, 'Ractive' : False, 
								  'Scrollup' : False, 'Scrolldown' : False, 
								  'pos' : (0, 0)}

		self.mod_key = 'None'
		self.k_space = False
		self.active_tools = []

		self.action = 'None'
		self.action_time = 0
		self.follow_mouse = [False]
		self.input_req = {"Action" : False,
											"Allowlist" : [],
											"NoDrawlist" : []}

		self.selected = False
		self.selecting = False
		self.copy_selection = False

		self.timedown_vs_speed_pairs = [[0 , SCALE()],
																		[10, 0],
																		[35, 2*SCALE()]]
		self.texts = {}

		self.draw_list = []

		self.starttime = time.clock()

	def handle_framerate(self):

		time_dif = time.clock()-self.starttime
		if time_dif < 0.03: time.sleep(0.033 - time_dif)
		
		time_dif_2 = time.clock()-self.starttime
		framerate =  int(round(1/time_dif_2))
		self.texts['framerate'] = Text(self.large_font, str(framerate), (self.width, 53*SCALE()), background=None, align_right=True)
		
		self.starttime = time.clock()

	def update(self):

		clear()

		self.handle_framerate()

		pygame.mouse.get_pos()
		self.events_update()

		self.get_elements()

		self.tool_buttons = self.tools_window.tool_buttons

		self.update_states()

		self.check_active()

		self.enforce_action()

	def get_elements(self):

		self.elements = [self.tools_window, self.trace] + self.buttons.values() + self.scrollbars.values() + self.texts.values()
		
		if self.selecting or self.selected: self.elements.append(self.selection)

		self.elements.sort(key=lambda x: x.z)


	def check_active(self):

		new_action = False

		self.cm.adjust(self.mouse)

		cursor_set = 'arrow'

		for obj in reversed(self.elements):
			if self.follow_mouse[0] == obj.id or not self.follow_mouse[0] and ((not self.input_req["Action"]) or obj.id in self.input_req["Allowlist"]):
				obj.check_active(self.mouse)
				
				if obj.hover and cursor_set == 'arrow':
					cursor_set = obj.get_hover()

				if obj.active:
					new_action = obj.get_action()
					break

		if self.follow_mouse[0]:

			if not (self.mouse['Lactive'] or self.mouse['Ractive']):
				self.action = 'None'
				self.follow_mouse = [False]
			else:
				print "/".join(str(i) for i in self.follow_mouse) + '/following mouse'

		if self.follow_mouse[-1] != "until click stops":
			if new_action:

				if self.action != new_action:
					self.action_time = 0
				else:
					self.action_time += 1

				self.action = new_action
				
				if not self.follow_mouse[0]: print "/".join(str(i) for i in self.action)

			else:
				self.action = 'None'

		if self.follow_mouse[0] or (cursor_set == "click" and (self.mouse["Lactive"] or self.mouse["Ractive"])):

			cursor_set = "grab"

		if self.cm.cursor != cursor_set:

			self.cm.set(cursor_set, self.mouse)

		self.tool_actions_check_active()


	def update_states(self):

		self.settings['tools window pos'] = self.tools_window.rect.topleft

		self.tools_window.update(self.mod_key)

		self.zoom = (100 - self.scrollbars['zoom scrollbar'].sprites[-1].percent) / 11.0 + 1

		self.scrollbars['up scrollbar'].update(zoom=self.zoom)
		self.scrollbars['across scrollbar'].update(zoom=self.zoom)

		self.pos_percent = (self.scrollbars['across scrollbar'].sprites[-1].percent,
												self.scrollbars['up scrollbar'].sprites[-1].percent)
			
		self.trace.update(zoom=self.zoom, pos=self.pos_percent, tools=self.active_tools, space=self.k_space, mod=self.mod_key)

		if self.input_req["Action"]:
			self.trace.update(input_req=self.input_req["Action"])

		elif "action required text" in self.texts:
			self.texts["action required text"].expired = True

		self.info_text_update()


	def check_speed(self, clicktime):
		
		for pair in self.timedown_vs_speed_pairs:
			if clicktime <= pair[0]: 
				return pair[1]

		return 6*SCALE()


	def enforce_action(self):
		cf = self.trace.get_cf()

		# scrollbar management


		if self.action[0] == 'zoom scrollbar':

			self.texts['info'] = Text(self.med_font, 'zoom = ' + str(self.zoom)[:4] + 'x', (3*SCALE(), 53*SCALE()))
			
			if self.action[1] == 'increase':
				self.scrollbars['zoom scrollbar'].sprites[-1].update(add=-self.check_speed(self.action_time))
			
			if self.action[1] == 'decrease':
				self.scrollbars['zoom scrollbar'].sprites[-1].update(add=self.check_speed(self.action_time))

			if self.action[1] == 'slider': 
				self.follow_mouse = ('zoom scrollbar', 'slider', 'until click stops')



		elif self.action[0] == 'up scrollbar':

			self.texts['info'] = Text(self.med_font, 'top left Y pos = ' + str(cf.rect.topleft[1])[:4], (3*SCALE(), 53*SCALE()))
			
			if self.action[1] == 'increase':
				self.scrollbars['up scrollbar'].sprites[-1].update(add=-self.check_speed(self.action_time))
			
			if self.action[1] == 'decrease':
				self.scrollbars['up scrollbar'].sprites[-1].update(add=self.check_speed(self.action_time))

			if self.action[1] == 'slider':
				self.follow_mouse = ('up scrollbar', 'slider', 'until click stops')



		elif self.action[0] == 'across scrollbar':

			self.texts['info'] = Text(self.med_font, 'top left X pos = ' + str(cf.rect.topleft[0])[:4], (3*SCALE(), 53*SCALE()))
			
			if self.action[1] == 'increase':
				self.scrollbars['across scrollbar'].sprites[-1].update(add=self.check_speed(self.action_time))
			
			if self.action[1] == 'decrease':
				self.scrollbars['across scrollbar'].sprites[-1].update(add=-self.check_speed(self.action_time))

			if self.action[1] == 'slider':
				self.follow_mouse = ('across scrollbar', 'slider', 'until click stops')



		if self.action[0] == 'frame scrollbar':

			if self.action[1] == 'increase':
				self.scrollbars['frame scrollbar'].sprites[-1].update(add=self.check_speed(self.action_time))
			
			if self.action[1] == 'decrease':
				self.scrollbars['frame scrollbar'].sprites[-1].update(add=-self.check_speed(self.action_time))
			
			self.trace.frame_selector.update(displace=self.scrollbars['frame scrollbar'].sprites[-1].percent/100)
		
			if self.action[1] == 'slider': 
				self.follow_mouse = ('frame scrollbar', 'slider', 'until click stops')


		# management of things pertaining to frame/selection		


		elif self.action[0] == 'trace' and self.action[1] == 'frame':
			

			if self.action[-2] == 'move point':
				self.follow_mouse = ("trace point", self.action[-1], 'until click stops')
				cf.move_point(self.mouse)

				move_amounts = cf.change_pos

				if move_amounts[0] != 0:
					self.scrollbars['across scrollbar'].sprites[-1].update(add=self.check_speed(self.action_time)*move_amounts[0])

				if move_amounts[1] != 0:
					self.scrollbars['up scrollbar'].sprites[-1].update(add=self.check_speed(self.action_time)*move_amounts[1])


			elif self.action[-1] == 'delete point':
				cf.delete_point('active')


			elif self.action[-1] == 'add point':
				cf.add_point(cf.min_distance['next_point'], cf.min_distance['pos'], True)


			elif self.action[-1] == 'toggle line':
				cf.toggle_line(cf.min_distance['next_point'])


			elif self.action[-1] == 'make selection':
				cf.make_selection(self.mouse)
				self.follow_mouse = self.action


			elif self.action[-1] == 'mutate selection':
				if any(len(i) > 0 for i in self.tool_buttons['mutate selection']):
					self.tools_window.update_tool_buttons(self.tool_buttons['mutate selection'][0][0], 'make selection', self.tool_buttons['mutate selection'][0][1] if len(self.tool_buttons['mutate selection'][0]) > 1 else 'None')


			elif self.action[-3] == 'selection':

				cf.update_selection(self.action[-1], point=self.action[-2], mouse=self.mouse)
				self.follow_mouse = self.action + ('until click stops',)


			elif self.action[-1] == "end paste":

				cf.add_point(cf.min_distance['next_point'], [self.copy_selection.points_in_rect[key] for key in sorted(self.copy_selection.points_in_rect)])

				cf.selection = self.copy_selection.copy()

				cf.selection.points_in_rect = {}

				i = 0
				for key in sorted(self.copy_selection.points_in_rect):

					cf.selection.points_in_rect[cf.min_distance['next_point'] + i] = self.copy_selection.points_in_rect[key]
					i += 1

				self.input_req = {"Action" : False,
													"Allowlist" : [],
													"NoDrawlist" : []}
				cf.active = False
				cf.action = False
				self.trace.update(input_req = False)

			elif self.action[-1] == 'toggle select type':

				if any(self.mod_key in i for i in self.tool_buttons['make selection']) or (self.mod_key == "None" and any(len(i) == 1 for i in self.tool_buttons['make selection'])):
					self.tools_window.update_tool_buttons(self.tool_buttons['make selection'][0][0], 'mutate selection')

				elif any(self.mod_key in i for i in self.tool_buttons['mutate selection']) or (self.mod_key == "None" and any(len(i) == 1 for i in self.tool_buttons['mutate selection'])):
					self.tools_window.update_tool_buttons(self.tool_buttons['mutate selection'][0][0], 'make selection')


			elif self.action[-1] in ('grab & move', 'scroll up', 'scroll down', 'scroll right', 'scroll left', 'zoom in', 'zoom out'):
				move_amounts = cf.change_pos
				
				if move_amounts[0] != 0:
					self.scrollbars['across scrollbar'].sprites[-1].update(add_displace=move_amounts[0])

				if move_amounts[1] != 0:
					self.scrollbars['up scrollbar'].sprites[-1].update(add_displace=move_amounts[1])

				if move_amounts[2] != 0:
					self.scrollbars['zoom scrollbar'].sprites[-1].update(add_displace=move_amounts[2])

				# self.follow_mouse = 'frame ' + str(self.trace.curr_frame_n)


		# manage frame selector


		if self.action[0] == 'trace' and self.action[1] == 'frame selector':


			if self.action[2] == 'select frame':

				self.trace.curr_frame_n = int(self.trace.frame_selector.active)


			elif self.action[2] == 'delete frame':

				self.trace.delete_frame(int(self.trace.frame_selector.active))
				self.scrollbars['frame scrollbar'].sprites[-1].update(length=self.scrollbars['frame scrollbar'].sprites[-1].range/self.trace.frame_selector.len_percent)
				self.trace.frame_selector.update(displace=self.scrollbars['frame scrollbar'].sprites[-1].percent/100)


			elif self.action[2] == 'add empty frame':

				self.trace.add_frame([])
				self.scrollbars['frame scrollbar'].sprites[-1].update(max=True, length=self.scrollbars['frame scrollbar'].sprites[-1].range/self.trace.frame_selector.len_percent)
				self.trace.frame_selector.update(displace=self.scrollbars['frame scrollbar'].sprites[-1].percent/100)


		# manage tools window


		elif self.action[0] == 'tools window':


			if self.action[1] == 'move':
				self.follow_mouse = ('tools window', 'until click stops')
				self.tools_window.move(self.mouse)


			elif self.action[-2] == 'slider':
				self.follow_mouse = ('tools window', 'slider', 'until click stops')


		# manage toolbar buttons


		if self.action[0] == 'deselect' and cf.selection:
			cf.selection = False
			if any(len(i) > 0 for i in self.tool_buttons['mutate selection']):
				self.tools_window.update_tool_buttons(self.tool_buttons['mutate selection'][0][0], 'make selection', self.tool_buttons['mutate selection'][0][1] if len(self.tool_buttons['mutate selection'][0]) > 1 else 'None')



		elif self.action[0] == 'grid':
			self.buttons['grid'].cycle()

			self.settings['grid type'] = self.grid_types[self.buttons['grid'].curr_image]
			self.trace.grid_type = self.settings['grid type']

			text = 'Grid type is now ' + self.settings['grid type']
			if self.action[-1] == '1': text += ' - Warning: May cause low framerate'
			self.texts['grid info'] = Text(self.med_font, text, (3*SCALE(), 53*SCALE()))



		elif self.action[0] == 'save':
			self.trace.save_file(CWD() + '\Traces\\' + self.name, self.name)



		elif self.action[0] == 'cut':
			self.copy_selection = cf.update_selection("cut", mouse=self.mouse)


		elif self.action[0] == 'copy':
			self.copy_selection = cf.selection.copy()


		elif self.action[0] == 'paste':
			if self.copy_selection:
				if cf.selection:
					cf.selection = False

				self.input_req = {"Action" : "paste",
													"Allowlist" : ["trace", "up scrollbar", "across scrollbar", "zoom scrollbar", "action required text", "zoom text", "mouse x pos text", "mouse y pos text", "frame x pos text", "frame y pos text"],
													"NoDrawlist" : ["tools window"]}

				self.texts["action required text"] = Text(self.med_font, "Please select a line to paste onto", (3*SCALE(), 53*SCALE()), lifetime = None)


		elif self.action[0] == 'help':

			for button in self.buttons:
				self.texts[button] = Text(self.small_font, button, self.buttons[button].rect.bottomleft)

			for button in self.tools_window.tools:
				if button[:5] != "blank": 
					if self.tools_window.tools[button].tool_no % 2: self.texts[button] = Text(self.small_font, button, add_tuple(self.tools_window.rect.topleft, self.tools_window.tools[button].rect.bottomleft, (0, -SCALE()*10)), z=11, fit_rect=self.tools_window.rect, only_show_in_bounding_rect=True)
					else: self.texts[button] = Text(self.small_font, button, add_tuple(self.tools_window.rect.topleft, self.tools_window.tools[button].rect.topleft), z=11, fit_rect=self.tools_window.rect, only_show_in_bounding_rect=True)



		
		point_pos_update = False
		for text in self.texts:
			if text[:9] == 'point pos':
				point_pos_update = True

		if self.action[0] == 'show point pos' or point_pos_update:

			lifetime = 125

			pop_lst = []
			for text in self.texts:
				if text[:9] == 'point pos':
					pop_lst.append(text)
					lifetime = self.texts[text].lifetime

			for text in pop_lst:
				self.texts.pop(text)

			if lifetime > 1:
				points = self.trace.get_points()
				
				for point in points:
					self.texts['point pos ' + str(point)] = Text(self.med_font, str(point) + ': ' + str(tuple(points[point][0])), add_tuple(self.trace_rect.topleft, points[point][1]), lifetime=lifetime, fit_rect = self.trace_rect)


	def events_update(self):

		events = pygame.event.get()

		self.mouse['Ldown'] = False
		self.mouse['Lup'] = False
		self.mouse['Rdown'] = False
		self.mouse['Rup'] = False
		self.mouse['Scrollup'] = False
		self.mouse['Scrolldown'] = False
		self.mouse['pos'] = pygame.mouse.get_pos()

		for event in events:
			if event.type == pygame.QUIT:
				if any(len(i) > 0 for i in self.tool_buttons['mutate selection']):
					self.tools_window.update_tool_buttons(self.tool_buttons['mutate selection'][0][0], 'make selection', self.tool_buttons['mutate selection'][0][1] if len(self.tool_buttons['mutate selection'][0]) > 1 else 'None')
				self.local_settings_write()
				exit(0)

			# manage mouse button updates

			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					self.mouse['Ldown'] = True
					self.mouse['Lactive'] = True
				elif event.button == 3:
					self.mouse['Rdown'] = True
					self.mouse['Ractive'] = True

			elif event.type == MOUSEBUTTONUP:
				if event.button == 1:
					self.mouse['Lup'] = True
					self.mouse['Lactive'] = False
				elif event.button == 3:
					self.mouse['Rup'] = True
					self.mouse['Ractive'] = False
				elif event.button == 4:
					self.mouse['Scrollup'] = True
				elif event.button == 5:
					self.mouse['Scrolldown'] = True


		# get alteration key states

		if pygame.key.get_focused():

			mod_keys = pygame.key.get_mods()
			if mod_keys & pygame.KMOD_ALT:
				if self.mod_key == 'None':
					self.mod_key = 'alt'
			elif self.mod_key == 'alt':
				self.mod_key = 'None'
			
			if mod_keys & pygame.KMOD_CTRL:
				if self.mod_key == 'None':
					self.mod_key = 'ctrl'
			elif self.mod_key == 'ctrl':
				self.mod_key = 'None'
			
			if mod_keys & pygame.KMOD_SHIFT:
				if self.mod_key == 'None':
					self.mod_key = 'shift'
			elif self.mod_key == 'shift':
				self.mod_key = 'None'

			keys = pygame.key.get_pressed()
			if keys[K_SPACE]:
				self.k_space = True
			else:
				self.k_space = False
	
	def draw(self):

		# draw background

		self.display.fill((200, 200, 200))

		pygame.draw.rect(self.display, (0, 170, 0), (subtract_tuple(self.trace_rect.topleft, (SCALE()*2, SCALE()*2)), add_tuple(self.trace_rect.size, (SCALE()*4, SCALE()*4))))
		
		pygame.draw.rect(self.display, (125, 125, 125), ((0, int(630*SCALE())), (self.width, self.height - int(630*SCALE()))))
		pygame.draw.line(self.display, (255, 255, 255), (0, int(631*SCALE())), (self.width, int(631*SCALE())), int(3*SCALE()))

		pygame.draw.rect(self.display, (125, 125, 125), ((0, 0), (self.width, int(50*SCALE()))))
		pygame.draw.line(self.display, (255, 255, 255), (0, int(50*SCALE())), (self.width, int(50*SCALE())), 3)

		pygame.draw.rect(self.display, (68, 68, 68), ((int(58*SCALE()-2), int(636*SCALE())-2), (int(784*SCALE())+4, int(134*SCALE())+4)), 1)
		pygame.draw.rect(self.display, (153, 153, 153), ((int(58*SCALE()-1), int(636*SCALE())-1), (int(784*SCALE())+2, int(134*SCALE())+2)), 1)

		# draw elements in order
		
		if self.input_req["Action"]:
			for obj in self.elements: 
				if obj.id not in self.input_req["NoDrawlist"]:
					obj.draw(self.display)

			self.display.blit(self.whitewash, (0, 0))

			for obj in self.elements: 
				if obj.id not in self.input_req["NoDrawlist"] and obj.id in self.input_req["Allowlist"]:
					obj.draw(self.display)

		else:
			for obj in self.elements: 
				obj.draw(self.display)

		pygame.display.update()

	# read from local settings file

	def get_local_settings(self):

		self.settings = {}		
		settings_file = open('local_settings.txt', 'r')

		lines = [line.rstrip('\n') for line in settings_file]

		settings_file.close()

		settings = lines[:lines.index('Tool buttons:')]
		tool_button_lines = lines[lines.index('Tool buttons:') + 1:]

		for line in settings:
			key = line[:line.find('=') - 1]
			value = line[line.find('=') + 2:]
			self.settings[key] = value

		self.settings['tools window pos'] = convert_str_tuple_to_tuple(self.settings['tools window pos'], type=float)
		self.settings['window size'] = str(max(1.0, min(4.0, float(self.settings['window size'][:-1])))) + 'x'

		self.tool_buttons = {}

		for line in tool_button_lines:
			key, value = line[:line.find('=') - 1], line[line.find('=') + 2:]

			if '],[' in value:
				lmouse, rmouse = value[:value.find('],[')+1], value[value.find('],[')+2:]
				self.tool_buttons[key] = [convert_str_list_to_list(lmouse), convert_str_list_to_list(rmouse)]
			else:
				self.tool_buttons[key] = [convert_str_list_to_list(value)]

	# write to local settings file

	def local_settings_write(self):
		
		settings_file = open('local_settings.txt', 'w')

		# self.tool_buttons = self.tools_window.get_tools()

		to_write = ''
		for key in self.settings:
			to_write += key + ' = ' + str(self.settings[key]) + '\n'

		to_write += 'Tool buttons:\n'

		for tool in self.tool_buttons:

			if len(self.tool_buttons[tool]) == 2:
				to_write += tool + ' = [' + reduce(lambda x, y : x + ',' + y, self.tool_buttons[tool][0]) + '],[' + reduce(lambda x, y : x + ',' + y, self.tool_buttons[tool][1]) + ']\n'
			elif len(self.tool_buttons[tool]) == 1:
				to_write += tool + ' = [' + reduce(lambda x, y : x + ',' + y, self.tool_buttons[tool][0]) + ']\n'

		settings_file.write(to_write)

		settings_file.close()

	def tools_window_init(self, directory):

		self.tools_window = Tools_Window(self.settings['tools window pos'], 0, self.small_font, directory, self.tool_buttons,
																		{'add point' : Tool(directory + 'Tools\\add_point_tool.png', 0),
																		 'delete point' :  Tool(directory + 'Tools\\delete_point_tool.png', 1),
																		 'move point' :  Tool(directory + 'Tools\\move_point_tool.png', 2),
																		 'toggle line' :  Tool(directory + 'Tools\\toggle_line_tool.png', 3),
																		 'make selection' :  Tool(directory + 'Tools\\select_tool.png', 4),
																		 'blank5' :  Tool(directory + 'Tools\\blank_tool.png', 5),
																		 'mutate selection' :  Tool(directory + 'Tools\\mutate_selection.png', 6),
																		 'blank7' :  Tool(directory + 'Tools\\blank_tool.png', 7),
																		 'blank8' :  Tool(directory + 'Tools\\blank_tool.png', 8),
																		 'blank9' :  Tool(directory + 'Tools\\blank_tool.png', 9),
																		 'blank10' :  Tool(directory + 'Tools\\blank_tool.png', 10)},
																		{'Lmouse' : Sprite(None, directory + 'Tools\\Lmouse.png'),
																		 'Rmouse' : Sprite(None, directory + 'Tools\\Rmouse.png'),
																		 'L&Rmouse' : Sprite(None, directory + 'Tools\\L&Rmouse.png'),
																		 'Lalt' : Sprite(None, directory + 'Tools\\Lalt.png'),
																		 'Ralt' : Sprite(None, directory + 'Tools\\Ralt.png'),
																		 'Lctrl' : Sprite(None, directory + 'Tools\\Lctrl.png'),
																		 'Rctrl' : Sprite(None, directory + 'Tools\\Rctrl.png'),
																		 'Lshift' : Sprite(None, directory + 'Tools\\Lshift.png'),
																		 'Rshift' : Sprite(None, directory + 'Tools\\Rshift.png')},)
		
		self.tools_window.load()

	def scrollbars_init(self, directory):

		scrollbar_up = Scrollbar((872, 78), 0, Button((0, 0), directory + 'scrollbar_arrow.png', type='on_mouse_down'),
																				   Sprite((0, 28), directory + 'scrollbar_up_bar.png'),
																				   Button((0, 496), directory + 'scrollbar_arrow.png', type='on_mouse_down'))
		scrollbar_up.load(id='up scrollbar')
		scrollbar_up.sprites[2].image = pygame.transform.flip(scrollbar_up.sprites[2].image, False, True)

		scrollbar_across = Scrollbar((28, 602), 1, Button((0, 0), directory + 'scrollbar_arrow.png', type='on_mouse_down'),
																						   Sprite((28, 0), directory + 'scrollbar_across_bar.png'),
																						   Button((816, 0), directory + 'scrollbar_arrow.png', type='on_mouse_down'))
		scrollbar_across.load(id='across scrollbar')
		scrollbar_across.sprites[0].image = pygame.transform.rotate(scrollbar_across.sprites[0].image, 90)
	 	scrollbar_across.sprites[2].image = pygame.transform.rotate(scrollbar_across.sprites[2].image, 270)

	 	scrollbar_frames = Scrollbar((0, 634), 1, Button((0, 0), directory + 'frame_scrollbar_arrow.png', type='on_mouse_down'),
																						   Sprite((56, 138), directory + 'scrollbar_across_bar.png'),
																						   Button((844, 0), directory + 'frame_scrollbar_arrow.png', type='on_mouse_down'))
	 	scrollbar_frames.load(id='frame scrollbar')
	 	
	 	scrollbar_frames.sprites[2].image = pygame.transform.flip(scrollbar_frames.sprites[0].image, True, False)
	 	scrollbar_frames.sprites[-1].update(length=scrollbar_frames.sprites[-1].range/self.trace.frame_selector.len_percent)

	 	scrollbar_zoom = Scrollbar((0, 78), 0, Button((0, 0), directory + 'zoomin_button.png', type='on_mouse_down'),
																				   Sprite((0, 28), directory + 'scrollbar_up_bar.png'),
																				   Button((0, 496), directory + 'zoomout_button.png', type='on_mouse_down'))
		scrollbar_zoom.load(id='zoom scrollbar')

		self.scrollbars = {scrollbar_up.id : scrollbar_up,
										   scrollbar_across.id : scrollbar_across,
										   scrollbar_zoom.id : scrollbar_zoom,
										   scrollbar_frames.id : scrollbar_frames}

	def buttons_init(self, directory):
		self.buttons = {'save' : Button((4*SCALE(), 4*SCALE()), directory + 'save_button.png'),
										'grid' : Cyclic_Button((48*SCALE(), 4*SCALE()), self.grid_types.index(self.settings['grid type']), directory + 'grid_button_1.png', directory + 'grid_button_2.png', directory + 'grid_button_3.png'),
										'deselect' : Button((92*SCALE(), 4*SCALE()), directory + 'deselect_button.png'),
										'cut' : Button((136*SCALE(), 4*SCALE()), directory + 'cut_button.png'),
										'copy' : Button((180*SCALE(), 4*SCALE()), directory + 'copy_button.png'),
										'paste' : Button((224*SCALE(), 4*SCALE()), directory + 'paste_button.png'),
										'help' : Button((810*SCALE(), 4*SCALE()), directory + 'help_button.png'),
										'show point pos' : Button((854*SCALE(), 4*SCALE()), directory + 'show_point_pos_button.png') }
		
		for button in self.buttons:
			self.buttons[button].load(id=button, scale=SCALE())

	def info_text_update(self):
	
		del_lst = []

		for text in self.texts:
			self.texts[text].age()
			if self.texts[text].expired == True:

				del_lst.append(text)

			if not self.texts[text].id:
				self.texts[text].id = text

		for text in del_lst:
			del self.texts[text]

		self.texts['zoom text'] = Text(self.small_font, str(self.zoom)[:4], (0, 601*SCALE()), background=False, lifetime=None)
		self.texts['frame x pos text'] = Text(self.small_font, 'X: ' + str(self.trace.get_cf().rect.topleft[0])[:4], (0, 610*SCALE()), background=False, lifetime=None)
		self.texts['frame y pos text'] = Text(self.small_font, 'Y: ' + str(self.trace.get_cf().rect.topleft[1])[:4], (0, 619*SCALE()), background=False, lifetime=None)

		if self.trace_rect.collidepoint(self.mouse['pos']): 
			self.mouse_frame_pos = self.trace.global_to_rel((self.mouse['pos']))
			self.texts['mouse x pos text'] = Text(self.small_font, 'X: ' + str(int(round(self.mouse_frame_pos[0]))), (871*SCALE(), 604*SCALE()), background=False, lifetime=None)
			self.texts['mouse y pos text'] = Text(self.small_font, 'Y: ' + str(int(round(self.mouse_frame_pos[1]))), (871*SCALE(), 616*SCALE()), background=False, lifetime=None)
		elif 'mouse pos x text' in self.texts:
			self.texts.pop('mouse x pos text')
			self.texts.pop('mouse y pos text')

	def tool_actions_check_active(self):

		self.active_tools = {}
		
		for tool in self.tool_buttons:
			
			for combination in self.tool_buttons[tool]:
				if len(combination) > 1:
					mod_key = combination[1]
				else:
					mod_key = 'None'
				if mod_key == self.mod_key:
					if tool not in self.active_tools: self.active_tools[tool] = ()
					self.active_tools[tool] += (combination[0],)