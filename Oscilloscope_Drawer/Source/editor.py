import pygame
import xbm_generator
from pygame.locals import *
from sprites import *
from selection import *
from basic import *
from tools_window import *

class Editor(object):

	def __init__(self, trace, CWD, name):

		self.CWD = CWD
		self.name = name
		self.trace = trace

		pygame.font.init()

		self.get_local_settings()
		
		self.scale = int(float(self.settings['window size'][:-1]))
		self.width = int(900*self.scale)
		self.height = int(800*self.scale)
		self.trace_rect = Rect((int(30)*self.scale, int(80*self.scale)), (int(840*self.scale), int(520*self.scale)))
		self.zoom = 1.0
		self.screen_pos = 0
		self.display = pygame.display.set_mode((self.width, self.height))
		
		self.large_font = pygame.font.Font('C:\Windows\Fonts\\calibri.ttf', int(18*self.scale))
		self.med_font = pygame.font.Font('C:\Windows\Fonts\\calibri.ttf', int(14*self.scale))
		self.small_font = pygame.font.Font('C:\Windows\Fonts\\calibri.ttf', int(10*self.scale))
		
		self.grid_types = ['Lined',
						   'Dotted',
						   'None']

		xbm_generator.generate(self.scale, self.CWD)

		self.cursors = {'arrow'      : pygame.cursors.load_xbm(CWD + '\Cursors\\arrow.xbm',      CWD + '\Cursors\\arrow_mask.xbm'),
						'click'      : pygame.cursors.load_xbm(CWD + '\Cursors\\click.xbm',      CWD + '\Cursors\\click_mask.xbm'),
						'grab'       : pygame.cursors.load_xbm(CWD + '\Cursors\\grab.xbm',       CWD + '\Cursors\\grab_mask.xbm'),
						'horizontal' : pygame.cursors.load_xbm(CWD + '\Cursors\\horizontal.xbm', CWD + '\Cursors\\horizontal_mask.xbm'),
						'vertical'   : pygame.cursors.load_xbm(CWD + '\Cursors\\vertical.xbm',   CWD + '\Cursors\\vertical_mask.xbm'),
						'diag1'      : pygame.cursors.load_xbm(CWD + '\Cursors\\diag1.xbm',      CWD + '\Cursors\\diag1_mask.xbm'),
						'diag2'      : pygame.cursors.load_xbm(CWD + '\Cursors\\diag2.xbm',      CWD + '\Cursors\\diag1_mask.xbm')}

		self.cursor = 'arrow'
		pygame.mouse.set_visible(1)

		self.trace.load(self.trace_rect, self.scale, self.settings['grid type'])

		self.tools_window_init(CWD + '\Images\\')
		self.scrollbars_init(CWD + '\Images\\')
		self.buttons_init(CWD + '\Images\\')
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
		self.follow_mouse = False

		self.selected = False
		self.selecting = False

		self.timedown_vs_speed_pairs = [[0 , self.scale],
										[10, 0],
										[35, 2*self.scale]]
		self.texts = {}

		self.draw_list = []

		self.starttime = time.clock()

	def handle_framerate(self):

		time_dif = time.clock()-self.starttime
		if time_dif < 0.03: time.sleep(0.033 - time_dif)
		
		time_dif_2 = time.clock()-self.starttime
		framerate =  int(round(1/time_dif_2))
		self.texts['framerate'] = Text(self.large_font, str(framerate), (self.width, 53*self.scale), background=None, align_right=True)
		
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
		
		if self.selecting: self.elements.append(self.selector)
		elif self.selected: self.elements.append(self.selection)

		self.elements.sort(key=lambda x: x.z)

	# def set_action(self, action):

	# 	if _bool:
	# 		if self.action == 'None':
	# 			self.action = action 
	# 	elif self.action == action:
	# 		self.action = 'None'

	def check_active(self):

		new_action = False

		if self.cursor == 'click': 
			self.mouse['pos'] = add_tuple(self.mouse['pos'], (5*self.scale, 0))
		elif self.cursor == 'horizontal' or self.cursor == 'vertical' or self.cursor[:4] == 'diag':
			self.mouse['pos'] = add_tuple(self.mouse['pos'], (12*self.scale, 12*self.scale))

		cursor_set = 'arrow'

		for obj in reversed(self.elements):
			if self.follow_mouse == obj.id or not self.follow_mouse:
				obj.check_active(self.mouse)
				
				if obj.hover:
					cursor_set = obj.get_hover()

				if obj.active:
					new_action = obj.get_action()
					break

		if self.follow_mouse:

			if not (self.mouse['Lactive'] or self.mouse['Ractive']):
				self.action = 'None'
				self.follow_mouse = False
			else:
				print self.follow_mouse + '/following mouse'

		else:

			if new_action:

				if self.action != new_action:
					self.action_time = 0
				else:
					self.action_time += 1

				self.action = new_action
				print self.action

			else:
				self.action = 'None'

		if self.cursor != cursor_set:
			
			if self.cursor == 'arrow' and cursor_set == 'click':
				pygame.mouse.set_pos(subtract_tuple(self.mouse['pos'], (5*self.scale, 0)))

			elif self.cursor == 'click' and cursor_set == 'arrow':
				pygame.mouse.set_pos(add_tuple(self.mouse['pos'], (1, 0)))

			if self.cursor == 'arrow' and (cursor_set == 'horizontal' or cursor_set == 'vertical' or cursor_set[:4] == 'diag'):
				pygame.mouse.set_pos(subtract_tuple(self.mouse['pos'], (12*self.scale, 12*self.scale)))

			elif (self.cursor == 'horizontal' or self.cursor == 'vertical' or self.cursor[:4] == 'diag') and cursor_set == 'arrow':
				pygame.mouse.set_pos(add_tuple(self.mouse['pos'], (1, 0)))

			self.cursor = cursor_set

		if self.cursor == None:
			self.cursor = 'arrow'

		pygame.mouse.set_cursor(*self.cursors[self.cursor])

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

		if self.selecting:
			self.trace.update(selector_rect=self.selector.rect)

		self.info_text_update()

	def check_speed(self, clicktime):
		
		for pair in self.timedown_vs_speed_pairs:
			if clicktime <= pair[0]: 
				return pair[1]

		return 6*self.scale

	def enforce_action(self):

		if self.action[:15] == 'zoom scrollbar/':

			self.texts['info'] = Text(self.med_font, 'zoom = ' + str(self.zoom)[:4] + 'x', (3*self.scale, 53*self.scale))
			
			if 'increase' in self.action:
				self.scrollbars['zoom scrollbar'].sprites[-1].update(add=-self.check_speed(self.action_time))
			
			if 'decrease' in self.action:
				self.scrollbars['zoom scrollbar'].sprites[-1].update(add=self.check_speed(self.action_time))

			if 'slider' in self.action: 
				self.follow_mouse = 'zoom scrollbar'

		elif self.action[:13] == 'up scrollbar/':

			self.texts['info'] = Text(self.med_font, 'top left Y pos = ' + str(self.trace.get_cf().rect.topleft[1])[:4], (3*self.scale, 53*self.scale))
			
			if 'increase' in self.action:
				self.scrollbars['up scrollbar'].sprites[-1].update(add=-self.check_speed(self.action_time))
			
			if 'decrease' in self.action:
				self.scrollbars['up scrollbar'].sprites[-1].update(add=self.check_speed(self.action_time))

			if 'slider' in self.action: self.follow_mouse = 'up scrollbar'

		elif self.action[:17] == 'across scrollbar/':

			self.texts['info'] = Text(self.med_font, 'top left X pos = ' + str(self.trace.get_cf().rect.topleft[0])[:4], (3*self.scale, 53*self.scale))
			
			if 'increase' in self.action:
				self.scrollbars['across scrollbar'].sprites[-1].update(add=self.check_speed(self.action_time))
			
			if 'decrease' in self.action:
				self.scrollbars['across scrollbar'].sprites[-1].update(add=-self.check_speed(self.action_time))

			if 'slider' in self.action: self.follow_mouse = 'across scrollbar'

		if self.action[:16] == 'frame scrollbar/':

			if 'increase' in self.action:
				self.scrollbars['frame scrollbar'].sprites[-1].update(add=self.check_speed(self.action_time))
			
			if 'decrease' in self.action:
				self.scrollbars['frame scrollbar'].sprites[-1].update(add=-self.check_speed(self.action_time))
			
			self.trace.frame_selector.update(displace=self.scrollbars['frame scrollbar'].sprites[-1].percent/100)
		
			if 'slider' in self.action: self.follow_mouse = 'frame scrollbar'

		elif self.action[:6] == 'frame ' and self.action[7] == '/':
			
			if 'move point' in self.action:
				self.trace.get_cf().move_point(self.mouse)

				move_amounts = self.trace.get_cf().change_pos

				if move_amounts[0] != 0:
					self.scrollbars['across scrollbar'].sprites[-1].update(add=self.check_speed(self.action_time)*move_amounts[0])

				if move_amounts[1] != 0:
					self.scrollbars['up scrollbar'].sprites[-1].update(add=self.check_speed(self.action_time)*move_amounts[1])

			elif 'delete point' in self.action:
				self.trace.get_cf().delete_point('active')

			elif 'add point' in self.action:
				self.trace.get_cf().add_point(self.trace.get_cf().min_distance['next_point'], self.trace.get_cf().min_distance['pos'])

			elif 'toggle line' in self.action:
				self.trace.get_cf().toggle_line(self.trace.get_cf().min_distance['next_point'])

			elif 'select' in self.action:
				if self.selecting:
					self.selector.update(mouse=self.mouse['pos'])
				else:
					self.selector = Selector(self.mouse['pos'], self.scale, self.trace_rect, z=8, id='temp_selector')
					self.selecting = True
					self.follow_mouse = 'temp_selector'

			elif 'grab & move' in self.action or 'scroll up' in self.action or 'scroll down' in self.action or 'scroll right' in self.action or 'scroll left' in self.action or 'zoom in' in self.action or 'zoom out' in self.action:
				move_amounts = self.trace.get_cf().change_pos
				
				if move_amounts[0] != 0:
					self.scrollbars['across scrollbar'].sprites[-1].update(add_displace=move_amounts[0])

				if move_amounts[1] != 0:
					self.scrollbars['up scrollbar'].sprites[-1].update(add_displace=move_amounts[1])

				if move_amounts[2] != 0:
					self.scrollbars['zoom scrollbar'].sprites[-1].update(add_displace=move_amounts[2])

				# self.follow_mouse = 'frame ' + str(self.trace.curr_frame_n)

		if not 'select' in self.action and self.selecting:
			self.selecting = False
			self.selected = True
			self.selection = Selection(self.selector.rect, self.scale, self.trace_rect, self.CWD + '\Images\Selection\\', z=8, id='selection')
			del self.selector

		if self.action == 'deselect/click' and self.selected:
			self.selected = False
			del self.selection

		if self.action[:15] == 'frame selector/':

			if 'select frame' in self.action:
				self.trace.curr_frame_n = int(self.trace.frame_selector.active)
			elif 'delete frame' in self.action:
				self.trace.delete_frame(int(self.trace.frame_selector.active))
				self.scrollbars['frame scrollbar'].sprites[-1].update(length=self.scrollbars['frame scrollbar'].sprites[-1].range/self.trace.frame_selector.len_percent)
				self.trace.frame_selector.update(displace=self.scrollbars['frame scrollbar'].sprites[-1].percent/100)

			elif 'add empty frame' in self.action:
				self.trace.add_frame([])
				self.scrollbars['frame scrollbar'].sprites[-1].update(max=True, length=self.scrollbars['frame scrollbar'].sprites[-1].range/self.trace.frame_selector.len_percent)
				self.trace.frame_selector.update(displace=self.scrollbars['frame scrollbar'].sprites[-1].percent/100)

		elif self.action == 'tools window/move':
			self.follow_mouse = 'tools window'
			self.tools_window.move(self.mouse)

		elif self.action == 'tools window/scrollbar/slider/click':
			self.follow_mouse = 'tools window'

		elif self.action == 'grid button/click':
			self.buttons['grid button'].cycle()

			self.settings['grid type'] = self.grid_types[self.buttons['grid button'].curr_image]
			self.trace.grid_type = self.settings['grid type']

			text = 'Grid type is now ' + self.settings['grid type']
			if self.action[-1] == '1': text += ' - Warning: May cause low framerate'
			self.texts['grid info'] = Text(self.med_font, text, (3*self.scale, 53*self.scale))

		elif self.action == 'save button/click':
			self.trace.save_file(self.CWD + '\Traces\\' + self.name, self.name)

		point_pos_update = False
		for text in self.texts:
			if text[:9] == 'point pos':
				point_pos_update = True

		if self.action == 'show point pos/click' or point_pos_update:

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
				self.local_settings_write()
				exit(0)
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

		self.draw_background()
		
		for obj in self.elements: obj.draw(self.display)

		pygame.display.update()

	def draw_background(self):

		self.display.fill((200, 200, 200))

		pygame.draw.rect(self.display, (0, 170, 0), (subtract_tuple(self.trace_rect.topleft, (self.scale*2, self.scale*2)), add_tuple(self.trace_rect.size, (self.scale*4, self.scale*4))))
		
		pygame.draw.rect(self.display, (125, 125, 125), ((0, int(630*self.scale)), (self.width, self.height - int(630*self.scale))))
		pygame.draw.line(self.display, (255, 255, 255), (0, int(631*self.scale)), (self.width, int(631*self.scale)), int(3*self.scale))

		pygame.draw.rect(self.display, (125, 125, 125), ((0, 0), (self.width, int(50*self.scale))))
		pygame.draw.line(self.display, (255, 255, 255), (0, int(50*self.scale)), (self.width, int(50*self.scale)), 3)

		pygame.draw.rect(self.display, (68, 68, 68), ((int(58*self.scale-2), int(636*self.scale)-2), (int(784*self.scale)+4, int(134*self.scale)+4)), 1)
		pygame.draw.rect(self.display, (153, 153, 153), ((int(58*self.scale-1), int(636*self.scale)-1), (int(784*self.scale)+2, int(134*self.scale)+2)), 1)

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

		self.tools_window = Tools_Window(self.settings['tools window pos'], 0, self.small_font, directory, self.tool_buttons, self.scale,
										{'add point' : Tool(directory + 'Tools\\add_point_tool.png', 0),
										 'delete point' :  Tool(directory + 'Tools\\delete_point_tool.png', 1),
										 'move point' :  Tool(directory + 'Tools\\move_point_tool.png', 2),
										 'toggle line' :  Tool(directory + 'Tools\\toggle_line_tool.png', 3),
										 'select' :  Tool(directory + 'Tools\\select_tool.png', 4),
										 'blank5' :  Tool(directory + 'Tools\\blank_tool.png', 5),
										 'blank6' :  Tool(directory + 'Tools\\blank_tool.png', 6),
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
		
		self.tools_window.load(self.scale)

	def scrollbars_init(self, directory):

		scrollbar_up = Scrollbar((872, 78), 0, Button((0, 0), directory + 'scrollbar_arrow.png', type='on_mouse_down'),
											   Sprite((0, 28), directory + 'scrollbar_up_bar.png'),
											   Button((0, 496), directory + 'scrollbar_arrow.png', type='on_mouse_down'))
		scrollbar_up.load(self.scale, id='up scrollbar')
		scrollbar_up.sprites[2].image = pygame.transform.flip(scrollbar_up.sprites[2].image, False, True)

		scrollbar_across = Scrollbar((28, 602), 1, Button((0, 0), directory + 'scrollbar_arrow.png', type='on_mouse_down'),
												   Sprite((28, 0), directory + 'scrollbar_across_bar.png'),
												   Button((816, 0), directory + 'scrollbar_arrow.png', type='on_mouse_down'))
		scrollbar_across.load(self.scale, id='across scrollbar')
		scrollbar_across.sprites[0].image = pygame.transform.rotate(scrollbar_across.sprites[0].image, 90)
	 	scrollbar_across.sprites[2].image = pygame.transform.rotate(scrollbar_across.sprites[2].image, 270)

	 	scrollbar_frames = Scrollbar((0, 634), 1, Button((0, 0), directory + 'frame_scrollbar_arrow.png', type='on_mouse_down'),
												   Sprite((56, 138), directory + 'scrollbar_across_bar.png'),
												   Button((844, 0), directory + 'frame_scrollbar_arrow.png', type='on_mouse_down'))
	 	scrollbar_frames.load(self.scale, id='frame scrollbar')
	 	
	 	scrollbar_frames.sprites[2].image = pygame.transform.flip(scrollbar_frames.sprites[0].image, True, False)
	 	scrollbar_frames.sprites[-1].update(length=scrollbar_frames.sprites[-1].range/self.trace.frame_selector.len_percent)

	 	scrollbar_zoom = Scrollbar((0, 78), 0, Button((0, 0), directory + 'zoomin_button.png', type='on_mouse_down'),
											   Sprite((0, 28), directory + 'scrollbar_up_bar.png'),
											   Button((0, 496), directory + 'zoomout_button.png', type='on_mouse_down'))
		scrollbar_zoom.load(self.scale, id='zoom scrollbar')

		self.scrollbars = {scrollbar_up.id : scrollbar_up,
						   scrollbar_across.id : scrollbar_across,
						   scrollbar_zoom.id : scrollbar_zoom,
						   scrollbar_frames.id : scrollbar_frames}

	def buttons_init(self, directory):
		self.buttons = {'save button' : Button((4*self.scale, 4*self.scale), directory + 'save_button.png'),
						'grid button' : Cyclic_Button((48*self.scale, 4*self.scale), self.grid_types.index(self.settings['grid type']), directory + 'grid_button_1.png', directory + 'grid_button_2.png', directory + 'grid_button_3.png'),
						'show point pos' : Button((854*self.scale, 4*self.scale), directory + 'show_point_pos_button.png'),
						'deselect' : Button((92*self.scale, 4*self.scale), directory + 'deselect_button.png')}
		
		for button in self.buttons:
			self.buttons[button].load(scale=self.scale, id=button)

	def info_text_update(self):
	
		pop_lst = []

		for text in self.texts:
			self.texts[text].age()
			if self.texts[text].expired == True:
				pop_lst.append(text)

		for text in pop_lst:
			self.texts.pop(text)

		self.texts['zoom text'] = Text(self.small_font, str(self.zoom)[:4], (0, 601*self.scale), background=False, lifetime=None)
		self.texts['frame x pos text'] = Text(self.small_font, 'X: ' + str(self.trace.get_cf().rect.topleft[0])[:4], (0, 610*self.scale), background=False, lifetime=None)
		self.texts['frame y pos text'] = Text(self.small_font, 'Y: ' + str(self.trace.get_cf().rect.topleft[1])[:4], (0, 619*self.scale), background=False, lifetime=None)

		if self.trace_rect.collidepoint(self.mouse['pos']): 
			self.mouse_frame_pos = self.trace.global_to_rel((self.mouse['pos']))
			self.texts['mouse pos x text'] = Text(self.small_font, 'X: ' + str(int(round(self.mouse_frame_pos[0]))), (871*self.scale, 604*self.scale), background=False, lifetime=None)
			self.texts['mouse pos y text'] = Text(self.small_font, 'Y: ' + str(int(round(self.mouse_frame_pos[1]))), (871*self.scale, 616*self.scale), background=False, lifetime=None)
		elif 'mouse pos x text' in self.texts:
			self.texts.pop('mouse pos x text')
			self.texts.pop('mouse pos y text')

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