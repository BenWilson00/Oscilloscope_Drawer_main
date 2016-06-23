from basic import *
from sprites import *

class Tool(Button):

	def __init__(self, filepath, tool_no, _type='tool'):
		self.pos = (0, 0)
		self.filepath = filepath
		self.tool_no = tool_no
		self.state = 0
		self.type = _type
		self.hover = False
		self.Lactive = False
		self.Ractive = False
		self.mouse_pos = False

class Tools_Window(object):

	def __init__(self, pos, displace, font, directory, tool_buttons, tools, overlays, **kwargs):
		
		self.id = 'tools window'
		self.z = kwargs['z'] if 'z' in kwargs else 10
		self.pos = pos
		self.displace = displace
		self.tools = tools
		self.overlays = overlays
		self.tool_buttons = {tool : (tool_buttons[tool] if tool in tool_buttons else []) for tool in self.tools}
		self.mod_key = 'None'

		self.allowed_tool_combinations = [['add point', 'move point'], 
																		  ['add point', 'delete point'],
																		  ['delete point', 'toggle line'],
																		  ['move point', 'toggle line'],
																		  ['move point', 'select']]

		self.disallowed_tool_combinations = [['add point', 'toggle line']]

		self.forced_tool_combinations = {'add point' : ['move point']}

		for combination in self.allowed_tool_combinations:
			combination.sort()

		self.row_length = 2
		self.col_length = 5
		
		self.header_text = Text(font, 'TOOLS', (0, 0), background=False, lifetime=None)

		self.surface_size = map(int, scaleup(self.row_length * 34 + 30, self.col_length * 34 + self.header_text.rect.height/SCALE() + 18))
		self.surface = pygame.Surface(self.surface_size)

		self.rect = self.surface.get_rect()
		self.rect.topleft = self.pos

		self.header_rect = Rect((0, 0), (self.rect.width, (self.header_text.rect.height + 2)/SCALE()))
		self.header_text.rect.topleft = ((self.rect.width - self.header_text.rect.width)/2.0, self.header_rect.height/2)	

		self.scrollbar = Scrollbar((self.row_length * 34 + 2, self.header_rect.height + 2), 0, Button((0, 0), directory + 'scrollbar_arrow.png', type='on_mouse_down'),
																																												   Sprite((0, 28), directory + 'scrollbar_tool_bar.png'),
																																												   Button((0, self.col_length * 34 - 26), directory + 'scrollbar_arrow.png', type='on_mouse_down'))
	

		self.hover = False
		self.active = False
		self.mouse_pos = (0, 0)

		self.dropdown = True
		
		self.tools_rect = Rect(scaleup(2, self.header_rect.height + 4), scaleup(self.row_length * 34 - 2, self.col_length * 34 - 2))
		self.tools_range = SCALE() * 34 * ((len(self.tools) + 1) / 2)

		self.mod_keys_bar = Sprite((0, self.rect.height - 14*SCALE()), directory + 'Tools\\mod_keys_bar.png')

		if self.tools_range > self.tools_rect.height:
			self.len_percent = float(self.tools_range)/(self.tools_rect.height + 2)
		else:
			self.len_percent = 1.0

	def load(self):

		for tool in self.tools:
			self.tools[tool].load(scale=SCALE(), id=tool)
			row_pos = self.tools[tool].tool_no % 2
			col_pos = self.tools[tool].tool_no / 2
			self.tools[tool].set_pos((SCALE() * row_pos * 34 + 2, SCALE() * col_pos * 34 + self.header_text.rect.height + 4))
		
		for overlay in self.overlays:
			self.overlays[overlay].load('convert_alpha', scale=SCALE())

		self.scrollbar.load(id='scrollbar')
		self.scrollbar.sprites[2].image = pygame.transform.flip(self.scrollbar.sprites[2].image, False, True)

		self.scrollbar.sprites[-1].update(length=self.scrollbar.sprites[-1].range/self.len_percent)
		self.scrollbar.sprites[-1].update(displace=0)

		self.mod_keys_bar.load(scale=SCALE())

	def update(self, mod_key=None, **kwargs):

		self.displace = (self.scrollbar.sprites[-1].percent / 100) * (self.len_percent - 1) * (self.tools_rect.height + 2)
		
		if self.mod_key != mod_key and mod_key!=None:
			for tool in self.tools:
				self.tools[tool].load(scale=SCALE(), id=tool)

		if mod_key != None: self.mod_key = mod_key

		for tool in self.tools:
			row_pos = self.tools[tool].tool_no % 2
			col_pos = self.tools[tool].tool_no / 2
			self.tools[tool].set_pos((SCALE() * row_pos * 34 + self.tools_rect.left, SCALE() * col_pos * 34 + self.tools_rect.top - self.displace))			
	
		if self.scrollbar.sprites[0].active: self.scrollbar.sprites[-1].update(add=-2)
		elif self.scrollbar.sprites[2].active: self.scrollbar.sprites[-1].update(add=2)

		if 'set_tool' in kwargs:
			self.update_tool_buttons(*kwargs['set_tool'])

		if "toggle_select" in kwargs:
			if kwargs["toggle_select"] == "force make":
				
				if self.tool_buttons["mutate selection"] != []:
					comb = self.tool_buttons["mutate selection"][0]
					if len(comb) > 1:
						mod = comb[-1]
					else:
						mod = False
					self.update_tool_buttons(comb[0], "make selection", mod)


	def check_active(self, mouse):

		adjusted_mouse = mouse.copy()

		adjusted_mouse['pos'] = subtract_tuple(mouse['pos'], self.rect.topleft)

		self.active = False

		if self.rect.collidepoint(mouse['pos']):

			self.active = True

			if mouse['Ldown']:
				self.mouse_pos = subtract_tuple(mouse['pos'], self.rect.topleft)


		adjusted_hdr_rect = Rect((0, 0), (self.header_rect.width, (self.header_rect.height + 2)*SCALE() + 1))
		if adjusted_hdr_rect.collidepoint(adjusted_mouse['pos']) and mouse['Rdown']:
			if self.dropdown:
				self.dropdown = False
				self.surface = pygame.Surface(adjusted_hdr_rect.size)

			else:
				self.dropdown = True
				self.surface = pygame.Surface(self.surface_size)

			return



		if self.dropdown:

			self.scrollbar.check_active(adjusted_mouse)

			self.hover = self.scrollbar.hover

			for tool in self.tools:

				self.tools[tool].check_active(adjusted_mouse, clip=self.tools_rect)

				if self.tools[tool].Lactive:
					self.update_tool_buttons('Lmouse', tool)
				elif self.tools[tool].Ractive:
					self.update_tool_buttons('Rmouse', tool)

				if self.tools[tool].hover:
					self.hover = True

	def move(self, mouse):

		if mouse['Lactive']:
			if self.mouse_pos:
		 		self.rect.topleft = subtract_tuple(mouse['pos'], self.mouse_pos)
		else:
			self.mouse_pos = False

	def get_hover(self):

		if self.scrollbar.hover: return 'click'
		
		for tool in self.tools:
			if self.tools[tool].hover: return 'click'

	def get_action(self):

		if self.scrollbar.active:
			return (self.id,) + self.scrollbar.get_action()
		
		for tool in self.tools:
			if self.tools[tool].Lactive or self.tools[tool].Ractive:
				return (self.id,) + self.tools[tool].get_action()

		if self.mouse_pos: return (self.id, 'move')
		return (self.id, 'mouse over')

	def check_multiple_tools_allowed(self, *tools):
		if sorted(list(tools)) in self.allowed_tool_combinations: return True
		return False

	def update_tool_buttons(self, mouse, tool, mod = False):

		print tool
		print "\ntools:"
		for tool1 in self.tool_buttons:
			if self.tool_buttons[tool1] != []:
				print tool1, self.tool_buttons[tool1]

		print "\n"

		if not mod: mod = self.mod_key
		combination = [mouse, mod] if mod != 'None' else [mouse]

		test = False
		for toolset in self.disallowed_tool_combinations:
			if tool in toolset:
				test = list(toolset)
				test.remove(tool)
				break

		if test:
			for tool1 in test:

				rem_mouses = ()
				if mod == "None":
					for i in self.tool_buttons[tool1]:
						if len(i) == 1:
							rem_mouses += (i[0],)
				else:
					for i in self.tool_buttons[tool1]:
						if len(i) > 1:
							if i[1] == mod:
								rem_mouses += (i[0],)

				if len(rem_mouses) > 0:
					print "disallowed combination detected"

					for i in self.tool_buttons[tool1]:
						if i[0] in rem_mouses:
							print "remove", tool1, self.tool_buttons[tool1], "\n"
							self.tool_buttons[tool1].remove(i)
							self.tools[tool1].load(scale=SCALE(), name=tool1)
				
		for tool2 in self.tool_buttons:
			if combination in self.tool_buttons[tool2] and not self.check_multiple_tools_allowed(tool, tool2):
				print "remove", tool2, combination
				self.tool_buttons[tool2].remove(combination)
				self.tools[tool2].load(scale=SCALE(), name=tool2) 

		new_toolset = (tool,)

		print "insert", mouse, tool, combination
		self.insert_tool(mouse, tool, combination)

		if tool in self.forced_tool_combinations:
			for tool2 in self.forced_tool_combinations[tool]:
				if not (combination in self.tool_buttons[tool2]):

					new_toolset += (tool2,)

					print "insert", mouse, tool2, combination
					self.insert_tool(mouse, tool2, combination)


		for tool1 in self.tool_buttons:
			for tool2 in new_toolset:
				if tool != tool2 and tool1 != tool2:
					if combination in self.tool_buttons[tool1] and not self.check_multiple_tools_allowed(tool1, tool2):
						print "remove", tool2, combination
						self.tool_buttons[tool2].remove(combination)
						self.tools[tool2].load(scale=SCALE(), name=tool2) 

		print "\ntools:"
		for tool1 in self.tool_buttons:
			if self.tool_buttons[tool1] != []:
				print tool1, self.tool_buttons[tool1]

		#pause()

	def insert_tool(self, mouse, tool, combination):

		if len(self.tool_buttons[tool]) > 0:
			found = False
			for combination2 in range(0, len(self.tool_buttons[tool])):
				if mouse in self.tool_buttons[tool][combination2]:
					self.tool_buttons[tool][combination2] = combination
					found = True
					
			if not found: self.tool_buttons[tool].insert(0, combination) 
		else:
			self.tool_buttons[tool].append(combination) 

	def tools_draw(self):

		for tool in self.tools:
			
			if tool in self.tool_buttons:

				draw = []

				for combination in self.tool_buttons[tool]:

					mouse = combination[0]
					mod_key = combination[1] if len(combination) > 1 else 'None'

					if self.mod_key == mod_key:
						
						draw.append(mouse)

						if mod_key != 'None':
							draw.append(mouse[0] + mod_key)

				if 'Lmouse' in draw and 'Rmouse' in draw:
					self.overlays['L&Rmouse'].draw(self.tools[tool].image)
					draw.remove('Lmouse')
					draw.remove('Rmouse')
			
				for key in draw:
					self.overlays[key].draw(self.tools[tool].image)
				
			self.tools[tool].draw(self.surface, clip=self.tools_rect)

	def draw(self, display):

		self.surface.fill((200, 200, 200))


		if self.dropdown:

			pygame.draw.rect(self.surface, (68, 68, 68), (scaleup(0, self.header_rect.height + 2), scaleup(self.row_length * 34 + 2, self.col_length * 34 + 2)), int(SCALE()))
			pygame.draw.rect(self.surface, (153, 153, 153), (scaleup(1, self.header_rect.height + 3), scaleup(self.row_length * 34, self.col_length * 34)), int(SCALE()))
			pygame.draw.rect(self.surface, (68, 68, 68), ((0, self.rect.height - SCALE()*14), (self.rect.width, SCALE()*14)), int(SCALE()))
			pygame.draw.rect(self.surface, (153, 153, 153), ((SCALE(), self.rect.height - SCALE()*13), (self.rect.width - 2*SCALE(), SCALE()*12)), int(SCALE()))
			
			

			self.tools_draw()

			self.scrollbar.draw(self.surface)

			self.mod_keys_bar.draw(self.surface)

			if self.mod_key == 'None':
				pygame.draw.rect(self.surface, (0, 255, 0), (self.mod_keys_bar.rect.topleft, scaleup(25, 14)), 1)		
			elif self.mod_key == 'ctrl':
				pygame.draw.rect(self.surface, (0, 255, 0), (add_tuple(self.mod_keys_bar.rect.topleft, scaleup(25, 0)), scaleup(25, 14)), 1)
			elif self.mod_key == 'alt':
				pygame.draw.rect(self.surface, (0, 255, 0), (add_tuple(self.mod_keys_bar.rect.topleft, scaleup(49, 0)), scaleup(25, 14)), 1)
			elif self.mod_key == 'shift':
				pygame.draw.rect(self.surface, (0, 255, 0), (add_tuple(self.mod_keys_bar.rect.topleft, scaleup(73, 0)), scaleup(25, 14)), 1)



		pygame.draw.rect(self.surface, (68, 68, 68), ((0, 0), (self.rect.width - 1, SCALE()*(self.header_rect.height + 2))), int(SCALE()*1.5))
		pygame.draw.rect(self.surface, (153, 153, 153), (scaleup(1, 1), (self.rect.width - SCALE()*2 - 1, SCALE()*self.header_rect.height)), int(SCALE()))
		self.header_text.draw(self.surface)

		display.blit(self.surface, self.rect.topleft)
		
